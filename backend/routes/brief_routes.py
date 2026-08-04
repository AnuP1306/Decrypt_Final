from flask import Blueprint, request, jsonify
from google import genai
from groq import Groq
from dotenv import load_dotenv
import os, json, requests, hashlib, time, threading, random
from datetime import datetime, timedelta

load_dotenv()

brief_bp = Blueprint("brief_bp", __name__)


def _get_gemini():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _get_groq():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def _gnews_key():
    return os.getenv("GNEWS_API_KEY")


# =============================================
# CACHE FILES
# =============================================
BRIEF_NEWS_CACHE_FILE = "cache/brief_news_cache.json"
BRIEF_CARDS_CACHE_FILE = "cache/brief_cards_cache.json"
BRIEF_STATE_FILE = "cache/brief_state.json"  # tracks "has GNews already run today"

# Single lock guarding all reads/writes to the in-memory cache dicts below.
# Fixes: RuntimeError: dictionary changed size during iteration, caused by
# concurrent Flask threads mutating + json.dump-ing the same dict at once.
_cache_lock = threading.Lock()


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_json(path, data):
    """Thread-safe, atomic save. Snapshot the dict under the lock, then
    write to a temp file and rename — so a half-written file can never
    be read, and concurrent mutation during dump can never happen."""
    with _cache_lock:
        snapshot = dict(data)
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


BRIEF_NEWS_CACHE = _load_json(BRIEF_NEWS_CACHE_FILE)
BRIEF_CARDS_CACHE = _load_json(BRIEF_CARDS_CACHE_FILE)
BRIEF_STATE = _load_json(BRIEF_STATE_FILE)


def _today_str():
    return datetime.utcnow().strftime("%Y-%m-%d")


def _is_brief_locked_today():
    """True once today's GNews fetch attempt has already happened —
    regardless of whether it reached the full target of 10."""
    return BRIEF_STATE.get("date") == _today_str() and BRIEF_STATE.get("locked") is True


def _mark_brief_locked(count):
    BRIEF_STATE["date"] = _today_str()
    BRIEF_STATE["locked"] = True
    BRIEF_STATE["count"] = count
    _save_json(BRIEF_STATE_FILE, BRIEF_STATE)


# =============================================
# DOMAIN AUTO-DETECT (unchanged)
# =============================================
DOMAIN_KEYWORDS = {
    "World Affairs": [
        "war",
        "conflict",
        "diplomacy",
        "government",
        "election",
        "president",
        "prime minister",
        "parliament",
        "treaty",
        "sanctions",
        "protest",
        "military",
        "nato",
        "united nations",
        "geopolit",
        "refugee",
        "coup",
    ],
    "Finance": [
        "stock",
        "market",
        "economy",
        "inflation",
        "gdp",
        "crypto",
        "bitcoin",
        "ethereum",
        "investment",
        "fund",
        "bank",
        "fed",
        "interest rate",
        "recession",
        "trade",
        "currency",
        "ipo",
        "revenue",
        "profit",
        "debt",
        "fiscal",
    ],
    "Science": [
        "nasa",
        "spacex",
        "rocket",
        "planet",
        "asteroid",
        "galaxy",
        "research",
        "study",
        "discovery",
        "experiment",
        "physics",
        "chemistry",
        "biology",
        "genome",
        "particle",
        "quantum",
        "telescope",
        "satellite",
        "orbit",
    ],
    "Health": [
        "health",
        "disease",
        "cancer",
        "virus",
        "vaccine",
        "hospital",
        "medicine",
        "drug",
        "mental health",
        "therapy",
        "diet",
        "fitness",
        "obesity",
        "diabetes",
        "covid",
        "fda",
        "clinical",
        "doctor",
        "patient",
        "surgery",
    ],
    "Environment": [
        "climate",
        "carbon",
        "emission",
        "renewable",
        "solar",
        "wind",
        "fossil fuel",
        "deforestation",
        "biodiversity",
        "ocean",
        "glacier",
        "wildfire",
        "flood",
        "drought",
        "pollution",
        "sustainable",
        "green energy",
        "net zero",
        "paris agreement",
    ],
    "Tech": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "startup",
        "cybersecurity",
        "hack",
        "software",
        "app",
        "gadget",
        "smartphone",
        "chip",
        "semiconductor",
        "cloud",
        "robot",
        "automation",
        "openai",
        "google",
        "meta",
        "microsoft",
        "apple",
    ],
    "Culture": [
        "social media",
        "viral",
        "trend",
        "influencer",
        "tiktok",
        "instagram",
        "youtube",
        "celebrity",
        "music",
        "film",
        "movie",
        "series",
        "gaming",
        "fashion",
        "art",
        "meme",
        "pop culture",
    ],
    "Sports": [
        "football",
        "soccer",
        "cricket",
        "tennis",
        "basketball",
        "olympics",
        "world cup",
        "tournament",
        "athlete",
        "match",
        "championship",
        "league",
        "player",
        "goal",
        "medal",
        "formula 1",
        "f1",
        "nba",
        "fifa",
        "ipl",
    ],
    "Business": [
        "company",
        "acquisition",
        "merger",
        "ceo",
        "layoff",
        "hiring",
        "entrepreneur",
        "venture capital",
        "unicorn",
        "ecommerce",
        "amazon",
        "tesla",
        "nvidia",
        "valuation",
        "brand",
        "product launch",
    ],
    "Education": [
        "university",
        "student",
        "school",
        "degree",
        "scholarship",
        "career",
        "skill",
        "course",
        "learning",
        "graduation",
        "college",
        "exam",
        "tuition",
        "literacy",
        "teacher",
    ],
}


def detect_domain(title: str, desc: str) -> str:
    text = (title + " " + desc).lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[domain] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Tech"


def generate_article_id(title: str) -> str:
    """Canonical article ID — used as the shared key in BOTH
    brief_news_cache.json and brief_cards_cache.json."""
    return hashlib.md5(title.lower().strip().encode()).hexdigest()


BRIEF_GNEWS_QUERIES = [
    {
        "label": "World & Society",
        "q": (
            "politics OR government OR election OR war OR conflict "
            "OR diplomacy OR economy OR finance OR inflation OR trade"
        ),
    },
    {
        "label": "Science & Planet",
        "q": (
            "climate change OR environment OR space OR NASA OR SpaceX "
            "OR health OR medicine OR vaccine OR science discovery OR mental health"
        ),
    },
    {
        "label": "Tech & Future",
        "q": (
            "artificial intelligence OR cybersecurity OR startup "
            "OR electric vehicle OR renewable energy OR social media "
            "OR sports championship OR education OR career"
        ),
    },
]

BRIEF_TARGET = 10


def _gather_today_topped_up(today, yesterday):
    """
    Today's cached articles, topped up with recent cache if short.
    Looks back up to 5 days so a GNews outage lasting a few days
    doesn't result in an empty brief — users see something real
    rather than a blank page.
    """
    from datetime import timedelta

    with _cache_lock:
        all_today = [a for a in BRIEF_NEWS_CACHE.values() if a.get("date") == today]
        combined = list(all_today)
        seen_ids = {a.get("id") for a in combined}

        if len(combined) < BRIEF_TARGET:
            # Walk back up to 5 days to find cached articles
            for days_back in range(1, 6):
                if len(combined) >= BRIEF_TARGET:
                    break
                past_date = (datetime.utcnow() - timedelta(days=days_back)).strftime(
                    "%Y-%m-%d"
                )
                past_articles = [
                    a
                    for a in BRIEF_NEWS_CACHE.values()
                    if a.get("date") == past_date and a.get("id") not in seen_ids
                ]
                for a in past_articles:
                    if len(combined) >= BRIEF_TARGET:
                        break
                    combined.append(a)
                    seen_ids.add(a.get("id"))

    return combined


# def _gather_today_topped_up(today, yesterday):
#     """Today's cached articles, topped up with yesterday's if short."""
#     with _cache_lock:
#         all_today = [a for a in BRIEF_NEWS_CACHE.values() if a.get("date") == today]
#         combined = list(all_today)
#         seen_ids = {a.get("id") for a in combined}
#         if len(combined) < BRIEF_TARGET:
#             yesterday_articles = [
#                 a
#                 for a in BRIEF_NEWS_CACHE.values()
#                 if a.get("date") == yesterday and a.get("id") not in seen_ids
#             ]
#             for a in yesterday_articles:
#                 if len(combined) >= BRIEF_TARGET:
#                     break
#                 combined.append(a)
#                 seen_ids.add(a.get("id"))
#     return combined


# =============================================
# /get-brief
# GNews is called AT MOST ONCE PER DAY. Once today's
# fetch attempt is marked locked, every later visit
# is served purely from brief_news_cache.json.
# =============================================
@brief_bp.route("/get-brief", methods=["GET"])
def get_brief():
    global BRIEF_NEWS_CACHE

    today = _today_str()
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    # ── Fast path: already fetched today → cache only, never call GNews ──

    if _is_brief_locked_today():
        combined = _gather_today_topped_up(today, yesterday)
        if combined:
            random.shuffle(combined)
            print(
                f"⚡ Daily Brief: serving {len(combined)} from cache — GNews already ran today"
            )
            return jsonify({"articles": combined[:BRIEF_TARGET], "source": "cache"})
        else:
            print(
                "⚠️  Brief locked but cache is empty (server likely restarted) — re-fetching"
            )
            # Fall through to the fresh fetch below
    # if _is_brief_locked_today():
    #     combined = _gather_today_topped_up(today, yesterday)
    #     random.shuffle(combined)
    #     print(
    #         f"⚡ Daily Brief: serving {len(combined)} from cache — GNews already ran today"
    #     )
    #     return jsonify({"articles": combined[:BRIEF_TARGET], "source": "cache"})

    # ── Need a fresh fetch ──
    print("📰 Daily Brief fetch started")

    with _cache_lock:
        today_articles = [
            a for a in BRIEF_NEWS_CACHE.values() if a.get("date") == today
        ]

    for query_obj in BRIEF_GNEWS_QUERIES:
        if len(today_articles) >= BRIEF_TARGET:
            break

        url = (
            f"https://gnews.io/api/v4/search"
            f"?q={requests.utils.quote(query_obj['q'])}"
            f"&lang=en&max=5&from={today}&sortby=publishedAt"
            f"&apikey={_gnews_key()}"
        )
        try:
            res = requests.get(url, timeout=6)
            data = res.json()

            for art in data.get("articles", []):
                if len(today_articles) >= BRIEF_TARGET:
                    break

                title = art.get("title", "")
                desc = art.get("description", "") or ""
                art_id = generate_article_id(title)

                with _cache_lock:
                    already_have = art_id in BRIEF_NEWS_CACHE
                if already_have:
                    continue

                article = {
                    "id": art_id,
                    "title": title,
                    "desc": desc,
                    "content": art.get("content", "") or "",
                    "image": art.get("image") or "",
                    "domain": detect_domain(title, desc),
                    "date": today,
                    "url": art.get("url", ""),
                }

                with _cache_lock:
                    BRIEF_NEWS_CACHE[art_id] = article
                today_articles.append(article)

        except Exception as e:
            print(f"❌ Brief GNews query failed ({query_obj['label']}):", e)

    _save_json(BRIEF_NEWS_CACHE_FILE, BRIEF_NEWS_CACHE)

    if len(today_articles) >= BRIEF_TARGET:
        print(f"📰 GNews target reached: {len(today_articles)}/{BRIEF_TARGET}")
    else:
        print(
            f"⚠️  GNews only returned {len(today_articles)}/{BRIEF_TARGET} — topping up from yesterday's cache"
        )

    combined = _gather_today_topped_up(today, yesterday)

    if len(combined) > 0:
        # Only lock once we actually have something to serve.
        # If GNews returned nothing AND cache is empty, don't lock —
        # let the next visit try again instead of permanently returning 0.
        _mark_brief_locked(len(combined))
        print("🔒 Daily Brief marked complete for today")
    else:
        print("⚠️  Not locking — got 0 articles, will retry on next visit")

    random.shuffle(combined)
    result = combined[:BRIEF_TARGET]
    print(f"✅ Daily Brief: returning {len(result)} articles")
    return jsonify({"articles": result, "source": "fresh"})

    # combined = _gather_today_topped_up(today, yesterday)

    # # Lock for the day regardless of whether we hit 10 — the requirement
    # # is "never retry GNews repeatedly," not "retry until 10 every visit."
    # _mark_brief_locked(len(combined))
    # print("🔒 Daily Brief marked complete for today")

    # random.shuffle(combined)
    # result = combined[:BRIEF_TARGET]
    # print(f"✅ Daily Brief: returning {len(result)} articles")
    # return jsonify({"articles": result, "source": "fresh"})


# =============================================
# /get-brief-count — mirrors get_brief's logic,
# never calls GNews.
# =============================================
@brief_bp.route("/get-brief-count", methods=["GET"])
def get_brief_count():
    today = _today_str()
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    combined = _gather_today_topped_up(today, yesterday)
    count = min(len(combined), BRIEF_TARGET)
    return jsonify({"count": max(count, 1)})


# =============================================
# /generate-brief-card
# Lazy, per-card. Keyed by the SAME article id used
# in brief_news_cache.json (passed from frontend; falls
# back to recomputing from title if missing).
# =============================================
@brief_bp.route("/generate-brief-card", methods=["POST"])
def generate_brief_card():
    global BRIEF_CARDS_CACHE

    data = request.json or {}
    title = (data.get("title") or "").strip()
    desc = (data.get("desc") or "").strip()
    content = (data.get("content") or "").strip()
    article_id = data.get("id") or generate_article_id(title)

    with _cache_lock:
        cached = BRIEF_CARDS_CACHE.get(article_id)

    if cached:
        b, i, a = (
            cached.get("beginner", ""),
            cached.get("intermediate", ""),
            cached.get("advanced", ""),
        )
        if b != i or i != a:
            print(f"🟢 CACHE HIT — {title[:50]}")
            return jsonify({"card": cached, "source": "cache"})
        else:
            print(f"⚠️  Bad cached card (identical levels), regenerating: {title[:50]}")
            with _cache_lock:
                BRIEF_CARDS_CACHE.pop(article_id, None)

    print(f"🟡 CACHE MISS — {title[:50]}")

    full_text = f"{title}. {desc}. {content}"

    prompt = f"""You are a news explainer for a youth audience (16-35 years old).

Write THREE clearly DIFFERENT explanations of the news article below.
Each must be genuinely different in vocabulary, depth and assumed knowledge.

IMPORTANT:

Use the article as the primary source.
If the article is short, incomplete, vague, or missing context, intelligently use your general knowledge to fill in the background.
Never say "the article does not provide enough information".
Never leave explanations empty.
Never repeat the same wording across levels.
Each level should feel written for a different audience.
Focus on helping the reader understand WHY the story matters.

BEGINNER (40–60 words):

Explain like you're talking to a curious teenager.
Avoid jargon completely.
Use simple language.
Focus on what happened and why people should care.

INTERMEDIATE (60–80 words):

Assume the reader follows technology, business, science or world news occasionally.
Include useful context.
Explain why this development matters.

ADVANCED (75–100 words):

Assume the reader understands industry trends, economics, policy, geopolitics or technology.
Include implications, trade-offs, strategic impact and stakeholder effects.
Add relevant context not explicitly present in the article when necessary.

QUALITY RULES:

Every field must contain meaningful text.
Every field must meet its target length.
Use complete sentences.
Do not copy article text verbatim.
Return valid JSON only.
No markdown.
No explanations outside JSON.

STRICT OUTPUT FORMAT — return ONLY this JSON, no extra text, no markdown fences:
{{"beginner": "your beginner text here", "intermediate": "your intermediate text here", "advanced": "your advanced text here"}}

NEWS ARTICLE:
{full_text}"""

    def _parse_card(raw: str):
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")
        return json.loads(raw[start:end])

    def _is_valid(card: dict) -> bool:
        b = card.get("beginner", "")
        i = card.get("intermediate", "")
        a = card.get("advanced", "")
        return bool(b) and bool(i) and bool(a) and not (b == i == a) and len(b) > 30

    card = None
    print("🤖 Calling Gemini")
    try:
        response = _get_gemini().models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        card = _parse_card(response.text)
        if not _is_valid(card):
            raise ValueError(f"Gemini returned invalid card: {card}")
        print(f"🟢 Generated by Gemini: {title[:50]}")

    except Exception as e:
        print(f"❌ Gemini failed: {e} — trying Groq fallback")
        card = None
        try:
            groq_response = _get_groq().chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a news explainer. When given a news article, "
                            "return ONLY a JSON object with exactly three keys: "
                            "beginner, intermediate, advanced. "
                            "Each value must be a meaningfully DIFFERENT paragraph "
                            "explaining the same news at different knowledge levels. "
                            "No markdown. No extra text. Just the JSON object."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            card = _parse_card(groq_response.choices[0].message.content)
            if not _is_valid(card):
                raise ValueError(f"Groq returned invalid card: {card}")
            print(f"🔵 Generated by Groq: {title[:50]}")

        except Exception as e2:
            print(f"❌ Groq also failed: {e2} — using split-desc fallback")
            words = (desc or title).split()
            card = {
                "beginner": " ".join(words[: min(30, len(words))]),
                "intermediate": desc or title,
                "advanced": f"{desc or title} This story is still developing.",
            }

    if card and _is_valid(card):
        with _cache_lock:
            BRIEF_CARDS_CACHE[article_id] = card
        _save_json(BRIEF_CARDS_CACHE_FILE, BRIEF_CARDS_CACHE)
        print(f"💾 Cached explanation — {title[:50]}")
    else:
        print(f"⚠️  Not caching invalid card for: {title[:50]}")

    return jsonify({"card": card, "source": "generated"})

from flask import Blueprint, request, jsonify
from google import genai
from groq import Groq
from dotenv import load_dotenv
import os, json, requests, hashlib, time
from datetime import datetime, timedelta

# Ensure .env is loaded before reading any keys
load_dotenv()

brief_bp = Blueprint("brief_bp", __name__)

# =============================================
# CLIENTS — lazy helpers so keys are always
# read after dotenv has loaded
# =============================================
def _get_gemini():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def _get_groq():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def _gnews_key():
    return os.getenv("GNEWS_API_KEY")

# =============================================
# CACHE FILES (separate from home page cache)
# =============================================
BRIEF_NEWS_CACHE_FILE   = "cache/brief_news_cache.json"
BRIEF_CARDS_CACHE_FILE  = "cache/brief_cards_cache.json"

def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

BRIEF_NEWS_CACHE  = _load_json(BRIEF_NEWS_CACHE_FILE)
BRIEF_CARDS_CACHE = _load_json(BRIEF_CARDS_CACHE_FILE)

# =============================================
# DOMAIN AUTO-DETECT
# Maps keyword hits → friendly domain label
# =============================================
DOMAIN_KEYWORDS = {
    "World Affairs": [
        "war", "conflict", "diplomacy", "government", "election",
        "president", "prime minister", "parliament", "treaty",
        "sanctions", "protest", "military", "nato", "united nations",
        "geopolit", "refugee", "coup"
    ],
    "Finance": [
        "stock", "market", "economy", "inflation", "gdp", "crypto",
        "bitcoin", "ethereum", "investment", "fund", "bank", "fed",
        "interest rate", "recession", "trade", "currency", "ipo",
        "revenue", "profit", "debt", "fiscal"
    ],
    "Science": [
        "nasa", "spacex", "rocket", "planet", "asteroid", "galaxy",
        "research", "study", "discovery", "experiment", "physics",
        "chemistry", "biology", "genome", "particle", "quantum",
        "telescope", "satellite", "orbit"
    ],
    "Health": [
        "health", "disease", "cancer", "virus", "vaccine", "hospital",
        "medicine", "drug", "mental health", "therapy", "diet",
        "fitness", "obesity", "diabetes", "covid", "fda", "clinical",
        "doctor", "patient", "surgery"
    ],
    "Environment": [
        "climate", "carbon", "emission", "renewable", "solar", "wind",
        "fossil fuel", "deforestation", "biodiversity", "ocean",
        "glacier", "wildfire", "flood", "drought", "pollution",
        "sustainable", "green energy", "net zero", "paris agreement"
    ],
    "Tech": [
        "ai", "artificial intelligence", "machine learning", "startup",
        "cybersecurity", "hack", "software", "app", "gadget",
        "smartphone", "chip", "semiconductor", "cloud", "robot",
        "automation", "openai", "google", "meta", "microsoft", "apple"
    ],
    "Culture": [
        "social media", "viral", "trend", "influencer", "tiktok",
        "instagram", "youtube", "celebrity", "music", "film", "movie",
        "series", "gaming", "fashion", "art", "meme", "pop culture"
    ],
    "Sports": [
        "football", "soccer", "cricket", "tennis", "basketball",
        "olympics", "world cup", "tournament", "athlete", "match",
        "championship", "league", "player", "goal", "medal", "formula 1",
        "f1", "nba", "fifa", "ipl"
    ],
    "Business": [
        "company", "acquisition", "merger", "ceo", "layoff", "hiring",
        "entrepreneur", "venture capital", "unicorn", "ecommerce",
        "amazon", "tesla", "nvidia", "valuation", "brand", "product launch"
    ],
    "Education": [
        "university", "student", "school", "degree", "scholarship",
        "career", "skill", "course", "learning", "graduation",
        "college", "exam", "tuition", "literacy", "teacher"
    ],
}

def detect_domain(title: str, desc: str) -> str:
    """Return the best-matching domain label for an article."""
    text = (title + " " + desc).lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[domain] += 1
    best = max(scores, key=scores.get)
    # If nothing matched at all, default to Tech
    return best if scores[best] > 0 else "Tech"

def generate_article_id(title: str) -> str:
    return hashlib.md5(title.lower().strip().encode()).hexdigest()

# =============================================
# GNEWS BROAD QUERIES
# 3 calls cover all 10 domains → less API load
# =============================================
BRIEF_GNEWS_QUERIES = [
    {
        "label": "World & Society",
        "q": (
            "politics OR government OR election OR war OR conflict "
            "OR diplomacy OR economy OR finance OR inflation OR trade"
        )
    },
    {
        "label": "Science & Planet",
        "q": (
            "climate change OR environment OR space OR NASA OR SpaceX "
            "OR health OR medicine OR vaccine OR science discovery OR mental health"
        )
    },
    {
        "label": "Tech & Future",
        "q": (
            "artificial intelligence OR cybersecurity OR startup "
            "OR electric vehicle OR renewable energy OR social media "
            "OR sports championship OR education OR career"
        )
    },
]

# =============================================
# /get-brief  — main news endpoint for Daily Brief
# =============================================
@brief_bp.route("/get-brief", methods=["GET"])
def get_brief():
    global BRIEF_NEWS_CACHE

    today     = datetime.utcnow().strftime("%Y-%m-%d")
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    # ── 1. Collect today's cached articles ──────────────────────────────
    today_articles = [
        a for a in BRIEF_NEWS_CACHE.values()
        if a.get("date") == today
    ]

    # ── 2. If enough cached articles exist, return immediately ───────────
    if len(today_articles) >= 10:
        print(f"⚡ Brief: serving {len(today_articles)} articles from cache")
        import random
        random.shuffle(today_articles)
        return jsonify({"articles": today_articles[:10], "source": "cache"})

    # ── 3. Fetch fresh articles from GNews ──────────────────────────────
    print("📰 Brief: fetching fresh articles from GNews...")
    fresh_articles = []

    for query_obj in BRIEF_GNEWS_QUERIES:
        url = (
            f"https://gnews.io/api/v4/search"
            f"?q={requests.utils.quote(query_obj['q'])}"
            f"&lang=en"
            f"&max=5"
            f"&from={today}"
            f"&sortby=publishedAt"
            f"&apikey={_gnews_key()}"
        )
        try:
            res  = requests.get(url, timeout=10)
            data = res.json()

            for art in data.get("articles", []):
                title = art.get("title", "")
                desc  = art.get("description", "") or ""
                art_id = generate_article_id(title)

                if art_id in BRIEF_NEWS_CACHE:
                    continue  # already cached

                article = {
                    "id":      art_id,
                    "title":   title,
                    "desc":    desc,
                    "content": art.get("content", "") or "",
                    "image":   art.get("image") or "",
                    "domain":  detect_domain(title, desc),
                    "date":    today,
                    "url":     art.get("url", "")
                }

                BRIEF_NEWS_CACHE[art_id] = article
                fresh_articles.append(article)

        except Exception as e:
            print(f"❌ Brief GNews query failed ({query_obj['label']}):", e)

    # ── 4. Midnight edge case — if today still empty, use yesterday ──────
    all_today = [
        a for a in BRIEF_NEWS_CACHE.values()
        if a.get("date") == today
    ]

    if len(all_today) == 0:
        print("⚠️  Brief: no today articles yet, silently falling back to yesterday")
        all_today = [
            a for a in BRIEF_NEWS_CACHE.values()
            if a.get("date") == yesterday
        ]

    # ── 5. Save updated cache ────────────────────────────────────────────
    _save_json(BRIEF_NEWS_CACHE_FILE, BRIEF_NEWS_CACHE)
    print(f"🔵 Brief cache saved: {len(BRIEF_NEWS_CACHE)} total articles")

    # ── 6. Return 10 shuffled articles ──────────────────────────────────
    import random
    random.shuffle(all_today)
    result = all_today[:10]
    print(f"✅ Brief: returning {len(result)} articles")
    return jsonify({"articles": result, "source": "fresh"})


# =============================================
# /generate-brief-card  — single-slide B/I/A descriptions
# Much lighter than /generate-slides (no multi-slide array)
# =============================================
@brief_bp.route("/generate-brief-card", methods=["POST"])
def generate_brief_card():
    global BRIEF_CARDS_CACHE

    data    = request.json
    title   = data.get("title", "").strip()
    desc    = data.get("desc",  "").strip()
    content = data.get("content", "").strip()

    cache_key = hashlib.md5(title.lower().encode()).hexdigest()

    # ── Cache hit — but REJECT if all 3 levels are identical (bad prev generation) ─
    if cache_key in BRIEF_CARDS_CACHE:
        cached = BRIEF_CARDS_CACHE[cache_key]
        b = cached.get("beginner", "")
        i = cached.get("intermediate", "")
        a = cached.get("advanced", "")
        if b != i or i != a:
            # Good cache — all 3 are different
            print(f"🟢 Brief card cache HIT: {title[:50]}")
            return jsonify({"card": cached, "source": "cache"})
        else:
            # Bad cache — all same, delete and regenerate
            print(f"⚠️  Brief card cache had identical B/I/A, regenerating: {title[:50]}")
            del BRIEF_CARDS_CACHE[cache_key]

    full_text = f"{title}. {desc}. {content}"

    # Stronger prompt — explicit example format reduces JSON failures
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
        """Strip markdown fences and parse JSON. Returns dict or raises."""
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        # Find first { and last } in case there's surrounding text
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")
        return json.loads(raw[start:end])

    def _is_valid(card: dict) -> bool:
        """Card is valid if all 3 keys exist and are meaningfully different."""
        b = card.get("beginner", "")
        i = card.get("intermediate", "")
        a = card.get("advanced", "")
        return (
            bool(b) and bool(i) and bool(a)
            and not (b == i == a)           # all identical = bad
            and len(b) > 30                 # too short = bad
        )

    # ── Try Gemini first ─────────────────────────────────────────────────
    card = None
    try:
        response = _get_gemini().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        card = _parse_card(response.text)
        if not _is_valid(card):
            raise ValueError(f"Gemini returned invalid card: {card}")
        print(f"🟢 Brief card generated by Gemini: {title[:50]}")

    except Exception as e:
        print(f"❌ Gemini failed for brief card: {e} — trying Groq...")
        card = None

        # ── Groq fallback ────────────────────────────────────────────────
        try:
            groq_response = _get_groq().chat.completions.create(
                model="llama-3.1-8b-instant",
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
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            card = _parse_card(groq_response.choices[0].message.content)
            if not _is_valid(card):
                raise ValueError(f"Groq returned invalid card: {card}")
            print(f"🔵 Brief card generated by Groq: {title[:50]}")

        except Exception as e2:
            print(f"❌ Groq also failed: {e2} — using split-desc fallback")
            # Last resort: manually create 3 versions from desc
            # At least make them different lengths so switching feels different
            words = (desc or title).split()
            card = {
                "beginner":     " ".join(words[:min(30, len(words))]),
                "intermediate": desc or title,
                "advanced":     f"{desc or title} This story is still developing.",
            }

    # ── Only cache if valid — prevents bad data persisting ───────────────
    if card and _is_valid(card):
        BRIEF_CARDS_CACHE[cache_key] = card
        _save_json(BRIEF_CARDS_CACHE_FILE, BRIEF_CARDS_CACHE)
        print(f"💾 Cached valid card for: {title[:50]}")
    else:
        print(f"⚠️  Not caching invalid card for: {title[:50]}")

    return jsonify({"card": card, "source": "generated"})
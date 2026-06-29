from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from routes.home_routes import home_bp
from routes.opportunities_routes import opportunities  # samiksha ✅ added
from routes.auth_routes import auth_bp  # ✅ ADD THIS
from routes.tools_routes import tools_bp
import os
from dotenv import load_dotenv
import requests
from google import genai
import json
from datetime import datetime, timezone
import random
import hashlib
import threading
from datetime import timedelta
import time
import json
from groq import Groq
from routes.saved_routes import saved_bp
from routes.brief_routes import brief_bp

with open("static/data/fallback_news.json", "r") as f:
    FALLBACK_DATA = json.load(f)

CACHE_FILE = "cache/slides_cache.json"

try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        SLIDES_CACHE = json.load(f)
except:
    SLIDES_CACHE = {}

NEWS_CACHE_FILE = "cache/news_cache.json"

try:
    with open(NEWS_CACHE_FILE, "r", encoding="utf-8") as f:
        NEWS_CACHE = json.load(f)
except:
    NEWS_CACHE = {}

FETCH_META_FILE = "cache/fetch_meta.json"

try:
    with open(FETCH_META_FILE, "r", encoding="utf-8") as f:
        FETCH_META = json.load(f)
except:
    FETCH_META = {}


def get_last_fetch_date():
    return FETCH_META.get("last_fetch_date")


def set_last_fetch_date(date_str):
    global FETCH_META
    FETCH_META["last_fetch_date"] = date_str
    try:
        with open(FETCH_META_FILE, "w", encoding="utf-8") as f:
            json.dump(FETCH_META, f, ensure_ascii=False, indent=2)
        print(f"🔵 Marked GNews fetch as done for {date_str}")
    except Exception as e:
        print(f"❌ Failed to save fetch meta: {e}")


# create app FIRST
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY")  # 🔥 REQUIRED for session


def call_gemini_with_retry(model, prompt, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < retries - 1:
                print(f"⚠️ Retry {attempt+1}, waiting {delay}s")
                time.sleep(delay)
                delay *= 2
            else:
                raise e
    return None


# ================= SETUP =================
load_dotenv()

app.register_blueprint(home_bp)
app.register_blueprint(opportunities)  # samiksha ✅ added
app.register_blueprint(auth_bp)  # ✅ ADD THIS
app.register_blueprint(tools_bp)
app.register_blueprint(saved_bp)
app.register_blueprint(brief_bp)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# def generate_article_id(title):
#     return hashlib.md5(title.lower().strip().encode()).hexdigest()


def generate_article_id(title, domain=None, date=None):
    """
    Hash title + domain + date so the same headline republished
    on a different day (or classified into a different domain)
    gets a fresh cache slot instead of silently colliding with
    yesterday's entry and blocking new fetches.
    """
    key = title.lower().strip()
    if domain:
        key += f"|{domain.lower()}"
    if date:
        key += f"|{date}"
    return hashlib.md5(key.encode()).hexdigest()


# ================= DOMAIN CLASSIFICATION =================

# Keywords used to verify/fix domain labels based on article content
DOMAIN_KEYWORDS = {
    "AI": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural network",
        "llm",
        "large language model",
        "chatgpt",
        "gemini",
        "claude",
        "openai",
        "generative ai",
        "nlp",
        "computer vision",
        "reinforcement learning",
        "transformer",
        "diffusion model",
        "gpt",
        "mistral",
        "llama",
        "hugging face",
        "stable diffusion",
        "midjourney",
        "copilot",
        "ai model",
        "ai tool",
        "foundation model",
    ],
    "IT": [
        "cybersecurity",
        "software",
        "programming",
        "developer",
        "devops",
        "cloud computing",
        "aws",
        "azure",
        "google cloud",
        "kubernetes",
        "docker",
        "database",
        "sql",
        "api",
        "backend",
        "frontend",
        "web development",
        "javascript",
        "python",
        "data science",
        "networking",
        "ransomware",
        "data breach",
        "malware",
        "firewall",
        "open source",
        "github",
        "linux",
        "server",
        "saas",
        "startup",
    ],
    "Electronics": [
        "semiconductor",
        "chip",
        "processor",
        "gpu",
        "cpu",
        "vlsi",
        "embedded",
        "microcontroller",
        "arduino",
        "raspberry pi",
        "fpga",
        "iot",
        "internet of things",
        "sensor",
        "circuit",
        "transistor",
        "silicon",
        "wafer",
        "fabrication",
        "tsmc",
        "intel",
        "amd",
        "nvidia",
        "qualcomm",
        "arm",
        "5g",
        "rf",
        "pcb",
        "battery",
        "power management",
        "electronics",
        "hardware",
        "drone",
        "robotics",
    ],
}


def classify_domain(title, desc, content=""):
    """
    Classify an article into AI / IT / Electronics based on keyword matching.
    Returns the best-matching domain or None if no clear match.
    """
    combined = f"{title} {desc} {content}".lower()

    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                scores[domain] += 1

    best_domain = max(scores, key=scores.get)

    # Only override if we found at least one matching keyword
    if scores[best_domain] > 0:
        return best_domain

    return None  # Unclear — keep the query-assigned domain


# ================= CACHE HELPERS =================


def prune_news_cache():
    global NEWS_CACHE

    today = datetime.now(timezone.utc).date()

    fresh_cache = {}

    for article_id, article in NEWS_CACHE.items():

        try:
            article_date = datetime.strptime(article.get("date", ""), "%Y-%m-%d").date()

            age = (today - article_date).days

            # keep today + previous 2 days
            if age <= 2:
                fresh_cache[article_id] = article

        except:
            pass

    removed = len(NEWS_CACHE) - len(fresh_cache)

    NEWS_CACHE = fresh_cache

    print(f"🧹 Cache pruned. Removed {removed}. Remaining {len(NEWS_CACHE)}")


def save_news_cache():
    """Persist NEWS_CACHE to disk."""
    try:
        with open(NEWS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(NEWS_CACHE, f, ensure_ascii=False, indent=2)
        print(f"🔵 Saved {len(NEWS_CACHE)} cached articles")
    except Exception as e:
        print(f"❌ Failed to save news cache: {e}")


# ================= CHATBOT =================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")

    system_prompt = f"""
    You are the AI assistant for a website called Decrypt.

    About Decrypt:
     - It simplifies complex news into easy explanations
     - It consists of only 3 domains for now which are AI, IT and Electronics 
     - Thers's a feature called daily brief/ today's brief
     - It uses Beginner, Intermediate, Advanced levels
     - It shows underrated AI tools
     - Helps users understand news clearly

    User: {user_msg}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=system_prompt
        )
        return jsonify({"reply": response.text})

    except Exception as e:
        print("❌ Chatbot Gemini failed:", e)
        return jsonify({"reply": "AI is currently busy. Please try again later."})


# ================= FETCH NEWS =================

# Flip to False once your GNews quota has reset and you're ready for live fetching.
# True = only fallback_news.json is used, zero GNews calls made.
DEBUG_FALLBACK_ONLY = False

# 29/6 2nd version :


# =============================================
# BACKGROUND REFRESH ARCHITECTURE
#
# /get-news must NEVER make the user's request wait on GNews. Instead:
#   - /get-news always reads instantly from NEWS_CACHE + fallback.
#   - A background thread refreshes NEWS_CACHE on its own schedule,
#     with its own timeout + single retry, completely decoupled from
#     any single HTTP request's lifecycle.
#   - REFRESH_STATE is observable — /get-refresh-status exposes it —
#     so the frontend has a real signal instead of guessing from
#     article dates.
#   - A threading.Lock prevents two refresh cycles from running
#     concurrently and racing on NEWS_CACHE (the same class of bug
#     that caused the RuntimeError crash in brief_routes.py earlier).
# =============================================

REFRESH_STATE = {
    "in_progress": False,
    "last_run_started": None,
    "last_run_finished": None,
    "domains": {},
}
_refresh_lock = threading.Lock()

DOMAIN_QUERIES = {
    "AI": "AI OR artificial intelligence OR machine learning OR ChatGPT OR OpenAI OR Gemini OR LLM",
    "IT": "software OR cybersecurity OR programming OR cloud OR developer OR tech industry",
    "Electronics": "semiconductor OR chip OR hardware OR processor OR electronics OR robotics",
}

TARGET_FRESH = 10
TARGET_TOTAL = 15
GNEWS_TIMEOUT = 8
MIN_REFRESH_INTERVAL_SECONDS = 60  # don't trigger a new cycle more than once a minute


def normalize_title(title):
    """
    Aggressively normalize a title for duplicate detection — strips all
    quote variants (curly/straight), dashes, and punctuation, collapses
    whitespace. Catches near-duplicate headlines that differ only in
    cosmetic punctuation (the real bug we hit: two outlets running the
    same story with different quote-mark styles around the same phrase).
    """
    import re

    t = title.strip().lower()
    t = re.sub(r"[\"'\u2018\u2019\u201c\u201d\u2013\u2014\-,.:;!?()]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def extract_entities(title):
    """
    Extract likely proper nouns from a title: capitalized words in the
    ORIGINAL (pre-lowercase) text, excluding the sentence-initial word
    (always capitalized regardless of whether it's a proper noun).
    Used to catch wire-syndication duplicates — the same story rewritten
    by different outlets with different verbs/structure, but sharing
    the same named entities (companies, people, products).
    """
    import re

    words = title.split()
    entities = set()
    for i, w in enumerate(words):
        clean = re.sub(r"[^A-Za-z]", "", w)
        if len(clean) < 2 or i == 0:
            continue
        if clean[0].isupper():
            entities.add(clean.lower())
    return entities


def is_likely_same_story(title_a, title_b, domain_word=None):
    """
    Two articles are treated as the same underlying story if they share
    2+ proper nouns, EXCLUDING the domain's own name (e.g. "AI" will
    trivially appear in every AI-domain headline and isn't a useful
    signal on its own).
    """
    entities_a = extract_entities(title_a)
    entities_b = extract_entities(title_b)
    if domain_word:
        entities_a = entities_a - {domain_word.lower()}
        entities_b = entities_b - {domain_word.lower()}
    shared = entities_a & entities_b
    return len(shared) >= 2


def _fetch_domain_with_retry(domain, query, needed):
    """One GNews call, with a single retry on timeout. Returns the raw
    'articles' list from GNews, or raises on final failure."""
    url = (
        f"https://gnews.io/api/v4/search?"
        f"q={requests.utils.quote(query)}"
        f"&lang=en"
        f"&max={min(needed, 10)}"
        f"&from={datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
        f"&sortby=publishedAt"
        f"&apikey={GNEWS_API_KEY}"
    )
    try:
        res = requests.get(url, timeout=GNEWS_TIMEOUT)
        data = res.json()
    except requests.exceptions.Timeout:
        print(f"⏳ {domain}: first attempt timed out, retrying once...")
        res = requests.get(url, timeout=GNEWS_TIMEOUT)
        data = res.json()

    if "articles" not in data:
        raise ValueError(f"no 'articles' key in response: {data}")
    return data["articles"]


def _refresh_cycle():
    """
    The actual background refresh. Runs in its own thread. Holds the
    lock for its full duration so no second cycle (timer-triggered or
    request-triggered) can run concurrently and corrupt NEWS_CACHE.
    """
    global REFRESH_STATE

    if not _refresh_lock.acquire(blocking=False):
        print("⏳ Refresh already in progress — skipping this trigger")
        return

    try:
        REFRESH_STATE["in_progress"] = True
        REFRESH_STATE["last_run_started"] = datetime.now(timezone.utc).isoformat()

        prune_news_cache()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        cache_updated = False

        for domain, query in DOMAIN_QUERIES.items():
            fresh_in_cache = [
                a
                for a in NEWS_CACHE.values()
                if a.get("domain") == domain and a.get("date") == today
            ]
            current_fresh_count = len(fresh_in_cache)

            if current_fresh_count >= TARGET_FRESH:
                REFRESH_STATE["domains"][domain] = {
                    "status": "ok",
                    "fresh_count": current_fresh_count,
                    "last_success": REFRESH_STATE["domains"]
                    .get(domain, {})
                    .get("last_success"),
                }
                print(
                    f"✅ {domain}: already has {current_fresh_count} fresh today — skipping GNews"
                )
                continue

            needed = TARGET_FRESH - current_fresh_count
            print(
                f"📰 {domain}: has {current_fresh_count} fresh, fetching {needed} more"
            )

            try:
                articles = _fetch_domain_with_retry(domain, query, needed)

                added = 0
                dropped_offtopic = 0
                dropped_dup = 0

                for art in articles:
                    title = art.get("title", "")
                    desc = art.get("description", "") or ""
                    content = art.get("content", "") or ""

                    detected_domain = classify_domain(title, desc, content)
                    if detected_domain is None:
                        dropped_offtopic += 1
                        continue

                    final_domain = detected_domain
                    norm_title = normalize_title(title)

                    already_have = any(
                        normalize_title(a.get("title", "")) == norm_title
                        or is_likely_same_story(
                            title, a.get("title", ""), domain_word=final_domain
                        )
                        for a in NEWS_CACHE.values()
                        if a.get("domain") == final_domain
                    )
                    if already_have:
                        dropped_dup += 1
                        continue

                    article_id = generate_article_id(title, final_domain, today)
                    if article_id in NEWS_CACHE:
                        continue

                    NEWS_CACHE[article_id] = {
                        "id": article_id,
                        "title": title,
                        "desc": desc,
                        "content": content,
                        "image": art.get("image"),
                        "domain": final_domain,
                        "date": today,
                    }
                    cache_updated = True
                    added += 1

                new_fresh_count = len(
                    [
                        a
                        for a in NEWS_CACHE.values()
                        if a.get("domain") == domain and a.get("date") == today
                    ]
                )
                REFRESH_STATE["domains"][domain] = {
                    "status": "ok",
                    "fresh_count": new_fresh_count,
                    "last_success": datetime.now(timezone.utc).isoformat(),
                }
                print(
                    f"🔵 {domain}: added {added}, dropped {dropped_offtopic} off-topic, "
                    f"{dropped_dup} duplicate. Fresh total now: {new_fresh_count}/{TARGET_FRESH}"
                )

            except Exception as e:
                REFRESH_STATE["domains"][domain] = {
                    "status": "failed",
                    "fresh_count": current_fresh_count,
                    "last_success": REFRESH_STATE["domains"]
                    .get(domain, {})
                    .get("last_success"),
                }
                print(f"❌ {domain}: refresh failed — {e}")

        if cache_updated:
            save_news_cache()

        REFRESH_STATE["last_run_finished"] = datetime.now(timezone.utc).isoformat()

    finally:
        REFRESH_STATE["in_progress"] = False
        _refresh_lock.release()


def trigger_refresh_if_needed():
    """
    Cheap, non-blocking check called on every /get-news request. If a
    refresh is already running, or the last one finished too recently,
    this does nothing and returns instantly. Otherwise it starts a
    background thread and returns instantly — the HTTP request never
    waits on this call.
    """
    if REFRESH_STATE["in_progress"]:
        return

    last_finished = REFRESH_STATE.get("last_run_finished")
    if last_finished:
        last_dt = datetime.fromisoformat(last_finished)
        elapsed = (datetime.now(timezone.utc) - last_dt).total_seconds()
        if elapsed < MIN_REFRESH_INTERVAL_SECONDS:
            return

    thread = threading.Thread(target=_refresh_cycle, daemon=True)
    thread.start()


def get_news_live():
    """
    Always returns instantly from cache + fallback. Triggers a
    background refresh if one is due, but never waits on it.
    """
    trigger_refresh_if_needed()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")

    all_articles = []
    seen_ids = set()
    seen_norm_titles = set()

    for domain in DOMAIN_QUERIES.keys():

        fresh_articles = sorted(
            [
                a
                for a in NEWS_CACHE.values()
                if a.get("domain") == domain and a.get("date") == today
            ],
            key=lambda a: a.get("id", ""),
        )
        cached_articles = sorted(
            [
                a
                for a in NEWS_CACHE.values()
                if a.get("domain") == domain and a.get("date") == yesterday
            ],
            key=lambda a: a.get("id", ""),
        )

        domain_feed = []

        for art in fresh_articles + cached_articles:
            aid = art.get("id")
            norm_title = normalize_title(art.get("title", ""))
            title = art.get("title", "")

            if not aid or aid in seen_ids:
                continue
            if norm_title and norm_title in seen_norm_titles:
                continue

            is_dup = any(
                is_likely_same_story(title, existing_title, domain_word=domain)
                for existing_title in [a.get("title", "") for a in domain_feed]
            )
            if is_dup:
                continue

            domain_feed.append(art)
            seen_ids.add(aid)
            seen_norm_titles.add(norm_title)

            if len(domain_feed) >= TARGET_TOTAL:
                break

        remaining = TARGET_TOTAL - len(domain_feed)

        if remaining > 0:
            fallback_count = 0
            for item in FALLBACK_DATA:
                if fallback_count >= remaining:
                    break
                if item.get("domain", "").lower() != domain.lower():
                    continue

                norm_title = normalize_title(item.get("title", ""))
                if norm_title in seen_norm_titles:
                    continue

                fallback_id = generate_article_id(item.get("title", ""), domain, today)
                if fallback_id in seen_ids:
                    continue

                image = item.get("image", "")
                if image.startswith("/static/news-image/"):
                    image = image.replace("/static/news-image/", "/news-image/")

                domain_feed.append(
                    {
                        "id": fallback_id,
                        "title": item.get("title", ""),
                        "desc": item.get("desc", ""),
                        "content": item.get("content", ""),
                        "image": image,
                        "domain": domain,
                        "date": today,
                    }
                )
                seen_ids.add(fallback_id)
                seen_norm_titles.add(norm_title)
                fallback_count += 1

        all_articles.extend(domain_feed)

    return jsonify({"articles": all_articles, "refresh_state": REFRESH_STATE})


def get_news_fallback_only():
    print("⚠️ Using FALLBACK NEWS (DEBUG MODE)")

    fixed_articles = []

    for article in FALLBACK_DATA:
        article_copy = article.copy()

        if article_copy.get("image", "").startswith("/static/news-image/"):
            article_copy["image"] = article_copy["image"].replace(
                "/static/news-image/", "/news-image/"
            )

        fixed_articles.append(article_copy)

    return jsonify({"articles": fixed_articles})


@app.route("/get-news", methods=["GET"])
def get_news():
    if DEBUG_FALLBACK_ONLY:
        return get_news_fallback_only()
    return get_news_live()


@app.route("/get-refresh-status", methods=["GET"])
def get_refresh_status():
    """Lightweight, cache-only — lets the frontend poll for whether a
    background refresh has completed since the page loaded, without
    re-fetching the full article list."""
    return jsonify(REFRESH_STATE)


# ================= GENERATE SLIDES =================
@app.route("/generate-slides", methods=["POST"])
def generate_slides():

    data = request.json
    index = data.get("index", 0)
    title = data.get("title", "")

    cache_key = title.strip().lower().replace("'", "'")

    # 🔥 CHECK CACHE FIRST
    if cache_key in SLIDES_CACHE:
        print(f"🟢 CACHE HIT for: {title}")
        return jsonify({"slides": SLIDES_CACHE[cache_key], "source": "cache"})

    desc = data.get("desc", "")
    content = data.get("content", "")
    full_text = f"{title}. {desc}. {content}"

    prompt = f"""
    You are an AI that converts news into swipeable learning cards.

    RULES:
    - Beginner: simple
    - Intermediate: balanced
    - Advanced: deeper (min 60 words)

    Each slide:
    - minimum 35 words
    - no cut sentences

    Return JSON EXACTLY like:
    {{
      "beginner": [{{"title": "...", "desc": "..."}}],
      "intermediate": [...],
      "advanced": [...]
    }}

    News:
    {full_text}
    """

    try:
        raw_text = call_gemini_with_retry("gemini-2.5-flash", prompt)

        if not raw_text:
            raise Exception("Gemini failed after retries")

        raw_text = raw_text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # slides = json.loads(raw_text)
        # SLIDES_CACHE[cache_key] = slides
        # with open(CACHE_FILE, "w", encoding="utf-8") as f:
        #     json.dump(SLIDES_CACHE, f, ensure_ascii=False, indent=2)
        # print(f"🔵 CACHE SAVED for: {title}")

        slides = json.loads(raw_text)
        SLIDES_CACHE[cache_key] = slides

        # ── Trim cache once it gets too large ────────────────────────────
        # Dicts preserve insertion order in Python 3.7+, so the oldest
        # entries are simply the first N keys.
        MAX_SLIDES_CACHE_SIZE = 500
        if len(SLIDES_CACHE) > MAX_SLIDES_CACHE_SIZE:
            excess = len(SLIDES_CACHE) - MAX_SLIDES_CACHE_SIZE
            oldest_keys = list(SLIDES_CACHE.keys())[:excess]
            for k in oldest_keys:
                del SLIDES_CACHE[k]
            print(
                f"🧹 Trimmed {excess} oldest slide cache entries (cap: {MAX_SLIDES_CACHE_SIZE})"
            )

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(SLIDES_CACHE, f, ensure_ascii=False, indent=2)
        print(f"🔵 CACHE SAVED for: {title}")

        return jsonify({"slides": slides, "source": "gemini"})

    except Exception as e:
        print("❌ Gemini failed:", e)

        try:
            if index < len(FALLBACK_DATA):
                fallback = FALLBACK_DATA[index]
            else:
                fallback = FALLBACK_DATA[index % len(FALLBACK_DATA)]
            print(f"⚠️ Using FALLBACK for card index {index}")
            return jsonify({"slides": fallback["slides"], "source": "fallback"})
        except:
            print(f"⚠️ Fallback index missing: {index}")

        # 🛟 LAST RESORT
        print(f"⚠️ No fallback match, using minimal safe fallback: {title}")
        safe_text = desc if desc else content if content else title

        return jsonify(
            {
                "slides": {
                    "beginner": [{"title": title, "desc": safe_text[:120]}],
                    "intermediate": [{"title": title, "desc": safe_text[:220]}],
                    "advanced": [
                        {
                            "title": title,
                            "desc": (
                                safe_text
                                + " This development may have broader implications as more details emerge."
                            ),
                        }
                    ],
                }
            }
        )


# ================= ARTICLE CHAT =================


@app.route("/ask-article", methods=["POST"])
def ask_article():

    data = request.json
    question = data.get("question", "")
    article = data.get("article", "")
    full_text = article

    prompt = f"""
    You are a smart assistant.

    Answer using article + your knowledge if needed.

    ARTICLE:
    {full_text}

    QUESTION:
    {question}
    """

    # ── GEMINI FIRST ──────────────────────────────────────────────────────
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        print("🟢 ARTICLE BOT ANSWERED BY GEMINI")
        return jsonify({"reply": response.text, "source": "gemini"})

    except Exception as e:
        print("❌ Gemini failed:", e)
        print("🟡 Switching to Groq...")

    # ── GROQ FALLBACK ─────────────────────────────────────────────────────
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an intelligent and helpful news assistant.

                    - Use the provided article as your MAIN context.
                    - You may use general knowledge ONLY if it directly supports the article or is related to the article.
                    - Do NOT change topic or introduce unrelated domains.
                    - If question is outside the article, say so politely.
                    - If the article is incomplete, fill gaps intelligently.
                    - Do NOT say "according to the article" again and again.
                    - Speak naturally like a human in a friendly tone.
                    - Keep answers clear, simple, and slightly conversational.
                    - If comparison is asked, use general knowledge.
                    """,
                },
                {
                    "role": "user",
                    "content": f"ARTICLE:\n{full_text}\n\nQUESTION:\n{question}",
                },
            ],
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        print("🔵 ARTICLE BOT ANSWERED BY GROQ")
        return jsonify({"reply": reply, "source": "groq"})

    except Exception as e:
        print("❌ Groq failed:", e)
        return jsonify({"reply": "AI is currently unavailable.", "source": "none"})


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)

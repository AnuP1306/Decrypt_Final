from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from routes.home_routes import home_bp
from routes.opportunities_routes import opportunities   # samiksha ✅ added
from routes.auth_routes import auth_bp   # ✅ ADD THIS
from routes.tools_routes import tools_bp
import os
from dotenv import load_dotenv
import requests
from google import genai
import json
from datetime import datetime
import random
import hashlib

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
    with open(
        NEWS_CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        NEWS_CACHE = json.load(f)

except:

    NEWS_CACHE = {}


# create app FIRST
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY")   # 🔥 REQUIRED for session

def call_gemini_with_retry(model, prompt, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
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
app.register_blueprint(opportunities)   # samiksha ✅ added
app.register_blueprint(auth_bp)   # ✅ ADD THIS
app.register_blueprint(tools_bp)
app.register_blueprint(saved_bp)
app.register_blueprint(brief_bp)

# app.register_blueprint(opportunities)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_article_id(title):

    return hashlib.md5(
        title.lower().strip().encode()
    ).hexdigest()


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
            model="gemini-2.5-flash",
            contents=system_prompt
        )
        return jsonify({"reply": response.text})

    except Exception as e:
        print("❌ Chatbot Gemini failed:", e)
        return jsonify({"reply": "AI is currently busy. Please try again later."})


# ================= FETCH NEWS =================

# this version will only show fallback data and doesn't work with react
# @app.route("/get-news", methods=["GET"])
# def get_news():
#     print("⚠️ Using FALLBACK NEWS (API limit hit)")

#     return jsonify({
#         "articles": FALLBACK_DATA
#     })

# only fallback data (works properly)
# @app.route("/get-news", methods=["GET"])
# def get_news():

#     print("⚠️ Using FALLBACK NEWS (API limit hit)")

#     fixed_articles = []

#     for article in FALLBACK_DATA:

#         article_copy = article.copy()

#         if article_copy.get("image", "").startswith("/static/news-image/"):

#             article_copy["image"] = article_copy["image"].replace(
#                 "/static/news-image/",
#                 "/news-image/"
#             )

#         fixed_articles.append(article_copy)

#     return jsonify({
#         "articles": fixed_articles
#     })


def prune_news_cache():

    global NEWS_CACHE
    
    today = datetime.utcnow().strftime(
        "%Y-%m-%d"
    )

    fresh_cache = {}

    for article_id, article in NEWS_CACHE.items():

        article_date = article.get("date")

        if article_date == today:

            fresh_cache[article_id] = article

    NEWS_CACHE = fresh_cache

    print(
        f"🧹 Cache pruned. Remaining:"
        f" {len(NEWS_CACHE)} articles"
    )

@app.route("/get-news", methods=["GET"])
def get_news():
    today = datetime.utcnow().strftime(
        "%Y-%m-%d"
    )
    prune_news_cache()

    user_topics = request.args.get("topics", "")

    topic_list = [
        t.strip()
        for t in user_topics.split(",")
        if t.strip()
    ]

    TOPIC_MAP = {
        "Machine Learning":
            "machine learning OR deep learning OR neural networks",

        "Web Dev":
            "web development OR frontend OR backend OR JavaScript",

        "Robotics":
            "robotics OR automation OR robot",

        "Cloud Computing":
            "AWS OR Azure OR Google Cloud OR cloud computing",

        "Quantum Computing":
            "quantum computing OR qubit",

        "Space Technology":
            "NASA OR SpaceX OR satellite OR space technology",

        "IOT":
            "Internet of Things OR IoT OR smart devices",

        "Cybersecurity":
            "cybersecurity OR ransomware OR data breach"
    }

    DEFAULT_QUERIES = {

        "AI":
            (
                "artificial intelligence OR generative AI "
                "OR machine learning OR deep learning "
                "OR LLM OR ChatGPT OR Gemini OR Claude"
            ),

        "IT":
            (
                "cybersecurity OR software development "
                "OR programming OR cloud computing "
                "OR DevOps OR networking "
                "OR data science "
                "OR database"
            ),

        "Electronics":
            (
                "semiconductor OR VLSI "
                "OR embedded systems "
                "OR IoT hardware "
                "OR microcontroller "
                "OR processor OR GPU "
                "OR chip manufacturing "
                "OR electronics"
            )
    }

    if topic_list:

        queries = {}

        for topic in topic_list[:4]:

            if topic in TOPIC_MAP:

                queries[topic] = TOPIC_MAP[topic]

        if not queries:

            queries = DEFAULT_QUERIES

    else:

        queries = DEFAULT_QUERIES

    # =====================================
    # LOAD TODAY CACHE
    # =====================================

    all_articles = []

    today_articles = []

    for article_id, article in NEWS_CACHE.items():

        if article.get("date") == today:

            today_articles.append(article)

    all_articles.extend(today_articles)

    print(
        f"🟢 Loaded {len(today_articles)} articles from cache"
    )

    # =====================================
    # RETURN CACHE IF ALREADY 15+
    # =====================================

    if len(today_articles) >= 15:

        print(
            "⚡ Serving entirely from cache"
        )

        return jsonify({
            "articles": today_articles[:15]
        })

    # =====================================
    # FETCH FROM GNEWS
    # =====================================

    needed_articles = max(
        0,
        15 - len(all_articles)
    )

    print(
        f"📰 Need {needed_articles} more articles"
    )

    articles_per_domain = max(
        1,
        (needed_articles // len(queries)) + 1
    )

    for domain, query in queries.items():

        url = (
            f"https://gnews.io/api/v4/search?"
            f"q={query}"
            f"&lang=en"
            f"&max={articles_per_domain}"
            f"&from={today}"
            f"&sortby=publishedAt"
            f"&apikey={GNEWS_API_KEY}"
        )

        try:

            res = requests.get(url)

            data = res.json()

            if "articles" not in data:
                continue

            for art in data["articles"]:

                article = {

                    "id":
                        generate_article_id(
                            art.get(
                                "title",
                                ""
                            )
                        ),

                    "title":
                        art.get(
                            "title",
                            ""
                        ),

                    "desc":
                        art.get(
                            "description",
                            ""
                        ),

                    "content":
                        art.get(
                            "content",
                            ""
                        ),

                    "image":
                        art.get(
                            "image"
                        ),

                    "domain":
                        domain,

                    "date":
                        today
                }

                if article["id"] not in NEWS_CACHE:

                    NEWS_CACHE[
                        article["id"]
                    ] = article

                    all_articles.append(
                        article
                    )

        except Exception as e:

            print(
                f"❌ Failed fetching {domain}:",
                e
            )

    # =====================================
    # FALLBACK IF STILL BELOW 15
    # =====================================

    if len(all_articles) < 15:

        print(
            f"⚠️ Only {len(all_articles)} articles. "
            f"Loading fallback news."
        )

        existing_ids = {

            article["id"]

            for article in all_articles

            if "id" in article

        }

        for item in FALLBACK_DATA:

            fallback_id = generate_article_id(
                item.get("title", "")
            )

            if fallback_id in existing_ids:

                continue

            fallback_article = {

                "id":
                    fallback_id,

                "title":
                    item.get(
                        "title",
                        ""
                    ),

                "desc":
                    item.get(
                        "desc",
                        ""
                    ),

                "content":
                    item.get(
                        "content",
                        ""
                    ),

                "image":
                    item.get(
                        "image",
                        ""
                    ),

                "domain":
                    item.get(
                        "domain",
                        "AI"
                    ),

                "date":
                    today
            }

            all_articles.append(
                fallback_article
            )

            NEWS_CACHE[
                fallback_id
            ] = fallback_article

            if len(all_articles) >= 15:

                break

    # =====================================
    # SAVE CACHE
    # =====================================

    with open(
        NEWS_CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            NEWS_CACHE,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"🔵 Saved {len(NEWS_CACHE)} cached articles"
    )

    # =====================================
    # RETURN EXACTLY 15
    # =====================================

    all_articles = all_articles[:15]

    print(
        f"✅ Returning {len(all_articles)} articles"
    )

    return jsonify({
        "articles": all_articles
    })
# ================= GENERATE SLIDES =================
@app.route("/generate-slides", methods=["POST"])
def generate_slides():

    data = request.json
    index = data.get("index", 0)

    title = data.get("title", "")

    cache_key = (
        title.strip()
        .lower()
        .replace("’", "'")
    )

    # 🔥 CHECK CACHE FIRST
    if cache_key in SLIDES_CACHE:
        print(f"🟢 CACHE HIT for: {title}")
        return jsonify({
            "slides": SLIDES_CACHE[cache_key],
            "source": "cache"
        })
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
        # response = client.models.generate_content(
        #     model="gemini-2.5-flash",
        #     contents=prompt
        # )

        # raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        slides = json.loads(raw_text)
        SLIDES_CACHE[cache_key] = slides
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                SLIDES_CACHE,
                f,
                ensure_ascii=False,
                indent=2
            )
        print(f"🔵 CACHE SAVED for: {title}")

        return jsonify({
            "slides": slides,
            "source": "gemini"
        })

    except Exception as e:
        print("❌ Gemini failed:", e)

        try:
            # fallback = FALLBACK_DATA[index]
            if index < len(FALLBACK_DATA):
                fallback = FALLBACK_DATA[index]
            else:
                fallback = FALLBACK_DATA[index % len(FALLBACK_DATA)]
            print(f"⚠️ Using FALLBACK for card index {index}")
            return jsonify({
                "slides": fallback["slides"],
                "source": "fallback"
            })
        except:
            print(f"⚠️ Fallback index missing: {index}")

        # 🔥 CURATED FALLBACK
        # fallback = None

        # for item in FALLBACK_DATA:
        #     for keyword in item["keywords"]:
        #         if keyword.lower() in title.lower():
        #             fallback = item
        #             break
        #     if fallback:
        #         break

        # if fallback:
        #     print(f"⚠️ Using FALLBACK for: {title}")
        #     return jsonify({
        #         "slides": fallback["slides"],
        #         "source": "fallback"
        #     })

        # 🛟 LAST RESORT (very rare)
        print(f"⚠️ No fallback match, using minimal safe fallback: {title}")

        return jsonify({
            "slides": {
                "beginner": [{"title": title, "desc": desc or title}],
                "intermediate": [{"title": title, "desc": desc or title}],
                "advanced": [{"title": title, "desc": desc or title}]
            }
        })
        # safe_text = desc if desc else content if content else title

        # return jsonify({
        #     "slides": {
        #         "beginner": [{"title": title, "desc": safe_text[:200]}],
        #         "intermediate": [{"title": title, "desc": safe_text[:150]}],
        #         "advanced": [{"title": title, "desc": safe_text[:300]}]
        #     }
        # })


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

    # =====================================
    # GEMINI FIRST
    # =====================================

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("🟢 ARTICLE BOT ANSWERED BY GEMINI")

        return jsonify({
            "reply": response.text,
            "source": "gemini"
        })

    except Exception as e:

        print("❌ Gemini failed:", e)
        print("🟡 Switching to Groq...")

    # =====================================
    # GROQ FALLBACK
    # =====================================

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
                    """
                },
                {
                    "role": "user",

                    "content":
                        f"ARTICLE:\n{full_text}\n\nQUESTION:\n{question}"
                }
            ],

            temperature=0.7,
        )

        reply = response.choices[0].message.content

        print("🔵 ARTICLE BOT ANSWERED BY GROQ")

        return jsonify({
            "reply": reply,
            "source": "groq"
        })

    except Exception as e:

        print("❌ Groq failed:", e)

        return jsonify({
            "reply": "AI is currently unavailable.",
            "source": "none"
        })
# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
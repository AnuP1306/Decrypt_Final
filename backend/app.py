# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# from routes.home_routes import home_bp
# from routes.opportunities_routes import opportunities  # samiksha ✅ added
# from routes.auth_routes import auth_bp  # ✅ ADD THIS
# from routes.tools_routes import tools_bp
# import os
# from dotenv import load_dotenv
# import requests
# from google import genai
# import json
# from datetime import datetime
# import random
# import hashlib

# import time
# import json
# from groq import Groq
# from routes.saved_routes import saved_bp
# from routes.brief_routes import brief_bp

# with open("static/data/fallback_news.json", "r") as f:
#     FALLBACK_DATA = json.load(f)

# CACHE_FILE = "cache/slides_cache.json"

# try:
#     with open(CACHE_FILE, "r", encoding="utf-8") as f:
#         SLIDES_CACHE = json.load(f)
# except:
#     SLIDES_CACHE = {}

# NEWS_CACHE_FILE = "cache/news_cache.json"

# try:
#     with open(NEWS_CACHE_FILE, "r", encoding="utf-8") as f:

#         NEWS_CACHE = json.load(f)

# except:

#     NEWS_CACHE = {}


# # create app FIRST
# app = Flask(__name__)
# CORS(app)
# app.secret_key = os.getenv("SECRET_KEY")  # 🔥 REQUIRED for session


# def call_gemini_with_retry(model, prompt, retries=3, delay=2):
#     for attempt in range(retries):
#         try:
#             response = client.models.generate_content(model=model, contents=prompt)
#             return response.text
#         except Exception as e:
#             if "503" in str(e) and attempt < retries - 1:
#                 print(f"⚠️ Retry {attempt+1}, waiting {delay}s")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 raise e
#     return None


# # ================= SETUP =================
# load_dotenv()

# app.register_blueprint(home_bp)
# app.register_blueprint(opportunities)  # samiksha ✅ added
# app.register_blueprint(auth_bp)  # ✅ ADD THIS
# app.register_blueprint(tools_bp)
# app.register_blueprint(saved_bp)
# app.register_blueprint(brief_bp)

# # app.register_blueprint(opportunities)

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# def generate_article_id(title):

#     return hashlib.md5(title.lower().strip().encode()).hexdigest()


# # ================= CHATBOT =================
# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     user_msg = data.get("message", "")

#     system_prompt = f"""
#     You are the AI assistant for a website called Decrypt.

#     About Decrypt:
#      - It simplifies complex news into easy explanations
#      - It consists of only 3 domains for now which are AI, IT and Electronics
#      - Thers's a feature called daily brief/ today's brief
#      - It uses Beginner, Intermediate, Advanced levels
#      - It shows underrated AI tools
#      - Helps users understand news clearly

#     User: {user_msg}
#     """

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash", contents=system_prompt
#         )
#         return jsonify({"reply": response.text})

#     except Exception as e:
#         print("❌ Chatbot Gemini failed:", e)
#         return jsonify({"reply": "AI is currently busy. Please try again later."})


# # ================= FETCH NEWS =================

# # this version will only show fallback data and doesn't work with react
# # @app.route("/get-news", methods=["GET"])
# # def get_news():
# #     print("⚠️ Using FALLBACK NEWS (API limit hit)")

# #     return jsonify({
# #         "articles": FALLBACK_DATA
# #     })

# # only fallback data (works properly)
# # @app.route("/get-news", methods=["GET"])
# # def get_news():

# #     print("⚠️ Using FALLBACK NEWS (API limit hit)")

# #     fixed_articles = []

# #     for article in FALLBACK_DATA:

# #         article_copy = article.copy()

# #         if article_copy.get("image", "").startswith("/static/news-image/"):

# #             article_copy["image"] = article_copy["image"].replace(
# #                 "/static/news-image/",
# #                 "/news-image/"
# #             )

# #         fixed_articles.append(article_copy)

# #     return jsonify({
# #         "articles": fixed_articles
# #     })


# def prune_news_cache():

#     global NEWS_CACHE

#     today = datetime.utcnow().strftime("%Y-%m-%d")

#     fresh_cache = {}

#     for article_id, article in NEWS_CACHE.items():

#         article_date = article.get("date")

#         if article_date == today:

#             fresh_cache[article_id] = article

#     NEWS_CACHE = fresh_cache

#     print(f"🧹 Cache pruned. Remaining:" f" {len(NEWS_CACHE)} articles")


# @app.route("/get-news", methods=["GET"])
# def get_news():
#     today = datetime.utcnow().strftime("%Y-%m-%d")
#     prune_news_cache()

#     user_topics = request.args.get("topics", "")

#     topic_list = [t.strip() for t in user_topics.split(",") if t.strip()]

#     TOPIC_MAP = {
#         "Machine Learning": "machine learning OR deep learning OR neural networks",
#         "Web Dev": "web development OR frontend OR backend OR JavaScript",
#         "Robotics": "robotics OR automation OR robot",
#         "Cloud Computing": "AWS OR Azure OR Google Cloud OR cloud computing",
#         "Quantum Computing": "quantum computing OR qubit",
#         "Space Technology": "NASA OR SpaceX OR satellite OR space technology",
#         "IOT": "Internet of Things OR IoT OR smart devices",
#         "Cybersecurity": "cybersecurity OR ransomware OR data breach",
#     }

#     DEFAULT_QUERIES = {
#         "AI": (
#             "artificial intelligence OR generative AI "
#             "OR machine learning OR deep learning "
#             "OR LLM OR ChatGPT OR Gemini OR Claude"
#         ),
#         "IT": (
#             "cybersecurity OR software development "
#             "OR programming OR cloud computing "
#             "OR DevOps OR networking "
#             "OR data science "
#             "OR database"
#         ),
#         "Electronics": (
#             "semiconductor OR VLSI "
#             "OR embedded systems "
#             "OR IoT hardware "
#             "OR microcontroller "
#             "OR processor OR GPU "
#             "OR chip manufacturing "
#             "OR electronics"
#         ),
#     }

#     if topic_list:

#         queries = {}

#         for topic in topic_list[:4]:

#             if topic in TOPIC_MAP:

#                 queries[topic] = TOPIC_MAP[topic]

#         if not queries:

#             queries = DEFAULT_QUERIES

#     else:

#         queries = DEFAULT_QUERIES

#     # =====================================
#     # LOAD TODAY CACHE
#     # =====================================

#     all_articles = []

#     today_articles = []

#     for article_id, article in NEWS_CACHE.items():

#         if article.get("date") == today:

#             today_articles.append(article)

#     all_articles.extend(today_articles)

#     print(f"🟢 Loaded {len(today_articles)} articles from cache")

#     # =====================================
#     # RETURN CACHE IF ALREADY 15+
#     # =====================================

#     if len(today_articles) >= 15:

#         print("⚡ Serving entirely from cache")

#         return jsonify({"articles": today_articles[:15]})

#     # =====================================
#     # FETCH FROM GNEWS
#     # =====================================

#     needed_articles = max(0, 15 - len(all_articles))

#     print(f"📰 Need {needed_articles} more articles")

#     articles_per_domain = max(1, (needed_articles // len(queries)) + 1)

#     for domain, query in queries.items():

#         url = (
#             f"https://gnews.io/api/v4/search?"
#             f"q={query}"
#             f"&lang=en"
#             f"&max={articles_per_domain}"
#             f"&from={today}"
#             f"&sortby=publishedAt"
#             f"&apikey={GNEWS_API_KEY}"
#         )

#         try:

#             res = requests.get(url)

#             data = res.json()

#             if "articles" not in data:
#                 continue

#             for art in data["articles"]:

#                 article = {
#                     "id": generate_article_id(art.get("title", "")),
#                     "title": art.get("title", ""),
#                     "desc": art.get("description", ""),
#                     "content": art.get("content", ""),
#                     "image": art.get("image"),
#                     "domain": domain,
#                     "date": today,
#                 }

#                 if article["id"] not in NEWS_CACHE:

#                     NEWS_CACHE[article["id"]] = article

#                     all_articles.append(article)

#         except Exception as e:

#             print(f"❌ Failed fetching {domain}:", e)

#     # =====================================
#     # FALLBACK IF STILL BELOW 15
#     # =====================================

#     if len(all_articles) < 15:

#         print(f"⚠️ Only {len(all_articles)} articles. " f"Loading fallback news.")

#         existing_ids = {article["id"] for article in all_articles if "id" in article}

#         for item in FALLBACK_DATA:

#             fallback_id = generate_article_id(item.get("title", ""))

#             if fallback_id in existing_ids:

#                 continue

#             fallback_article = {
#                 "id": fallback_id,
#                 "title": item.get("title", ""),
#                 "desc": item.get("desc", ""),
#                 "content": item.get("content", ""),
#                 "image": item.get("image", ""),
#                 "domain": item.get("domain", "AI"),
#                 "date": today,
#             }

#             all_articles.append(fallback_article)

#             NEWS_CACHE[fallback_id] = fallback_article

#             if len(all_articles) >= 15:

#                 break

#     # =====================================
#     # SAVE CACHE
#     # =====================================

#     with open(NEWS_CACHE_FILE, "w", encoding="utf-8") as f:

#         json.dump(NEWS_CACHE, f, ensure_ascii=False, indent=2)

#     print(f"🔵 Saved {len(NEWS_CACHE)} cached articles")

#     # =====================================
#     # RETURN EXACTLY 15
#     # =====================================

#     all_articles = all_articles[:15]

#     print(f"✅ Returning {len(all_articles)} articles")

#     return jsonify({"articles": all_articles})


# # ================= GENERATE SLIDES =================
# @app.route("/generate-slides", methods=["POST"])
# def generate_slides():

#     data = request.json
#     index = data.get("index", 0)

#     title = data.get("title", "")

#     cache_key = title.strip().lower().replace("’", "'")

#     # 🔥 CHECK CACHE FIRST
#     if cache_key in SLIDES_CACHE:
#         print(f"🟢 CACHE HIT for: {title}")
#         return jsonify({"slides": SLIDES_CACHE[cache_key], "source": "cache"})
#     desc = data.get("desc", "")
#     content = data.get("content", "")

#     full_text = f"{title}. {desc}. {content}"

#     prompt = f"""
#     You are an AI that converts news into swipeable learning cards.

#     RULES:
#     - Beginner: simple
#     - Intermediate: balanced
#     - Advanced: deeper (min 60 words)

#     Each slide:
#     - minimum 35 words
#     - no cut sentences

#     Return JSON EXACTLY like:
#     {{
#       "beginner": [{{"title": "...", "desc": "..."}}],
#       "intermediate": [...],
#       "advanced": [...]
#     }}

#     News:
#     {full_text}
#     """

#     try:
#         raw_text = call_gemini_with_retry("gemini-2.5-flash", prompt)

#         if not raw_text:
#             raise Exception("Gemini failed after retries")

#         raw_text = raw_text.strip()
#         # response = client.models.generate_content(
#         #     model="gemini-2.5-flash",
#         #     contents=prompt
#         # )

#         # raw_text = response.text.strip()

#         if raw_text.startswith("```"):
#             raw_text = raw_text.replace("```json", "").replace("```", "").strip()

#         slides = json.loads(raw_text)
#         SLIDES_CACHE[cache_key] = slides
#         with open(CACHE_FILE, "w", encoding="utf-8") as f:
#             json.dump(SLIDES_CACHE, f, ensure_ascii=False, indent=2)
#         print(f"🔵 CACHE SAVED for: {title}")

#         return jsonify({"slides": slides, "source": "gemini"})

#     except Exception as e:
#         print("❌ Gemini failed:", e)

#         try:
#             # fallback = FALLBACK_DATA[index]
#             if index < len(FALLBACK_DATA):
#                 fallback = FALLBACK_DATA[index]
#             else:
#                 fallback = FALLBACK_DATA[index % len(FALLBACK_DATA)]
#             print(f"⚠️ Using FALLBACK for card index {index}")
#             return jsonify({"slides": fallback["slides"], "source": "fallback"})
#         except:
#             print(f"⚠️ Fallback index missing: {index}")

#         # 🔥 CURATED FALLBACK
#         # fallback = None

#         # for item in FALLBACK_DATA:
#         #     for keyword in item["keywords"]:
#         #         if keyword.lower() in title.lower():
#         #             fallback = item
#         #             break
#         #     if fallback:
#         #         break

#         # if fallback:
#         #     print(f"⚠️ Using FALLBACK for: {title}")
#         #     return jsonify({
#         #         "slides": fallback["slides"],
#         #         "source": "fallback"
#         #     })

#         # # 🛟 LAST RESORT (very rare)
#         # print(f"⚠️ No fallback match, using minimal safe fallback: {title}")

#         # 🛟 LAST RESORT (very rare)
#         print(f"⚠️ No fallback match, using minimal safe fallback: {title}")

#         safe_text = desc if desc else content if content else title

#         return jsonify(
#             {
#                 "slides": {
#                     "beginner": [{"title": title, "desc": safe_text[:120]}],
#                     "intermediate": [{"title": title, "desc": safe_text[:220]}],
#                     "advanced": [
#                         {
#                             "title": title,
#                             "desc": (
#                                 safe_text
#                                 + " This development may have broader implications as more details emerge."
#                             ),
#                         }
#                     ],
#                 }
#             }
#         )

#         # return jsonify({
#         #     "slides": {
#         #         "beginner": [{"title": title, "desc": desc or title}],
#         #         "intermediate": [{"title": title, "desc": desc or title}],
#         #         "advanced": [{"title": title, "desc": desc or title}]
#         #     }
#         # })
#         # safe_text = desc if desc else content if content else title

#         # return jsonify({
#         #     "slides": {
#         #         "beginner": [{"title": title, "desc": safe_text[:200]}],
#         #         "intermediate": [{"title": title, "desc": safe_text[:150]}],
#         #         "advanced": [{"title": title, "desc": safe_text[:300]}]
#         #     }
#         # })


# # ================= ARTICLE CHAT =================


# @app.route("/ask-article", methods=["POST"])
# def ask_article():

#     data = request.json

#     question = data.get("question", "")
#     article = data.get("article", "")

#     full_text = article

#     prompt = f"""
#     You are a smart assistant.

#     Answer using article + your knowledge if needed.

#     ARTICLE:
#     {full_text}

#     QUESTION:
#     {question}
#     """

#     # =====================================
#     # GEMINI FIRST
#     # =====================================

#     try:

#         response = client.models.generate_content(
#             model="gemini-2.5-flash", contents=prompt
#         )

#         print("🟢 ARTICLE BOT ANSWERED BY GEMINI")

#         return jsonify({"reply": response.text, "source": "gemini"})

#     except Exception as e:

#         print("❌ Gemini failed:", e)
#         print("🟡 Switching to Groq...")

#     # =====================================
#     # GROQ FALLBACK
#     # =====================================

#     try:

#         response = groq_client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
#                     You are an intelligent and helpful news assistant.

#                     - Use the provided article as your MAIN context.
#                     - You may use general knowledge ONLY if it directly supports the article or is related to the article.
#                     - Do NOT change topic or introduce unrelated domains.
#                     - If question is outside the article, say so politely.
#                     - If the article is incomplete, fill gaps intelligently.
#                     - Do NOT say "according to the article" again and again.
#                     - Speak naturally like a human in a friendly tone.
#                     - Keep answers clear, simple, and slightly conversational.
#                     - If comparison is asked, use general knowledge.
#                     """,
#                 },
#                 {
#                     "role": "user",
#                     "content": f"ARTICLE:\n{full_text}\n\nQUESTION:\n{question}",
#                 },
#             ],
#             temperature=0.7,
#         )

#         reply = response.choices[0].message.content

#         print("🔵 ARTICLE BOT ANSWERED BY GROQ")

#         return jsonify({"reply": reply, "source": "groq"})

#     except Exception as e:

#         print("❌ Groq failed:", e)

#         return jsonify({"reply": "AI is currently unavailable.", "source": "none"})


# # ================= RUN =================
# if __name__ == "__main__":
#     app.run(debug=True)

# 17th june version

# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# from routes.home_routes import home_bp
# from routes.opportunities_routes import opportunities  # samiksha ✅ added
# from routes.auth_routes import auth_bp  # ✅ ADD THIS
# from routes.tools_routes import tools_bp
# import os
# from dotenv import load_dotenv
# import requests
# from google import genai
# import json
# from datetime import datetime
# import random
# import hashlib

# import time
# import json
# from groq import Groq
# from routes.saved_routes import saved_bp
# from routes.brief_routes import brief_bp

# with open("static/data/fallback_news.json", "r") as f:
#     FALLBACK_DATA = json.load(f)

# CACHE_FILE = "cache/slides_cache.json"

# try:
#     with open(CACHE_FILE, "r", encoding="utf-8") as f:
#         SLIDES_CACHE = json.load(f)
# except:
#     SLIDES_CACHE = {}

# NEWS_CACHE_FILE = "cache/news_cache.json"

# try:
#     with open(NEWS_CACHE_FILE, "r", encoding="utf-8") as f:
#         NEWS_CACHE = json.load(f)
# except:
#     NEWS_CACHE = {}


# # create app FIRST
# app = Flask(__name__)
# CORS(app)
# app.secret_key = os.getenv("SECRET_KEY")  # 🔥 REQUIRED for session


# def call_gemini_with_retry(model, prompt, retries=3, delay=2):
#     for attempt in range(retries):
#         try:
#             response = client.models.generate_content(model=model, contents=prompt)
#             return response.text
#         except Exception as e:
#             if "503" in str(e) and attempt < retries - 1:
#                 print(f"⚠️ Retry {attempt+1}, waiting {delay}s")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 raise e
#     return None


# # ================= SETUP =================
# load_dotenv()

# app.register_blueprint(home_bp)
# app.register_blueprint(opportunities)  # samiksha ✅ added
# app.register_blueprint(auth_bp)  # ✅ ADD THIS
# app.register_blueprint(tools_bp)
# app.register_blueprint(saved_bp)
# app.register_blueprint(brief_bp)

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# def generate_article_id(title):
#     return hashlib.md5(title.lower().strip().encode()).hexdigest()


# # ================= DOMAIN CLASSIFICATION =================

# # Keywords used to verify/fix domain labels based on article content
# DOMAIN_KEYWORDS = {
#     "AI": [
#         "artificial intelligence",
#         "machine learning",
#         "deep learning",
#         "neural network",
#         "llm",
#         "large language model",
#         "chatgpt",
#         "gemini",
#         "claude",
#         "openai",
#         "generative ai",
#         "nlp",
#         "computer vision",
#         "reinforcement learning",
#         "transformer",
#         "diffusion model",
#         "gpt",
#         "mistral",
#         "llama",
#         "hugging face",
#         "stable diffusion",
#         "midjourney",
#         "copilot",
#         "ai model",
#         "ai tool",
#         "foundation model",
#     ],
#     "IT": [
#         "cybersecurity",
#         "software",
#         "programming",
#         "developer",
#         "devops",
#         "cloud computing",
#         "aws",
#         "azure",
#         "google cloud",
#         "kubernetes",
#         "docker",
#         "database",
#         "sql",
#         "api",
#         "backend",
#         "frontend",
#         "web development",
#         "javascript",
#         "python",
#         "data science",
#         "networking",
#         "ransomware",
#         "data breach",
#         "malware",
#         "firewall",
#         "open source",
#         "github",
#         "linux",
#         "server",
#         "saas",
#         "startup",
#     ],
#     "Electronics": [
#         "semiconductor",
#         "chip",
#         "processor",
#         "gpu",
#         "cpu",
#         "vlsi",
#         "embedded",
#         "microcontroller",
#         "arduino",
#         "raspberry pi",
#         "fpga",
#         "iot",
#         "internet of things",
#         "sensor",
#         "circuit",
#         "transistor",
#         "silicon",
#         "wafer",
#         "fabrication",
#         "tsmc",
#         "intel",
#         "amd",
#         "nvidia",
#         "qualcomm",
#         "arm",
#         "5g",
#         "rf",
#         "pcb",
#         "battery",
#         "power management",
#         "electronics",
#         "hardware",
#         "drone",
#         "robotics",
#     ],
# }


# def classify_domain(title, desc, content=""):
#     """
#     Classify an article into AI / IT / Electronics based on keyword matching.
#     Returns the best-matching domain or None if no clear match.
#     """
#     combined = f"{title} {desc} {content}".lower()

#     scores = {domain: 0 for domain in DOMAIN_KEYWORDS}

#     for domain, keywords in DOMAIN_KEYWORDS.items():
#         for kw in keywords:
#             if kw in combined:
#                 scores[domain] += 1

#     best_domain = max(scores, key=scores.get)

#     # Only override if we found at least one matching keyword
#     if scores[best_domain] > 0:
#         return best_domain

#     return None  # Unclear — keep the query-assigned domain


# # ================= CACHE HELPERS =================


# def prune_news_cache():
#     global NEWS_CACHE

#     today = datetime.utcnow().date()

#     fresh_cache = {}

#     for article_id, article in NEWS_CACHE.items():

#         try:
#             article_date = datetime.strptime(article.get("date", ""), "%Y-%m-%d").date()

#             age = (today - article_date).days

#             # keep today + previous 2 days
#             if age <= 2:
#                 fresh_cache[article_id] = article

#         except:
#             pass

#     removed = len(NEWS_CACHE) - len(fresh_cache)

#     NEWS_CACHE = fresh_cache

#     print(f"🧹 Cache pruned. Removed {removed}. " f"Remaining {len(NEWS_CACHE)}")


# # def prune_news_cache():

# # """
# # Remove articles that are NOT from today.
# # We intentionally keep only today's articles to stay fresh.
# # Articles from previous days are served from the fallback file instead.
# # """
# # global NEWS_CACHE

# # today = datetime.utcnow().strftime("%Y-%m-%d")
# # fresh_cache = {
# #     article_id: article
# #     for article_id, article in NEWS_CACHE.items()
# #     if article.get("date") == today
# # }

# # removed = len(NEWS_CACHE) - len(fresh_cache)
# # NEWS_CACHE = fresh_cache
# # print(
# #     f"🧹 Cache pruned. Removed {removed} old articles. Remaining: {len(NEWS_CACHE)}"
# # )


# def save_news_cache():
#     """Persist NEWS_CACHE to disk."""
#     try:
#         with open(NEWS_CACHE_FILE, "w", encoding="utf-8") as f:
#             json.dump(NEWS_CACHE, f, ensure_ascii=False, indent=2)
#         print(f"🔵 Saved {len(NEWS_CACHE)} cached articles")
#     except Exception as e:
#         print(f"❌ Failed to save news cache: {e}")


# # ================= CHATBOT =================
# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     user_msg = data.get("message", "")

#     system_prompt = f"""
#     You are the AI assistant for a website called Decrypt.

#     About Decrypt:
#      - It simplifies complex news into easy explanations
#      - It consists of only 3 domains for now which are AI, IT and Electronics
#      - Thers's a feature called daily brief/ today's brief
#      - It uses Beginner, Intermediate, Advanced levels
#      - It shows underrated AI tools
#      - Helps users understand news clearly

#     User: {user_msg}
#     """

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash", contents=system_prompt
#         )
#         return jsonify({"reply": response.text})

#     except Exception as e:
#         print("❌ Chatbot Gemini failed:", e)
#         return jsonify({"reply": "AI is currently busy. Please try again later."})


# # ================= FETCH NEWS =================


# @app.route("/get-news", methods=["GET"])
# def get_news():

#     print("⚠️ Using FALLBACK NEWS (DEBUG MODE)")

#     fixed_articles = []

#     for article in FALLBACK_DATA:

#         article_copy = article.copy()

#         if article_copy.get("image", "").startswith("/static/news-image/"):

#             article_copy["image"] = article_copy["image"].replace(
#                 "/static/news-image/", "/news-image/"
#             )

#         fixed_articles.append(article_copy)

#     return jsonify({"articles": fixed_articles})


# # original get-news function
# # @app.route("/get-news", methods=["GET"])
# # def get_news():
# #     today = datetime.utcnow().strftime("%Y-%m-%d")

# #     # ── 1. Prune stale cache entries ─────────────────────────────────────
# #     prune_news_cache()

# #     # ── 2. Resolve query topics ───────────────────────────────────────────
# #     user_topics = request.args.get("topics", "")
# #     topic_list = [t.strip() for t in user_topics.split(",") if t.strip()]

# #     TOPIC_MAP = {
# #         "Machine Learning": "machine learning OR deep learning OR neural networks",
# #         "Web Dev": "web development OR frontend OR backend OR JavaScript",
# #         "Robotics": "robotics OR automation OR robot",
# #         "Cloud Computing": "AWS OR Azure OR Google Cloud OR cloud computing",
# #         "Quantum Computing": "quantum computing OR qubit",
# #         "Space Technology": "NASA OR SpaceX OR satellite OR space technology",
# #         "IOT": "Internet of Things OR IoT OR smart devices",
# #         "Cybersecurity": "cybersecurity OR ransomware OR data breach",
# #     }

# #     # Fixed queries — always fetch all 3 domains so every domain has cards
# #     DEFAULT_QUERIES = {
# #         "AI": (
# #             "artificial intelligence OR generative AI "
# #             "OR machine learning OR deep learning "
# #             "OR LLM OR ChatGPT OR Gemini OR Claude"
# #         ),
# #         "IT": (
# #             "cybersecurity OR software development "
# #             "OR programming OR cloud computing "
# #             "OR DevOps OR networking "
# #             "OR data science OR database"
# #         ),
# #         "Electronics": (
# #             "semiconductor OR VLSI "
# #             "OR embedded systems "
# #             "OR IoT hardware "
# #             "OR microcontroller "
# #             "OR processor OR GPU "
# #             "OR chip manufacturing "
# #             "OR electronics"
# #         ),
# #     }

# #     if topic_list:
# #         queries = {}
# #         for topic in topic_list[:4]:
# #             if topic in TOPIC_MAP:
# #                 queries[topic] = TOPIC_MAP[topic]
# #         if not queries:
# #             queries = DEFAULT_QUERIES
# #     else:
# #         queries = DEFAULT_QUERIES

# #     # ── 3. Collect today's cached articles ───────────────────────────────
# #     today_articles = [
# #         article for article in NEWS_CACHE.values() if article.get("date") == today
# #     ]
# #     print(f"🟢 Loaded {len(today_articles)} articles from cache")

# #     # ── 4. Return early if cache is full (5 per domain = 15 total) ───────
# #     # Count per domain in cache
# #     domain_counts = {}
# #     for art in today_articles:
# #         d = art.get("domain", "")
# #         domain_counts[d] = domain_counts.get(d, 0) + 1

# #     # We need at least 5 per domain; if all domains already have 5, serve cache
# #     all_domains_full = all(domain_counts.get(d, 0) >= 5 for d in queries.keys())

# #     if all_domains_full:
# #         print("⚡ Serving entirely from cache")
# #         # return jsonify({"articles": today_articles})

# #     # ── 5. Fetch from GNews for domains that need more articles ───────────
# #     # Always fetch exactly 5 per domain from GNews regardless of cache state.
# #     # This ensures every domain has fresh articles today.
# #     ARTICLES_PER_DOMAIN = 5
# #     new_articles = []
# #     cache_updated = False

# #     for domain, query in queries.items():
# #         existing_for_domain = domain_counts.get(domain, 0)
# #         if existing_for_domain >= ARTICLES_PER_DOMAIN:
# #             print(
# #                 f"✅ {domain} already has {existing_for_domain} articles, skipping fetch"
# #             )
# #             continue

# #         needed_for_domain = ARTICLES_PER_DOMAIN - existing_for_domain
# #         print(f"📰 Fetching {needed_for_domain} more articles for {domain}")

# #         url = (
# #             f"https://gnews.io/api/v4/search?"
# #             f"q={query}"
# #             f"&lang=en"
# #             f"&max={needed_for_domain}"
# #             f"&from={today}"
# #             f"&sortby=publishedAt"
# #             f"&apikey={GNEWS_API_KEY}"
# #         )

# #         try:
# #             res = requests.get(url, timeout=10)
# #             data = res.json()

# #             if "articles" not in data:
# #                 print(f"⚠️ No articles in GNews response for {domain}: {data}")
# #                 continue

# #             for art in data["articles"]:
# #                 title = art.get("title", "")
# #                 desc = art.get("description", "")
# #                 content = art.get("content", "")

# #                 # Verify / correct domain label using keyword matching
# #                 detected_domain = classify_domain(title, desc, content)
# #                 final_domain = detected_domain if detected_domain else domain

# #                 article = {
# #                     "id": generate_article_id(title),
# #                     "title": title,
# #                     "desc": desc,
# #                     "content": content,
# #                     "image": art.get("image"),
# #                     "domain": final_domain,  # keyword-verified domain
# #                     "date": today,
# #                 }

# #                 if article["id"] not in NEWS_CACHE:
# #                     NEWS_CACHE[article["id"]] = article
# #                     new_articles.append(article)
# #                     cache_updated = True

# #         except Exception as e:
# #             print(f"❌ Failed fetching {domain}: {e}")
# #     # Build final feed per domain

# #     all_articles = []

# #     for domain in queries.keys():

# #         # Today's articles
# #         fresh_articles = [
# #             article
# #             for article in NEWS_CACHE.values()
# #             if article.get("domain") == domain and article.get("date") == today
# #         ]

# #         fresh_articles = fresh_articles[:5]

# #         # Older cached articles
# #         cached_articles = [
# #             article
# #             for article in NEWS_CACHE.values()
# #             if article.get("domain") == domain and article.get("date") != today
# #         ]

# #         cached_articles = cached_articles[:10]

# #         domain_feed = fresh_articles + cached_articles

# #         # Fill remaining slots from fallback
# #         remaining = 15 - len(domain_feed)

# #         if remaining > 0:

# #             fallback_count = 0

# #             for item in FALLBACK_DATA:

# #                 if fallback_count >= remaining:
# #                     break

# #                 item_domain = item.get("domain", "")

# #                 if item_domain.lower() != domain.lower():
# #                     continue

# #                 fallback_article = {
# #                     "id": generate_article_id(item.get("title", "")),
# #                     "title": item.get("title", ""),
# #                     "desc": item.get("desc", ""),
# #                     "content": item.get("content", ""),
# #                     "image": item.get("image", ""),
# #                     "domain": domain,
# #                     "date": today,
# #                 }

# #                 domain_feed.append(fallback_article)
# #                 fallback_count += 1

# #         all_articles.extend(domain_feed)

# #     if cache_updated:
# #         save_news_cache()

# #     print(f"✅ Returning {len(all_articles)} articles")
# #     return jsonify({"articles": all_articles})

# #     # Merge cache articles + new articles
# #     # all_articles = today_articles + new_articles

# #     # # ── 6. Fallback from static file if still below 5 per domain ─────────
# #     # # Recalculate domain counts after fetching
# #     # domain_counts_after = {}
# #     # for art in all_articles:
# #     #     d = art.get("domain", "")
# #     #     domain_counts_after[d] = domain_counts_after.get(d, 0) + 1

# #     # existing_ids = {art["id"] for art in all_articles if "id" in art}

# #     # for domain in queries.keys():
# #     #     needed = ARTICLES_PER_DOMAIN - domain_counts_after.get(domain, 0)
# #     #     if needed <= 0:
# #     #         continue

# #     #     print(f"⚠️ {domain} still needs {needed} articles — loading from fallback")

# #     #     fallback_added = 0
# #     #     for item in FALLBACK_DATA:
# #     #         if fallback_added >= needed:
# #     #             break

# #     #         # Match fallback items to this domain (case-insensitive)
# #     #         item_domain = item.get("domain", "")
# #     #         if item_domain.lower() != domain.lower():
# #     #             continue

# #     #         fallback_id = generate_article_id(item.get("title", ""))
# #     #         if fallback_id in existing_ids:
# #     #             continue

# #     #         fallback_article = {
# #     #             "id": fallback_id,
# #     #             "title": item.get("title", ""),
# #     #             "desc": item.get("desc", ""),
# #     #             "content": item.get("content", ""),
# #     #             "image": item.get("image", ""),
# #     #             "domain": domain,  # use the expected domain, not whatever's in the file
# #     #             "date": today,
# #     #         }

# #     #         all_articles.append(fallback_article)
# #     #         existing_ids.add(fallback_id)

# #     #         # Don't pollute the live cache with fallback data
# #     #         # (we want GNews to replace these tomorrow)
# #     #         fallback_added += 1

# #     # # ── 7. Save cache if anything new was fetched ─────────────────────────
# #     # if cache_updated:
# #     #     save_news_cache()

# #     # print(f"✅ Returning {len(all_articles)} articles")
# #     # return jsonify({"articles": all_articles})


# # ================= GENERATE SLIDES =================
# @app.route("/generate-slides", methods=["POST"])
# def generate_slides():

#     data = request.json
#     index = data.get("index", 0)
#     title = data.get("title", "")

#     cache_key = title.strip().lower().replace("'", "'")

#     # 🔥 CHECK CACHE FIRST
#     if cache_key in SLIDES_CACHE:
#         print(f"🟢 CACHE HIT for: {title}")
#         return jsonify({"slides": SLIDES_CACHE[cache_key], "source": "cache"})

#     desc = data.get("desc", "")
#     content = data.get("content", "")
#     full_text = f"{title}. {desc}. {content}"

#     prompt = f"""
#     You are an AI that converts news into swipeable learning cards.

#     RULES:
#     - Beginner: simple
#     - Intermediate: balanced
#     - Advanced: deeper (min 60 words)

#     Each slide:
#     - minimum 35 words
#     - no cut sentences

#     Return JSON EXACTLY like:
#     {{
#       "beginner": [{{"title": "...", "desc": "..."}}],
#       "intermediate": [...],
#       "advanced": [...]
#     }}

#     News:
#     {full_text}
#     """

#     try:
#         raw_text = call_gemini_with_retry("gemini-2.5-flash", prompt)

#         if not raw_text:
#             raise Exception("Gemini failed after retries")

#         raw_text = raw_text.strip()

#         if raw_text.startswith("```"):
#             raw_text = raw_text.replace("```json", "").replace("```", "").strip()

#         slides = json.loads(raw_text)
#         SLIDES_CACHE[cache_key] = slides
#         with open(CACHE_FILE, "w", encoding="utf-8") as f:
#             json.dump(SLIDES_CACHE, f, ensure_ascii=False, indent=2)
#         print(f"🔵 CACHE SAVED for: {title}")

#         return jsonify({"slides": slides, "source": "gemini"})

#     except Exception as e:
#         print("❌ Gemini failed:", e)

#         try:
#             if index < len(FALLBACK_DATA):
#                 fallback = FALLBACK_DATA[index]
#             else:
#                 fallback = FALLBACK_DATA[index % len(FALLBACK_DATA)]
#             print(f"⚠️ Using FALLBACK for card index {index}")
#             return jsonify({"slides": fallback["slides"], "source": "fallback"})
#         except:
#             print(f"⚠️ Fallback index missing: {index}")

#         # 🛟 LAST RESORT
#         print(f"⚠️ No fallback match, using minimal safe fallback: {title}")
#         safe_text = desc if desc else content if content else title

#         return jsonify(
#             {
#                 "slides": {
#                     "beginner": [{"title": title, "desc": safe_text[:120]}],
#                     "intermediate": [{"title": title, "desc": safe_text[:220]}],
#                     "advanced": [
#                         {
#                             "title": title,
#                             "desc": (
#                                 safe_text
#                                 + " This development may have broader implications as more details emerge."
#                             ),
#                         }
#                     ],
#                 }
#             }
#         )


# # ================= ARTICLE CHAT =================


# @app.route("/ask-article", methods=["POST"])
# def ask_article():

#     data = request.json
#     question = data.get("question", "")
#     article = data.get("article", "")
#     full_text = article

#     prompt = f"""
#     You are a smart assistant.

#     Answer using article + your knowledge if needed.

#     ARTICLE:
#     {full_text}

#     QUESTION:
#     {question}
#     """

#     # ── GEMINI FIRST ──────────────────────────────────────────────────────
#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash", contents=prompt
#         )
#         print("🟢 ARTICLE BOT ANSWERED BY GEMINI")
#         return jsonify({"reply": response.text, "source": "gemini"})

#     except Exception as e:
#         print("❌ Gemini failed:", e)
#         print("🟡 Switching to Groq...")

#     # ── GROQ FALLBACK ─────────────────────────────────────────────────────
#     try:
#         response = groq_client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
#                     You are an intelligent and helpful news assistant.

#                     - Use the provided article as your MAIN context.
#                     - You may use general knowledge ONLY if it directly supports the article or is related to the article.
#                     - Do NOT change topic or introduce unrelated domains.
#                     - If question is outside the article, say so politely.
#                     - If the article is incomplete, fill gaps intelligently.
#                     - Do NOT say "according to the article" again and again.
#                     - Speak naturally like a human in a friendly tone.
#                     - Keep answers clear, simple, and slightly conversational.
#                     - If comparison is asked, use general knowledge.
#                     """,
#                 },
#                 {
#                     "role": "user",
#                     "content": f"ARTICLE:\n{full_text}\n\nQUESTION:\n{question}",
#                 },
#             ],
#             temperature=0.7,
#         )

#         reply = response.choices[0].message.content
#         print("🔵 ARTICLE BOT ANSWERED BY GROQ")
#         return jsonify({"reply": reply, "source": "groq"})

#     except Exception as e:
#         print("❌ Groq failed:", e)
#         return jsonify({"reply": "AI is currently unavailable.", "source": "none"})


# # ================= RUN =================
# if __name__ == "__main__":
#     app.run(debug=True)


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


def generate_article_id(title):
    return hashlib.md5(title.lower().strip().encode()).hexdigest()


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


def get_news_live():
    """
    Fetches from GNews AT MOST ONCE per calendar day.
    - On first request of the day: calls GNews, updates cache, marks today as fetched.
    - On all subsequent requests that day: serves entirely from cache + fallback.
    - If GNews fails/rate-limits: still marks today as fetched so we don't retry.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Optional manual override for testing: GET /get-news?force_refresh=true
    force_refresh = request.args.get("force_refresh", "").lower() == "true"

    prune_news_cache()

    user_topics = request.args.get("topics", "")
    topic_list = [t.strip() for t in user_topics.split(",") if t.strip()]

    TOPIC_MAP = {
        "Machine Learning": "machine learning OR deep learning OR neural networks",
        "Web Dev": "web development OR frontend OR backend OR JavaScript",
        "Robotics": "robotics OR automation OR robot",
        "Cloud Computing": "AWS OR Azure OR Google Cloud OR cloud computing",
        "Quantum Computing": "quantum computing OR qubit",
        "Space Technology": "NASA OR SpaceX OR satellite OR space technology",
        "IOT": "Internet of Things OR IoT OR smart devices",
        "Cybersecurity": "cybersecurity OR ransomware OR data breach",
    }

    DEFAULT_QUERIES = {
        "AI": (
            "artificial intelligence OR generative AI "
            "OR machine learning OR deep learning "
            "OR LLM OR ChatGPT OR Gemini OR Claude"
        ),
        "IT": (
            "cybersecurity OR software development "
            "OR programming OR cloud computing "
            "OR DevOps OR networking "
            "OR data science OR database"
        ),
        "Electronics": (
            "semiconductor OR VLSI "
            "OR embedded systems "
            "OR IoT hardware "
            "OR microcontroller "
            "OR processor OR GPU "
            "OR chip manufacturing "
            "OR electronics"
        ),
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

    # ── THE ONCE-PER-DAY GATE ────────────────────────────────────────────
    last_fetch_date = get_last_fetch_date()
    needs_fetch = force_refresh or (last_fetch_date != today)

    cache_updated = False

    if needs_fetch:
        print(
            f"🌐 Last fetch was {last_fetch_date}, today is {today} — calling GNews once"
        )

        domain_counts = {}
        for art in NEWS_CACHE.values():
            if art.get("date") == today:
                d = art.get("domain", "")
                domain_counts[d] = domain_counts.get(d, 0) + 1

        ARTICLES_PER_DOMAIN = 5

        for domain, query in queries.items():
            existing_for_domain = domain_counts.get(domain, 0)
            if existing_for_domain >= ARTICLES_PER_DOMAIN:
                print(
                    f"✅ {domain} already has {existing_for_domain} today, skipping fetch"
                )
                continue

            needed_for_domain = ARTICLES_PER_DOMAIN - existing_for_domain
            print(f"📰 Fetching {needed_for_domain} more for {domain}")

            url = (
                f"https://gnews.io/api/v4/search?"
                f"q={query}"
                f"&lang=en"
                f"&max={needed_for_domain}"
                f"&from={today}"
                f"&sortby=publishedAt"
                f"&apikey={GNEWS_API_KEY}"
            )

            try:
                res = requests.get(url, timeout=10)
                data = res.json()

                if "articles" not in data:
                    print(f"⚠️ No articles in GNews response for {domain}: {data}")
                    continue

                for art in data["articles"]:
                    title = art.get("title", "")
                    desc = art.get("description", "")
                    content = art.get("content", "")

                    detected_domain = classify_domain(title, desc, content)
                    final_domain = detected_domain if detected_domain else domain

                    article = {
                        "id": generate_article_id(title),
                        "title": title,
                        "desc": desc,
                        "content": content,
                        "image": art.get("image"),
                        "domain": final_domain,
                        "date": today,
                    }

                    if article["id"] not in NEWS_CACHE:
                        NEWS_CACHE[article["id"]] = article
                        cache_updated = True

            except Exception as e:
                print(f"❌ Failed fetching {domain}: {e}")

        # 🔒 Mark today as "done" NO MATTER WHAT — even if every domain got
        # rate-limited. This kills the repeated-429 spiral.
        set_last_fetch_date(today)

    else:
        print(
            f"⚡ Already fetched today ({today}) — serving from cache, GNews NOT called"
        )

    if cache_updated:
        save_news_cache()

    # ── Build the final per-domain feed: fresh -> cached -> fallback ──────
    all_articles = []

    for domain in queries.keys():

        fresh_articles = [
            a
            for a in NEWS_CACHE.values()
            if a.get("domain") == domain and a.get("date") == today
        ][:5]

        cached_articles = [
            a
            for a in NEWS_CACHE.values()
            if a.get("domain") == domain and a.get("date") != today
        ][:10]

        domain_feed = fresh_articles + cached_articles
        existing_ids = {a["id"] for a in domain_feed if "id" in a}

        remaining = 15 - len(domain_feed)

        if remaining > 0:
            fallback_count = 0
            for item in FALLBACK_DATA:
                if fallback_count >= remaining:
                    break

                if item.get("domain", "").lower() != domain.lower():
                    continue

                fallback_id = generate_article_id(item.get("title", ""))
                if fallback_id in existing_ids:
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
                existing_ids.add(fallback_id)
                fallback_count += 1

        all_articles.extend(domain_feed)

    print(
        f"✅ Returning {len(all_articles)} articles (GNews hit this request: {needs_fetch})"
    )
    return jsonify({"articles": all_articles})


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

        slides = json.loads(raw_text)
        SLIDES_CACHE[cache_key] = slides
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

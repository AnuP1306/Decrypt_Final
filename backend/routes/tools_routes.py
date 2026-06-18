# from flask import Blueprint, render_template, jsonify
# from routes.home_routes import get_user_data
# from dotenv import load_dotenv
# import os, json, requests, re
# from datetime import datetime, timezone
# from urllib.parse import urlparse

# load_dotenv()
# tools_bp = Blueprint("tools", __name__)

# TOOLS_CACHE_FILE = "cache/tools_cache.json"
# PH_TOKEN = os.getenv("PRODUCT_HUNT_TOKEN")

# # ── 8 categories ──────────────────────────────────────────────────────────────
# CATEGORIES = [
#     "AI",
#     "Developer Tools",
#     "Design",
#     "Productivity",
#     "Security",
#     "Finance",
#     "Health & Wellness",
#     "Education",
# ]

# # ── Category keywords — ORDER MATTERS (checked top to bottom, first match wins)
# # More specific / distinctive keywords first; generic ones last.
# # Each category's keywords should NOT overlap with more specific categories.
# CATEGORY_KEYWORDS = {
#     "AI": [
#         "llm",
#         "large language model",
#         "gpt",
#         "openai",
#         "anthropic",
#         "claude",
#         "gemini",
#         "mistral",
#         "ollama",
#         "hugging face",
#         "stable diffusion",
#         "midjourney",
#         "dall-e",
#         "image generation",
#         "text generation",
#         "ai assistant",
#         "ai agent",
#         "ai tool",
#         "ai-powered",
#         "machine learning",
#         "neural network",
#         "fine-tun",
#         "rag ",
#         "retrieval augmented",
#         "vector embed",
#         "semantic search",
#         "ai chat",
#         "chatbot",
#         "copilot",
#         "ai model",
#         "ai platform",
#         "ai api",
#         "inference",
#         "prompt engineer",
#         "diffusion model",
#         "multimodal",
#         "speech recognition",
#         "tts ",
#         "text to speech",
#         "ai write",
#         "ai cod",
#         "ai generat",
#     ],
#     "Security": [
#         "security",
#         "cybersecurity",
#         "penetration test",
#         "pentest",
#         "exploit",
#         "vulnerability",
#         "cve",
#         "malware",
#         "phishing",
#         "ransomware",
#         "firewall",
#         "intrusion",
#         "siem",
#         "zero trust",
#         "threat intel",
#         "red team",
#         "blue team",
#         "ctf ",
#         "capture the flag",
#         "reverse engineer",
#         "decompil",
#         "forensic",
#         "osint",
#         "reconnaissance",
#         "password manager",
#         "password audit",
#         "secret manager",
#         "key management",
#         "2fa",
#         "mfa",
#         "vpn",
#         "proxy",
#         "anonymi",
#         "privacy tool",
#         "data breach",
#         "encrypt",
#         "decrypt",
#         "ssl ",
#         "tls ",
#         "certificate",
#         "audit log",
#     ],
#     "Finance": [
#         "finance",
#         "fintech",
#         "accounting",
#         "bookkeeping",
#         "invoice",
#         "payroll",
#         "expense track",
#         "budget",
#         "tax",
#         "trading",
#         "stock",
#         "equit",
#         "crypto",
#         "defi",
#         "blockchain",
#         "nft",
#         "wallet",
#         "payment",
#         "subscription billing",
#         "revenue",
#         "saas metric",
#         "mrr",
#         "arr",
#         "cap table",
#         "fundrais",
#         "investor",
#         "portfolio track",
#         "asset",
#         "personal finance",
#         "net worth",
#         "financial model",
#         "spreadsheet finance",
#         "bank",
#         "lending",
#         "mortgage",
#         "insurance",
#         "fund",
#     ],
#     "Health & Wellness": [
#         "health",
#         "fitness",
#         "workout",
#         "exercise",
#         "gym",
#         "nutrition",
#         "diet",
#         "calorie",
#         "sleep track",
#         "circadian",
#         "meditat",
#         "mindful",
#         "mental health",
#         "therapy",
#         "anxiety",
#         "stress",
#         "mood track",
#         "biohack",
#         "longevit",
#         "supplement",
#         "habit track",
#         "wellness",
#         "running",
#         "cycling",
#         "strength train",
#         "recovery",
#         "hrv",
#         "wearable",
#         "blood glucose",
#         "heart rate",
#         "breath",
#         "fasting",
#         "weight loss",
#         "body comp",
#     ],
#     "Education": [
#         "learn",
#         "course",
#         "tutorial",
#         "teach",
#         "education",
#         "student",
#         "classroom",
#         "school",
#         "university",
#         "study",
#         "quiz",
#         "flashcard",
#         "spaced repetition",
#         "curriculum",
#         "lesson",
#         "lecture",
#         "mooc",
#         "bootcamp",
#         "certification",
#         "skill",
#         "language learn",
#         "math",
#         "science education",
#         "coding learn",
#         "interview prep",
#         "practice problem",
#         "homework",
#         "academic",
#         "research paper",
#         "citation",
#     ],
#     "Design": [
#         "design",
#         "ui/ux",
#         "ux research",
#         "figma",
#         "sketch app",
#         "framer",
#         "wireframe",
#         "mockup",
#         "prototype",
#         "design system",
#         "component library",
#         "icon",
#         "illustration",
#         "vector",
#         "svg ",
#         "color palette",
#         "typography",
#         "font pair",
#         "logo",
#         "brand",
#         "visual identity",
#         "motion design",
#         "animation tool",
#         "3d design",
#         "generative art",
#         "creative tool",
#         "canva",
#         "photoshop alternative",
#         "image edit",
#         "background remov",
#         "screenshot beautif",
#         "design token",
#     ],
#     "Productivity": [
#         "productivity",
#         "note-tak",
#         "note taking",
#         "knowledge base",
#         "second brain",
#         "task manag",
#         "to-do",
#         "project manag",
#         "kanban",
#         "roadmap",
#         "time track",
#         "time block",
#         "calendar",
#         "scheduling",
#         "meeting",
#         "async",
#         "workflow automat",
#         "no-code automat",
#         "zapier alternative",
#         "email manag",
#         "inbox",
#         "writing tool",
#         "document editor",
#         "wiki",
#         "team collab",
#         "remote work",
#         "focus",
#         "pomodoro",
#         "distraction",
#         "clipboard",
#         "launcher",
#         "shortcut",
#         "bookmark",
#     ],
#     "Developer Tools": [
#         # intentionally last — broad terms like "api", "cli", "open source"
#         # only match here if nothing above matched first
#         "developer",
#         "devtool",
#         "dev tool",
#         "debugg",
#         "profil",
#         "terminal emulat",
#         "shell",
#         "cli tool",
#         "command line",
#         "sdk",
#         "ide ",
#         "code editor",
#         "vscode extension",
#         "jetbrains plugin",
#         "linter",
#         "formatter",
#         "static analys",
#         "code review",
#         "ci/cd",
#         "continuous integr",
#         "continuous deploy",
#         "pipeline",
#         "docker",
#         "kubernetes",
#         "k8s",
#         "container",
#         "orchestrat",
#         "infrastructure",
#         "iac",
#         "terraform",
#         "ansible",
#         "api test",
#         "api mock",
#         "api document",
#         "openapi",
#         "swagger",
#         "database tool",
#         "sql client",
#         "migration",
#         "orm ",
#         "monit",
#         "observ",
#         "logging",
#         "tracing",
#         "alerting",
#         "git ",
#         "github",
#         "gitlab",
#         "version control",
#         "code snippet",
#         "package manag",
#         "dependency",
#         "build tool",
#         "bundler",
#         "web scraper",
#         "headless browser",
#         "testing framework",
#         "mock",
#         "fixture",
#         "e2e test",
#         "unit test",
#         "backend",
#         "frontend",
#         "fullstack",
#         "framework",
#         "library",
#         "open source",
#         "self-host",
#         "selfhost",
#         "api ",
#     ],
# }


# # Minimum required keyword match score to assign a category
# # (prevents weak single-word matches on short titles)
# def detect_category(text: str) -> str:
#     """
#     Score each category by counting how many of its keywords appear in `text`.
#     Returns the highest-scoring category.  Falls back to 'Developer Tools'.
#     """
#     t = text.lower()
#     best_cat = "Developer Tools"
#     best_score = 0

#     for cat, kws in CATEGORY_KEYWORDS.items():
#         score = sum(1 for kw in kws if kw in t)
#         if score > best_score:
#             best_score = score
#             best_cat = cat

#     return best_cat


# def _today() -> str:
#     return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# def _days_ago(n: int) -> str:
#     from datetime import timedelta

#     return (datetime.now(timezone.utc) - timedelta(days=n)).strftime(
#         "%Y-%m-%dT00:00:00Z"
#     )


# def _load_cache() -> dict:
#     try:
#         with open(TOOLS_CACHE_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception:
#         return {}


# def _save_cache(data: dict):
#     try:
#         os.makedirs(os.path.dirname(TOOLS_CACHE_FILE), exist_ok=True)
#         with open(TOOLS_CACHE_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print(f"⚠️  Cache save error: {e}")


# def _domain(url: str) -> str:
#     try:
#         return urlparse(url).netloc.replace("www.", "").strip()
#     except Exception:
#         return ""


# def _favicon(url: str) -> str:
#     d = _domain(url)
#     return f"https://www.google.com/s2/favicons?domain={d}&sz=128" if d else ""


# # ── Genuinely underrated fallback tools (6 per category) ─────────────────────
# FALLBACK_TOOLS = [
#     # ── AI ────────────────────────────────────────────────────────────────────
#     {
#         "id": "fb-ai-1",
#         "name": "OpenRouter",
#         "tagline": "One API for every frontier model",
#         "description": "Single unified API key to access Claude, GPT-4, Mistral, Llama 3, Gemini and 50+ models. Pay per token, no subscriptions. Insanely useful for comparing outputs.",
#         "url": "https://openrouter.ai",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=openrouter.ai&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LLM", "#API"],
#     },
#     {
#         "id": "fb-ai-2",
#         "name": "LM Studio",
#         "tagline": "Run LLMs locally on your laptop",
#         "description": "Download and run Llama 3, Mistral, Phi-3 and hundreds of models entirely on your machine. No cloud, no API keys, no usage fees. Works offline.",
#         "url": "https://lmstudio.ai",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=lmstudio.ai&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LocalLLM", "#Free"],
#     },
#     {
#         "id": "fb-ai-3",
#         "name": "Msty",
#         "tagline": "Local AI chat with split-screen comparison",
#         "description": "Chat with local or cloud models side by side. Compare Claude vs GPT-4 vs Llama in the same window. Great for prompt testing.",
#         "url": "https://msty.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=msty.app&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LocalLLM", "#Free"],
#     },
#     {
#         "id": "fb-ai-4",
#         "name": "Langfuse",
#         "tagline": "Open-source LLM observability",
#         "description": "Trace, debug, and evaluate every LLM call in your app. Track costs, latency, and quality. Self-hostable and free for small teams.",
#         "url": "https://langfuse.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=langfuse.com&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#DevTool", "#OpenSource"],
#     },
#     {
#         "id": "fb-ai-5",
#         "name": "Fabric",
#         "tagline": "AI patterns for your terminal",
#         "description": "Open-source CLI that applies pre-built AI prompts (patterns) to any input. Summarize PDFs, extract insights from YouTube, write essays — all from your terminal.",
#         "url": "https://github.com/danielmiessler/fabric",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=github.com&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#CLI", "#OpenSource"],
#     },
#     {
#         "id": "fb-ai-6",
#         "name": "Kolors",
#         "tagline": "Underrated Chinese image AI that goes hard",
#         "description": "Image generation model from Kuaishou that rivals Midjourney on photorealism and follows prompts better than most Western alternatives. Free on Replicate.",
#         "url": "https://replicate.com/kwai-kolors/kolors",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=replicate.com&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#ImageGen", "#Free"],
#     },
#     # ── Developer Tools ───────────────────────────────────────────────────────
#     {
#         "id": "fb-dev-1",
#         "name": "Devbox",
#         "tagline": "Instant, isolated dev environments",
#         "description": "Create reproducible, isolated dev environments with a single JSON file. No Docker needed. Works like nix but without the learning curve.",
#         "url": "https://www.jetify.com/devbox",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=jetify.com&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#DevEnv", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-2",
#         "name": "Bruno",
#         "tagline": "Offline-first Postman alternative",
#         "description": "API client that stores collections as plain text files in your repo. No cloud sync, no accounts, no bloat. Version control your API tests with git.",
#         "url": "https://www.usebruno.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=usebruno.com&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#API", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-3",
#         "name": "Infisical",
#         "tagline": "Open-source secrets manager",
#         "description": "Sync .env files and secrets across your team and CI/CD. End-to-end encrypted. Self-hostable. The open-source alternative to Vault and Doppler.",
#         "url": "https://infisical.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=infisical.com&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#Security", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-4",
#         "name": "Mermaid Live",
#         "tagline": "Diagrams as code in your browser",
#         "description": "Write flowcharts, ERDs, sequence diagrams, and Gantt charts in plain text markdown syntax. Renders live. Embed anywhere with one URL.",
#         "url": "https://mermaid.live",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=mermaid.live&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#Diagrams", "#Free"],
#     },
#     {
#         "id": "fb-dev-5",
#         "name": "Litestream",
#         "tagline": "Continuous SQLite replication",
#         "description": "Replicate your SQLite database to S3, GCS, or Azure in real time. Run SQLite in production with zero operational overhead. Used by thousands of solo devs.",
#         "url": "https://litestream.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=litestream.io&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#SQLite", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-6",
#         "name": "Webhook.site",
#         "tagline": "Inspect and debug webhooks instantly",
#         "description": "Get a unique URL, send any HTTP request to it, and inspect the payload in real time. No sign-up needed. Saves hours of ngrok tunneling for webhook debugging.",
#         "url": "https://webhook.site",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=webhook.site&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#Webhooks", "#Free"],
#     },
#     # ── Design ────────────────────────────────────────────────────────────────
#     {
#         "id": "fb-design-1",
#         "name": "Penpot",
#         "tagline": "Open-source Figma alternative",
#         "description": "Design and prototype tool that stores files as SVG — not a proprietary format. Self-hostable, free forever, and works in the browser. Real Figma alternative.",
#         "url": "https://penpot.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=penpot.app&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#OpenSource", "#Free"],
#     },
#     {
#         "id": "fb-design-2",
#         "name": "Spline",
#         "tagline": "3D design for the web without Blender pain",
#         "description": "Create interactive 3D scenes that run in the browser. Export as embeddable iframes or React components. Free tier is generous for personal projects.",
#         "url": "https://spline.design",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=spline.design&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#3D", "#Web"],
#     },
#     {
#         "id": "fb-design-3",
#         "name": "Realtime Colors",
#         "tagline": "Preview color palettes on a real UI",
#         "description": "Visualize font and color combinations on an actual website layout, not just swatches. Exports to CSS, Tailwind, and Figma. Instantly see if your palette works.",
#         "url": "https://realtimecolors.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=realtimecolors.com&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Color", "#Free"],
#     },
#     {
#         "id": "fb-design-4",
#         "name": "UI Verse",
#         "tagline": "Open-source CSS component library",
#         "description": "Library of 5000+ beautifully crafted CSS and Tailwind components made by the community. Copy-paste buttons, cards, loaders, inputs — all free, no framework needed.",
#         "url": "https://uiverse.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=uiverse.io&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#CSS", "#OpenSource"],
#     },
#     {
#         "id": "fb-design-5",
#         "name": "Rive",
#         "tagline": "Interactive animations that run anywhere",
#         "description": "Design animations with a state machine that reacts to user input. Export as a tiny file that runs in web, mobile, or game engines. Way beyond Lottie.",
#         "url": "https://rive.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=rive.app&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Animation", "#Free"],
#     },
#     {
#         "id": "fb-design-6",
#         "name": "Dora",
#         "tagline": "3D animated websites with zero code",
#         "description": "Build scroll-animated, 3D landing pages by dragging and dropping. No code, no Webflow knowledge. Output is real HTML. Insane for portfolios.",
#         "url": "https://www.dora.run",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=dora.run&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#NoCode", "#3D"],
#     },
#     # ── Productivity ──────────────────────────────────────────────────────────
#     {
#         "id": "fb-prod-1",
#         "name": "Capacities",
#         "tagline": "The note-taking app that thinks like you",
#         "description": "Object-based notes — every person, book, project, and idea is its own typed object that links to everything else. More powerful than Notion for knowledge work.",
#         "url": "https://capacities.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=capacities.io&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Notes", "#PKM"],
#     },
#     {
#         "id": "fb-prod-2",
#         "name": "Raycast",
#         "tagline": "Spotlight replacement that does everything",
#         "description": "App launcher with built-in AI, clipboard history, window management, snippet expansion, and 1000+ extensions. Mac only but completely changes how you use your computer.",
#         "url": "https://raycast.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=raycast.com&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Mac", "#AI"],
#     },
#     {
#         "id": "fb-prod-3",
#         "name": "Superwhisper",
#         "tagline": "Voice-to-text that actually works",
#         "description": "Runs Whisper locally on your Mac for instant, insanely accurate voice transcription in any app. Dictate emails, code comments, Slack messages — offline, private.",
#         "url": "https://superwhisper.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=superwhisper.com&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Voice", "#AI"],
#     },
#     {
#         "id": "fb-prod-4",
#         "name": "Silverbullet",
#         "tagline": "Markdown wiki you self-host",
#         "description": "Open-source, self-hosted markdown knowledge base with slash commands, live queries, and a plugin system. Runs as a single binary. Your notes, your server.",
#         "url": "https://silverbullet.md",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=silverbullet.md&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#SelfHost", "#OpenSource"],
#     },
#     {
#         "id": "fb-prod-5",
#         "name": "Reclaim.ai",
#         "tagline": "AI that defends your calendar",
#         "description": "Automatically blocks time for tasks, habits, and breaks around your meetings. Reschedules itself when things run over. Connects to Linear, Asana, and Todoist.",
#         "url": "https://reclaim.ai",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=reclaim.ai&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Calendar", "#AI"],
#     },
#     {
#         "id": "fb-prod-6",
#         "name": "Anytype",
#         "tagline": "Local-first Notion alternative",
#         "description": "End-to-end encrypted, local-first workspace with pages, databases, and graphs. No vendor lock-in — data lives on your device and syncs peer-to-peer. Free forever.",
#         "url": "https://anytype.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=anytype.io&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#LocalFirst", "#Free"],
#     },
#     # ── Security ──────────────────────────────────────────────────────────────
#     {
#         "id": "fb-sec-1",
#         "name": "Caido",
#         "tagline": "Modern Burp Suite alternative",
#         "description": "Web security testing proxy built from scratch with a clean UI. Faster than Burp, better UX, free community tier. Built by ex-Burp power users.",
#         "url": "https://caido.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=caido.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#WebSec", "#Pentest"],
#     },
#     {
#         "id": "fb-sec-2",
#         "name": "Trufflehog",
#         "tagline": "Find secrets leaked in your git history",
#         "description": "Scans git repos, S3 buckets, Slack, Jira, and 700+ sources for accidentally committed API keys, passwords, and credentials. Free and open-source.",
#         "url": "https://trufflesecurity.com/trufflehog",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=trufflesecurity.com&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#SecretScanning", "#OpenSource"],
#     },
#     {
#         "id": "fb-sec-3",
#         "name": "Nuclei",
#         "tagline": "Community vulnerability scanner",
#         "description": "Fast, template-based vulnerability scanner with 9000+ community-written templates. Scan any target for CVEs, misconfigs, and exposed panels in minutes.",
#         "url": "https://nuclei.projectdiscovery.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=projectdiscovery.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Scanner", "#OpenSource"],
#     },
#     {
#         "id": "fb-sec-4",
#         "name": "CyberChef",
#         "tagline": "The Swiss Army knife of data encoding",
#         "description": "GCHQ's open-source web tool to encode, decode, encrypt, hash, and analyse data visually. Chain operations together like a pipeline. Runs 100% in the browser.",
#         "url": "https://gchq.github.io/CyberChef",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=gchq.github.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Encoding", "#GCHQ"],
#     },
#     {
#         "id": "fb-sec-5",
#         "name": "Proxyman",
#         "tagline": "Native macOS HTTP debugging proxy",
#         "description": "Intercept and inspect HTTPS traffic from any app, including iOS simulators and real devices. Way faster and cleaner than Charles Proxy.",
#         "url": "https://proxyman.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=proxyman.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Proxy", "#Mac"],
#     },
#     {
#         "id": "fb-sec-6",
#         "name": "Semgrep",
#         "tagline": "Static analysis that finds real bugs",
#         "description": "Write custom security rules in 5 minutes that find real vulnerabilities in your code. 3000+ community rules for every language. Integrates with GitHub CI.",
#         "url": "https://semgrep.dev",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=semgrep.dev&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#SAST", "#OpenSource"],
#     },
#     # ── Finance ───────────────────────────────────────────────────────────────
#     {
#         "id": "fb-fin-1",
#         "name": "Actual Budget",
#         "tagline": "Local-first YNAB alternative",
#         "description": "Self-hosted, open-source budgeting app based on envelope budgeting. Your data never leaves your machine. One-time price or free if you self-host.",
#         "url": "https://actualbudget.org",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=actualbudget.org&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Budget", "#SelfHost"],
#     },
#     {
#         "id": "fb-fin-2",
#         "name": "Ghostfolio",
#         "tagline": "Open-source wealth management",
#         "description": "Self-hostable portfolio tracker for stocks, crypto, and ETFs. Clean dashboard, performance charts, and fire number calculator. No subscription, your data.",
#         "url": "https://ghostfol.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=ghostfol.io&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Portfolio", "#OpenSource"],
#     },
#     {
#         "id": "fb-fin-3",
#         "name": "Lago",
#         "tagline": "Open-source billing and metering",
#         "description": "Usage-based billing infrastructure you can self-host. Replaces Stripe Billing, Chargebee, or Maxio. Handles metering, invoicing, and revenue recognition.",
#         "url": "https://getlago.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=getlago.com&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Billing", "#OpenSource"],
#     },
#     {
#         "id": "fb-fin-4",
#         "name": "Simplefi",
#         "tagline": "Indian stock portfolio tracker",
#         "description": "Portfolio tracker built for Indian investors — supports NSE/BSE stocks, mutual funds, SGBs, and US stocks. Tax P&L reports, XIRR, and asset allocation all free.",
#         "url": "https://simplefi.in",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=simplefi.in&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#India", "#Investing"],
#     },
#     {
#         "id": "fb-fin-5",
#         "name": "Maybe Finance",
#         "tagline": "Open-source personal finance OS",
#         "description": "Connect all your accounts, track net worth, and plan for retirement. Was a $1M VC-backed startup, now fully open-source and self-hostable after shutdown.",
#         "url": "https://maybefinance.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=maybefinance.com&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#NetWorth", "#OpenSource"],
#     },
#     {
#         "id": "fb-fin-6",
#         "name": "Hledger",
#         "tagline": "Plain text accounting for nerds",
#         "description": "Track finances in plain text files you version-control with git. Run queries, generate P&L and balance sheets from the command line. Free, no lock-in ever.",
#         "url": "https://hledger.org",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=hledger.org&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#PlainText", "#OpenSource"],
#     },
#     # ── Health & Wellness ─────────────────────────────────────────────────────
#     {
#         "id": "fb-health-1",
#         "name": "Intervals.icu",
#         "tagline": "Free Garmin Connect / Training Peaks alternative",
#         "description": "Analyze your cycling, running, and swimming data with power zones, fatigue tracking, and AI training load. Syncs from Garmin, Wahoo, Strava. 100% free.",
#         "url": "https://intervals.icu",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=intervals.icu&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Training", "#Free"],
#     },
#     {
#         "id": "fb-health-2",
#         "name": "Macrofactor",
#         "tagline": "Nutrition app that actually adapts",
#         "description": "Tracks calories and adjusts your targets based on your real-world weight trend — not just generic formulas. Most accurate TDEE estimator available. Worth paying for.",
#         "url": "https://macrofactorapp.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=macrofactorapp.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Nutrition", "#Science"],
#     },
#     {
#         "id": "fb-health-3",
#         "name": "Bearable",
#         "tagline": "Track everything that affects your health",
#         "description": "Log symptoms, mood, energy, sleep, meds, and habits in one place. Automatically finds correlations — like noticing your energy crashes when you sleep under 7h.",
#         "url": "https://bearable.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=bearable.app&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Tracking", "#Symptoms"],
#     },
#     {
#         "id": "fb-health-4",
#         "name": "Welltory",
#         "tagline": "HRV-based stress and energy scanner",
#         "description": "Measure your HRV using just your phone's camera, get a stress and energy score, and see which habits are actually affecting your recovery. Free tier is solid.",
#         "url": "https://welltory.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=welltory.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#HRV", "#Biohacking"],
#     },
#     {
#         "id": "fb-health-5",
#         "name": "Examine.com",
#         "tagline": "Unbiased supplement research database",
#         "description": "Massive database of human research on supplements and nutrition. No sponsored content, no brand deals. Find out what actually works before buying anything.",
#         "url": "https://examine.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=examine.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Supplements", "#Research"],
#     },
#     {
#         "id": "fb-health-6",
#         "name": "Balance",
#         "tagline": "Personalized meditation — first year free",
#         "description": "Meditation app that customizes every session based on your goals, experience, and how you're feeling. Built by the team behind Calm. First year is completely free.",
#         "url": "https://www.balanceapp.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=balanceapp.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Meditation", "#Free"],
#     },
#     # ── Education ─────────────────────────────────────────────────────────────
#     {
#         "id": "fb-edu-1",
#         "name": "Missing Semester",
#         "tagline": "The CS class your degree skipped",
#         "description": "MIT's free course on shell, vim, git, tmux, debugging, and security — the practical tools every programmer needs but no university actually teaches properly.",
#         "url": "https://missing.csail.mit.edu",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=missing.csail.mit.edu&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#MIT", "#Free"],
#     },
#     {
#         "id": "fb-edu-2",
#         "name": "Khanmigo",
#         "tagline": "AI Socratic tutor from Khan Academy",
#         "description": "AI tutor that asks you questions instead of giving answers — forces you to actually think. Built on GPT-4, designed to help students actually learn, not just get answers.",
#         "url": "https://www.khanacademy.org/khan-labs",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=khanacademy.org&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#AI", "#Tutoring"],
#     },
#     {
#         "id": "fb-edu-3",
#         "name": "Every.to/almanack",
#         "tagline": "Naval Ravikant's wisdom, organized",
#         "description": "The full Almanack of Naval Ravikant on wealth and happiness, free online. Better ROI per hour than most MBA content.",
#         "url": "https://www.navalmanack.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=navalmanack.com&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Wisdom", "#Free"],
#     },
#     {
#         "id": "fb-edu-4",
#         "name": "CS50",
#         "tagline": "Harvard's intro CS course, free forever",
#         "description": "The most enrolled course in Harvard's history, available free on edX. Best entry point into programming — covers C, Python, SQL, JavaScript in 12 weeks.",
#         "url": "https://cs50.harvard.edu",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=cs50.harvard.edu&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Harvard", "#CS"],
#     },
#     {
#         "id": "fb-edu-5",
#         "name": "Cursor rules",
#         "tagline": "Curated AI coding instructions",
#         "description": "Community library of .cursorrules files — instructions that tell AI coding assistants how to write code in your style, framework, and conventions. Massive time saver.",
#         "url": "https://cursor.directory",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=cursor.directory&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#AI", "#Coding"],
#     },
#     {
#         "id": "fb-edu-6",
#         "name": "Andymatuschak.org",
#         "tagline": "How to actually retain what you learn",
#         "description": "Andy Matuschak's public notes on memory, spaced repetition, and learning science. Includes interactive mnemonic medium essays. Changed how thousands of people learn.",
#         "url": "https://andymatuschak.org",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=andymatuschak.org&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Learning", "#Science"],
#     },
# ]


# # ── Hacker News ───────────────────────────────────────────────────────────────
# def fetch_hacker_news(per_category: int = 4) -> list:
#     """
#     Pull Show HN posts from last 14 days.
#     Uses the correct Algolia HN API tag syntax and a broader toolword set.
#     """
#     FOURTEEN_DAYS_AGO = int(datetime.now(timezone.utc).timestamp()) - 14 * 86400

#     # Algolia HN API: tags must be a single param like "show_hn,story"
#     # The correct format is query param repeated or as "(show_hn,story)"
#     try:
#         res = requests.get(
#             "https://hn.algolia.com/api/v1/search",
#             params={
#                 "query": "Show HN",
#                 "tags": "(show_hn,story)",
#                 "numericFilters": f"created_at_i>{FOURTEEN_DAYS_AGO},points>2",
#                 "hitsPerPage": 200,
#             },
#             timeout=15,
#         )
#         res.raise_for_status()
#         hits = res.json().get("hits", [])
#         print(f"📡 HN raw hits: {len(hits)}")
#     except Exception as e:
#         print(f"❌ HN fetch error: {e}")
#         return []

#     # Wider tool-word set — many Show HN posts don't say "tool" or "app"
#     TOOL_SIGNALS = {
#         "tool",
#         "app",
#         "platform",
#         "ai",
#         "generator",
#         "builder",
#         "editor",
#         "api",
#         "library",
#         "extension",
#         "bot",
#         "dashboard",
#         "cli",
#         "tracker",
#         "monitor",
#         "search",
#         "automat",
#         "scraper",
#         "analytic",
#         "service",
#         "site",
#         "plugin",
#         "agent",
#         "assistant",
#         "checker",
#         "viewer",
#         "manager",
#         "runner",
#         "deploy",
#         "host",
#         "server",
#         "client",
#         "convert",
#         "parser",
#         "detect",
#         "scan",
#         "audit",
#         "sync",
#         "backup",
#         "export",
#         "import",
#         "integrat",
#         "workflow",
#         "pipeline",
#         "template",
#     }

#     by_cat = {c: [] for c in CATEGORIES}
#     seen_dom: set = set()
#     rejected = 0

#     for hit in hits:
#         url = hit.get("url", "").strip()
#         title = hit.get("title", "").strip()
#         if not url or not title:
#             continue

#         # Clean the Show HN prefix
#         clean = re.sub(r"^Show HN\s*:?\s*", "", title, flags=re.IGNORECASE).strip()
#         title_lower = clean.lower()

#         # Signal check against BOTH title parts (name + description after dash)
#         if not any(sig in title_lower for sig in TOOL_SIGNALS):
#             rejected += 1
#             continue

#         dom = _domain(url)
#         if not dom or dom in seen_dom:
#             continue
#         seen_dom.add(dom)

#         # Parse "Name – description" or "Name: description" patterns
#         parts = re.split(r"\s+[-–—:]\s+", clean, maxsplit=1)
#         name = parts[0][:70].strip()
#         tagline = (parts[1] if len(parts) > 1 else clean)[:200].strip()

#         # Score category on full text for better matching
#         full_text = f"{name} {tagline}"
#         cat = detect_category(full_text)

#         if len(by_cat[cat]) >= per_category:
#             continue

#         by_cat[cat].append(
#             {
#                 "id": f"hn-{hit['objectID']}",
#                 "name": name,
#                 "tagline": tagline,
#                 "description": tagline,
#                 "url": url,
#                 "image": "",
#                 "favicon": _favicon(url),
#                 "category": cat,
#                 "is_free": True,
#                 "votes": hit.get("points", 0),
#                 "source": "hackernews",
#                 "tags": [
#                     f"#{cat.replace(' & ', '').replace(' ', '')}",
#                     "#ShowHN",
#                     "#Free",
#                 ],
#             }
#         )

#     result = [t for tools_list in by_cat.values() for t in tools_list]
#     print(f"✅ HN: {len(result)} tools kept ({rejected} rejected by signal check)")
#     return result


# # ── Product Hunt ──────────────────────────────────────────────────────────────
# def fetch_product_hunt(per_category: int = 4) -> list:
#     """
#     Fetch top PH launches from the last 7 days.
#     Uses a wider date window so there's enough data on any given day.
#     """
#     if not PH_TOKEN:
#         print("⚠️  No PRODUCT_HUNT_TOKEN — skipping PH fetch")
#         return []

#     # 7-day window gives ~200 launches to pick from
#     after_date = _days_ago(7)

#     query = """
#     query {
#       posts(order: VOTES, postedAfter: "%s", first: 50) {
#         edges {
#           node {
#             id
#             name
#             tagline
#             website
#             votesCount
#             thumbnail { url }
#             topics { edges { node { slug name } } }
#           }
#         }
#       }
#     }
#     """ % after_date

#     try:
#         res = requests.post(
#             "https://api.producthunt.com/v2/api/graphql",
#             json={"query": query},
#             headers={
#                 "Authorization": f"Bearer {PH_TOKEN}",
#                 "Content-Type": "application/json",
#                 "Accept": "application/json",
#             },
#             timeout=15,
#         )
#         res.raise_for_status()
#         payload = res.json()

#         if "errors" in payload:
#             print(f"❌ PH GraphQL errors: {payload['errors']}")
#             return []

#         edges = payload.get("data", {}).get("posts", {}).get("edges", [])
#         print(f"📡 PH raw edges: {len(edges)}")

#     except Exception as e:
#         print(f"❌ PH fetch error: {e}")
#         return []

#     by_cat = {c: [] for c in CATEGORIES}
#     seen_dom: set = set()

#     for edge in edges:
#         n = edge.get("node", {})
#         name = (n.get("name") or "").strip()
#         tagline = (n.get("tagline") or "").strip()
#         website = (n.get("website") or "").strip()

#         if not name or not tagline or not website:
#             continue

#         dom = _domain(website)
#         if not dom or dom in seen_dom:
#             continue
#         seen_dom.add(dom)

#         # Score on full text
#         cat = detect_category(f"{name} {tagline}")

#         if len(by_cat[cat]) >= per_category:
#             continue

#         # Prefer the PH thumbnail; fall back to favicon
#         thumbnail_url = (n.get("thumbnail") or {}).get("url", "")

#         by_cat[cat].append(
#             {
#                 "id": f"ph-{n['id']}",
#                 "name": name,
#                 "tagline": tagline,
#                 "description": tagline[:250],
#                 "url": website,
#                 "image": thumbnail_url,
#                 "favicon": _favicon(website),
#                 "category": cat,
#                 "is_free": True,
#                 "votes": n.get("votesCount", 0),
#                 "source": "producthunt",
#                 "tags": [
#                     f"#{cat.replace(' & ', '').replace(' ', '')}",
#                     "#ProductHunt",
#                 ],
#             }
#         )

#     result = [t for tools_list in by_cat.values() for t in tools_list]
#     print(f"✅ PH: {len(result)} tools across categories")
#     return result


# # ── Merge + pad ───────────────────────────────────────────────────────────────
# def build_final_list(ph: list, hn: list) -> list:
#     """
#     Merge PH (priority) + HN, deduplicate by domain,
#     then pad each category to TARGET_PER_CAT with curated fallback.
#     Always returns 8 × TARGET_PER_CAT tools.
#     """
#     TARGET_PER_CAT = 6

#     by_cat = {c: [] for c in CATEGORIES}
#     seen_dom: set = set()

#     # PH first (higher signal-to-noise), then HN
#     for t in ph + hn:
#         dom = _domain(t.get("url", ""))
#         if not dom or dom in seen_dom:
#             continue
#         seen_dom.add(dom)
#         cat = t["category"]
#         if cat in by_cat and len(by_cat[cat]) < TARGET_PER_CAT:
#             by_cat[cat].append(t)

#     # Pad with curated fallback
#     fb_by_cat: dict = {}
#     for t in FALLBACK_TOOLS:
#         fb_by_cat.setdefault(t["category"], []).append(t)

#     for cat in CATEGORIES:
#         needed = TARGET_PER_CAT - len(by_cat[cat])
#         if needed > 0:
#             pool = [
#                 t
#                 for t in fb_by_cat.get(cat, [])
#                 if _domain(t.get("url", "")) not in seen_dom
#             ][:needed]
#             for t in pool:
#                 seen_dom.add(_domain(t.get("url", "")))
#             by_cat[cat].extend(pool)
#             live = TARGET_PER_CAT - needed
#             print(f"  ↳ {cat}: {live} live + {len(pool)} fallback")

#     result = [t for cat in CATEGORIES for t in by_cat[cat]]
#     print(f"✅ Final tool list: {len(result)} tools")
#     return result


# # ── Flask routes ──────────────────────────────────────────────────────────────
# @tools_bp.route("/tools")
# def tools():
#     user_name, user_level, user_domain = get_user_data()
#     return render_template(
#         "tools.html",
#         user_name=user_name,
#         user_level=user_level,
#         user_domain=user_domain,
#     )


# @tools_bp.route("/get-tools", methods=["GET"])
# def get_tools():
#     cache = _load_cache()
#     today = _today()

#     if cache.get("date") == today and len(cache.get("tools", [])) >= 40:
#         print("⚡ Tools: serving from today's cache")
#         return jsonify({"tools": cache["tools"], "date": today, "source": "cache"})

#     print("🔄 Tools: fetching fresh data…")
#     ph = fetch_product_hunt(per_category=4)
#     hn = fetch_hacker_news(per_category=4)
#     data = build_final_list(ph, hn)

#     _save_cache({"date": today, "tools": data})
#     return jsonify({"tools": data, "date": today, "source": "fresh"})


# from flask import Blueprint, render_template, jsonify
# from routes.home_routes import get_user_data
# from dotenv import load_dotenv
# import os, json, requests, re
# from datetime import datetime, timezone
# from urllib.parse import urlparse

# load_dotenv()
# tools_bp = Blueprint("tools", __name__)

# TOOLS_CACHE_FILE = "cache/tools_cache.json"
# PH_TOKEN = os.getenv("PRODUCT_HUNT_TOKEN")

# # ── 8 categories ──────────────────────────────────────────────────────────────
# CATEGORIES = [
#     "AI",
#     "Developer Tools",
#     "Design",
#     "Productivity",
#     "Security",
#     "Finance",
#     "Health & Wellness",
#     "Education",
# ]

# # ── Category keywords — ORDER MATTERS (checked top to bottom, first match wins)
# # More specific / distinctive keywords first; generic ones last.
# # Each category's keywords should NOT overlap with more specific categories.
# CATEGORY_KEYWORDS = {
#     "AI": [
#         "llm",
#         "large language model",
#         "gpt",
#         "openai",
#         "anthropic",
#         "claude",
#         "gemini",
#         "mistral",
#         "ollama",
#         "hugging face",
#         "stable diffusion",
#         "midjourney",
#         "dall-e",
#         "image generation",
#         "text generation",
#         "ai assistant",
#         "ai agent",
#         "ai tool",
#         "ai-powered",
#         "machine learning",
#         "neural network",
#         "fine-tun",
#         "rag ",
#         "retrieval augmented",
#         "vector embed",
#         "semantic search",
#         "ai chat",
#         "chatbot",
#         "copilot",
#         "ai model",
#         "ai platform",
#         "ai api",
#         "inference",
#         "prompt engineer",
#         "diffusion model",
#         "multimodal",
#         "speech recognition",
#         "tts ",
#         "text to speech",
#         "ai write",
#         "ai cod",
#         "ai generat",
#     ],
#     "Security": [
#         "security",
#         "cybersecurity",
#         "penetration test",
#         "pentest",
#         "exploit",
#         "vulnerability",
#         "cve",
#         "malware",
#         "phishing",
#         "ransomware",
#         "firewall",
#         "intrusion",
#         "siem",
#         "zero trust",
#         "threat intel",
#         "red team",
#         "blue team",
#         "ctf ",
#         "capture the flag",
#         "reverse engineer",
#         "decompil",
#         "forensic",
#         "osint",
#         "reconnaissance",
#         "password manager",
#         "password audit",
#         "secret manager",
#         "key management",
#         "2fa",
#         "mfa",
#         "vpn",
#         "proxy",
#         "anonymi",
#         "privacy tool",
#         "data breach",
#         "encrypt",
#         "decrypt",
#         "ssl ",
#         "tls ",
#         "certificate",
#         "audit log",
#     ],
#     "Finance": [
#         "finance",
#         "fintech",
#         "accounting",
#         "bookkeeping",
#         "invoice",
#         "payroll",
#         "expense track",
#         "budget",
#         "tax",
#         "trading",
#         "stock",
#         "equit",
#         "crypto",
#         "defi",
#         "blockchain",
#         "nft",
#         "wallet",
#         "payment",
#         "subscription billing",
#         "revenue",
#         "saas metric",
#         "mrr",
#         "arr",
#         "cap table",
#         "fundrais",
#         "investor",
#         "portfolio track",
#         "asset",
#         "personal finance",
#         "net worth",
#         "financial model",
#         "spreadsheet finance",
#         "bank",
#         "lending",
#         "mortgage",
#         "insurance",
#         "fund",
#     ],
#     "Health & Wellness": [
#         "health",
#         "fitness",
#         "workout",
#         "exercise",
#         "gym",
#         "nutrition",
#         "diet",
#         "calorie",
#         "sleep track",
#         "circadian",
#         "meditat",
#         "mindful",
#         "mental health",
#         "therapy",
#         "anxiety",
#         "stress",
#         "mood track",
#         "biohack",
#         "longevit",
#         "supplement",
#         "habit track",
#         "wellness",
#         "running",
#         "cycling",
#         "strength train",
#         "recovery",
#         "hrv",
#         "wearable",
#         "blood glucose",
#         "heart rate",
#         "breath",
#         "fasting",
#         "weight loss",
#         "body comp",
#     ],
#     "Education": [
#         "learn",
#         "course",
#         "tutorial",
#         "teach",
#         "education",
#         "student",
#         "classroom",
#         "school",
#         "university",
#         "study",
#         "quiz",
#         "flashcard",
#         "spaced repetition",
#         "curriculum",
#         "lesson",
#         "lecture",
#         "mooc",
#         "bootcamp",
#         "certification",
#         "skill",
#         "language learn",
#         "math",
#         "science education",
#         "coding learn",
#         "interview prep",
#         "practice problem",
#         "homework",
#         "academic",
#         "research paper",
#         "citation",
#     ],
#     "Design": [
#         "design",
#         "ui/ux",
#         "ux research",
#         "figma",
#         "sketch app",
#         "framer",
#         "wireframe",
#         "mockup",
#         "prototype",
#         "design system",
#         "component library",
#         "icon",
#         "illustration",
#         "vector",
#         "svg ",
#         "color palette",
#         "typography",
#         "font pair",
#         "logo",
#         "brand",
#         "visual identity",
#         "motion design",
#         "animation tool",
#         "3d design",
#         "generative art",
#         "creative tool",
#         "canva",
#         "photoshop alternative",
#         "image edit",
#         "background remov",
#         "screenshot beautif",
#         "design token",
#     ],
#     "Productivity": [
#         "productivity",
#         "note-tak",
#         "note taking",
#         "knowledge base",
#         "second brain",
#         "task manag",
#         "to-do",
#         "project manag",
#         "kanban",
#         "roadmap",
#         "time track",
#         "time block",
#         "calendar",
#         "scheduling",
#         "meeting",
#         "async",
#         "workflow automat",
#         "no-code automat",
#         "zapier alternative",
#         "email manag",
#         "inbox",
#         "writing tool",
#         "document editor",
#         "wiki",
#         "team collab",
#         "remote work",
#         "focus",
#         "pomodoro",
#         "distraction",
#         "clipboard",
#         "launcher",
#         "shortcut",
#         "bookmark",
#     ],
#     "Developer Tools": [
#         # intentionally last — broad terms like "api", "cli", "open source"
#         # only match here if nothing above matched first
#         "developer",
#         "devtool",
#         "dev tool",
#         "debugg",
#         "profil",
#         "terminal emulat",
#         "shell",
#         "cli tool",
#         "command line",
#         "sdk",
#         "ide ",
#         "code editor",
#         "vscode extension",
#         "jetbrains plugin",
#         "linter",
#         "formatter",
#         "static analys",
#         "code review",
#         "ci/cd",
#         "continuous integr",
#         "continuous deploy",
#         "pipeline",
#         "docker",
#         "kubernetes",
#         "k8s",
#         "container",
#         "orchestrat",
#         "infrastructure",
#         "iac",
#         "terraform",
#         "ansible",
#         "api test",
#         "api mock",
#         "api document",
#         "openapi",
#         "swagger",
#         "database tool",
#         "sql client",
#         "migration",
#         "orm ",
#         "monit",
#         "observ",
#         "logging",
#         "tracing",
#         "alerting",
#         "git ",
#         "github",
#         "gitlab",
#         "version control",
#         "code snippet",
#         "package manag",
#         "dependency",
#         "build tool",
#         "bundler",
#         "web scraper",
#         "headless browser",
#         "testing framework",
#         "mock",
#         "fixture",
#         "e2e test",
#         "unit test",
#         "backend",
#         "frontend",
#         "fullstack",
#         "framework",
#         "library",
#         "open source",
#         "self-host",
#         "selfhost",
#         "api ",
#     ],
# }


# # Minimum required keyword match score to assign a category
# # (prevents weak single-word matches on short titles)
# def detect_category(text: str) -> str:
#     """
#     Score each category by counting how many of its keywords appear in `text`.
#     Returns the highest-scoring category.  Falls back to 'Developer Tools'.
#     """
#     t = text.lower()
#     best_cat = "Developer Tools"
#     best_score = 0

#     for cat, kws in CATEGORY_KEYWORDS.items():
#         score = sum(1 for kw in kws if kw in t)
#         if score > best_score:
#             best_score = score
#             best_cat = cat

#     return best_cat


# def _today() -> str:
#     return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# def _days_ago(n: int) -> str:
#     from datetime import timedelta

#     return (datetime.now(timezone.utc) - timedelta(days=n)).strftime(
#         "%Y-%m-%dT00:00:00Z"
#     )


# def _load_cache() -> dict:
#     try:
#         with open(TOOLS_CACHE_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception:
#         return {}


# def _save_cache(data: dict):
#     try:
#         os.makedirs(os.path.dirname(TOOLS_CACHE_FILE), exist_ok=True)
#         with open(TOOLS_CACHE_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print(f"⚠️  Cache save error: {e}")


# def _domain(url: str) -> str:
#     try:
#         return urlparse(url).netloc.replace("www.", "").strip()
#     except Exception:
#         return ""


# def _favicon(url: str) -> str:
#     d = _domain(url)
#     return f"https://www.google.com/s2/favicons?domain={d}&sz=128" if d else ""


# # ── Genuinely underrated fallback tools (6 per category) ─────────────────────
# FALLBACK_TOOLS = [
#     # ── AI ────────────────────────────────────────────────────────────────────
#     {
#         "id": "fb-ai-1",
#         "name": "OpenRouter",
#         "tagline": "One API for every frontier model",
#         "description": "Single unified API key to access Claude, GPT-4, Mistral, Llama 3, Gemini and 50+ models. Pay per token, no subscriptions. Insanely useful for comparing outputs.",
#         "url": "https://openrouter.ai",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=openrouter.ai&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LLM", "#API"],
#     },
#     {
#         "id": "fb-ai-2",
#         "name": "LM Studio",
#         "tagline": "Run LLMs locally on your laptop",
#         "description": "Download and run Llama 3, Mistral, Phi-3 and hundreds of models entirely on your machine. No cloud, no API keys, no usage fees. Works offline.",
#         "url": "https://lmstudio.ai",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=lmstudio.ai&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LocalLLM", "#Free"],
#     },
#     {
#         "id": "fb-ai-3",
#         "name": "Msty",
#         "tagline": "Local AI chat with split-screen comparison",
#         "description": "Chat with local or cloud models side by side. Compare Claude vs GPT-4 vs Llama in the same window. Great for prompt testing.",
#         "url": "https://msty.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=msty.app&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LocalLLM", "#Free"],
#     },
#     {
#         "id": "fb-ai-4",
#         "name": "Langfuse",
#         "tagline": "Open-source LLM observability",
#         "description": "Trace, debug, and evaluate every LLM call in your app. Track costs, latency, and quality. Self-hostable and free for small teams.",
#         "url": "https://langfuse.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=langfuse.com&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#DevTool", "#OpenSource"],
#     },
#     {
#         "id": "fb-ai-5",
#         "name": "Fabric",
#         "tagline": "AI patterns for your terminal",
#         "description": "Open-source CLI that applies pre-built AI prompts (patterns) to any input. Summarize PDFs, extract insights from YouTube, write essays — all from your terminal.",
#         "url": "https://github.com/danielmiessler/fabric",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=github.com&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#CLI", "#OpenSource"],
#     },
#     {
#         "id": "fb-ai-6",
#         "name": "Kolors",
#         "tagline": "Underrated Chinese image AI that goes hard",
#         "description": "Image generation model from Kuaishou that rivals Midjourney on photorealism and follows prompts better than most Western alternatives. Free on Replicate.",
#         "url": "https://replicate.com/kwai-kolors/kolors",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=replicate.com&sz=128",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#ImageGen", "#Free"],
#     },
#     # ── Developer Tools ───────────────────────────────────────────────────────
#     {
#         "id": "fb-dev-1",
#         "name": "Devbox",
#         "tagline": "Instant, isolated dev environments",
#         "description": "Create reproducible, isolated dev environments with a single JSON file. No Docker needed. Works like nix but without the learning curve.",
#         "url": "https://www.jetify.com/devbox",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=jetify.com&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#DevEnv", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-2",
#         "name": "Bruno",
#         "tagline": "Offline-first Postman alternative",
#         "description": "API client that stores collections as plain text files in your repo. No cloud sync, no accounts, no bloat. Version control your API tests with git.",
#         "url": "https://www.usebruno.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=usebruno.com&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#API", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-3",
#         "name": "Infisical",
#         "tagline": "Open-source secrets manager",
#         "description": "Sync .env files and secrets across your team and CI/CD. End-to-end encrypted. Self-hostable. The open-source alternative to Vault and Doppler.",
#         "url": "https://infisical.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=infisical.com&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#Security", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-4",
#         "name": "Mermaid Live",
#         "tagline": "Diagrams as code in your browser",
#         "description": "Write flowcharts, ERDs, sequence diagrams, and Gantt charts in plain text markdown syntax. Renders live. Embed anywhere with one URL.",
#         "url": "https://mermaid.live",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=mermaid.live&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#Diagrams", "#Free"],
#     },
#     {
#         "id": "fb-dev-5",
#         "name": "Litestream",
#         "tagline": "Continuous SQLite replication",
#         "description": "Replicate your SQLite database to S3, GCS, or Azure in real time. Run SQLite in production with zero operational overhead. Used by thousands of solo devs.",
#         "url": "https://litestream.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=litestream.io&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#SQLite", "#OpenSource"],
#     },
#     {
#         "id": "fb-dev-6",
#         "name": "Webhook.site",
#         "tagline": "Inspect and debug webhooks instantly",
#         "description": "Get a unique URL, send any HTTP request to it, and inspect the payload in real time. No sign-up needed. Saves hours of ngrok tunneling for webhook debugging.",
#         "url": "https://webhook.site",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=webhook.site&sz=128",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#DevTools", "#Webhooks", "#Free"],
#     },
#     # ── Design ────────────────────────────────────────────────────────────────
#     {
#         "id": "fb-design-1",
#         "name": "Penpot",
#         "tagline": "Open-source Figma alternative",
#         "description": "Design and prototype tool that stores files as SVG — not a proprietary format. Self-hostable, free forever, and works in the browser. Real Figma alternative.",
#         "url": "https://penpot.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=penpot.app&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#OpenSource", "#Free"],
#     },
#     {
#         "id": "fb-design-2",
#         "name": "Spline",
#         "tagline": "3D design for the web without Blender pain",
#         "description": "Create interactive 3D scenes that run in the browser. Export as embeddable iframes or React components. Free tier is generous for personal projects.",
#         "url": "https://spline.design",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=spline.design&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#3D", "#Web"],
#     },
#     {
#         "id": "fb-design-3",
#         "name": "Realtime Colors",
#         "tagline": "Preview color palettes on a real UI",
#         "description": "Visualize font and color combinations on an actual website layout, not just swatches. Exports to CSS, Tailwind, and Figma. Instantly see if your palette works.",
#         "url": "https://realtimecolors.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=realtimecolors.com&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Color", "#Free"],
#     },
#     {
#         "id": "fb-design-4",
#         "name": "UI Verse",
#         "tagline": "Open-source CSS component library",
#         "description": "Library of 5000+ beautifully crafted CSS and Tailwind components made by the community. Copy-paste buttons, cards, loaders, inputs — all free, no framework needed.",
#         "url": "https://uiverse.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=uiverse.io&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#CSS", "#OpenSource"],
#     },
#     {
#         "id": "fb-design-5",
#         "name": "Rive",
#         "tagline": "Interactive animations that run anywhere",
#         "description": "Design animations with a state machine that reacts to user input. Export as a tiny file that runs in web, mobile, or game engines. Way beyond Lottie.",
#         "url": "https://rive.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=rive.app&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Animation", "#Free"],
#     },
#     {
#         "id": "fb-design-6",
#         "name": "Dora",
#         "tagline": "3D animated websites with zero code",
#         "description": "Build scroll-animated, 3D landing pages by dragging and dropping. No code, no Webflow knowledge. Output is real HTML. Insane for portfolios.",
#         "url": "https://www.dora.run",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=dora.run&sz=128",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#NoCode", "#3D"],
#     },
#     # ── Productivity ──────────────────────────────────────────────────────────
#     {
#         "id": "fb-prod-1",
#         "name": "Capacities",
#         "tagline": "The note-taking app that thinks like you",
#         "description": "Object-based notes — every person, book, project, and idea is its own typed object that links to everything else. More powerful than Notion for knowledge work.",
#         "url": "https://capacities.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=capacities.io&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Notes", "#PKM"],
#     },
#     {
#         "id": "fb-prod-2",
#         "name": "Raycast",
#         "tagline": "Spotlight replacement that does everything",
#         "description": "App launcher with built-in AI, clipboard history, window management, snippet expansion, and 1000+ extensions. Mac only but completely changes how you use your computer.",
#         "url": "https://raycast.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=raycast.com&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Mac", "#AI"],
#     },
#     {
#         "id": "fb-prod-3",
#         "name": "Superwhisper",
#         "tagline": "Voice-to-text that actually works",
#         "description": "Runs Whisper locally on your Mac for instant, insanely accurate voice transcription in any app. Dictate emails, code comments, Slack messages — offline, private.",
#         "url": "https://superwhisper.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=superwhisper.com&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Voice", "#AI"],
#     },
#     {
#         "id": "fb-prod-4",
#         "name": "Silverbullet",
#         "tagline": "Markdown wiki you self-host",
#         "description": "Open-source, self-hosted markdown knowledge base with slash commands, live queries, and a plugin system. Runs as a single binary. Your notes, your server.",
#         "url": "https://silverbullet.md",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=silverbullet.md&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#SelfHost", "#OpenSource"],
#     },
#     {
#         "id": "fb-prod-5",
#         "name": "Reclaim.ai",
#         "tagline": "AI that defends your calendar",
#         "description": "Automatically blocks time for tasks, habits, and breaks around your meetings. Reschedules itself when things run over. Connects to Linear, Asana, and Todoist.",
#         "url": "https://reclaim.ai",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=reclaim.ai&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Calendar", "#AI"],
#     },
#     {
#         "id": "fb-prod-6",
#         "name": "Anytype",
#         "tagline": "Local-first Notion alternative",
#         "description": "End-to-end encrypted, local-first workspace with pages, databases, and graphs. No vendor lock-in — data lives on your device and syncs peer-to-peer. Free forever.",
#         "url": "https://anytype.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=anytype.io&sz=128",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#LocalFirst", "#Free"],
#     },
#     # ── Security ──────────────────────────────────────────────────────────────
#     {
#         "id": "fb-sec-1",
#         "name": "Caido",
#         "tagline": "Modern Burp Suite alternative",
#         "description": "Web security testing proxy built from scratch with a clean UI. Faster than Burp, better UX, free community tier. Built by ex-Burp power users.",
#         "url": "https://caido.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=caido.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#WebSec", "#Pentest"],
#     },
#     {
#         "id": "fb-sec-2",
#         "name": "Trufflehog",
#         "tagline": "Find secrets leaked in your git history",
#         "description": "Scans git repos, S3 buckets, Slack, Jira, and 700+ sources for accidentally committed API keys, passwords, and credentials. Free and open-source.",
#         "url": "https://trufflesecurity.com/trufflehog",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=trufflesecurity.com&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#SecretScanning", "#OpenSource"],
#     },
#     {
#         "id": "fb-sec-3",
#         "name": "Nuclei",
#         "tagline": "Community vulnerability scanner",
#         "description": "Fast, template-based vulnerability scanner with 9000+ community-written templates. Scan any target for CVEs, misconfigs, and exposed panels in minutes.",
#         "url": "https://nuclei.projectdiscovery.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=projectdiscovery.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Scanner", "#OpenSource"],
#     },
#     {
#         "id": "fb-sec-4",
#         "name": "CyberChef",
#         "tagline": "The Swiss Army knife of data encoding",
#         "description": "GCHQ's open-source web tool to encode, decode, encrypt, hash, and analyse data visually. Chain operations together like a pipeline. Runs 100% in the browser.",
#         "url": "https://gchq.github.io/CyberChef",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=gchq.github.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Encoding", "#GCHQ"],
#     },
#     {
#         "id": "fb-sec-5",
#         "name": "Proxyman",
#         "tagline": "Native macOS HTTP debugging proxy",
#         "description": "Intercept and inspect HTTPS traffic from any app, including iOS simulators and real devices. Way faster and cleaner than Charles Proxy.",
#         "url": "https://proxyman.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=proxyman.io&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Proxy", "#Mac"],
#     },
#     {
#         "id": "fb-sec-6",
#         "name": "Semgrep",
#         "tagline": "Static analysis that finds real bugs",
#         "description": "Write custom security rules in 5 minutes that find real vulnerabilities in your code. 3000+ community rules for every language. Integrates with GitHub CI.",
#         "url": "https://semgrep.dev",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=semgrep.dev&sz=128",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#SAST", "#OpenSource"],
#     },
#     # ── Finance ───────────────────────────────────────────────────────────────
#     {
#         "id": "fb-fin-1",
#         "name": "Actual Budget",
#         "tagline": "Local-first YNAB alternative",
#         "description": "Self-hosted, open-source budgeting app based on envelope budgeting. Your data never leaves your machine. One-time price or free if you self-host.",
#         "url": "https://actualbudget.org",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=actualbudget.org&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Budget", "#SelfHost"],
#     },
#     {
#         "id": "fb-fin-2",
#         "name": "Ghostfolio",
#         "tagline": "Open-source wealth management",
#         "description": "Self-hostable portfolio tracker for stocks, crypto, and ETFs. Clean dashboard, performance charts, and fire number calculator. No subscription, your data.",
#         "url": "https://ghostfol.io",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=ghostfol.io&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Portfolio", "#OpenSource"],
#     },
#     {
#         "id": "fb-fin-3",
#         "name": "Lago",
#         "tagline": "Open-source billing and metering",
#         "description": "Usage-based billing infrastructure you can self-host. Replaces Stripe Billing, Chargebee, or Maxio. Handles metering, invoicing, and revenue recognition.",
#         "url": "https://getlago.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=getlago.com&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Billing", "#OpenSource"],
#     },
#     {
#         "id": "fb-fin-4",
#         "name": "Simplefi",
#         "tagline": "Indian stock portfolio tracker",
#         "description": "Portfolio tracker built for Indian investors — supports NSE/BSE stocks, mutual funds, SGBs, and US stocks. Tax P&L reports, XIRR, and asset allocation all free.",
#         "url": "https://simplefi.in",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=simplefi.in&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#India", "#Investing"],
#     },
#     {
#         "id": "fb-fin-5",
#         "name": "Maybe Finance",
#         "tagline": "Open-source personal finance OS",
#         "description": "Connect all your accounts, track net worth, and plan for retirement. Was a $1M VC-backed startup, now fully open-source and self-hostable after shutdown.",
#         "url": "https://maybefinance.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=maybefinance.com&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#NetWorth", "#OpenSource"],
#     },
#     {
#         "id": "fb-fin-6",
#         "name": "Hledger",
#         "tagline": "Plain text accounting for nerds",
#         "description": "Track finances in plain text files you version-control with git. Run queries, generate P&L and balance sheets from the command line. Free, no lock-in ever.",
#         "url": "https://hledger.org",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=hledger.org&sz=128",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#PlainText", "#OpenSource"],
#     },
#     # ── Health & Wellness ─────────────────────────────────────────────────────
#     {
#         "id": "fb-health-1",
#         "name": "Intervals.icu",
#         "tagline": "Free Garmin Connect / Training Peaks alternative",
#         "description": "Analyze your cycling, running, and swimming data with power zones, fatigue tracking, and AI training load. Syncs from Garmin, Wahoo, Strava. 100% free.",
#         "url": "https://intervals.icu",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=intervals.icu&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Training", "#Free"],
#     },
#     {
#         "id": "fb-health-2",
#         "name": "Macrofactor",
#         "tagline": "Nutrition app that actually adapts",
#         "description": "Tracks calories and adjusts your targets based on your real-world weight trend — not just generic formulas. Most accurate TDEE estimator available. Worth paying for.",
#         "url": "https://macrofactorapp.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=macrofactorapp.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Nutrition", "#Science"],
#     },
#     {
#         "id": "fb-health-3",
#         "name": "Bearable",
#         "tagline": "Track everything that affects your health",
#         "description": "Log symptoms, mood, energy, sleep, meds, and habits in one place. Automatically finds correlations — like noticing your energy crashes when you sleep under 7h.",
#         "url": "https://bearable.app",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=bearable.app&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Tracking", "#Symptoms"],
#     },
#     {
#         "id": "fb-health-4",
#         "name": "Welltory",
#         "tagline": "HRV-based stress and energy scanner",
#         "description": "Measure your HRV using just your phone's camera, get a stress and energy score, and see which habits are actually affecting your recovery. Free tier is solid.",
#         "url": "https://welltory.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=welltory.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#HRV", "#Biohacking"],
#     },
#     {
#         "id": "fb-health-5",
#         "name": "Examine.com",
#         "tagline": "Unbiased supplement research database",
#         "description": "Massive database of human research on supplements and nutrition. No sponsored content, no brand deals. Find out what actually works before buying anything.",
#         "url": "https://examine.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=examine.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Supplements", "#Research"],
#     },
#     {
#         "id": "fb-health-6",
#         "name": "Balance",
#         "tagline": "Personalized meditation — first year free",
#         "description": "Meditation app that customizes every session based on your goals, experience, and how you're feeling. Built by the team behind Calm. First year is completely free.",
#         "url": "https://www.balanceapp.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=balanceapp.com&sz=128",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Meditation", "#Free"],
#     },
#     # ── Education ─────────────────────────────────────────────────────────────
#     {
#         "id": "fb-edu-1",
#         "name": "Missing Semester",
#         "tagline": "The CS class your degree skipped",
#         "description": "MIT's free course on shell, vim, git, tmux, debugging, and security — the practical tools every programmer needs but no university actually teaches properly.",
#         "url": "https://missing.csail.mit.edu",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=missing.csail.mit.edu&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#MIT", "#Free"],
#     },
#     {
#         "id": "fb-edu-2",
#         "name": "Khanmigo",
#         "tagline": "AI Socratic tutor from Khan Academy",
#         "description": "AI tutor that asks you questions instead of giving answers — forces you to actually think. Built on GPT-4, designed to help students actually learn, not just get answers.",
#         "url": "https://www.khanacademy.org/khan-labs",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=khanacademy.org&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#AI", "#Tutoring"],
#     },
#     {
#         "id": "fb-edu-3",
#         "name": "Every.to/almanack",
#         "tagline": "Naval Ravikant's wisdom, organized",
#         "description": "The full Almanack of Naval Ravikant on wealth and happiness, free online. Better ROI per hour than most MBA content.",
#         "url": "https://www.navalmanack.com",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=navalmanack.com&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Wisdom", "#Free"],
#     },
#     {
#         "id": "fb-edu-4",
#         "name": "CS50",
#         "tagline": "Harvard's intro CS course, free forever",
#         "description": "The most enrolled course in Harvard's history, available free on edX. Best entry point into programming — covers C, Python, SQL, JavaScript in 12 weeks.",
#         "url": "https://cs50.harvard.edu",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=cs50.harvard.edu&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Harvard", "#CS"],
#     },
#     {
#         "id": "fb-edu-5",
#         "name": "Cursor rules",
#         "tagline": "Curated AI coding instructions",
#         "description": "Community library of .cursorrules files — instructions that tell AI coding assistants how to write code in your style, framework, and conventions. Massive time saver.",
#         "url": "https://cursor.directory",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=cursor.directory&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#AI", "#Coding"],
#     },
#     {
#         "id": "fb-edu-6",
#         "name": "Andymatuschak.org",
#         "tagline": "How to actually retain what you learn",
#         "description": "Andy Matuschak's public notes on memory, spaced repetition, and learning science. Includes interactive mnemonic medium essays. Changed how thousands of people learn.",
#         "url": "https://andymatuschak.org",
#         "image": "",
#         "favicon": "https://www.google.com/s2/favicons?domain=andymatuschak.org&sz=128",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Learning", "#Science"],
#     },
# ]


# # ── Hacker News ───────────────────────────────────────────────────────────────
# def fetch_hacker_news(per_category: int = 4) -> list:
#     """
#     Pull Show HN posts from last 14 days.
#     Uses the correct Algolia HN API tag syntax and a broader toolword set.
#     """
#     FOURTEEN_DAYS_AGO = int(datetime.now(timezone.utc).timestamp()) - 14 * 86400

#     # Algolia HN API: tags must be a single param like "show_hn,story"
#     # The correct format is query param repeated or as "(show_hn,story)"
#     try:
#         res = requests.get(
#             "https://hn.algolia.com/api/v1/search",
#             params={
#                 "query": "Show HN",
#                 "tags": "(show_hn,story)",
#                 "numericFilters": f"created_at_i>{FOURTEEN_DAYS_AGO},points>2",
#                 "hitsPerPage": 200,
#             },
#             timeout=15,
#         )
#         res.raise_for_status()
#         hits = res.json().get("hits", [])
#         print(f"📡 HN raw hits: {len(hits)}")
#     except Exception as e:
#         print(f"❌ HN fetch error: {e}")
#         return []

#     # Wider tool-word set — many Show HN posts don't say "tool" or "app"
#     TOOL_SIGNALS = {
#         "tool",
#         "app",
#         "platform",
#         "ai",
#         "generator",
#         "builder",
#         "editor",
#         "api",
#         "library",
#         "extension",
#         "bot",
#         "dashboard",
#         "cli",
#         "tracker",
#         "monitor",
#         "search",
#         "automat",
#         "scraper",
#         "analytic",
#         "service",
#         "site",
#         "plugin",
#         "agent",
#         "assistant",
#         "checker",
#         "viewer",
#         "manager",
#         "runner",
#         "deploy",
#         "host",
#         "server",
#         "client",
#         "convert",
#         "parser",
#         "detect",
#         "scan",
#         "audit",
#         "sync",
#         "backup",
#         "export",
#         "import",
#         "integrat",
#         "workflow",
#         "pipeline",
#         "template",
#     }

#     by_cat = {c: [] for c in CATEGORIES}
#     seen_dom: set = set()
#     rejected = 0

#     for hit in hits:
#         url = hit.get("url", "").strip()
#         title = hit.get("title", "").strip()
#         if not url or not title:
#             continue

#         # Clean the Show HN prefix
#         clean = re.sub(r"^Show HN\s*:?\s*", "", title, flags=re.IGNORECASE).strip()
#         title_lower = clean.lower()

#         # Signal check against BOTH title parts (name + description after dash)
#         if not any(sig in title_lower for sig in TOOL_SIGNALS):
#             rejected += 1
#             continue

#         dom = _domain(url)
#         if not dom or dom in seen_dom:
#             continue
#         seen_dom.add(dom)

#         # Parse "Name – description" or "Name: description" patterns
#         parts = re.split(r"\s+[-–—:]\s+", clean, maxsplit=1)
#         name = parts[0][:70].strip()
#         tagline = (parts[1] if len(parts) > 1 else clean)[:200].strip()

#         # Score category on full text for better matching
#         full_text = f"{name} {tagline}"
#         cat = detect_category(full_text)

#         if len(by_cat[cat]) >= per_category:
#             continue

#         by_cat[cat].append(
#             {
#                 "id": f"hn-{hit['objectID']}",
#                 "name": name,
#                 "tagline": tagline,
#                 "description": tagline,
#                 "url": url,
#                 "image": "",
#                 "favicon": _favicon(url),
#                 "category": cat,
#                 "is_free": True,
#                 "votes": hit.get("points", 0),
#                 "source": "hackernews",
#                 "tags": [
#                     f"#{cat.replace(' & ', '').replace(' ', '')}",
#                     "#ShowHN",
#                     "#Free",
#                 ],
#             }
#         )

#     result = [t for tools_list in by_cat.values() for t in tools_list]
#     print(f"✅ HN: {len(result)} tools kept ({rejected} rejected by signal check)")
#     return result


# # ── Product Hunt ──────────────────────────────────────────────────────────────
# def fetch_product_hunt(per_category: int = 4) -> list:
#     """
#     Fetch top PH launches from the last 7 days.
#     Uses a wider date window so there's enough data on any given day.
#     """
#     if not PH_TOKEN:
#         print("⚠️  No PRODUCT_HUNT_TOKEN — skipping PH fetch")
#         return []

#     # 7-day window gives ~100+ launches to pick from.
#     # IMPORTANT: keep the query as flat as possible.
#     # `topics` is a nested collection that multiplies complexity ~500x per post
#     # and immediately blows PH's 500k complexity cap — never include it.
#     after_date = _days_ago(7)

#     query = """
#     query {
#       posts(order: VOTES, postedAfter: "%s", first: 30) {
#         edges {
#           node {
#             id
#             name
#             tagline
#             website
#             votesCount
#             thumbnail { url }
#           }
#         }
#       }
#     }
#     """ % after_date

#     try:
#         res = requests.post(
#             "https://api.producthunt.com/v2/api/graphql",
#             json={"query": query},
#             headers={
#                 "Authorization": f"Bearer {PH_TOKEN}",
#                 "Content-Type": "application/json",
#                 "Accept": "application/json",
#             },
#             timeout=15,
#         )
#         res.raise_for_status()
#         payload = res.json()

#         if "errors" in payload:
#             print(f"❌ PH GraphQL errors: {payload['errors']}")
#             return []

#         edges = payload.get("data", {}).get("posts", {}).get("edges", [])
#         print(f"📡 PH raw edges: {len(edges)}")

#     except Exception as e:
#         print(f"❌ PH fetch error: {e}")
#         return []

#     by_cat = {c: [] for c in CATEGORIES}
#     seen_dom: set = set()

#     for edge in edges:
#         n = edge.get("node", {})
#         name = (n.get("name") or "").strip()
#         tagline = (n.get("tagline") or "").strip()
#         website = (n.get("website") or "").strip()

#         if not name or not tagline or not website:
#             continue

#         dom = _domain(website)
#         if not dom or dom in seen_dom:
#             continue
#         seen_dom.add(dom)

#         # Score on full text
#         cat = detect_category(f"{name} {tagline}")

#         if len(by_cat[cat]) >= per_category:
#             continue

#         # Prefer the PH thumbnail; fall back to favicon
#         thumbnail_url = (n.get("thumbnail") or {}).get("url", "")

#         by_cat[cat].append(
#             {
#                 "id": f"ph-{n['id']}",
#                 "name": name,
#                 "tagline": tagline,
#                 "description": tagline[:250],
#                 "url": website,
#                 "image": thumbnail_url,
#                 "favicon": _favicon(website),
#                 "category": cat,
#                 "is_free": True,
#                 "votes": n.get("votesCount", 0),
#                 "source": "producthunt",
#                 "tags": [
#                     f"#{cat.replace(' & ', '').replace(' ', '')}",
#                     "#ProductHunt",
#                 ],
#             }
#         )

#     result = [t for tools_list in by_cat.values() for t in tools_list]
#     print(f"✅ PH: {len(result)} tools across categories")
#     return result


# # ── Merge + pad ───────────────────────────────────────────────────────────────
# def build_final_list(ph: list, hn: list) -> list:
#     """
#     Merge PH (priority) + HN, deduplicate by domain,
#     then pad each category to TARGET_PER_CAT with curated fallback.
#     Always returns 8 × TARGET_PER_CAT tools.
#     """
#     TARGET_PER_CAT = 6

#     by_cat = {c: [] for c in CATEGORIES}
#     seen_dom: set = set()

#     # PH first (higher signal-to-noise), then HN
#     for t in ph + hn:
#         dom = _domain(t.get("url", ""))
#         if not dom or dom in seen_dom:
#             continue
#         seen_dom.add(dom)
#         cat = t["category"]
#         if cat in by_cat and len(by_cat[cat]) < TARGET_PER_CAT:
#             by_cat[cat].append(t)

#     # Pad with curated fallback
#     fb_by_cat: dict = {}
#     for t in FALLBACK_TOOLS:
#         fb_by_cat.setdefault(t["category"], []).append(t)

#     for cat in CATEGORIES:
#         needed = TARGET_PER_CAT - len(by_cat[cat])
#         if needed > 0:
#             pool = [
#                 t
#                 for t in fb_by_cat.get(cat, [])
#                 if _domain(t.get("url", "")) not in seen_dom
#             ][:needed]
#             for t in pool:
#                 seen_dom.add(_domain(t.get("url", "")))
#             by_cat[cat].extend(pool)
#             live = TARGET_PER_CAT - needed
#             print(f"  ↳ {cat}: {live} live + {len(pool)} fallback")

#     result = [t for cat in CATEGORIES for t in by_cat[cat]]
#     print(f"✅ Final tool list: {len(result)} tools")
#     return result


# # ── Flask routes ──────────────────────────────────────────────────────────────
# @tools_bp.route("/tools")
# def tools():
#     user_name, user_level, user_domain = get_user_data()
#     return render_template(
#         "tools.html",
#         user_name=user_name,
#         user_level=user_level,
#         user_domain=user_domain,
#     )


# @tools_bp.route("/get-tools", methods=["GET"])
# def get_tools():
#     cache = _load_cache()
#     today = _today()

#     if cache.get("date") == today and len(cache.get("tools", [])) >= 40:
#         print("⚡ Tools: serving from today's cache")
#         return jsonify({"tools": cache["tools"], "date": today, "source": "cache"})

#     print("🔄 Tools: fetching fresh data…")
#     ph = fetch_product_hunt(per_category=4)
#     hn = fetch_hacker_news(per_category=4)
#     data = build_final_list(ph, hn)

#     _save_cache({"date": today, "tools": data})
#     return jsonify({"tools": data, "date": today, "source": "fresh"})


# from flask import Blueprint, render_template, jsonify
# from routes.home_routes import get_user_data
# from dotenv import load_dotenv
# import os, json, requests, re
# from datetime import datetime, timezone

# load_dotenv()
# tools_bp = Blueprint("tools", __name__)

# TOOLS_CACHE_FILE = "cache/tools_cache.json"
# PH_TOKEN = os.getenv("PRODUCT_HUNT_TOKEN")  # optional — add to .env when ready

# # ── 8 audience-relevant categories ───────────────────────────────────────────
# CATEGORIES = [
#     "AI Agents",
#     "LLMs",
#     "Developer Tools",
#     "Design & Creative",
#     "Productivity",
#     "Marketing & Sales",
#     "Health & Wellness",
#     "Engineering & Development",
# ]

# CATEGORY_KEYWORDS = {
#     "AI": [
#         "ai",
#         "gpt",
#         "llm",
#         "machine learning",
#         "neural",
#         "openai",
#         "claude",
#         "gemini",
#         "copilot",
#         "chatbot",
#         "ml",
#         "inference",
#         "language model",
#         "diffusion",
#         "stable diffusion",
#         "midjourney",
#     ],
#     "LLMs": [
#         "llm",
#         "language model",
#         "gpt",
#         "claude",
#         "gemini",
#         "mistral",
#         "openai",
#         "anthropic",
#         "prompt",
#         "rag",
#         "vector database",
#         "embedding",
#         "fine tuning",
#     ],
#     "Marketing & Sales": [
#         "marketing",
#         "sales",
#         "lead",
#         "crm",
#         "seo",
#         "email campaign",
#         "growth",
#         "social media",
#         "linkedin",
#         "outreach",
#         "ad campaign",
#         "conversion",
#     ],
#     "Engineering & Development": [
#         "engineering",
#         "developer",
#         "coding",
#         "code",
#         "github",
#         "react",
#         "typescript",
#         "python",
#         "api",
#         "framework",
#         "sdk",
#         "database",
#         "backend",
#         "frontend",
#         "devops",
#         "docker",
#         "kubernetes",
#     ],
#     "Developer Tools": [
#         "developer",
#         "dev tool",
#         "api",
#         "cli",
#         "terminal",
#         "vscode",
#         "extension",
#         "library",
#         "framework",
#         "sdk",
#         "open source",
#         "github",
#         "git",
#         "docker",
#         "kubernetes",
#         "ci/cd",
#         "devops",
#         "debug",
#         "lint",
#         "compiler",
#         "database",
#         "backend",
#         "frontend",
#         "react",
#         "vue",
#         "svelte",
#         "next.js",
#         "typescript",
#     ],
#     "Design & Creative": [
#         "design",
#         "ui",
#         "ux",
#         "figma",
#         "mockup",
#         "prototype",
#         "css",
#         "animation",
#         "svg",
#         "visual",
#         "color",
#         "font",
#         "typography",
#         "icon",
#         "illustration",
#         "brand",
#         "logo",
#         "canva",
#     ],
#     "Productivity": [
#         "productivity",
#         "workflow",
#         "automation",
#         "note",
#         "task",
#         "calendar",
#         "focus",
#         "writing",
#         "doc",
#         "meeting",
#         "email",
#         "slack",
#         "notion",
#         "todo",
#         "reminder",
#         "habit",
#         "schedule",
#     ],
#     # "Security": [
#     #     "security",
#     #     "privacy",
#     #     "encrypt",
#     #     "password",
#     #     "vpn",
#     #     "firewall",
#     #     "cyber",
#     #     "hack",
#     #     "vulnerability",
#     #     "auth",
#     #     "oauth",
#     #     "2fa",
#     #     "penetration",
#     #     "pentest",
#     #     "malware",
#     #     "phishing",
#     # ],
#     # "Finance": [
#     #     "finance",
#     #     "money",
#     #     "invest",
#     #     "stock",
#     #     "crypto",
#     #     "bitcoin",
#     #     "blockchain",
#     #     "budget",
#     #     "expense",
#     #     "tax",
#     #     "accounting",
#     #     "trading",
#     #     "portfolio",
#     #     "bank",
#     #     "payment",
#     #     "fintech",
#     # ],
#     "Health & Wellness": [
#         "health",
#         "fitness",
#         "mental",
#         "wellness",
#         "sleep",
#         "meditat",
#         "diet",
#         "nutrition",
#         "exercise",
#         "workout",
#         "therapy",
#         "stress",
#         "anxiety",
#         "mood",
#         "habit",
#         "mindful",
#     ],
#     # "Education": [
#     #     "learn",
#     #     "course",
#     #     "tutorial",
#     #     "education",
#     #     "student",
#     #     "study",
#     #     "quiz",
#     #     "teach",
#     #     "school",
#     #     "university",
#     #     "skill",
#     #     "coding bootcamp",
#     #     "certification",
#     #     "math",
#     #     "science",
#     #     "language",
#     # ],
# }


# def detect_category(text: str) -> str:
#     t = text.lower()
#     for cat, kws in CATEGORY_KEYWORDS.items():
#         if any(kw in t for kw in kws):
#             return cat
#     return "Developer Tools"  # sensible default for Show HN audience


# def _today() -> str:
#     return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# def _load_cache() -> dict:
#     try:
#         with open(TOOLS_CACHE_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except:
#         return {}


# def _save_cache(data: dict):
#     try:
#         with open(TOOLS_CACHE_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print(f"⚠️ Cache save error: {e}")


# # ── Curated fallback — 6 per category — shown when APIs return too little ─────
# FALLBACK_TOOLS = [
#     # AI
#     {
#         "id": "fb-1",
#         "name": "Perplexity AI",
#         "tagline": "AI-powered answer engine",
#         "description": "Ask anything and get cited, real-time answers. Think Google but it actually explains things.",
#         "url": "https://perplexity.ai",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#Search", "#Free"],
#     },
#     {
#         "id": "fb-2",
#         "name": "Phind",
#         "tagline": "AI search for developers",
#         "description": "Developer-focused AI search that understands code. Answers technical questions with code examples and sources.",
#         "url": "https://phind.com",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#Dev", "#Free"],
#     },
#     {
#         "id": "fb-3",
#         "name": "Krea AI",
#         "tagline": "Real-time AI image canvas",
#         "description": "Draw rough shapes, watch AI render it live as you edit. Free daily credits, zero friction.",
#         "url": "https://krea.ai",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#Image", "#Free"],
#     },
#     {
#         "id": "fb-4",
#         "name": "Poe",
#         "tagline": "Chat with multiple AI models",
#         "description": "Access Claude, GPT-4, Gemini and dozens of other models in one place. Great for comparing outputs.",
#         "url": "https://poe.com",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#LLM", "#Free"],
#     },
#     {
#         "id": "fb-5",
#         "name": "Ideogram",
#         "tagline": "AI images that can actually spell",
#         "description": "One of the only image generators that renders readable text inside images. Great for thumbnails.",
#         "url": "https://ideogram.ai",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#Image", "#Free"],
#     },
#     {
#         "id": "fb-6",
#         "name": "Udio",
#         "tagline": "AI music generation",
#         "description": "Type a genre and mood, get a full song with vocals in seconds. Free tier gives 10 songs/day.",
#         "url": "https://udio.com",
#         "category": "AI",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#AI", "#Music", "#Free"],
#     },
#     # Developer Tools
#     {
#         "id": "fb-7",
#         "name": "Warp",
#         "tagline": "The terminal for the 21st century",
#         "description": "AI-powered terminal with autocomplete, natural language commands, and team workflows built in.",
#         "url": "https://warp.dev",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Dev", "#Terminal", "#AI"],
#     },
#     {
#         "id": "fb-8",
#         "name": "Codeium",
#         "tagline": "Free GitHub Copilot alternative",
#         "description": "AI autocomplete that works in 70+ editors. Same quality as Copilot, completely free forever.",
#         "url": "https://codeium.com",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Dev", "#AI", "#Free"],
#     },
#     {
#         "id": "fb-9",
#         "name": "Ray.so",
#         "tagline": "Beautiful code screenshots",
#         "description": "Paste code, pick a theme, get a stunning screenshot for Twitter or your portfolio. Made by Raycast.",
#         "url": "https://ray.so",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Dev", "#Design", "#Free"],
#     },
#     {
#         "id": "fb-10",
#         "name": "Excalidraw",
#         "tagline": "Hand-drawn style whiteboard",
#         "description": "Open-source infinite canvas for architecture diagrams, wireframes, and quick sketches. No login needed.",
#         "url": "https://excalidraw.com",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Dev", "#Diagram", "#OpenSource"],
#     },
#     {
#         "id": "fb-11",
#         "name": "Hoppscotch",
#         "tagline": "Open-source Postman alternative",
#         "description": "Lightweight API testing tool that runs in the browser. Faster and less bloated than Postman.",
#         "url": "https://hoppscotch.io",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Dev", "#API", "#Free"],
#     },
#     {
#         "id": "fb-12",
#         "name": "Pieces",
#         "tagline": "AI code snippet manager",
#         "description": "Saves code snippets from anywhere, auto-tags them with context, and resurfaces them when you need them.",
#         "url": "https://pieces.app",
#         "category": "Developer Tools",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Dev", "#AI", "#Snippets"],
#     },
#     # Design
#     {
#         "id": "fb-13",
#         "name": "Fontjoy",
#         "tagline": "Font pairing with neural networks",
#         "description": "Click generate and get a perfectly matched heading, subheading, and body font combo instantly.",
#         "url": "https://fontjoy.com",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Typography", "#Free"],
#     },
#     {
#         "id": "fb-14",
#         "name": "Haikei",
#         "tagline": "Organic SVG blob and wave generator",
#         "description": "Generate layered blobs, waves, and stack SVG dividers with color control. Download or copy CSS.",
#         "url": "https://haikei.app",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#SVG", "#Free"],
#     },
#     {
#         "id": "fb-15",
#         "name": "Shots.so",
#         "tagline": "Device mockups in 30 seconds",
#         "description": "Drop in any screenshot and get a browser-framed or gradient-background mockup instantly.",
#         "url": "https://shots.so",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Mockup", "#Free"],
#     },
#     {
#         "id": "fb-16",
#         "name": "Animista",
#         "tagline": "CSS animation library with live preview",
#         "description": "Browse 100+ CSS animations, tweak timing and delay in real time, copy the keyframe code you need.",
#         "url": "https://animista.net",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#CSS", "#Animation"],
#     },
#     {
#         "id": "fb-17",
#         "name": "Coolors",
#         "tagline": "Generate color palettes in seconds",
#         "description": "Lock any color, hit spacebar to regenerate the rest. Export to CSS, Tailwind, Figma instantly.",
#         "url": "https://coolors.co",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#Color", "#Free"],
#     },
#     {
#         "id": "fb-18",
#         "name": "Recraft",
#         "tagline": "AI vector and brand illustration",
#         "description": "Generate consistent brand illustrations and icons that export as true SVG — not just rasterized.",
#         "url": "https://recraft.ai",
#         "category": "Design",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Design", "#AI", "#SVG"],
#     },
#     # Productivity
#     {
#         "id": "fb-19",
#         "name": "Tally",
#         "tagline": "Beautiful forms, free forever",
#         "description": "Form builder that doesn't look like Google Forms. Logic jumps, payments, file uploads — all free.",
#         "url": "https://tally.so",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Forms", "#Free"],
#     },
#     {
#         "id": "fb-20",
#         "name": "Obsidian",
#         "tagline": "Offline knowledge base with linked notes",
#         "description": "Local-first notes app with bidirectional links. Free forever, no subscription, data stays on your device.",
#         "url": "https://obsidian.md",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Notes", "#Free"],
#     },
#     {
#         "id": "fb-21",
#         "name": "Pika.style",
#         "tagline": "Instant beautiful screenshots",
#         "description": "Paste a screenshot, get a beautifully framed version with gradient background and padding in seconds.",
#         "url": "https://pika.style",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Design", "#Free"],
#     },
#     {
#         "id": "fb-22",
#         "name": "Lex",
#         "tagline": "AI writing inside a clean editor",
#         "description": "Writing tool built around a distraction-free editor. Hit Cmd+Enter and AI continues in your voice.",
#         "url": "https://lex.page",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#AI", "#Writing"],
#     },
#     {
#         "id": "fb-23",
#         "name": "Summarize.tech",
#         "tagline": "Summarize any YouTube video",
#         "description": "Paste any YouTube URL and get a full AI-generated summary. Saves hours of watching talks.",
#         "url": "https://summarize.tech",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#AI", "#YouTube"],
#     },
#     {
#         "id": "fb-24",
#         "name": "Loom",
#         "tagline": "Async video for teams",
#         "description": "Record screen + camera, share in one link. Replaces long Slack threads for explaining things.",
#         "url": "https://loom.com",
#         "category": "Productivity",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Productivity", "#Video", "#Teams"],
#     },
#     # Security
#     {
#         "id": "fb-25",
#         "name": "Have I Been Pwned",
#         "tagline": "Check if your email was breached",
#         "description": "Enter your email and instantly find out if it appeared in any known data breach. Run by Troy Hunt.",
#         "url": "https://haveibeenpwned.com",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Privacy", "#Free"],
#     },
#     {
#         "id": "fb-26",
#         "name": "Bitwarden",
#         "tagline": "Open-source password manager",
#         "description": "Free, open-source password manager that syncs across all devices. Audited and battle-tested.",
#         "url": "https://bitwarden.com",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Password", "#OpenSource"],
#     },
#     {
#         "id": "fb-27",
#         "name": "VirusTotal",
#         "tagline": "Scan files and URLs for malware",
#         "description": "Upload any file or URL and get 70+ antivirus scan results in seconds. Owned by Google.",
#         "url": "https://virustotal.com",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Malware", "#Free"],
#     },
#     {
#         "id": "fb-28",
#         "name": "Privacy Badger",
#         "tagline": "Block invisible trackers automatically",
#         "description": "EFF's browser extension that automatically learns to block trackers that violate Do Not Track.",
#         "url": "https://privacybadger.org",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Privacy", "#Extension"],
#     },
#     {
#         "id": "fb-29",
#         "name": "Mullvad VPN",
#         "tagline": "No-log VPN that accepts cash",
#         "description": "Privacy-first VPN that doesn't require an email or account. Pay anonymously. €5/month flat.",
#         "url": "https://mullvad.net",
#         "category": "Security",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#VPN", "#Privacy"],
#     },
#     {
#         "id": "fb-30",
#         "name": "Shodan",
#         "tagline": "Search engine for connected devices",
#         "description": "Find internet-connected devices, open ports, and vulnerabilities. Essential for security research.",
#         "url": "https://shodan.io",
#         "category": "Security",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Security", "#Research", "#OSINT"],
#     },
#     # Finance
#     {
#         "id": "fb-31",
#         "name": "Levels.fyi",
#         "tagline": "Real salary data from tech employees",
#         "description": "Crowdsourced compensation data from actual employees. Negotiate better with real numbers.",
#         "url": "https://levels.fyi",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Salary", "#Career"],
#     },
#     {
#         "id": "fb-32",
#         "name": "Exploding Topics",
#         "tagline": "Trends before they explode",
#         "description": "Finds fast-growing topics before they go mainstream. Great for startup ideas and investment research.",
#         "url": "https://explodingtopics.com",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Trends", "#Research"],
#     },
#     {
#         "id": "fb-33",
#         "name": "OpenBB",
#         "tagline": "Open-source Bloomberg Terminal",
#         "description": "Free, open-source investment research platform. Stocks, crypto, macroeconomics, all in one CLI.",
#         "url": "https://openbb.co",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Investing", "#OpenSource"],
#     },
#     {
#         "id": "fb-34",
#         "name": "Finviz",
#         "tagline": "Stock screener and market map",
#         "description": "Filter stocks by 60+ criteria, see the famous heatmap of the entire market. Free tier is powerful.",
#         "url": "https://finviz.com",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Stocks", "#Screener"],
#     },
#     {
#         "id": "fb-35",
#         "name": "CoinGecko",
#         "tagline": "Crypto data without the noise",
#         "description": "Track crypto prices, market cap, and on-chain data. Cleaner than CoinMarketCap, with better API.",
#         "url": "https://coingecko.com",
#         "category": "Finance",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Crypto", "#Free"],
#     },
#     {
#         "id": "fb-36",
#         "name": "Monarch Money",
#         "tagline": "Personal finance dashboard",
#         "description": "Connect all your accounts, track spending, set budgets, and see your net worth in one place.",
#         "url": "https://monarchmoney.com",
#         "category": "Finance",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Finance", "#Budget", "#Personal"],
#     },
#     # Health & Wellness
#     {
#         "id": "fb-37",
#         "name": "Huberman Lab",
#         "tagline": "Science-backed health protocols",
#         "description": "Free protocols from Stanford neuroscientist Andrew Huberman on sleep, focus, fitness, and stress.",
#         "url": "https://hubermanlab.com",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Science", "#Free"],
#     },
#     {
#         "id": "fb-38",
#         "name": "Waking Up",
#         "tagline": "Meditation without the fluff",
#         "description": "Sam Harris's meditation app with no spiritual baggage. Theory + practice. 30-day free trial.",
#         "url": "https://wakingup.com",
#         "category": "Health & Wellness",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Meditation", "#Mindfulness"],
#     },
#     {
#         "id": "fb-39",
#         "name": "Cronometer",
#         "tagline": "Precise nutrition tracking",
#         "description": "Track micronutrients, not just calories. Obsessively accurate food database loved by biohackers.",
#         "url": "https://cronometer.com",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Nutrition", "#Free"],
#     },
#     {
#         "id": "fb-40",
#         "name": "Supermaven",
#         "tagline": "AI fitness program generator",
#         "description": "Describe your goals and constraints, get a personalized workout program generated by AI.",
#         "url": "https://supermaven.ai",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#AI", "#Fitness"],
#     },
#     {
#         "id": "fb-41",
#         "name": "Oak",
#         "tagline": "Free breathing and meditation app",
#         "description": "Simple, beautifully designed breathing exercises and guided meditations. Completely free, no ads.",
#         "url": "https://oakmeditation.com",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Breathing", "#Free"],
#     },
#     {
#         "id": "fb-42",
#         "name": "Zero",
#         "tagline": "Intermittent fasting tracker",
#         "description": "Track fasting windows, log meals, and access science-backed content on fasting. Clean and simple.",
#         "url": "https://zerofasting.com",
#         "category": "Health & Wellness",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Health", "#Fasting", "#Free"],
#     },
#     # Education
#     {
#         "id": "fb-43",
#         "name": "Brilliant",
#         "tagline": "Learn by doing, not watching",
#         "description": "Interactive math, science, and CS courses built around problem-solving. Way more effective than videos.",
#         "url": "https://brilliant.org",
#         "category": "Education",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Math", "#CS"],
#     },
#     {
#         "id": "fb-44",
#         "name": "Anki",
#         "tagline": "Spaced repetition flashcards",
#         "description": "The gold standard for memorizing anything. Open-source, works on all platforms, and actually works.",
#         "url": "https://apps.ankiweb.net",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Memory", "#Free"],
#     },
#     {
#         "id": "fb-45",
#         "name": "Explainpaper",
#         "tagline": "Understand any research paper",
#         "description": "Upload a PDF, highlight confusing text, ask AI to explain it in plain English. Made for students.",
#         "url": "https://explainpaper.com",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#AI", "#Research"],
#     },
#     {
#         "id": "fb-46",
#         "name": "Readwise",
#         "tagline": "Remember what you read",
#         "description": "Resurfaces highlights from books, articles, and Kindle. Daily email of your best saved passages.",
#         "url": "https://readwise.io",
#         "category": "Education",
#         "is_free": False,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Reading", "#Memory"],
#     },
#     {
#         "id": "fb-47",
#         "name": "Scrimba",
#         "tagline": "Learn to code by doing",
#         "description": "Interactive coding environment where you edit the instructor's code mid-video. Genuinely different.",
#         "url": "https://scrimba.com",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Coding", "#Free"],
#     },
#     {
#         "id": "fb-48",
#         "name": "roadmap.sh",
#         "tagline": "Developer roadmaps for every path",
#         "description": "Community-built roadmaps for frontend, backend, DevOps, AI, and more. Free, open-source, updated.",
#         "url": "https://roadmap.sh",
#         "category": "Education",
#         "is_free": True,
#         "votes": 0,
#         "source": "curated",
#         "tags": ["#Education", "#Dev", "#Free"],
#     },
# ]


# def fetch_hacker_news(per_category=3):
#     """Pull Show HN tools from last 7 days, categorize them."""
#     try:
#         res = requests.get(
#             "https://hn.algolia.com/api/v1/search",
#             params={
#                 "query": "Show HN",
#                 "tags": "show_hn,story",
#                 "numericFilters": f"created_at_i>{int(datetime.now(timezone.utc).timestamp()) - 7*86400}",
#                 "hitsPerPage": 100,
#             },
#             timeout=12,
#         )
#         hits = res.json().get("hits", [])

#         TOOL_WORDS = [
#             "tool",
#             "app",
#             "platform",
#             "ai",
#             "generator",
#             "builder",
#             "editor",
#             "api",
#             "library",
#             "extension",
#             "bot",
#             "dashboard",
#             "cli",
#             "tracker",
#             "monitor",
#             "search",
#             "automat",
#             "scraper",
#             "analytic",
#         ]

#         by_cat = {c: [] for c in CATEGORIES}
#         seen_dom = set()

#         for hit in hits:
#             url = hit.get("url", "")
#             title = hit.get("title", "")
#             if not url or not title:
#                 continue
#             if not any(w in title.lower() for w in TOOL_WORDS):
#                 continue
#             try:
#                 domain = requests.utils.urlparse(url).netloc.replace("www.", "")
#             except:
#                 continue
#             if domain in seen_dom:
#                 continue
#             seen_dom.add(domain)

#             clean = re.sub(r"^Show HN\s*:?\s*", "", title, flags=re.IGNORECASE).strip()
#             parts = re.split(r"\s+[-–]\s+", clean, maxsplit=1)
#             name = parts[0][:60]
#             tagline = parts[1] if len(parts) > 1 else clean
#             cat = detect_category(clean + " " + tagline)

#             if len(by_cat[cat]) >= per_category:
#                 continue

#             by_cat[cat].append(
#                 {
#                     "id": f"hn-{hit['objectID']}",
#                     "name": name,
#                     "tagline": tagline[:120],
#                     "description": tagline[:220],
#                     "url": url,
#                     "image": "",  # filled below
#                     "favicon": f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
#                     "category": cat,
#                     "is_free": True,
#                     "votes": hit.get("points", 0),
#                     "source": "hackernews",
#                     "tags": [
#                         f"#{cat.replace(' & ', '').replace(' ', '')}",
#                         "#ShowHN",
#                         "#Free" if True else "",
#                     ],
#                 }
#             )

#         result = [t for tools in by_cat.values() for t in tools]
#         print(f"✅ HN: {len(result)} tools across categories")
#         return result
#     except Exception as e:
#         print(f"❌ HN fetch failed: {e}")
#         return []


# def fetch_product_hunt(per_category=3):
#     """Pull today's PH launches if token exists."""
#     if not PH_TOKEN:
#         print("⚠️  No PRODUCT_HUNT_TOKEN — skipping PH")
#         return []
#     query = """
#     query {
#       posts(order: VOTES, postedAfter: "%sT00:00:00Z", first: 30) {
#         edges { node {
#           id name tagline website votesCount
#           thumbnail { url }
#           topics { edges { node { slug name } } }
#         }}
#       }
#     }
#     """ % _today()
#     try:
#         res = requests.post(
#             "https://api.producthunt.com/v2/api/graphql",
#             json={"query": query},
#             headers={
#                 "Authorization": f"Bearer {PH_TOKEN}",
#                 "Content-Type": "application/json",
#             },
#             timeout=12,
#         )
#         edges = res.json().get("data", {}).get("posts", {}).get("edges", [])
#         by_cat = {c: [] for c in CATEGORIES}

#         for edge in edges:
#             n = edge["node"]
#             # cat = detect_category(n["name"] + " " + n["tagline"])
#             topic_names = [
#                 t["node"]["name"] for t in n.get("topics", {}).get("edges", [])
#             ]

#             topic_map = {
#                 "AI Agents": "AI Agents",
#                 "LLMs": "LLMs",
#                 "Developer Tools": "Developer Tools",
#                 "Engineering & Development": "Engineering & Development",
#                 "Design Tools": "Design & Creative",
#                 "Design & Creative": "Design & Creative",
#                 "Productivity": "Productivity",
#                 "Marketing": "Marketing & Sales",
#                 "Marketing & Sales": "Marketing & Sales",
#                 "Health & Fitness": "Health & Wellness",
#                 "Health": "Health & Wellness",
#                 # fallback mappings
#                 "Artificial Intelligence": "AI Agents",
#             }

#             # topic_map = {
#             #     "Artificial Intelligence": "AI",
#             #     "Developer Tools": "Developer Tools",
#             #     "Design Tools": "Design",
#             #     "Productivity": "Productivity",
#             #     "Finance": "Finance",
#             #     "Education": "Education",
#             #     "Health & Fitness": "Health & Wellness",
#             #     "Security": "Security",
#             # }

#             cat = None

#             for topic in topic_names:
#                 if topic in topic_map:
#                     cat = topic_map[topic]
#                     break

#             if not cat:
#                 cat = detect_category(n["name"] + " " + n["tagline"])
#             if len(by_cat[cat]) >= per_category:
#                 continue
#             try:
#                 domain = requests.utils.urlparse(n["website"]).netloc.replace(
#                     "www.", ""
#                 )
#             except:
#                 domain = ""
#             by_cat[cat].append(
#                 {
#                     "id": f"ph-{n['id']}",
#                     "name": n["name"],
#                     "tagline": n["tagline"],
#                     "description": n["tagline"][:220],
#                     "url": n["website"],
#                     "image": (n.get("thumbnail") or {}).get("url", ""),
#                     "favicon": f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
#                     "category": cat,
#                     "is_free": True,
#                     "votes": n["votesCount"],
#                     "source": "producthunt",
#                     "tags": [
#                         f"#{cat.replace(' & ', '').replace(' ', '')}",
#                         "#ProductHunt",
#                     ],
#                 }
#             )

#         result = [t for tools in by_cat.values() for t in tools]
#         print(f"✅ PH: {len(result)} tools across categories")
#         return result
#     except Exception as e:
#         print(f"❌ PH fetch failed: {e}")
#         return []


# def build_final_list(ph, hn):
#     """
#     Merge PH + HN, then pad each category to exactly 6 from fallback.
#     Guarantees 48 tools (8 × 6) on the page always.
#     """
#     TARGET_PER_CAT = 6

#     # Group live tools by category
#     by_cat = {c: [] for c in CATEGORIES}
#     seen = set()

#     for t in ph + hn:
#         url = t.get("url", "")
#         if url in seen:
#             continue
#         seen.add(url)
#         cat = t["category"]
#         if cat in by_cat and len(by_cat[cat]) < TARGET_PER_CAT:
#             by_cat[cat].append(t)

#     # Pad with fallback where needed
#     fb_by_cat = {}
#     for t in FALLBACK_TOOLS:
#         fb_by_cat.setdefault(t["category"], []).append(t)

#     for cat in CATEGORIES:
#         needed = TARGET_PER_CAT - len(by_cat[cat])
#         if needed > 0:
#             pool = [t for t in fb_by_cat.get(cat, []) if t["url"] not in seen][:needed]
#             for t in pool:
#                 seen.add(t["url"])
#             by_cat[cat].extend(pool)
#             print(f"  ↳ {cat}: padded {len(pool)} from fallback")

#     result = [t for cat in CATEGORIES for t in by_cat[cat]]
#     print(f"✅ Final tool list: {len(result)} tools")
#     return result


# # ── Original Flask route — keep for sidebar/session ──────────────────────────
# @tools_bp.route("/tools")
# def tools():
#     user_name, user_level, user_domain = get_user_data()
#     return render_template(
#         "tools.html",
#         user_name=user_name,
#         user_level=user_level,
#         user_domain=user_domain,
#     )


# # ── React API ─────────────────────────────────────────────────────────────────
# @tools_bp.route("/get-tools", methods=["GET"])
# def get_tools():
#     cache = _load_cache()
#     today = _today()

#     # Serve cache if it's from today and has enough tools
#     if cache.get("date") == today and len(cache.get("tools", [])) >= 40:
#         print("⚡ Tools: serving from today's cache")
#         return jsonify({"tools": cache["tools"], "date": today, "source": "cache"})

#     print("🔄 Tools: fetching fresh data...")
#     ph = fetch_product_hunt(per_category=6)
#     hn = fetch_hacker_news(per_category=6)
#     data = build_final_list(ph, hn)

#     _save_cache({"date": today, "tools": data})
#     return jsonify({"tools": data, "date": today, "source": "fresh"})
from flask import Blueprint, render_template, jsonify
from routes.home_routes import get_user_data
from dotenv import load_dotenv
import os, json, requests, re
from datetime import datetime, timezone

load_dotenv()
tools_bp = Blueprint("tools", __name__)

TOOLS_CACHE_FILE = "cache/tools_cache.json"
PH_TOKEN = os.getenv("PRODUCT_HUNT_TOKEN")

# ── NEW 8 categories ──────────────────────────────────────────────────────────
CATEGORIES = [
    "AI Agents",
    "LLMs",
    "Developer Tools",
    "Design & Creative",
    "Productivity",
    "Marketing & Sales",
    "Health & Wellness",
    "Engineering & Development",
]

# ── Keywords updated to match new category names exactly ─────────────────────
CATEGORY_KEYWORDS = {
    "AI Agents": [
        "agent",
        "autonomous",
        "multi-agent",
        "agentic",
        "copilot",
        "assistant",
        "chatbot",
        "ai tool",
        "ai-powered",
        "ai platform",
        "ai api",
        "ai generat",
        "ai write",
        "ai cod",
        "ai assistant",
        "openai",
        "anthropic",
        "claude",
        "gemini",
        "midjourney",
        "stable diffusion",
        "dall-e",
        "image generation",
        "text generation",
        "speech recognition",
        "tts",
        "text to speech",
        "diffusion model",
        "multimodal",
        "prompt engineer",
    ],
    "LLMs": [
        "llm",
        "large language model",
        "gpt",
        "mistral",
        "ollama",
        "hugging face",
        "fine-tun",
        "rag ",
        "retrieval augmented",
        "vector embed",
        "semantic search",
        "inference",
        "ai model",
        "machine learning",
        "neural network",
        "transformer",
        "foundation model",
        "language model",
    ],
    "Developer Tools": [
        "dev tool",
        "cli tool",
        "command line",
        "terminal emulat",
        "shell",
        "debugg",
        "profil",
        "ide ",
        "code editor",
        "vscode extension",
        "linter",
        "formatter",
        "static analys",
        "code review",
        "api test",
        "api mock",
        "api document",
        "openapi",
        "swagger",
        "database tool",
        "sql client",
        "migration",
        "orm ",
        "monit",
        "observ",
        "logging",
        "tracing",
        "alerting",
        "code snippet",
        "package manag",
        "dependency",
        "build tool",
        "bundler",
        "web scraper",
        "headless browser",
        "testing framework",
        "e2e test",
        "unit test",
        "open source",
        "self-host",
        "selfhost",
    ],
    "Design & Creative": [
        "design",
        "ui/ux",
        "ux research",
        "figma",
        "sketch app",
        "framer",
        "wireframe",
        "mockup",
        "prototype",
        "design system",
        "component library",
        "icon",
        "illustration",
        "vector",
        "svg ",
        "color palette",
        "typography",
        "font pair",
        "logo",
        "brand",
        "visual identity",
        "motion design",
        "animation tool",
        "3d design",
        "generative art",
        "creative tool",
        "canva",
        "photoshop alternative",
        "image edit",
        "background remov",
        "screenshot beautif",
        "design token",
    ],
    "Productivity": [
        "productivity",
        "note-tak",
        "note taking",
        "knowledge base",
        "second brain",
        "task manag",
        "to-do",
        "project manag",
        "kanban",
        "roadmap",
        "time track",
        "time block",
        "calendar",
        "scheduling",
        "meeting",
        "async",
        "workflow automat",
        "email manag",
        "inbox",
        "writing tool",
        "document editor",
        "wiki",
        "team collab",
        "remote work",
        "focus",
        "pomodoro",
        "distraction",
        "bookmark",
        "notion",
        "todo",
        "reminder",
        "habit",
        "schedule",
        "slack",
    ],
    "Marketing & Sales": [
        "marketing",
        "sales",
        "lead",
        "crm",
        "seo",
        "email campaign",
        "growth hacking",
        "social media",
        "linkedin",
        "outreach",
        "ad campaign",
        "conversion",
        "funnel",
        "analytics",
        "traffic",
        "content marketing",
        "copywriting",
        "newsletter",
        "affiliate",
        "influencer",
        "brand awareness",
        "customer acqui",
        "ab test",
        "landing page",
        "drip campaign",
        "retarget",
    ],
    "Health & Wellness": [
        "health",
        "fitness",
        "workout",
        "exercise",
        "gym",
        "nutrition",
        "diet",
        "calorie",
        "sleep track",
        "circadian",
        "meditat",
        "mindful",
        "mental health",
        "therapy",
        "anxiety",
        "stress",
        "mood track",
        "biohack",
        "longevit",
        "supplement",
        "habit track",
        "wellness",
        "running",
        "cycling",
        "strength train",
        "recovery",
        "hrv",
        "wearable",
        "blood glucose",
        "heart rate",
        "breath",
        "fasting",
    ],
    "Engineering & Development": [
        "engineering",
        "developer",
        "coding",
        "code",
        "github",
        "react",
        "typescript",
        "python",
        "api ",
        "framework",
        "sdk",
        "database",
        "backend",
        "frontend",
        "fullstack",
        "devops",
        "docker",
        "kubernetes",
        "k8s",
        "container",
        "orchestrat",
        "infrastructure",
        "iac",
        "terraform",
        "ansible",
        "ci/cd",
        "continuous integr",
        "continuous deploy",
        "pipeline",
        "git ",
        "gitlab",
        "version control",
        "library",
        "open source",
    ],
}


def detect_category(text: str) -> str:
    """Score each category, return highest match. Defaults to Developer Tools."""
    t = text.lower()
    best_cat = "Developer Tools"
    best_score = 0
    for cat, kws in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in t)
        if score > best_score:
            best_score = score
            best_cat = cat
    return best_cat


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _load_cache() -> dict:
    try:
        with open(TOOLS_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_cache(data: dict):
    try:
        with open(TOOLS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Cache save error: {e}")


# ── FALLBACK TOOLS — all categories updated to new names, 6 per category ─────
FALLBACK_TOOLS = [
    # AI Agents
    {
        "id": "fb-ai-1",
        "name": "Perplexity AI",
        "tagline": "AI-powered answer engine",
        "description": "Ask anything and get cited, real-time answers. Think Google but it actually explains things.",
        "url": "https://perplexity.ai",
        "image": "",
        "favicon": "",
        "category": "AI Agents",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#AIAgents", "#Search", "#Free"],
    },
    {
        "id": "fb-ai-2",
        "name": "Krea AI",
        "tagline": "Real-time AI image canvas",
        "description": "Draw rough shapes, watch AI render it live as you edit. Free daily credits, zero friction.",
        "url": "https://krea.ai",
        "image": "",
        "favicon": "",
        "category": "AI Agents",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#AIAgents", "#Image", "#Free"],
    },
    {
        "id": "fb-ai-3",
        "name": "Poe",
        "tagline": "Chat with multiple AI models",
        "description": "Access Claude, GPT-4, Gemini and dozens of other models in one place. Great for comparing outputs.",
        "url": "https://poe.com",
        "image": "",
        "favicon": "",
        "category": "AI Agents",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#AIAgents", "#LLM", "#Free"],
    },
    {
        "id": "fb-ai-4",
        "name": "Ideogram",
        "tagline": "AI images that can actually spell",
        "description": "One of the only image generators that renders readable text inside images. Great for thumbnails.",
        "url": "https://ideogram.ai",
        "image": "",
        "favicon": "",
        "category": "AI Agents",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#AIAgents", "#Image", "#Free"],
    },
    {
        "id": "fb-ai-5",
        "name": "Udio",
        "tagline": "AI music generation",
        "description": "Type a genre and mood, get a full song with vocals in seconds. Free tier gives 10 songs/day.",
        "url": "https://udio.com",
        "image": "",
        "favicon": "",
        "category": "AI Agents",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#AIAgents", "#Music", "#Free"],
    },
    {
        "id": "fb-ai-6",
        "name": "Phind",
        "tagline": "AI search for developers",
        "description": "Developer-focused AI search that understands code. Answers technical questions with code examples.",
        "url": "https://phind.com",
        "image": "",
        "favicon": "",
        "category": "AI Agents",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#AIAgents", "#Dev", "#Free"],
    },
    # LLMs
    {
        "id": "fb-llm-1",
        "name": "OpenRouter",
        "tagline": "One API for every frontier model",
        "description": "Single unified API key to access Claude, GPT-4, Mistral, Llama 3, Gemini and 50+ models. Pay per token.",
        "url": "https://openrouter.ai",
        "image": "",
        "favicon": "",
        "category": "LLMs",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#LLMs", "#API", "#Free"],
    },
    {
        "id": "fb-llm-2",
        "name": "LM Studio",
        "tagline": "Run LLMs locally on your laptop",
        "description": "Download and run Llama 3, Mistral, Phi-3 and hundreds of models entirely on your machine. No cloud.",
        "url": "https://lmstudio.ai",
        "image": "",
        "favicon": "",
        "category": "LLMs",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#LLMs", "#Local", "#Free"],
    },
    {
        "id": "fb-llm-3",
        "name": "Msty",
        "tagline": "Local AI chat with split-screen comparison",
        "description": "Chat with local or cloud models side by side. Compare Claude vs GPT-4 vs Llama in the same window.",
        "url": "https://msty.app",
        "image": "",
        "favicon": "",
        "category": "LLMs",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#LLMs", "#Local", "#Free"],
    },
    {
        "id": "fb-llm-4",
        "name": "Langfuse",
        "tagline": "Open-source LLM observability",
        "description": "Trace, debug, and evaluate every LLM call in your app. Track costs, latency, and quality.",
        "url": "https://langfuse.com",
        "image": "",
        "favicon": "",
        "category": "LLMs",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#LLMs", "#DevTool", "#OpenSource"],
    },
    {
        "id": "fb-llm-5",
        "name": "Fabric",
        "tagline": "AI patterns for your terminal",
        "description": "Open-source CLI that applies pre-built AI prompts to any input. Summarize PDFs, extract insights from YouTube.",
        "url": "https://github.com/danielmiessler/fabric",
        "image": "",
        "favicon": "",
        "category": "LLMs",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#LLMs", "#CLI", "#OpenSource"],
    },
    {
        "id": "fb-llm-6",
        "name": "Jan",
        "tagline": "Open-source ChatGPT alternative",
        "description": "Runs 100% offline on your computer. Supports all major open-source models. No tracking, no subscriptions.",
        "url": "https://jan.ai",
        "image": "",
        "favicon": "",
        "category": "LLMs",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#LLMs", "#OpenSource", "#Free"],
    },
    # Developer Tools
    {
        "id": "fb-dev-1",
        "name": "Bruno",
        "tagline": "Offline-first Postman alternative",
        "description": "API client that stores collections as plain text files in your repo. No cloud sync, no accounts.",
        "url": "https://www.usebruno.com",
        "image": "",
        "favicon": "",
        "category": "Developer Tools",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#DevTools", "#API", "#OpenSource"],
    },
    {
        "id": "fb-dev-2",
        "name": "Infisical",
        "tagline": "Open-source secrets manager",
        "description": "Sync .env files and secrets across your team and CI/CD. End-to-end encrypted. Self-hostable.",
        "url": "https://infisical.com",
        "image": "",
        "favicon": "",
        "category": "Developer Tools",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#DevTools", "#Security", "#OpenSource"],
    },
    {
        "id": "fb-dev-3",
        "name": "Mermaid Live",
        "tagline": "Diagrams as code in your browser",
        "description": "Write flowcharts, ERDs, sequence diagrams in plain text markdown. Renders live. Embed anywhere.",
        "url": "https://mermaid.live",
        "image": "",
        "favicon": "",
        "category": "Developer Tools",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#DevTools", "#Diagrams", "#Free"],
    },
    {
        "id": "fb-dev-4",
        "name": "Webhook.site",
        "tagline": "Inspect and debug webhooks instantly",
        "description": "Get a unique URL, send any HTTP request to it, inspect the payload in real time. No sign-up needed.",
        "url": "https://webhook.site",
        "image": "",
        "favicon": "",
        "category": "Developer Tools",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#DevTools", "#Webhooks", "#Free"],
    },
    {
        "id": "fb-dev-5",
        "name": "Hoppscotch",
        "tagline": "Open-source Postman alternative",
        "description": "Lightweight API testing tool that runs in the browser. Faster and less bloated than Postman.",
        "url": "https://hoppscotch.io",
        "image": "",
        "favicon": "",
        "category": "Developer Tools",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#DevTools", "#API", "#Free"],
    },
    {
        "id": "fb-dev-6",
        "name": "Pieces",
        "tagline": "AI code snippet manager",
        "description": "Saves code snippets from anywhere, auto-tags them with context, and resurfaces them when needed.",
        "url": "https://pieces.app",
        "image": "",
        "favicon": "",
        "category": "Developer Tools",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#DevTools", "#AI", "#Snippets"],
    },
    # Design & Creative
    {
        "id": "fb-des-1",
        "name": "Penpot",
        "tagline": "Open-source Figma alternative",
        "description": "Design and prototype tool that stores files as SVG. Self-hostable, free forever, works in the browser.",
        "url": "https://penpot.app",
        "image": "",
        "favicon": "",
        "category": "Design & Creative",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Design", "#OpenSource", "#Free"],
    },
    {
        "id": "fb-des-2",
        "name": "Spline",
        "tagline": "3D design for the web",
        "description": "Create interactive 3D scenes that run in the browser. Export as embeddable iframes or React components.",
        "url": "https://spline.design",
        "image": "",
        "favicon": "",
        "category": "Design & Creative",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Design", "#3D", "#Web"],
    },
    {
        "id": "fb-des-3",
        "name": "Realtime Colors",
        "tagline": "Preview color palettes on a real UI",
        "description": "Visualize font and color combinations on an actual website layout. Exports to CSS, Tailwind, and Figma.",
        "url": "https://realtimecolors.com",
        "image": "",
        "favicon": "",
        "category": "Design & Creative",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Design", "#Color", "#Free"],
    },
    {
        "id": "fb-des-4",
        "name": "UI Verse",
        "tagline": "Open-source CSS component library",
        "description": "5000+ beautifully crafted CSS and Tailwind components made by the community. Copy-paste, no framework needed.",
        "url": "https://uiverse.io",
        "image": "",
        "favicon": "",
        "category": "Design & Creative",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Design", "#CSS", "#OpenSource"],
    },
    {
        "id": "fb-des-5",
        "name": "Rive",
        "tagline": "Interactive animations that run anywhere",
        "description": "Design animations with a state machine that reacts to user input. Export as tiny file for web or mobile.",
        "url": "https://rive.app",
        "image": "",
        "favicon": "",
        "category": "Design & Creative",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Design", "#Animation", "#Free"],
    },
    {
        "id": "fb-des-6",
        "name": "Haikei",
        "tagline": "Organic SVG blob and wave generator",
        "description": "Generate layered blobs, waves, and stack SVG dividers with color control. Download or copy CSS.",
        "url": "https://haikei.app",
        "image": "",
        "favicon": "",
        "category": "Design & Creative",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Design", "#SVG", "#Free"],
    },
    # Productivity
    {
        "id": "fb-prod-1",
        "name": "Obsidian",
        "tagline": "Offline knowledge base with linked notes",
        "description": "Local-first notes app with bidirectional links. Free forever, no subscription, data stays on device.",
        "url": "https://obsidian.md",
        "image": "",
        "favicon": "",
        "category": "Productivity",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Productivity", "#Notes", "#Free"],
    },
    {
        "id": "fb-prod-2",
        "name": "Raycast",
        "tagline": "Spotlight replacement that does everything",
        "description": "App launcher with built-in AI, clipboard history, window management, snippet expansion, and 1000+ extensions.",
        "url": "https://raycast.com",
        "image": "",
        "favicon": "",
        "category": "Productivity",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Productivity", "#Mac", "#AI"],
    },
    {
        "id": "fb-prod-3",
        "name": "Tally",
        "tagline": "Beautiful forms, free forever",
        "description": "Form builder that doesn't look like Google Forms. Logic jumps, payments, file uploads — all free.",
        "url": "https://tally.so",
        "image": "",
        "favicon": "",
        "category": "Productivity",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Productivity", "#Forms", "#Free"],
    },
    {
        "id": "fb-prod-4",
        "name": "Anytype",
        "tagline": "Local-first Notion alternative",
        "description": "End-to-end encrypted, local-first workspace with pages, databases, and graphs. Data stays on device.",
        "url": "https://anytype.io",
        "image": "",
        "favicon": "",
        "category": "Productivity",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Productivity", "#LocalFirst", "#Free"],
    },
    {
        "id": "fb-prod-5",
        "name": "Reclaim.ai",
        "tagline": "AI that defends your calendar",
        "description": "Automatically blocks time for tasks, habits, and breaks around your meetings. Reschedules itself.",
        "url": "https://reclaim.ai",
        "image": "",
        "favicon": "",
        "category": "Productivity",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Productivity", "#Calendar", "#AI"],
    },
    {
        "id": "fb-prod-6",
        "name": "Loom",
        "tagline": "Async video for teams",
        "description": "Record screen + camera, share in one link. Replaces long Slack threads for explaining things.",
        "url": "https://loom.com",
        "image": "",
        "favicon": "",
        "category": "Productivity",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Productivity", "#Video", "#Teams"],
    },
    # Marketing & Sales
    {
        "id": "fb-mkt-1",
        "name": "Exploding Topics",
        "tagline": "Trends before they explode",
        "description": "Finds fast-growing topics before they go mainstream. Great for startup ideas and marketing research.",
        "url": "https://explodingtopics.com",
        "image": "",
        "favicon": "",
        "category": "Marketing & Sales",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Marketing", "#Trends", "#Research"],
    },
    {
        "id": "fb-mkt-2",
        "name": "Beehiiv",
        "tagline": "Newsletter platform built for growth",
        "description": "Launch, grow, and monetize your newsletter. Built-in referral program, ad network, and analytics.",
        "url": "https://beehiiv.com",
        "image": "",
        "favicon": "",
        "category": "Marketing & Sales",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Marketing", "#Newsletter", "#Free"],
    },
    {
        "id": "fb-mkt-3",
        "name": "Taplio",
        "tagline": "AI-powered LinkedIn growth tool",
        "description": "Schedule posts, get AI content ideas, track analytics, and build your LinkedIn audience on autopilot.",
        "url": "https://taplio.com",
        "image": "",
        "favicon": "",
        "category": "Marketing & Sales",
        "is_free": False,
        "votes": 0,
        "source": "curated",
        "tags": ["#Marketing", "#LinkedIn", "#AI"],
    },
    {
        "id": "fb-mkt-4",
        "name": "Typefully",
        "tagline": "Write and schedule Twitter threads",
        "description": "Distraction-free Twitter/X thread composer with scheduling, analytics, and AI writing assistance.",
        "url": "https://typefully.com",
        "image": "",
        "favicon": "",
        "category": "Marketing & Sales",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Marketing", "#Twitter", "#Free"],
    },
    {
        "id": "fb-mkt-5",
        "name": "Lemlist",
        "tagline": "Cold email that actually gets replies",
        "description": "Personalized cold outreach with images, videos, and LinkedIn steps built into the sequence.",
        "url": "https://lemlist.com",
        "image": "",
        "favicon": "",
        "category": "Marketing & Sales",
        "is_free": False,
        "votes": 0,
        "source": "curated",
        "tags": ["#Marketing", "#Email", "#Sales"],
    },
    {
        "id": "fb-mkt-6",
        "name": "Hunter.io",
        "tagline": "Find anyone's professional email",
        "description": "Find and verify professional email addresses. 25 free searches per month. Used by 4M+ people.",
        "url": "https://hunter.io",
        "image": "",
        "favicon": "",
        "category": "Marketing & Sales",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Marketing", "#Email", "#Free"],
    },
    # Health & Wellness
    {
        "id": "fb-health-1",
        "name": "Cronometer",
        "tagline": "Precise nutrition tracking",
        "description": "Track micronutrients, not just calories. Obsessively accurate food database loved by biohackers.",
        "url": "https://cronometer.com",
        "image": "",
        "favicon": "",
        "category": "Health & Wellness",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Health", "#Nutrition", "#Free"],
    },
    {
        "id": "fb-health-2",
        "name": "Huberman Lab",
        "tagline": "Science-backed health protocols",
        "description": "Free protocols from Stanford neuroscientist Andrew Huberman on sleep, focus, fitness, and stress.",
        "url": "https://hubermanlab.com",
        "image": "",
        "favicon": "",
        "category": "Health & Wellness",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Health", "#Science", "#Free"],
    },
    {
        "id": "fb-health-3",
        "name": "Bearable",
        "tagline": "Track everything that affects your health",
        "description": "Log symptoms, mood, energy, sleep, meds, and habits. Automatically finds correlations.",
        "url": "https://bearable.app",
        "image": "",
        "favicon": "",
        "category": "Health & Wellness",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Health", "#Tracking", "#Symptoms"],
    },
    {
        "id": "fb-health-4",
        "name": "Welltory",
        "tagline": "HRV-based stress and energy scanner",
        "description": "Measure your HRV using just your phone camera, get a stress and energy score. Free tier is solid.",
        "url": "https://welltory.com",
        "image": "",
        "favicon": "",
        "category": "Health & Wellness",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Health", "#HRV", "#Biohacking"],
    },
    {
        "id": "fb-health-5",
        "name": "Examine.com",
        "tagline": "Unbiased supplement research database",
        "description": "Massive database of human research on supplements and nutrition. No sponsored content, no brand deals.",
        "url": "https://examine.com",
        "image": "",
        "favicon": "",
        "category": "Health & Wellness",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Health", "#Supplements", "#Research"],
    },
    {
        "id": "fb-health-6",
        "name": "Zero",
        "tagline": "Intermittent fasting tracker",
        "description": "Track fasting windows, log meals, and access science-backed content on fasting. Clean and simple.",
        "url": "https://zerofasting.com",
        "image": "",
        "favicon": "",
        "category": "Health & Wellness",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Health", "#Fasting", "#Free"],
    },
    # Engineering & Development
    {
        "id": "fb-eng-1",
        "name": "Warp",
        "tagline": "The terminal for the 21st century",
        "description": "AI-powered terminal with autocomplete, natural language commands, and team workflows built in.",
        "url": "https://warp.dev",
        "image": "",
        "favicon": "",
        "category": "Engineering & Development",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Engineering", "#Terminal", "#AI"],
    },
    {
        "id": "fb-eng-2",
        "name": "Codeium",
        "tagline": "Free GitHub Copilot alternative",
        "description": "AI autocomplete that works in 70+ editors. Same quality as Copilot, completely free forever.",
        "url": "https://codeium.com",
        "image": "",
        "favicon": "",
        "category": "Engineering & Development",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Engineering", "#AI", "#Free"],
    },
    {
        "id": "fb-eng-3",
        "name": "Ray.so",
        "tagline": "Beautiful code screenshots",
        "description": "Paste code, pick a theme, get a stunning screenshot for Twitter or your portfolio. Made by Raycast.",
        "url": "https://ray.so",
        "image": "",
        "favicon": "",
        "category": "Engineering & Development",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Engineering", "#Design", "#Free"],
    },
    {
        "id": "fb-eng-4",
        "name": "Excalidraw",
        "tagline": "Hand-drawn style whiteboard",
        "description": "Open-source infinite canvas for architecture diagrams, wireframes, and quick sketches. No login.",
        "url": "https://excalidraw.com",
        "image": "",
        "favicon": "",
        "category": "Engineering & Development",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Engineering", "#Diagram", "#OpenSource"],
    },
    {
        "id": "fb-eng-5",
        "name": "Devbox",
        "tagline": "Instant, isolated dev environments",
        "description": "Create reproducible, isolated dev environments with a single JSON file. No Docker needed.",
        "url": "https://www.jetify.com/devbox",
        "image": "",
        "favicon": "",
        "category": "Engineering & Development",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Engineering", "#DevEnv", "#OpenSource"],
    },
    {
        "id": "fb-eng-6",
        "name": "roadmap.sh",
        "tagline": "Developer roadmaps for every path",
        "description": "Community-built roadmaps for frontend, backend, DevOps, AI, and more. Free, open-source, updated.",
        "url": "https://roadmap.sh",
        "image": "",
        "favicon": "",
        "category": "Engineering & Development",
        "is_free": True,
        "votes": 0,
        "source": "curated",
        "tags": ["#Engineering", "#Dev", "#Free"],
    },
]

# ── PH topic → new category name ─────────────────────────────────────────────
PH_TOPIC_MAP = {
    "AI Agents": "AI Agents",
    "Artificial Intelligence": "AI Agents",
    "AI Assistant": "AI Agents",
    "ChatGPT": "AI Agents",
    "LLMs": "LLMs",
    "Large Language Models": "LLMs",
    "Developer Tools": "Developer Tools",
    "API": "Developer Tools",
    "Open Source": "Developer Tools",
    "Design Tools": "Design & Creative",
    "Design & Creative": "Design & Creative",
    "UI/UX": "Design & Creative",
    "Productivity": "Productivity",
    "Task Management": "Productivity",
    "Marketing": "Marketing & Sales",
    "Marketing & Sales": "Marketing & Sales",
    "Sales": "Marketing & Sales",
    "Social Media": "Marketing & Sales",
    "Health & Fitness": "Health & Wellness",
    "Health": "Health & Wellness",
    "Mental Health": "Health & Wellness",
    "Engineering & Development": "Engineering & Development",
    "Web Development": "Engineering & Development",
    "Software Engineering": "Engineering & Development",
    "DevOps": "Engineering & Development",
}


def fetch_hacker_news(per_category=6):
    try:
        res = requests.get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "query": "",
                "tags": "show_hn",
                # "numericFilters": f"created_at_i>{int(datetime.now(timezone.utc).timestamp()) - 14*86400},points>2",
                "hitsPerPage": 200,
            },
            timeout=15,
        )
        hits = res.json().get("hits", [])
        print(f"📡 HN raw hits: {len(hits)}")
    except Exception as e:
        print(f"❌ HN fetch error: {e}")
        return []

    TOOL_SIGNALS = {
        "tool",
        "app",
        "platform",
        "ai",
        "generator",
        "builder",
        "editor",
        "api",
        "library",
        "extension",
        "bot",
        "dashboard",
        "cli",
        "tracker",
        "monitor",
        "search",
        "automat",
        "scraper",
        "analytic",
        "service",
        "plugin",
        "agent",
        "assistant",
        "checker",
        "viewer",
        "manager",
        "runner",
        "deploy",
        "host",
        "server",
        "client",
        "convert",
        "parser",
        "detect",
        "scan",
        "audit",
        "sync",
        "backup",
        "export",
        "import",
        "integrat",
        "workflow",
        "pipeline",
        "template",
        "site",
    }

    by_cat = {c: [] for c in CATEGORIES}
    seen_dom = set()

    for hit in sorted(hits, key=lambda h: h.get("points", 0), reverse=True):
        url = hit.get("url", "").strip()
        title = hit.get("title", "").strip()
        if not url or not title:
            continue

        clean = re.sub(r"^Show HN\s*:?\s*", "", title, flags=re.IGNORECASE).strip()
        if not any(sig in clean.lower() for sig in TOOL_SIGNALS):
            continue

        try:
            domain = requests.utils.urlparse(url).netloc.replace("www.", "").strip()
        except:
            continue
        if not domain or domain in seen_dom:
            continue
        seen_dom.add(domain)

        parts = re.split(r"\s+[-–—]\s+", clean, maxsplit=1)
        name = parts[0][:70].strip()
        tagline = (parts[1] if len(parts) > 1 else clean)[:200].strip()
        cat = detect_category(f"{name} {tagline}")

        # Guarantee cat is a valid key
        if cat not in by_cat:
            cat = "Developer Tools"

        if len(by_cat[cat]) >= per_category:
            continue

        by_cat[cat].append(
            {
                "id": f"hn-{hit['objectID']}",
                "name": name,
                "tagline": tagline,
                "description": tagline,
                "url": url,
                "image": f"https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://{domain}&size=64",
                "favicon": f"https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://{domain}&size=64",
                "category": cat,
                "is_free": True,
                "votes": hit.get("points", 0),
                "source": "hackernews",
                "tags": [
                    f"#{cat.replace(' & ','').replace(' ','')}",
                    "#ShowHN",
                    "#Free",
                ],
            }
        )

    result = [t for tools_list in by_cat.values() for t in tools_list]
    print(f"✅ HN: {len(result)} tools fetched")
    return result


def fetch_product_hunt(per_category=6):
    if not PH_TOKEN:
        print("⚠️  No PRODUCT_HUNT_TOKEN — skipping PH")
        return []

    from datetime import timedelta

    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime(
        "%Y-%m-%dT00:00:00Z"
    )

    query = """
query {
  posts(order: VOTES, postedAfter: "%s", first: 40) {
    edges { node {
      id
      name
      tagline
      slug
      votesCount
      website
      thumbnail { url }
      topics { edges { node { name } } }
    }}
  }
}
""" % week_ago

    # query = """
    # query {
    #   posts(order: VOTES, postedAfter: "%s", first: 40) {
    #     edges { node {
    #       id name tagline slug votesCount
    #       thumbnail { url }
    #       topics { edges { node { name } } }
    #     }}
    #   }
    # }
    # """ % week_ago

    try:
        res = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": query},
            headers={
                "Authorization": f"Bearer {PH_TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        payload = res.json()
        if "errors" in payload:
            print(f"❌ PH GraphQL errors: {payload['errors']}")
            return []
        edges = payload.get("data", {}).get("posts", {}).get("edges", [])
        print(f"📡 PH raw edges: {len(edges)}")
    except Exception as e:
        print(f"❌ PH fetch error: {e}")
        return []

    by_cat = {c: [] for c in CATEGORIES}
    seen_slugs = set()

    for edge in sorted(
        edges, key=lambda e: e["node"].get("votesCount", 0), reverse=True
    ):
        n = edge.get("node", {})
        name = (n.get("name") or "").strip()
        tag = (n.get("tagline") or "").strip()
        slug = (n.get("slug") or "").strip()

        if not name or not tag or not slug or slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        # Try PH topic names first, fall back to keyword detection
        topic_names = [t["node"]["name"] for t in n.get("topics", {}).get("edges", [])]
        cat = None
        for topic in topic_names:
            if topic in PH_TOPIC_MAP:
                cat = PH_TOPIC_MAP[topic]
                break
        if not cat:
            cat = detect_category(f"{name} {tag}")

        # Guarantee cat is a valid key
        if cat not in by_cat:
            cat = "Developer Tools"

        if len(by_cat[cat]) >= per_category:
            continue

        thumb = (n.get("thumbnail") or {}).get("url", "")
        # card_url = f"https://www.producthunt.com/posts/{slug}"
        card_url = n.get("website") or f"https://www.producthunt.com/posts/{slug}"

        by_cat[cat].append(
            {
                "id": f"ph-{n['id']}",
                "name": name,
                "tagline": tag,
                "description": tag[:220],
                "url": card_url,
                "image": thumb,
                "favicon": "",
                "category": cat,
                "is_free": True,
                "votes": n.get("votesCount", 0),
                "source": "producthunt",
                "tags": [f"#{cat.replace(' & ','').replace(' ','')}", "#ProductHunt"],
            }
        )

    result = [t for tools_list in by_cat.values() for t in tools_list]
    print(f"✅ PH: {len(result)} tools fetched")
    return result


def build_final_list(ph, hn):
    TARGET_PER_CAT = 6
    by_cat = {c: [] for c in CATEGORIES}
    seen = set()

    for t in ph + hn:
        uid = t.get("id", "")
        if uid in seen:
            continue
        seen.add(uid)
        cat = t.get("category", "Developer Tools")
        # Safety: remap any stale old category names
        if cat not in by_cat:
            cat = "Developer Tools"
        if len(by_cat[cat]) < TARGET_PER_CAT:
            by_cat[cat].append(t)

    fb_by_cat = {}
    for t in FALLBACK_TOOLS:
        fb_by_cat.setdefault(t["category"], []).append(t)

    for cat in CATEGORIES:
        needed = TARGET_PER_CAT - len(by_cat[cat])
        if needed > 0:
            pad = [t for t in fb_by_cat.get(cat, []) if t["id"] not in seen][:needed]
            for t in pad:
                seen.add(t["id"])
            by_cat[cat].extend(pad)
            live = TARGET_PER_CAT - needed
            print(f"  ↳ {cat}: {live} live + {len(pad)} fallback")

    result = [t for cat in CATEGORIES for t in by_cat[cat]]
    print(f"✅ Final tool list: {len(result)} tools")
    return result


@tools_bp.route("/tools")
def tools():
    user_name, user_level, user_domain = get_user_data()
    return render_template(
        "tools.html",
        user_name=user_name,
        user_level=user_level,
        user_domain=user_domain,
    )


@tools_bp.route("/get-tools", methods=["GET"])
def get_tools():
    cache = _load_cache()
    today = _today()

    if cache.get("date") == today and len(cache.get("tools", [])) >= 40:
        print("⚡ Tools: serving from cache")
        return jsonify({"tools": cache["tools"], "date": today, "source": "cache"})

    print("🔄 Fetching fresh tools...")
    ph = fetch_product_hunt(per_category=6)
    hn = fetch_hacker_news(per_category=6)
    data = build_final_list(ph, hn)

    _save_cache({"date": today, "tools": data})
    return jsonify({"tools": data, "date": today, "source": "fresh"})

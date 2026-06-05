# Decrypt Final (React + Flask)

## Overview

Decrypt is an AI-powered educational news platform that simplifies technology news for students and beginners.

The project consists of:

* React + Vite frontend
* Flask backend
* Firebase Authentication
* Firestore Database
* Gemini AI Integration

---

# Project Structure

```text
Decrypt_Final/
│
├── backend/
│   ├── models/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── home_routes.py
│   │   ├── opportunities_routes.py
│   │   ├── saved_routes.py
│   │   └── tools_routes.py
│   │
│   ├── services/
│   │   ├── gemini_service.py
│   │   └── news_service.py
│   │
│   ├── utils/
│   │   ├── db.py
│   │   └── firebase_admin.py
│   │
│   ├── firebase_config/
│   │   └── serviceAccountKey.json (local only)
│   │
│   ├── static/
│   │   └── data/
│   │       └── fallback_news.json
│   │
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env (local only)
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   └── news-image/
│   │   │
│   │   ├── components/
│   │   │   ├── ArticleBot.jsx
│   │   │   ├── CommentSection.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── NewsCard.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   ├── RightSidebar.jsx
│   │   │   └── Sidebar.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── data/
│   │   │   └── fallback_news.json
│   │   │
│   │   ├── layouts/
│   │   │
│   │   ├── pages/
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── Onboarding1.jsx
│   │   │   ├── Onboarding2.jsx
│   │   │   ├── Onboarding3.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── DailyBrief.jsx
│   │   │   ├── Opportunities.jsx
│   │   │   ├── Saved.jsx
│   │   │   └── Tools.jsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   ├── newsService.js
│   │   │   ├── opportunityService.js
│   │   │   └── toolService.js
│   │   │
│   │   ├── styles/
│   │   │   ├── style.css
│   │   │   ├── home.css
│   │   │   ├── dailyBrief.css
│   │   │   ├── opportunities.css
│   │   │   ├── saved.css
│   │   │   ├── tools.css
│   │   │   ├── login.css
│   │   │   ├── signup.css
│   │   │   ├── landing.css
│   │   │   ├── onboarding1.css
│   │   │   ├── onboarding2.css
│   │   │   └── onboarding3.css
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .env (local only)
│
├── README.md
└── .gitignore
```

---

# Frontend Setup

## 1. Navigate to frontend

```bash
cd frontend
```

## 2. Install dependencies

```bash
npm install
```

## 3. Start development server

```bash
npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

# Backend Setup

## 1. Navigate to backend

```bash
cd backend
```

## 2. Create virtual environment

```bash
python -m venv venv
```

## 3. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Create .env file

Example:

```env
GEMINI_API_KEY=YOUR_GEMINI_KEY
```

## 6. Add Firebase Service Account Key

Place:

```text
serviceAccountKey.json
```

inside:

```text
backend/firebase_config/
```

## 7. Run backend

```bash
python app.py
```

Backend will run on:

```text
http://127.0.0.1:5000
```

---

# Git Workflow

## Clone Repository

```bash
git clone <repo-url>
```

## Enter Project

```bash
cd Decrypt_Final
```

## Pull Latest Changes

```bash
git pull origin main
```

## Create New Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Push Branch

```bash
git push origin feature/your-feature-name
```

---

# Tech Stack

### Frontend

* React
* Vite
* React Router DOM
* CSS

### Backend

* Flask
* Firebase Authentication
* Firestore
* Gemini API
* GROQ API

### Database

* Firebase Firestore

---




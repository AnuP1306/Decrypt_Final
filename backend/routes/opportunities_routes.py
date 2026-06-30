from flask import Blueprint, render_template, jsonify, request
from routes.home_routes import get_user_data

from services.opportunity_service import (
    get_opportunities_by_type
)

import json
import os
import time

opportunities = Blueprint('opportunities', __name__)

# ── Flask HTML route (original — DO NOT TOUCH) ───────────────────────────────
@opportunities.route('/opportunities')
def opportunities_page():
    user_name, user_level, user_domain = get_user_data()
    opportunities_data = [
        {
            "title": "Google Software Courses",
            "company": "Google",
            "desc": "Work on cutting-edge AI and scalable systems.",
            "deadline": "April 30",
            "location": "Remote",
            "stipend": "",
            "type": "Courses",
            "tags": ["AI", "Backend"],
            "image": "/static/images/opportunitiescard.png",
            "link": "https://careers.google.com"
        },
        {
            "title": "GitHub Student Developer Pack",
            "company": "GitHub",
            "desc": "Get access to premium dev tools for free.",
            "deadline": "Ongoing",
            "location": "Global",
            "stipend": "",
            "type": "Student Perks",
            "tags": ["GitHub", "FreeTools", "StudentPerks"],
            "image": "/static/images/opportunitiescard2.png",
            "link": "https://education.github.com/pack"
        },
        {
            "title": "MLH Workshops",
            "company": "MLH",
            "desc": "Build real-world projects with global devs.",
            "deadline": "May 15",
            "location": "Remote",
            "stipend": "",
            "type": "Workshops",
            "tags": ["OpenSource", "Community"],
            "image": "/static/images/opportunitiescard3.png",
            "link": "https://fellowship.mlh.io/"
        },
        {
            "title": "Notion Student Plan",
            "company": "Notion",
            "desc": "Get Notion Plus plan free for students with unlimited blocks and uploads.",
            "deadline": "Ongoing",
            "location": "Global",
            "stipend": "",
            "type": "Student Perks",
            "tags": ["Productivity", "FreeTools"],
            "image": "/static/images/opportunitiescard5.png",
            "link": "https://www.notion.so/students"
        },
        {
            "title": "CS50x by Harvard",
            "company": "Harvard University",
            "desc": "Learn computer science fundamentals from scratch with hands-on projects.",
            "deadline": "Self-paced",
            "location": "Online",
            "stipend": "",
            "type": "Courses",
            "tags": ["Programming", "Beginner"],
            "image": "/static/images/opportunitiescard7.png",
            "link": "https://cs50.harvard.edu/x/"
        },
        {
            "title": "Web Development Bootcamp",
            "company": "freeCodeCamp",
            "desc": "Live workshop covering full-stack web development with real projects.",
            "deadline": "Rolling",
            "location": "Online",
            "stipend": "",
            "type": "Workshops",
            "tags": ["WebDev", "FullStack"],
            "image": "/static/images/opportunitiescard6.png",
            "link": "https://www.freecodecamp.org"
        },
        {
            "title": "Microsoft Explore Workshops",
            "company": "Microsoft",
            "desc": "Learn software engineering fundamentals.",
            "deadline": "June 10",
            "location": "Hybrid",
            "stipend": "",
            "type": "Workshops",
            "tags": ["Microsoft", "Workshops"],
            "image": "/static/images/opportunitiescard4.png",
            "link": "https://learn.microsoft.com"
        }
    ]

    return render_template(
        "opportunities.html",
        opportunities=opportunities_data,
        active_page="opportunities",
        user_name=user_name,
        user_level=user_level,
        user_domain=user_domain
    )


# ── React API endpoint (feature/opportunity-live-data) ───────────────────────
@opportunities.route("/get-opportunities", methods=["GET"])
def get_opportunities_api():
    """
    React frontend calls this.
    GET /get-opportunities
    GET /get-opportunities?type=Student Perks
    GET /get-opportunities?type=Courses
    GET /get-opportunities?type=Workshops
    """
    try:
        opp_type = request.args.get("type", "All")
        data = get_opportunities_by_type(opp_type)

        return jsonify({"opportunities": data, "count": len(data)}), 200

    except Exception as e:
        print("Error in /get-opportunities:", e)
        return jsonify({"opportunities": [], "count": 0, "error": str(e)}), 500

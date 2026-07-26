<div align="center">

# 🌐 Network Relationship Management System
### *AI-Powered Talent Matching & Skill Gap Analytics Platform*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Deployment](https://img.shields.io/badge/Render-Live_Demo-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

<p align="center">
  <b>Bridging the gap between talent, AI recommendations, and actionable learning roadmaps.</b>
  <br />
  <a href="#-key-features">Key Features</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-environment-variables">Environment Setup</a>
</p>

---

</div>

## 📌 Project Overview

The **Network Relationship Management System** is an intelligent web application designed to help teams and organizations map technical expertise, discover skill synergies, and generate actionable career roadmaps.

By leveraging **Cosine Similarity Algorithms** alongside **Google Gemini AI**, the platform dynamically pairs talent with relevant technical repositories, recommends curated YouTube learning resources, and conducts real-time skill gap evaluations.

---

## 🔥 Key Features

| Feature | Description |
| :--- | :--- |
| 🎯 **Smart Skill Matching** | Utilizes TF-IDF vectorization and cosine similarity to match candidates based on skill compatibility. |
| 🧠 **AI-Powered Skill Gap Analysis** | Integrates Google Gemini AI to analyze missing competencies and generate step-by-step career roadmaps. |
| 📺 **Curated Resource Engine** | Automatically fetches targeted YouTube video tutorials and channels based on searched skill stacks. |
| 🐙 **Repository Recommendations** | Matches developer profiles with relevant GitHub/open-source projects for practical collaboration. |
| 📊 **Analytics Dashboard** | Displays visual insights on talent distribution, skill demand, and ecosystem performance. |

---

## 📐 System Architecture

```text
 ┌────────────────┐       ┌──────────────────┐       ┌───────────────────┐
 │   User / Client│ ────> │  Flask Backend   │ ────> │  MySQL Database   │
 └────────────────┘       │    (app.py)      │       └───────────────────┘
                          └────────┬─────────┘
                                   │
         ┌─────────────────────────┼────────────────────────┐
         ▼                         ▼                        ▼
┌──────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│ Gemini AI Engine │     │ YouTube API v3   │     │ Vectorizer Engine │
│ (Roadmaps & Gap) │     │ (Learning Media) │     │ (Cosine Matching) │
└──────────────────┘     └──────────────────┘     └───────────────────┘

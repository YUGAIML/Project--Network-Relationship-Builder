# Project--Network-Relationship-Builder
<div align="center">

# 🌐 Neural Nexus
### 🚀 AI-Powered Network Relationship Management System

<img src="https://readme-typing-svg.demolab.com?font=Poppins&weight=700&size=30&duration=3500&pause=1000&color=00C2FF&center=true&vCenter=true&width=900&lines=Build+Meaningful+Professional+Connections;AI-Powered+Relationship+Management;GitHub+Developer+Recommendation+System;Flask+%7C+Python+%7C+Machine+Learning+%7C+MySQL" alt="Typing SVG" />

<p align="center">
<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>
<img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask"/>
<img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript"/>
<img src="https://img.shields.io/badge/Machine%20Learning-TFIDF-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge"/>
</p>

---

### ⭐ Connect • Analyze • Recommend • Grow

</div>

---

# 📌 Overview

**Neural Nexus** is an AI-powered **Network Relationship Management System** designed to help professionals build, manage, and strengthen valuable connections.

Unlike traditional contact management systems, Neural Nexus intelligently analyzes user profiles, professional skills, educational background, work experience, and interests to recommend the most relevant developers and professionals.

The platform integrates **Machine Learning**, **GitHub API**, and **Relationship Analytics** to provide personalized networking recommendations and improve collaboration opportunities.

---

# 🎯 Project Objectives

✔ Build professional networking platform

✔ Store complete professional profiles

✔ Analyze relationship strength

✔ Recommend similar developers

✔ Visualize professional networks

✔ Improve collaboration opportunities

✔ Enable AI-powered networking

---

# ✨ Features

## 👤 User Authentication

- Secure Registration
- Login System
- Session Management
- Logout Functionality

---

## 🧑 Professional Profile

Users can add:

- Personal Information
- Contact Details
- Education
- Skills
- Interests
- Work Experience
- Company Details
- Professional Status

---

## 🤝 Relationship Management

- Create Professional Connections
- Store Relationship Type
- Connection Strength
- Connection Since
- Remarks
- Professional Network Database

---

## 🧠 AI Recommendation System

The recommendation engine uses:

- TF-IDF Vectorization
- Cosine Similarity
- Profile Matching
- Skill Similarity
- GitHub Profile Analysis

Developers with similar skills and interests are automatically recommended.

---

## 🌍 GitHub Integration

The application fetches developer information from GitHub including:

- Username
- Followers
- Following
- Public Repositories
- Bio
- Skills
- Languages
- Location
- Avatar
- GitHub Profile URL

---

## 📊 Network Analysis

Generate insights like:

- Most Connected Professionals
- Popular Skills
- Similar Developers
- Strong Relationships
- Professional Network Growth

---

# 🏗 System Architecture

```
                User
                  │
                  ▼
        Authentication System
                  │
                  ▼
        Personal Information
                  │
                  ▼
         Education Details
                  │
                  ▼
          Skills & Interests
                  │
                  ▼
      Relationship Management
                  │
                  ▼
      Recommendation Engine
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   GitHub API         SQLite/MySQL
        │                   │
        └─────────┬─────────┘
                  ▼
          AI Recommendation
                  │
                  ▼
              Dashboard
```

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## Database

- MySQL
- SQLite

## Machine Learning

- Scikit-Learn
- TF-IDF
- Cosine Similarity
- Pandas
- NumPy

## APIs

- GitHub REST API

---

# 📂 Project Structure

```
Neural-Nexus/
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── developer.html
│   ├── result.html
│   ├── network_analysis.html
│   └── forms
│
├── app.py
├── database.py
├── similarity.py
├── recommend.py
├── fetch_github.py
├── developers.db
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/neural-nexus.git
```

```bash
cd neural-nexus
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a **.env**

```
GITHUB_TOKEN=your_token_here
```

---

## Run

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

# 🗄 Database Design

## Users

- User ID
- Full Name
- Email
- Password
- Created At

---

## Personal Information

- Contact
- Gender
- DOB
- Address
- City
- State
- Country
- Qualification
- Job Role
- Experience
- Company

---

## Education

- Degree
- Specialization
- College
- University
- CGPA
- Passing Year
- Education Type

---

## Relationships

- Connected User
- Relationship Type
- Relationship Strength
- Connection Since
- Remarks

---

# 🧠 Recommendation Algorithm

The recommendation engine follows these steps:

```
Developer Profiles
        │
        ▼
Feature Extraction
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Cosine Similarity
        │
        ▼
Rank Developers
        │
        ▼
Top Recommendations
```

---

# 📈 Future Enhancements

- AI Chatbot
- Real-Time Messaging
- Email Notifications
- Friend Requests
- Graph Visualization
- Resume Parsing
- LinkedIn Integration
- JWT Authentication
- Docker Deployment
- Cloud Hosting
- NLP-Based Recommendations

---

# 📸 Screenshots

```
🏠 Home Page

🔐 Login Page

📝 Registration

📊 Dashboard

👤 Profile

🤝 Network Analysis

🧠 AI Recommendations

📈 Results
```

(Add your screenshots here.)

---

# 🎯 Key Highlights

⭐ AI-Based Recommendation System

⭐ GitHub Integration

⭐ Professional Relationship Management

⭐ Machine Learning Powered

⭐ Flask Backend

⭐ Secure Authentication

⭐ Modern Responsive UI

⭐ Database Driven

⭐ Professional Dashboard

⭐ Network Analytics

---

# 👨‍💻 Developed By

## Yug

Engineering Student | AI & ML Enthusiast | Python Developer

Passionate about Artificial Intelligence, Machine Learning, Web Development, and Building Intelligent Systems that solve real-world networking and collaboration challenges.

---

<div align="center">

### 🌟 If you like this project, give it a Star ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00c6ff,100:0072ff&height=120&section=footer"/>

</div>

# 🐞 Issue Tracker  

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)  
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-orange)  
![React](https://img.shields.io/badge/React-Frontend-blueviolet)  
![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue)  

A simple yet powerful **full-stack Issue Tracker** application.  
It helps users **manage, track, and update issues** efficiently using a **FastAPI backend** and a **React + TypeScript frontend**.  

---

## ✨ Features  

### 🔧 Backend (FastAPI – Python)  
- RESTful API with **CRUD operations**  
- **Search, filter, sort** issues  
- Auto-generated: `id`, `createdAt`, `updatedAt`  
- Built with **Uvicorn ASGI server**  

### 🎨 Frontend (React + TypeScript)  
- Fully **responsive UI** (desktop & mobile)  
- **Light/Dark mode themes**  
- Forms to create & edit issues  
- Dynamic table with **search, filter, sort**  
- Modal view for detailed issue information  
- Delete functionality with confirmation  
- Professional header & footer with social links  

---

## 📂 Project Structure  

issueTracker/

├── Backend/

│ ├── main.py

│ ├── requirements.txt

│ └── venv/ # (ignored by Git)

└── frontend/

├── public/

│ └── index.html

├── src/

│ ├── App.tsx

│ ├── App.css

│ └── … other React/TS files

├── package.json

└── tsconfig.json



---

## ⚙️ Getting Started  

### 1️⃣ Backend Setup  

```bash
cd Backend

# Create virtual environment
python -m venv venv

# Activate venv
# macOS/Linux
source venv/bin/activate
# Windows
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload

```

#### **Backend available at**: http://localhost:8000

---


### 2️⃣ **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

#### **Frontend available at**: http://localhost:3000


### 🛠️ **Tech Stack**

**Backend:** FastAPI (Python)

**Frontend:** React, TypeScript

**Styling:** CSS (optionally extend with Tailwind)

**Runtime:** Node.js, Uvicorn



### 🚀 **Future Enhancements**

🔐 Authentication & Authorization

📄 Pagination for large datasets

📎 File attachments for issues (logs/screenshots)

🗄️ Persistent Database (SQLite / PostgreSQL)

☁️ Deployment on Vercel, AWS, or Heroku

### 📜 **License**

This project is licensed under the MIT License.
Feel free to use, modify, and share.

⭐ **If you like this project, give it a star on GitHub!**

---

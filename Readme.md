# 🧠 Jira Task Manager Backend (Django)

## 🚀 Overview

This project is a backend API for a Jira-like task management system built using Django and Django REST Framework. It supports user authentication, task management, task movement across statuses, and dashboard analytics.

---

## 🛠 Tech Stack

* Django
* Django REST Framework
* SQLite
* JWT Authentication (SimpleJWT)

---

## 🔐 Authentication

* JWT-based authentication is used
* Login returns access token
* All protected APIs require token

### Header Format:

Authorization: Bearer <your_token>

---

## 👤 User Features

* Register user
* Login user
* Get all users

---

## 📌 Task Features

* Create task
* Get all tasks
* Update task
* Delete task
* Filter tasks:

  * By status
  * By assigned user
  * By deadline

---

## 🔄 Jira-like Move Logic

* Move task between statuses
* Reorder task within same column
* Insert task at specific position

---

## 📊 Dashboard Analytics

* Total tasks
* Tasks per status
* Overdue tasks
* Tasks per user
* Completed tasks
* Completion percentage

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/adityazinj/jirataskmanager.git

# Create virtual environment
 virtualenv venv

# Activate virtual environment

 # Windows:
  venv\Scripts\activate
 
 # Mac/Linux:
  source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```

---

## 📌 API Endpoints

### 🔐 Auth

* POST /api/register/
* POST /login/

### 👤 Users

* GET /api/users/

### 📌 Tasks

* POST /api/tasks/create/
* GET /api/tasks/
* PUT /api/tasks/{id}/
* DELETE /api/tasks/{id}/delete/
* PUT /api/tasks/move/

### 📊 Dashboard

* GET /api/dashboard/

---

## 📤 Postman Collection

The Postman collection is included in this repository:

jirataskmanagement.postman_collection.json

Import it into Postman to test all APIs easily.

---

## 🗄️ Database Schema

### User Table

* id (Primary Key)
* username
* email
* password
* name

### Task Table

* id (Primary Key)
* title
* description
* assigned_to (ForeignKey → User)
* created_by (ForeignKey → User)
* deadline
* status (not_started, in_progress, completed)
* position
* created_at
* updated_at

---

## 🔗 Relationships

* One user can create many tasks
* One user can be assigned many tasks
* Each task belongs to one creator and one assignee

---

## 💡 Notes

* SQLite is used for simplicity
* APIs are tested using Postman

---

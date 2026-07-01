

# 🚀 Full Stack Blog Platform

> A modern Full Stack Blog Platform built with Django REST Framework and React, designed using production-ready architecture and modern software engineering practices.

<br>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen?style=for-the-badge\&logo=django)
![DRF](https://img.shields.io/badge/Django_REST_Framework-red?style=for-the-badge)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge\&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge\&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge\&logo=redis)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge\&logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge\&logo=nginx)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge\&logo=elasticsearch)
![Kibana](https://img.shields.io/badge/Kibana-005571?style=for-the-badge\&logo=kibana)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge\&logo=celery)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge\&logo=pytest)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge\&logo=github-actions)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</p>

---

## 📸 Preview

> **Screenshots will be added soon.**

```
Frontend (React)
        │
        ▼
 REST API (Django REST Framework)
        │
 ┌──────┼───────────────┐
 ▼      ▼               ▼
Redis PostgreSQL Elasticsearch
 │                      │
 ▼                      ▼
Celery               Kibana
 │
 ▼
Email Tasks
```

---

# 📖 Table of Contents

* 🚀 About The Project
* ✨ Features
* 🏗 Architecture
* 🛠 Tech Stack
* 📂 Project Structure
* ⚙ Installation
* 🐳 Docker
* 🔍 Search Engine
* ⚡ Background Tasks
* 📊 Logging
* 🧪 Testing
* 🔄 Continuous Integration
* 📡 API Overview
* 📈 Performance
* 🔐 Security
* 🗺 Roadmap
* 🤝 Contributing
* 📄 License
* 👨‍💻 Author

---

# 🚀 About The Project

This project is a **Full Stack Blog Platform** built using **Django REST Framework** for the backend and **React** for the frontend.

The main goal of this project is to simulate a production-ready application by following modern backend and frontend development practices, scalable architecture, containerized deployment, automated testing, centralized logging, asynchronous task processing, and efficient full-text search.

Unlike a basic CRUD application, this project focuses on real-world software engineering concepts such as Dockerized infrastructure, Redis caching, Celery background workers, Elasticsearch integration, continuous integration using GitHub Actions, and clean REST API design.

The frontend communicates exclusively with the REST API, making the application completely API-driven and suitable for future mobile applications or additional frontend clients.

---

# ⭐ Why this project?

This project was created to demonstrate the implementation of a scalable Full Stack application using modern technologies commonly adopted in production environments.

It combines multiple backend services into a single ecosystem while maintaining clean architecture and separation of concerns.

Key objectives include:

* Building a production-ready REST API
* Applying clean project architecture
* Integrating multiple infrastructure services
* Learning distributed application design
* Improving DevOps knowledge using Docker
* Practicing asynchronous programming
* Implementing efficient search using Elasticsearch
* Building a maintainable frontend using React

---

# 🌟 Highlights

* RESTful API Design
* API First Architecture
* Full Stack Development
* Dockerized Environment
* PostgreSQL Database
* Redis Cache
* Celery Workers
* Elasticsearch Search
* ELK Logging Stack
* JWT Authentication
* React Query Data Fetching
* React Hook Form Validation
* GitHub Actions CI
* Automated Testing
* Production Ready Architecture
---

# ✨ Features

The platform has been designed using a modular architecture and provides a complete blogging experience with modern backend technologies and a responsive frontend.

## 👤 Authentication

* JWT Authentication
* User Registration
* Secure Login & Logout
* Email Verification
* Password Reset
* User Profile Management
* Protected API Endpoints

---

## 📝 Blog Management

* Create Posts
* Update Posts
* Delete Posts
* Publish Articles
* Upload Images
* Categorize Posts
* Rich Content Support

---

## 💬 Community

* Comment System
* Nested API Structure
* User-based Permissions

---

## 🔍 Search

Powered by **Elasticsearch**

Features include:

* Full Text Search
* Fuzzy Search
* Multi Match Queries
* Fast Search Performance
* Search Ranking

---

## ⚡ Performance

* Redis Cache
* Optimized Database Queries
* Background Tasks with Celery
* Dockerized Services

---

## 🧪 Quality Assurance

* API Testing with Pytest
* Load Testing using Locust
* GitHub Actions Continuous Integration

---

## 📊 Monitoring & Logging

* Centralized Logging
* Logstash Pipelines
* Elasticsearch Log Storage
* Kibana Dashboards

---

# 🏗 Architecture

The project follows an API-first architecture where the frontend and backend are completely separated.

```text
                        Client Browser
                               │
                               ▼
                        React Application
                               │
                    Axios / React Query
                               │
                               ▼
                   Django REST Framework API
                               │
      ┌─────────────┬──────────┴──────────────┬──────────────┐
      ▼             ▼                         ▼              ▼
 PostgreSQL       Redis                 Elasticsearch      Celery
      │             │                         │              │
      │             │                         │              ▼
      │             │                    Full Text      Email Tasks
      │             │                      Search
      │             │
      └─────────────┴───────────────┐
                                    ▼
                              Logstash
                                    │
                                    ▼
                             Elasticsearch
                                    │
                                    ▼
                                 Kibana
```

### Request Flow

```text
React
   │
   ▼
REST API
   │
Authentication
   │
Business Logic
   │
Database / Cache / Search
   │
JSON Response
   │
React UI
```

The frontend communicates exclusively with the REST API, making the application suitable for future mobile clients or additional frontend frameworks.

---

# 🛠 Tech Stack

## Backend

| Technology            | Purpose                |
| --------------------- | ---------------------- |
| Python                | Programming Language   |
| Django                | Web Framework          |
| Django REST Framework | REST API Development   |
| JWT                   | Authentication         |
| Celery                | Background Tasks       |
| Redis                 | Cache & Message Broker |
| Elasticsearch         | Full Text Search       |

---

## Frontend

| Technology      | Purpose                 |
| --------------- | ----------------------- |
| React           | User Interface          |
| React Router    | Client-side Routing     |
| React Query     | Server State Management |
| React Hook Form | Form Handling           |
| Axios           | HTTP Client             |
| HTML5           | Markup                  |
| CSS3            | Styling                 |

---

## Database

| Technology | Purpose             |
| ---------- | ------------------- |
| PostgreSQL | Relational Database |

---

## DevOps

| Technology     | Purpose                    |
| -------------- | -------------------------- |
| Docker         | Containerization           |
| Docker Compose | Multi-container Management |
| Nginx          | Reverse Proxy              |
| GitHub Actions | Continuous Integration     |

---

## Observability

| Technology    | Purpose           |
| ------------- | ----------------- |
| Elasticsearch | Log Storage       |
| Logstash      | Log Processing    |
| Kibana        | Log Visualization |

---

## Testing

| Technology | Purpose         |
| ---------- | --------------- |
| Pytest     | Backend Testing |
| Locust     | Load Testing    |
---

# 📂 Project Structure

The project follows a modular architecture to improve maintainability, scalability, and separation of concerns.

```text
.
├── backend/
│   ├── accounts/
│   ├── posts/
│   ├── comments/
│   ├── search/
│   ├── core/
│   ├── tests/
│   ├── media/
│   ├── requirements.txt
│   ├── manage.py
│   └── RestApiBlog/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── routes/
│   │   ├── context/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
│
├── logstash/
│   └── pipeline/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── docker-compose-stage.yml
├── default.conf
└── README.md
```

---

# ⚙️ Getting Started

Follow these instructions to run the project locally.

## Prerequisites

Make sure the following software is installed on your machine:

* Git
* Docker
* Docker Compose
* Python 3.12+
* Node.js 22+
* npm

---

# 📥 Clone Repository

```bash
git clone https://github.com/your-username/RestApiBlog.git
```

```bash
cd RestApiBlog
```

---

# 🔧 Environment Variables

Create a `.env` file inside the **backend** directory.

Example:

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=*

POSTGRES_DB=blog_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

EMAIL_HOST=smtp4dev
EMAIL_PORT=25

ELASTICSEARCH_HOST=http://elasticsearch:9200
```

> Never commit your production environment variables to version control.

---

# 🐳 Running with Docker

Build all services:

```bash
docker compose build
```

Start the containers:

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

Stop the project:

```bash
docker compose down
```

Rebuild images:

```bash
docker compose up --build
```

---

# 🐳 Docker Services

The project is composed of multiple services working together.

| Service       | Description                       |
| ------------- | --------------------------------- |
| backend       | Django REST Framework application |
| frontend      | React application                 |
| db            | PostgreSQL database               |
| redis         | Redis cache & Celery broker       |
| worker        | Celery worker                     |
| elasticsearch | Full-text search engine           |
| logstash      | Log processing pipeline           |
| kibana        | Log visualization                 |
| smtp4dev      | Local email testing server        |

---

# 🚀 Running Without Docker

### Backend

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate virtual environment:

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run development server:

```bash
python manage.py runserver
```

---

### Frontend

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

---

# 📦 Production Deployment

A production deployment typically includes:

* Nginx
* Gunicorn
* PostgreSQL
* Redis
* Celery
* Elasticsearch
* Logstash
* Kibana
* Docker Compose

The production stack is designed to provide scalability, reliability, and easier maintenance.

---

# 💡 Useful Commands

Build images:

```bash
docker compose build
```

Start services:

```bash
docker compose up
```

Stop services:

```bash
docker compose down
```

Run migrations:

```bash
docker compose exec backend python manage.py migrate
```

Create superuser:

```bash
docker compose exec backend python manage.py createsuperuser
```

Collect static files:

```bash
docker compose exec backend python manage.py collectstatic
```

Open Django shell:

```bash
docker compose exec backend python manage.py shell
```

View logs:

```bash
docker compose logs -f backend
```

Restart a service:

```bash
docker compose restart backend
```

---

# 📌 Notes

* Docker is the recommended way to run the project.
* Redis is used both as a cache server and as the Celery message broker.
* Elasticsearch powers the application's full-text search functionality.
* Kibana provides centralized log visualization for easier debugging.
* GitHub Actions automatically runs tests on every push and pull request.

📂 Project Structure

The project follows a modular architecture to improve maintainability, scalability, and separation of concerns.

.
├── backend/
│   ├── accounts/
│   │        └── tests/
│   ├── blogs/
│   │       └── tests/
│   │       └── search/
│   ├── core/
│   ├── media/
│   ├── requirements.txt
│   ├── manage.py
│   └── RestApiBlog/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── routes/
│   │   ├── context/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
│
├── logstash/
│   └── pipeline/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── docker-compose-stage.yml
├── default.conf
└── README.md
⚙️ Getting Started

Follow these instructions to run the project locally.

Prerequisites

Make sure the following software is installed on your machine:

Git
Docker
Docker Compose
Python 3.12+
Node.js 22+
npm
📥 Clone Repository
git clone https://github.com/your-username/RestApiBlog.git
cd RestApiBlog
🔧 Environment Variables

Create a .env file inside the backend directory.

Example:

SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=*

POSTGRES_DB=blog_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

EMAIL_HOST=smtp4dev
EMAIL_PORT=25

ELASTICSEARCH_HOST=http://elasticsearch:9200

Never commit your production environment variables to version control.

🐳 Running with Docker

Build all services:

docker compose build

Start the containers:

docker compose up

Run in detached mode:

docker compose up -d

Stop the project:

docker compose down

Rebuild images:

docker compose up --build
🐳 Docker Services

The project is composed of multiple services working together.

Service	Description
backend	Django REST Framework application
frontend	React application
db	PostgreSQL database
redis	Redis cache & Celery broker
worker	Celery worker
elasticsearch	Full-text search engine
logstash	Log processing pipeline
kibana	Log visualization
smtp4dev	Local email testing server
🚀 Running Without Docker
Backend
cd backend

Create virtual environment:

python -m venv .venv

Activate virtual environment:

Windows

.venv\Scripts\activate

Linux/macOS

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Run development server:

python manage.py runserver
Frontend
cd frontend

Install dependencies:

npm install

Run development server:

npm run dev
📦 Production Deployment

A production deployment typically includes:

Nginx
Gunicorn
PostgreSQL
Redis
Celery
Elasticsearch
Logstash
Kibana
Docker Compose

The production stack is designed to provide scalability, reliability, and easier maintenance.

💡 Useful Commands

Build images:

docker compose build

Start services:

docker compose up

Stop services:

docker compose down

Run migrations:

docker compose exec backend python manage.py migrate

Create superuser:

docker compose exec backend python manage.py createsuperuser

Collect static files:

docker compose exec backend python manage.py collectstatic

Open Django shell:

docker compose exec backend python manage.py shell

View logs:

docker compose logs -f backend

Restart a service:

docker compose restart backend
📌 Notes
Docker is the recommended way to run the project.
Redis is used both as a cache server and as the Celery message broker.
Elasticsearch powers the application's full-text search functionality.
Kibana provides centralized log visualization for easier debugging.
GitHub Actions automatically runs tests on every push and pull request.
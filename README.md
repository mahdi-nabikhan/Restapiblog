# 📌 RestApiBlog

A full-stack blog platform built with Django REST Framework (DRF) and React(React Query), featuring authentication, comments system, caching, pagination, and modern backend architecture.

---

## 🚀 Features.

### 🔐 Authentication
- JWT-based authentication (custom + SimpleJWT)
- Login / Register system
- Cookie-based auth support
- Protected routes (backend + frontend)

### 📝 Blog System
- Create / Read / Update / Delete Posts
- Categories support
- Post snippets for previews
- Image upload support

### 💬 Comments System
- Add comments to posts
- Update & delete comments
- Reply system support (ready for nested structure)

### ⚡ Performance
- Redis caching for post list
- Celery background tasks
- Rate limiting (throttling)

### 🔍 Search
- Elasticsearch integration ready (structure prepared)

### 📧 Email System
- SMTP integration using smtp4dev (development environment)

### 🧪 Testing
- Pytest-based tests
- Model tests (Post, Category, Comments)
- Serializer tests
- API endpoint tests

---

## 🧱 Tech Stack

### Backend
- Django 5+
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- SimpleJWT
- django-redis
- drf-yasg (Swagger)

### Frontend
- React.js
- React Router
- Context API
- Fetch API
- CSS (custom styling)

### DevOps
- Docker & Docker Compose
- Elasticsearch + Kibana + Logstash (ELK Stack)
- SMTP4dev

---

## 🐳 Run Project (Docker)

```bash
docker compose up --build

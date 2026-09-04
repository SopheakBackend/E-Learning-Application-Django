# 🎓 E-Learning Application

A comprehensive, production-ready E-Learning Platform built using **Django** and powered by asynchronous **WebSockets**. The system features a custom Content Management System (CMS) with custom draggable content allow for instructors to manage courses and modules without having to delete and start from scratch, module enrollments for students, and Real-Time Chat Rooms within individual course workspaces.

---

## 🚀 Features

### 👨‍🏫 For Instructors (CMS)
- **Course & Module Management:** Create, update, and organize courses dynamically.
- **Flexible Content Types:** Support for text, video, files, and images within lectures.
- **Order Management:** Drag-and-drop ordering system for modules and contents.

### 🧑‍🎓 For Students
- **Course Enrollment:** Simple discovery and student registration process for available courses.
- **Interactive Workspace:** Clean interface to follow multi-module educational courses.

### 💬 Real-Time Collaboration
- **Course Chat Rooms:** Instant message exchanging inside designated course channels.
- **Asynchronous Architecture:** Handled completely via persistent WebSocket connections.

---

## 🛠️ Tech Stack

- **Backend Framework:** Django (Python)
- **Asynchronous Engine:** Django Channels (ASGI) & WebSockets
- **Database:** PostgreSQL (Production-grade relational storage)
- **Caching & Channel Layer:** Redis (Memory store for WebSockets & content caching)
- **WSGI / ASGI Servers:** uWSGI (HTTP/WSGI) & Daphne (ASGI)
- **Reverse Proxy:** Nginx
- **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

```text
├── chat/               # WebSocket consumer logic and chat configurations
├── config/             # Main Django configuration directory (settings, URLs, ASGI/WSGI)
├── courses/            # Core CMS application (Course, Module, and Content models)
├── educa/              # Base setup parameters and templates
├── students/           # Student registration and course enrollment workspace
├── static/             # Global CSS, JS, and layout assets
└── templates/          # Global and base HTML templates
```

---

## ⚙️ Installation & Local Setup

### Prerequisites
Make sure you have the following installed on your machine:
- **Docker** and **Docker Compose**
- Python 3.11+ *(if running locally without containers)*

### Quick Start with Docker
The repository includes a `Dockerfile` and `docker-compose.yaml` to orchestrate Django, PostgreSQL, Redis, and Nginx.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SopheakBackend/E-Learning-Application.git
   cd E-Learning-Application
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the root directory (or update settings in `config/settings.py`) to specify:
   ```env
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   POSTGRES_DB=educa
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   ```

3. **Build and Run the Containers**
   ```bash
   docker-compose up --build
   ```
   *This command spins up the web server, applies migrations via `wait-for-it.sh`, initializes Redis caching, and maps the static directories.*

4. **Create a Superuser (Admin & Instructor Portal)**
   Open a separate terminal window and run:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the Application**
   - **Student Portal / Main Site:** `http://localhost:8000`
   - **Admin / CMS Portal:** `http://localhost:8000/admin`

---

## 🔒 Production Deployment Overview

In a staging or production workspace, the app relies on high-performance infrastructure:
- **Nginx** handles incoming traffic, SSL termination, and routes static/media files directly.
- **uWSGI** handles standard synchronous HTTP requests.
- **Daphne/Channels** proxies long-running WebSocket connections for the live chat features.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create.
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

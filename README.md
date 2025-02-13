# 🌥️ Nuage - Secure File & Media Sharing

Nuage is a **self-hosted** platform for **securely sharing files, videos, and images**, featuring **authentication and permission management**. 🚀

![Project Status](https://img.shields.io/badge/status-in%20development-orange?style=for-the-badge)

---
## 📜 **Installation**
🐳 Start the Containers with Docker:
```shell
docker-compose up -d --build  # build Docker images
```

📦 Install dependencies:
```shell
pip install -r requirements.txt
```

🚀 Run the project:
```shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

🧪 Run tests:
```shell
pytest tests/
```

Access the documentation 👉 [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
## ✨ **Features**
✅ **Secure File Storage** with **PostgreSQL** and **MinIO**  
✅ **JWT Authentication** with **bcrypt password hashing**  
✅ **Upload & View Files** (images, videos, PDFs...)  
✅ **User Management** with roles and permissions  
✅ **REST API** with **FastAPI** for integration and automation  
✅ **Dockerized Deployment** for easy setup  

---
## 🎯 **To-Do**
✅ Add a frontend using Nuxt 3 or Vue.js  
✅ Manage user roles & permissions  
✅ Upload & stream files directly in the browser  

# Microservices Architecture with API Gateway (FastAPI)

## Project Overview
This project demonstrates the implementation of a microservices-based backend system using FastAPI. The system consists of independent microservices for managing students and courses, with an API Gateway acting as a single entry point for all client requests. The API Gateway handles request routing, authentication, logging, and error handling.

The architecture follows modern microservices design principles such as separation of concerns, independent deployment, centralized access control, and service-to-service communication through HTTP.

---

## Author
- **Name:** Silva S. P. S  
- **Student Number:** IT22219602  

---

## System Architecture

- **API Gateway** – Port 8000  
  Acts as the single entry point for all client requests. Handles:
  - Request routing
  - JWT-based authentication
  - Logging middleware
  - Centralized error handling

- **Student Microservice** – Port 8001  
  Manages student-related CRUD operations.

- **Course Microservice** – Port 8002  
  Manages course-related CRUD operations.

---

## Technologies Used

- Python 3.11+
- FastAPI
- Uvicorn (ASGI Server)
- HTTPX (Service-to-service communication)
- Pydantic (Data validation)
- Passlib (Password hashing)
- Python-JOSE (JWT authentication)
- Python-Multipart (Form handling)
- Postman / Thunder Client (API testing)
- Visual Studio Code

---

## Project Structure
microservices-fastapi/
│
├── gateway/
│ ├── main.py
│ ├── auth.py
│ ├── logging_middleware.py
│ └── exceptions.py
│
├── student-service/
│ ├── main.py
│ ├── models.py
│ ├── service.py
│ └── data_service.py
│
├── course-service/
│ ├── main.py
│ ├── models.py
│ ├── service.py
│ └── data_service.py
│
├── requirements.txt
└── README.md

## Installation & Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
### 2. Install dependancies
```bash
pip install -r requirements.txt
```
### 3.Start Student Service
```bash
uvicorn student-service.main:app --port 8001 --reload
```
### 4. Start Course Service
```bash
uvicorn course-service.main:app --port 8002 --reload
```
### 5. Start API Gateway
```bash
uvicorn gateway.main:app --port 8000 --reload
```

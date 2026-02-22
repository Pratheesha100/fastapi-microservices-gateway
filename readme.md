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


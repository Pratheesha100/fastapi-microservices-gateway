# gateway/main.py 
import json
from fastapi import FastAPI, HTTPException, Request 
from fastapi.responses import JSONResponse 
import httpx 
from typing import Any 

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

from exceptions import (
    ServiceNotFoundException,
    DownstreamServiceUnavailableException,
    DownstreamTimeoutException,
    InvalidPayloadException,
    DownstreamErrorException,
)


from logging_middleware import LoggingMiddleware
 
app = FastAPI(title="API Gateway", version="1.0.0") 

app.add_middleware(LoggingMiddleware) #register the LoggingMiddleware after creating the app
 
# Service URLs 
SERVICES = { 
    "student": "http://localhost:8001",
    "course": "http://localhost:8002", 
} 
 
async def forward_request(service: str, path: str, method: str, **kwargs):
    if service not in SERVICES:
        raise ServiceNotFoundException(service)

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            if response.status_code >= 400:
                try:
                    error_body = response.json()
                except ValueError:
                    error_body = response.text or "Downstream service error"

                raise DownstreamErrorException(
                    service=service,
                    path=path,
                    error=error_body,
                    status_code=response.status_code
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )

        except httpx.ConnectError:
            raise DownstreamServiceUnavailableException(service, url)

        except httpx.ReadTimeout:
            raise DownstreamTimeoutException(service)

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Gateway error while contacting {service}: {str(e)}"
            ) 
        
@app.get("/") 
def read_root(): 
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())} 
 

# Authentication Route
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}



# Student Service Routes 
@app.get("/gateway/students") 
async def get_all_students(current_user: dict = Depends(get_current_user)): 
    """Get all students through gateway""" 
    return await forward_request("student", "/api/students", "GET") 
 
@app.get("/gateway/students/{student_id}") 
async def get_student(student_id: int, current_user: dict = Depends(get_current_user)): 
    """Get a student by ID through gateway""" 
    return await forward_request("student", f"/api/students/{student_id}", "GET") 
 
@app.post("/gateway/students") 
async def create_student(request: Request, current_user: dict = Depends(get_current_user)): 
    """Create a new student through gateway""" 
    try:
        body = await request.json()
        if not body:
            raise ValueError
    except Exception:
        raise InvalidPayloadException()

    return await forward_request("student", "/api/students", "POST", json=body) 
 
@app.put("/gateway/students/{student_id}") 
async def update_student(student_id: int, request: Request, current_user: dict = Depends(get_current_user)): 
    """Update a student through gateway""" 
    try:
        body = await request.json()
        if not body:
            raise ValueError
    except Exception:
        raise InvalidPayloadException()

    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body)
 
@app.delete("/gateway/students/{student_id}") 
async def delete_student(student_id: int, current_user: dict = Depends(get_current_user)): 
    """Delete a student through gateway""" 
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")


# Course Service Routes 
@app.get("/gateway/courses") 
async def get_all_courses(current_user: dict = Depends(get_current_user)): 
    """Get all courses through gateway""" 
    return await forward_request("course", "/api/courses", "GET") 
 
@app.get("/gateway/courses/{course_id}") 
async def get_course(course_id: int, current_user: dict = Depends(get_current_user)): 
    """Get a course by ID through gateway""" 
    return await forward_request("course", f"/api/courses/{course_id}", "GET") 
 
@app.post("/gateway/courses") 
async def create_course(request: Request, current_user: dict = Depends(get_current_user)): 
    """Create a new course through gateway""" 
    try:
        body = await request.json()
        if not body:
            raise ValueError
    except Exception:
        raise InvalidPayloadException()
    return await forward_request("course", "/api/courses", "POST", json=body) 
 
@app.put("/gateway/courses/{course_id}") 
async def update_course(course_id: int, request: Request, current_user: dict = Depends(get_current_user)): 
    """Update a course through gateway""" 
    try:
        body = await request.json()
        if not body:
            raise ValueError
    except Exception:
        raise InvalidPayloadException()

    return await forward_request("course", f"/api/courses/{course_id}", "PUT", json=body)
 
@app.delete("/gateway/courses/{course_id}") 
async def delete_course(course_id: int, current_user: dict = Depends(get_current_user)): 
    """Delete a course through gateway""" 
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")

    #Error handling testing route
@app.get("/gateway/test-marks")
async def test_marks():
    return await forward_request("marks", "/api/test", "GET")
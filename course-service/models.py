# course-service/models.py 
from pydantic import BaseModel 
from typing import Optional 
 
class Course(BaseModel): 
    id: int 
    name: str 
    code: str 
    description: str
 
class CourseCreate(BaseModel): 
    name: str 
    code: str 
    description: str 
 
class CourseUpdate(BaseModel): 
    name: Optional[str] = None 
    code: Optional[str] = None 
    description: Optional[str] = None 

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import json

app = FastAPI()

# Frontend se requests allow karne ke liye CORS setup
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# In-memory database (data will be lost on restart)
issues_db = []

# Pydantic model for Issue status and priority
class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Pydantic model for an Issue
class Issue(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: Status = Status.TODO
    priority: Priority = Priority.MEDIUM
    assignee: Optional[str] = None
    createdAt: str
    updatedAt: str

# Pydantic model for updating an Issue
class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    assignee: Optional[str] = None

# POST /issues - Create new issue
@app.post("/issues", response_model=Issue)
def create_issue(issue: IssueUpdate):
    # incoming data ko dictionary mein convert karte hain
    new_issue_data = issue.model_dump(exclude_unset=True)
    
    # naya issue object banate hain
    new_issue = Issue(
        **new_issue_data,
        id=str(uuid.uuid4()),
        createdAt=datetime.now().isoformat(),
        updatedAt=datetime.now().isoformat()
    )
    
    # issue ko database list mein add karte hain
    issues_db.append(new_issue)
    
    # naya issue return karte hain
    return new_issue

# GET /issues - Get list of all issues with search, filter, sort and pagination
@app.get("/issues", response_model=List[Issue])
def get_issues(
    title: Optional[str] = Query(None, description="Search issues by title"),
    status: Optional[Status] = Query(None, description="Filter issues by status"),
    priority: Optional[Priority] = Query(None, description="Filter issues by priority"),
    assignee: Optional[str] = Query(None, description="Filter issues by assignee"),
    sort_by: Optional[str] = Query("createdAt", description="Sort issues by a field (e.g., createdAt, title)"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc or desc)"),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    # filtered_issues list banate hain
    filtered_issues = issues_db
    
    # Filtering logic
    if title:
        filtered_issues = [issue for issue in filtered_issues if title.lower() in issue.title.lower()]
    
    if status:
        filtered_issues = [issue for issue in filtered_issues if issue.status == status]
    
    if priority:
        filtered_issues = [issue for issue in filtered_issues if issue.priority == priority]
        
    if assignee:
        filtered_issues = [issue for issue in filtered_issues if issue.assignee and assignee.lower() in issue.assignee.lower()]

    # Sorting logic
    if sort_by in Issue.__annotations__:
        reverse = (sort_order == "desc")
        filtered_issues.sort(key=lambda issue: getattr(issue, sort_by), reverse=reverse)
    
    # Pagination logic
    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize
    paginated_issues = filtered_issues[start_index:end_index]
    
    return paginated_issues

# GET /issues/:id - Return a single issue
@app.get("/issues/{issue_id}", response_model=Issue)
def get_issue(issue_id: str):
    # issues_db mein issue search karte hain
    for issue in issues_db:
        if issue.id == issue_id:
            return issue
    
    # agar issue nahi milta to 404 error return karte hain
    raise HTTPException(status_code=404, detail="Issue not found")

# PUT /issues/:id - Update an existing issue
@app.put("/issues/{issue_id}", response_model=Issue)
def update_issue(issue_id: str, updated_issue: IssueUpdate):
    # issue ko database mein search karte hain
    for index, issue in enumerate(issues_db):
        if issue.id == issue_id:
            # updated_issue se sirf provided fields ko nikalte hain
            update_data = updated_issue.model_dump(exclude_unset=True)
            
            # issue object ko update karte hain
            for key, value in update_data.items():
                setattr(issue, key, value)
            
            # updatedAt field ko refresh karte hain
            issue.updatedAt = datetime.now().isoformat()
            
            # updated issue ko return karte hain
            return issue
    
    # agar issue nahi milta to 404 error return karte hain
    raise HTTPException(status_code=404, detail="Issue not found")
# DELETE /issues/:id - Delete a single issue
@app.delete("/issues/{issue_id}", status_code=204)
def delete_issue(issue_id: str):
    global issues_db
    for index, issue in enumerate(issues_db):
        if issue.id == issue_id:
            issues_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Issue not found")
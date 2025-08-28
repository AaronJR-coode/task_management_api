Task management API
  Task Management API built using Django and Django REST Framework (DRF). This API simulate task manegement, user authentication, database modeling, and RESTful API design.
  * This API enables users to:
  - Create, update, delete, and view their personal tasks.
  - Mark tasks as complete or incomplete.
  - Filter and sort tasks by various parameters.
  - Authenticate and manage user accounts securely.
  - Each user has isolated access to their own data, and all API operations are protected accordingly.
Task Management (CRUD)
   - Attributes: Title, Description, Due Date, Priority (Low, Medium, High), Status (Pending, Completed).
Validation:
   - Due date must be in the future.
  - Restricted values for priority and status.
  - Completed tasks cannot be edited unless reverted to incomplete.
  - Timestamp added when a task is marked complete.
User Management (CRUD)
  - Users have: Username, Email, and Password.
  - Each user can manage only their own tasks.
  - Supports user registration, login, update, and deletion.
Task Completion
  - Endpoint to mark tasks as complete/incomplete.
  - When marked complete:
  - Task becomes read-only.
  - A completed_at timestamp is recorded.
  - Filtering & Sorting
Filter tasks by:
  - Status: Pending or Completed
  - Priority
  - Due Date
Sort tasks by:
  - Due Date
  - Priority Level


API Endpoints Overview

Method	    Endpoint	       Description	
POST	      /api/register/	 Register a new user	
POST	       /api/login/	  Login and get token (if JWT used)	
GET	        /api/task/	     List tasks (with filters/sorting)	
POST	       /api/task/	   Create a new task	
PUT	        /api/task/<id>/	  Update task (if not completed)	
DELETE	    /api/task/<id>/	  Delete a task	
POST	      /api/task/<id>/complete/	   Mark task as complete	
POST	     /api/task/<id>/incomplete/	  Revert task to incomplete	

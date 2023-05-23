# todolist-django
This is a README file for a Django REST Framework (DRF) Todo List Service with Authentication. This service provides an API for managing todo lists with user authentication. Users can create an account, log in, create and manage their own todo lists, and perform CRUD operations on individual todo items within their lists.

Features
User registration: Users can create a new account by providing a unique username and password.
User authentication: Users can log in to their account using their username and password.
Todo item management: Authenticated users can perform CRUD operations on individual todo items within their lists.
API endpoints: The service provides various API endpoints for interacting with the todo lists and items.

Installation
Clone the repository:


git clone https://github.com/sshekhas/todolist-django.git

Navigate to the project directory:

Create and activate a virtual environment (optional but recommended):


python3 -m venv venv
source venv/bin/activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt

make a postgress database in local and change the database setings in settings of the project according to your database
Perform database migrations:


python manage.py migrate

Start the development server:


python manage.py runserver

The service should now be running at http://localhost:8000/. You can access the API endpoints using a tool like cURL, Postman, or any other HTTP client.

API Endpoints
The following API endpoints are available for interacting with the todo list service:

POST /auth/register/: Create a new user account by providing a unique username, password1, password2, first_name.
POST /auth/login/: Log in to the service by providing your username and password.
POST /auth/logout/: Log out of the service.
GET /api/check-username-availability/?username=<your username>: check if provided username is available or get 3 suggested usernames.
POST /profiles/todo-list: Create a new todo list for the authenticated user.
GET /profiles/todo-list/: Retrieve todo lists.
PUT /profiles/todo-list/{list_id}: Update a specific todo list by its ID.
DELETE /profiles/todo-list//{list_id}: Delete a specific todo list by its ID.
GET /profiles/todo-list//{list_id}/: Retrieve a specific todo item by ID.
GET /profiles/ask-details/: retrive user's full name, done task, pending task, urgent task and total task numbers.
  
Authentication
Authentication is required for most of the API endpoints. To authenticate, include an Authorization header in your requests with the value Token <your_token>, where <your_token> is the token provided upon successful login.

# Setup Instructions
## Introduction
This is a REST API for managing todo items. The API uses FastAPI as the web framework, Supabase as the database, and JWT for authentication.

## Prerequisites
* Python 3.9 or higher
* pip 22.0 or higher
* A Supabase instance
* A .env file with the following environment variables:
	+ SUPABASE_URL
	+ SUPABASE_KEY
	+ JWT_SECRET

## Installation
1. Clone the repository: `git clone https://github.com/your-username/todo-app.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
	* On Linux/Mac: `source venv/bin/activate`
	* On Windows: `venv\Scripts\activate`
4. Install the dependencies: `pip install -r requirements.txt`
5. Create a .env file in the root directory and add the required environment variables

## Running the Application
1. Run the application: `uvicorn main:app --host 0.0.0.0 --port 8000`
2. Open a web browser and navigate to `http://localhost:8000/docs` to view the API documentation

## Environment Variables
The following environment variables are required:
* `SUPABASE_URL`: The URL of your Supabase instance
* `SUPABASE_KEY`: The key for your Supabase instance
* `JWT_SECRET`: The secret key for JWT authentication

## Railway Deployment
To deploy the application to Railway, follow these steps:
1. Create a new Railway project
2. Link your GitHub repository to the project
3. Configure the environment variables in the Railway dashboard
4. Deploy the application

## API Endpoints
The API has the following endpoints:
* `POST /users`: Create a new user
* `GET /users`: Get all users
* `GET /users/{user_id}`: Get a user by ID
* `POST /todos`: Create a new todo item
* `GET /todos`: Get all todo items
* `GET /todos/{todo_id}`: Get a todo item by ID

## API Documentation
The API documentation is available at `http://localhost:8000/docs`
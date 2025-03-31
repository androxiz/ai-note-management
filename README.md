# AI Note Management⚡ 

AI-powered Note Management system built with FastAPI.

## Description📜

The AI Note Management system is a backend application that allows users to create, manage, and summarize notes using AI-powered content generation. The app is designed to integrate seamlessly with a database (SQLite) and exposes various endpoints for managing notes. The AI summarization feature utilizes the Gemini model from Google for generating summaries of notes.

## Features🔥

- **CRUD operations** for managing notes (Create, Read, Update, Delete).
- **AI-powered summarization** of notes.
- **User authentication** and management (JWT tokens).
- **Analytics endpoint** for getting quick statistics
- Simple integration with SQLite.
- Dockerized for easy deployment and execution.

## Getting Started

Before running the project, make sure you have the following installed:

- Docker and Docker Compose
- Python 3.9+ (optional if using Docker)

### Running the Application🚀

To run the application in a Docker container, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/androxiz/ai-note-management.git
   cd ai-note-management
   ```
   
2. **Create a .env file:**
   In the root directory of the project, create a .env file and add the following variables:
   ```bash
   SECRET_KEY=YOUR_SECRET_KEY
   GEMINI_API_KEY=YOUR_API_KEY
   ```
   
3. **Build and start the Docker container:**
   ```bash
   docker-compose up --build
   ```
### Running Tests📊

1. **To run tests using Docker use:**

    ```bash
      docker-compose run --rm app pytest
    ```
2. **To look at test coverage use:**
    ```bash
    docker-compose run --rm app pytest --cov=. --cov-report=term --cov-config=.coveragerc
    ```

### API Docs 📚
Once the app is running, you can access the API documentation at:
[API Documentation](http://localhost:8000/docs)


   



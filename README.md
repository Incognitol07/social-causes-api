# Social Causes API

The **Social Causes API** is a RESTful API made to manage causes and contributions

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM(PostgreSQL also available as an alternative)
- **Testing**: Pytest
- **ER-Diagram**: Drawio

## Installation

### Prerequisites

- **Python 3.9+**

### Installation Steps  

#### 1. Clone the Repository  

Clone the repository to your local machine:  

```bash  
git clone https://github.com/Incognitol07/social-causes-api.git  
cd social-causes-api 
```  

#### 2. Set Up Virtual Environment  

To isolate your project dependencies, set up a Python virtual environment:

1. **Create the virtual environment**:  

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:  

   - **Command Prompt (Windows)**:  

     ```cmd
     .\venv\Scripts\activate
     ```

   - **PowerShell (Windows)**:  

     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

   - **Bash (Linux/Mac)**:  

     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:  

   ```bash
   pip install -r requirements.txt
   ```

4. **Deactivate the virtual environment (when done)**:  

   ```bash
   deactivate
   ```

---

#### 3. Set Up Environment Variables  

Create a `.env` file by copying the provided example file:  

- **Mac/Linux**:  

  ```bash  
  cp .env.example .env  
  ```  

- **Windows (Command Prompt)**:  

  ```cmd  
  copy .env.example .env  
  ```  

- **Windows (PowerShell)**:  

  ```powershell  
  Copy-Item .env.example .env  
  ```  

Edit the `.env` file and update the variables with your configuration:  

```plaintext  
ENVIRONMENT=development 
DATABASE_URL=sqlite:///./causes.db
```  

## Project Structure

```plaintext
social-causes-api/
├── app/
│   ├── main.py              # Application entry point
│   ├── utils/               # Utility functions (e.g., logging)
│   ├── router.py            # API endpoint router
│   ├── schemas.py           # Pydantic models for request validation
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database connection and session handling
│   └── config.py            # Configuration settings
├── tests/                   # Tests
├── requirements.txt         # Versions of installed packages
├── .env                     # Environment variables
└── README.md                # Project documentation
```


## Diagram

Check out the Entity-Relationship Diagram in `diagrams\er-diagram.png`

### Logging Support

The API includes robust logging functionality to ensure transparency and ease of debugging. The logging system is configured to capture critical events to help maintain a secure and reliable system.

#### Configuration

Logging is configured in the `app/utils/logging_config.py` file and integrates with routers across the application.

#### Example Log Structure

Here is an example of a log entry:

```plaintext
[2024-11-20 14:32:15,123] - INFO - Cause with ID: 7d05f4de-3b6d-49f3-982b-fe8efe6e1458 not found.
```

## Testing the API

You can test the API using **curl**, **Postman**, **Bruno**, or FastAPI's interactive docs available at `http://127.0.0.1:8000/docs`

### Example Request

To register a new user:

```bash
curl -X POST "http://127.0.0.1:8000/causes" -H "accept: application/json" -H "Content-Type: application/json" -d '{"title" :"Social Causes","description" : "A cause that is open to contributions","image_url" : "https://image.url"}'
```
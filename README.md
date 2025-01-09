# Social Causes API



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

<div align="center">

# 📝 TODO Management API with FastAPI

<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="300"/>

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-orange?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)](https://jwt.io/)

*A comprehensive TODO management system with user authentication and task management built with FastAPI*

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td>

### 🔥 **Core Features**
- **Task Management** - Complete CRUD operations for TODO items
- **User Authentication** - JWT-based secure authentication
- **Password Security** - Secure password hashing with pwdlib
- **Data Validation** - Type-safe request/response validation

</td>
<td>

### 🗃️ **Database & Architecture**
- **SQLAlchemy ORM** - Modern Python SQL toolkit
- **PostgreSQL Integration** - Robust relational database
- **Modular Design** - Organized router-based structure
- **Environment Configuration** - Secure environment variable management

</td>
</tr>
</table>

## 🏗️ Architecture

```mermaid
graph TD
    A[Client] -->|HTTP Requests| B[FastAPI Application]
    B --> C[User Router]
    B --> D[Task Router]
    
    C --> E[User Authentication]
    C --> F[JWT Token Management]
    D --> G[Task CRUD Operations]
    
    E --> H[SQLAlchemy Models]
    F --> H
    G --> H
    
    H --> I[PostgreSQL Database]
    
    B --> J[Pydantic Schemas]
    J --> K[Request Validation]
    J --> L[Response Serialization]
    
    style B fill:#009485
    style I fill:#336791
    style J fill:#E92063
    style E fill:#FF6B6B
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- PostgreSQL 12+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/NayeemHossenJim/Backend-with-FastAPI.git
   cd Backend-with-FastAPI
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   
   Create a `.env` file in the `project/TODO/` directory:
   ```env
   POSTGRES_DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   SECRET_KEY=your-super-secret-jwt-key-here
   ALGORITHM=HS256
   ```

5. **Database Setup**
   ```sql
   -- Create PostgreSQL database
   CREATE DATABASE todo_db;
   
   -- Tables will be created automatically by SQLAlchemy
   ```

6. **Start the server**
   ```bash
   cd project/TODO
   fastapi dev main.py
   ```

   🎉 Your API is now running at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Available Endpoints

### Available Endpoints

<details>
<summary><strong>👤 User Management</strong></summary>

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `POST` | `/users/` | Create a new user account | No |
| `POST` | `/users/token` | Login and get JWT access token | No |

**User Registration Example:**
```json
{
  "full_name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Login Example:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

</details>

<details>
<summary><strong>📋 Task Management</strong></summary>

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/tasks/` | Get all tasks | Optional |
| `POST` | `/tasks/` | Create a new task | Required |
| `GET` | `/tasks/{task_id}` | Get task by ID | Optional |
| `PUT` | `/tasks/{task_id}` | Update existing task | Required |
| `DELETE` | `/tasks/{task_id}` | Delete task by ID | Required |

**Task Creation Example:**
```json
{
  "task": "Complete project documentation",
  "description": "Write comprehensive README and API documentation",
  "priority": 1,
  "status": false,
  "owner_id": 1
}
```

</details>

### Request/Response Examples

<details>
<summary><strong>Create User Account</strong></summary>

**Request:**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "full_name": "John Doe",
       "username": "johndoe",
       "email": "john@example.com",
       "password": "securepassword123"
     }'
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-11-14T10:30:00"
  }
}
```

</details>

<details>
<summary><strong>Login and Get Token</strong></summary>

**Request:**
```bash
curl -X POST "http://localhost:8000/users/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=johndoe&password=securepassword123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

</details>

<details>
<summary><strong>Create Task</strong></summary>

**Request:**
```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "task": "Complete project documentation",
       "description": "Write comprehensive README and API documentation",
       "priority": 1,
       "status": false,
       "owner_id": 1
     }'
```

**Response:**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "task": "Complete project documentation",
    "description": "Write comprehensive README and API documentation",
    "priority": 1,
    "status": false,
    "owner_id": 1
  }
}
```

</details>

## 🛠️ Technology Stack

<div align="center">

| Category | Technology | Purpose |
|----------|------------|---------|
| **Framework** | FastAPI | High-performance async web framework |
| **Database** | PostgreSQL | Primary data storage |
| **ORM** | SQLAlchemy | Database abstraction and modeling |
| **Authentication** | PyJWT + python-jose | JWT token authentication |
| **Password Security** | pwdlib | Secure password hashing |
| **Validation** | Pydantic | Request/response data validation |
| **Environment** | python-dotenv | Environment variable management |
| **Email** | email-validator | Email validation |
| **Task Queue** | Celery + Redis | Background task processing |
| **Code Quality** | Ruff + isort | Linting and formatting |

</div>

## 📁 Project Structure

```
Backend-with-FastAPI/
├── 📄 LICENSE                    # License file
├── 📄 README.md                  # This file
├── 📄 requirements.txt           # Project dependencies
└── 📁 project/
    └── 📁 TODO/                  # Main application directory
        ├── 📄 __init__.py        # Package initialization
        ├── 📄 main.py            # FastAPI application entry point
        ├── 📄 database.py        # Database configuration and session management
        ├── 📄 model.py           # SQLAlchemy models (User, ToDo)
        ├── 📄 schema.py          # Pydantic schemas for validation
        ├── 📄 utils.py           # Utility functions (password hashing)
        └── 📁 routers/           # API route handlers
            ├── 📄 __init__.py    # Router package initialization
            ├── 📄 user.py        # User authentication and management routes
            └── 📄 task.py        # Task CRUD operation routes
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `project/TODO/` directory:

```env
# Database Configuration
POSTGRES_DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
ALGORITHM=HS256

# Application Settings (Optional)
DEBUG=True
```

### Database Models

#### User Model
- `id`: Primary key
- `full_name`: User's full name
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `created_at`: Account creation timestamp

#### ToDo Model
- `id`: Primary key
- `task`: Task title
- `description`: Task description
- `priority`: Task priority (integer)
- `status`: Task completion status (boolean)
- `owner_id`: Foreign key to User model

## 🚨 Error Handling

The API includes comprehensive error handling:

- **401 Unauthorized** - Invalid credentials or missing authentication
- **404 Not Found** - User or task doesn't exist
- **422 Validation Error** - Invalid request data format
- **500 Internal Server Error** - Database connection issues

Example error response:
```json
{
  "detail": "Task not found"
}
```

## 🧪 Testing

```bash
# Navigate to the application directory
cd project/TODO

# Run with pytest (install pytest first)
pip install pytest httpx
pytest

# Test specific endpoints
pytest -v tests/test_users.py
pytest -v tests/test_tasks.py
```

## 📈 Performance Features

- **Async/Await Support** - Non-blocking operations for high concurrency
- **JWT Authentication** - Stateless authentication mechanism
- **Database Session Management** - Efficient connection handling
- **Type Safety** - Full type hints and runtime validation
- **Modular Architecture** - Organized codebase with router separation
- **Password Security** - Modern password hashing algorithms

## 🔐 Security Features

- **JWT Tokens** - Secure authentication with configurable expiration
- **Password Hashing** - Using modern pwdlib for secure password storage
- **Input Validation** - Pydantic models prevent injection attacks
- **Environment Variables** - Secure configuration management
- **CORS Support** - Configurable cross-origin resource sharing

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Nayeem Hossen Jim**
- GitHub: [@NayeemHossenJim](https://github.com/NayeemHossenJim)

---
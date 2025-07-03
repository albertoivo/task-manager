# Task Manager API

A robust and scalable RESTful API for task management built with FastAPI and PostgreSQL. This project demonstrates modern Python web development practices, including comprehensive testing, database migrations, and containerization.

## 🎯 Project Motivation

This project was created to showcase a production-ready task management system that demonstrates:

- **Clean Architecture**: Well-structured codebase with clear separation of concerns
- **Modern Python Development**: Using FastAPI, SQLAlchemy, and Pydantic for type safety
- **Database Management**: Proper migrations with Alembic and data modeling
- **Testing Excellence**: Comprehensive test suite with 90%+ coverage
- **DevOps Ready**: Containerized with Docker and ready for deployment
- **API Documentation**: Auto-generated OpenAPI documentation

Whether you're learning modern Python web development or need a starting point for a task management system, this project provides a solid foundation.

## 🚀 Features

### Core Functionality
- ✅ **CRUD Operations**: Create, read, update, and delete tasks
- ✅ **Advanced Filtering**: Filter tasks by status, priority, assignee, and date ranges
- ✅ **Smart Queries**: Find overdue tasks, tasks due today, or due within a specific timeframe
- ✅ **Full-Text Search**: Search tasks by title or description
- ✅ **Data Validation**: Robust input validation with Pydantic schemas

### Technical Features
- ✅ **Database Migrations**: Version-controlled schema changes with Alembic
- ✅ **Comprehensive Testing**: Unit tests for all endpoints and business logic
- ✅ **Auto Documentation**: Interactive API docs with Swagger UI
- ✅ **Containerization**: Docker and Docker Compose support
- ✅ **Development Tools**: Code formatting, linting, and debugging setup

## 🛠️ Technologies & Frameworks

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for Python APIs
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Python SQL toolkit and ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type annotations
- **[PostgreSQL](https://www.postgresql.org/)** - Advanced open-source relational database

### Development & Testing
- **[Pytest](https://docs.pytest.org/)** - Testing framework
- **[Docker](https://www.docker.com/)** - Containerization platform
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server for running the application

### Code Quality
- **[Black](https://black.readthedocs.io/)** - Code formatter
- **[Flake8](https://flake8.pycqa.org/)** - Linting tool
- **Type Hints** - Full type annotation coverage

## 📋 API Endpoints

### Task Management
- `GET /tasks/` - List all tasks
- `GET /tasks/{id}` - Get specific task
- `POST /tasks/` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Filtering & Search
- `GET /tasks/filter/status/{status}` - Filter by status
- `GET /tasks/filter/priority/{priority}` - Filter by priority
- `GET /tasks/overdue` - Get overdue tasks
- `GET /tasks/due-today` - Get tasks due today
- `GET /tasks/due-soon?days=7` - Get tasks due soon
- `GET /tasks/search?q=term` - Search tasks
- `GET /tasks/filter` - Advanced filtering with multiple criteria

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- Git
- Docker & Docker Compose (for containerized setup)

### Option 1: Local Development with Virtual Environment

#### 1. Clone the Repository
```bash
git clone https://github.com/albertoivo/task-manager.git
cd task-manager
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanager
SECRET_KEY=your-secret-key-here
DEBUG=True
```

#### 5. Set Up Local Database
```bash
# Install and start PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE taskmanager;
CREATE USER taskuser WITH PASSWORD 'taskpass';
GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskuser;
\q
```

#### 6. Run Database Migrations
```bash
# Initialize Alembic (if not already done)
alembic upgrade head
```

#### 7. Start the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker Compose (Recommended)

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

#### 2. Start with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

#### 3. Run Database Migrations
```bash
# Execute migrations inside the container
docker-compose exec app alembic upgrade head
```

The API will be available at `http://localhost:8000`

## 📖 Usage Examples

### Using the Interactive Documentation
Visit `http://localhost:8000/docs` for the interactive Swagger UI documentation where you can test all endpoints.

### Using cURL

#### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Implement user authentication",
       "description": "Add JWT-based authentication to the API",
       "status": "pending",
       "priority": "high",
       "due_date": "2025-07-01T10:00:00",
       "assigned_to": "John Doe"
     }'
```

#### Get All Tasks
```bash
curl "http://localhost:8000/tasks/"
```

#### Filter Tasks by Status
```bash
curl "http://localhost:8000/tasks/filter/status/pending"
```

#### Search Tasks
```bash
curl "http://localhost:8000/tasks/search?q=authentication"
```

#### Advanced Filtering
```bash
curl "http://localhost:8000/tasks/filter?status=pending&priority=high&assigned_to=John%20Doe"
```

## 🧪 Testing

### Run All Tests
```bash
# With virtual environment activated
pytest -v

# With Docker
docker-compose exec app pytest -v
```

### Run Specific Test Categories
```bash
# CRUD tests only
pytest app/tests/test_task_crud.py -v

# Filter tests only
pytest app/tests/test_task_filters.py -v

# With coverage report
pytest --cov=app --cov-report=html -v
```

### Test Coverage
The project maintains high test coverage (90%+) with comprehensive tests for:
- All CRUD operations
- Input validation
- Error handling
- Filtering and search functionality
- Database operations

## 🗃️ Database Schema

### Task Model
```python
class Task:
    id: int                    # Primary key
    title: str                # Task title (required)
    description: str          # Task description (optional)
    status: TaskStatus        # pending, in_progress, completed
    priority: TaskPriority    # low, medium, high
    due_date: datetime        # Due date (optional)
    assigned_to: str          # Assignee name (optional)
    created_at: datetime      # Creation timestamp
    updated_at: datetime      # Last update timestamp
```

### Enums
```python
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

## 🔄 Database Migrations

This project uses Alembic for database migrations. All schema changes are version-controlled and can be applied consistently across environments.

### Common Migration Commands
```bash
# Create a new migration
alembic revision --autogenerate -m "Add new field to task"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# View migration history
alembic history
```

## 🐳 Docker Information

### Services
- **app**: FastAPI application
- **db**: PostgreSQL database
- **redis**: Redis cache (for future features)

### Volumes
- `postgres_data`: Persistent database storage
- `redis_data`: Persistent Redis storage

### Ports
- `8000`: FastAPI application
- `5432`: PostgreSQL database
- `6379`: Redis cache

## 🚀 Deployment

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

### Production Considerations
- Use a strong `SECRET_KEY` and `JWT_SECRET_KEY`
- Set `DEBUG=False` in production
- Use environment-specific database URLs
- Configure proper logging levels
- Set up database backups
- Use HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📞 Support

If you have any questions or issues, please:
- Check the [Issues](https://github.com/albertoivo/task-manager/issues) page
- Create a new issue if your problem isn't already reported
- Provide detailed information about your environment and the issue

---

**Happy coding!** 🎉
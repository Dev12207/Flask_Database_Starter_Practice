# Flask Database Learning Repository

A step-by-step guide to learn Flask with databases - from basic SQLite to production-ready PostgreSQL/MySQL.

## Prerequisites
- Python basics
- Flask basics (routes, templates, Jinja2)

## Course Structure

| Part | Topic | One-Line Summary |
|------|-------|------------------|
| **part-1** | Basic SQLite | Basic Flask app with SQLite connection and one simple table (Create & Read) |
| **part-2** | Full CRUD | Full CRUD operations (Create, Read, Update, Delete) with HTML forms |
| **part-3** | SQLAlchemy ORM | Flask-SQLAlchemy ORM integration with models and relationships |
| **part-4** | REST API | REST API with Flask for database operations (JSON responses) |
| **part-5** | Production DB | Switching to PostgreSQL/MySQL with environment configuration |

## Difficulty Progression

```
Easy ────────────────────────────────► Advanced

part-1 → part-2 → part-3 → part-4 → part-5
SQLite   CRUD     ORM      API      PostgreSQL
```

## Quick Start

```bash
# Clone repository
git clone <repo-url>
cd flask-database-starter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install base dependencies
pip install flask flask-sqlalchemy

# Start with part-1
cd part-1
python app.py
```

## Installation by Part

```bash
# Part 1-2: Basic Flask
pip install flask

# Part 3: SQLAlchemy ORM
pip install flask-sqlalchemy

# Part 4: REST API
# (No additional packages needed)

# Part 5: Production Databases
pip install psycopg2-binary  # PostgreSQL
pip install pymysql          # MySQL
pip install python-dotenv    # Environment variables
```

## Folder Structure

```
flask-database-starter/
├── README.md               <- You are here
├── part-1/                 <- Basic SQLite
│   ├── app.py
│   ├── templates/
│   └── README.md
├── part-2/                 <- Full CRUD
│   ├── app.py
│   ├── templates/
│   └── README.md
├── part-3/                 <- SQLAlchemy ORM
│   ├── app.py
│   ├── templates/
│   └── README.md
├── part-4/                 <- REST API
│   ├── app.py
│   └── README.md
└── part-5/                 <- PostgreSQL/MySQL
    ├── app.py
    ├── .env.example
    ├── templates/
    └── README.md
```

## Key Concepts Covered

- SQLite database connection
- SQL commands (CREATE, SELECT, INSERT, UPDATE, DELETE)
- Flask request handling (GET, POST)
- HTML forms and form data
- Flask-SQLAlchemy ORM
- Database relationships (One-to-Many)
- REST API design
- JSON responses
- Environment variables
- PostgreSQL/MySQL configuration

## Tips for Learning

1. **Run each part** before reading the code
2. **Read comments** in the code - they explain everything
3. **Try the exercises** at the end of each README
4. **Break things** - see what errors look like
5. **Modify the code** - add your own features

## Common Issues

### Port already in use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

### Module not found
```bash
# Make sure venv is activated and packages installed
pip install flask flask-sqlalchemy
```

### Database locked (SQLite)
```bash
# Close other connections or restart the app
```

## Next Steps After This Course

1. Learn Flask Blueprints for larger apps
2. Add unit testing with pytest
3. Deploy to Heroku/Railway/Render
4. Learn Docker for containerization
5. Add Redis for caching

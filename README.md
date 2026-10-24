# Social Media API

A REST API for a social media backend, built with **FastAPI**, **PostgreSQL** and **SQLAlchemy**. Users can register, log in with JWT authentication, create and manage posts, and vote on posts.

Built following Sanjeev Thiyagarajan's [FastAPI course](https://github.com/Sanjeev-Thiyagarajan/fastapi-course).

## Features

- **JWT authentication** with the OAuth2 password flow and bcrypt password hashing
- **Posts CRUD** with ownership checks: only a post's author can update or delete it
- **Votes**: one vote per user per post, enforced by a composite primary key
- **Search and pagination** on the post list, with vote counts computed in a single SQL query
- **Database migrations** with Alembic
- **Interactive API docs** at `/docs` (Swagger UI)

## Tech stack

FastAPI · PostgreSQL · SQLAlchemy 1.4 · Alembic · Pydantic · python-jose (JWT) · passlib (bcrypt)

## API endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/` | No | Health check |
| `POST` | `/users/` | No | Register a new user |
| `GET` | `/users/{id}` | No | Get a user by id |
| `POST` | `/login` | No | Log in (form data: `username` = email, `password`) and get a token |
| `GET` | `/posts/` | Yes | List posts with vote counts. Query params: `limit`, `skip`, `search` |
| `POST` | `/posts/` | Yes | Create a post |
| `GET` | `/posts/{id}` | Yes | Get one post with its vote count |
| `PUT` | `/posts/{id}` | Yes (owner) | Update a post |
| `DELETE` | `/posts/{id}` | Yes (owner) | Delete a post |
| `POST` | `/vote/` | Yes | Vote: `{"post_id": 1, "dir": 1}` to add, `"dir": 0` to remove |

## Project structure

```
.
├── app/
│   ├── main.py        # App setup, CORS, routers
│   ├── config.py      # Settings loaded from .env
│   ├── database.py    # Database engine and session
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic request/response schemas
│   ├── oauth2.py      # JWT creation and verification
│   ├── utils.py       # Password hashing
│   └── routers/       # auth, user, post, vote endpoints
├── alembic/           # Database migrations
├── alembic.ini
├── requirements.txt
└── .env.example
```

## Running locally

**Prerequisites:** Python 3.12 and PostgreSQL.

```bash
# 1. Clone the project
git clone https://github.com/pawansphere-art/fastapi-social-media-api.git
cd fastapi-social-media-api

# 2. Create a virtual environment and install dependencies
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Create the database
createdb fastapi

# 4. Set up environment variables (then edit .env)
cp .env.example .env

# 5. Create the tables
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs**. Register a user with `POST /users/`, then click **Authorize** and log in with that email and password to use the protected endpoints.

## Author

**Pawan**: [github.com/pawansphere-art](https://github.com/pawansphere-art)

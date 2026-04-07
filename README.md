# 💰 Expense Tracker — Full Stack Web Application

A production-ready full-stack expense tracking web application built with **Django REST Framework** and **React**, designed for AWS cloud deployment.

> Built as a portfolio project demonstrating full-stack development, REST API design, Docker containerization, and AWS cloud deployment for Cloud/DevOps roles.

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| Frontend | http://YOUR_S3_URL (after deployment) |
| API | http://YOUR_EC2_IP:8000/api/docs/ |
| Health Check | http://YOUR_EC2_IP:8000/api/v1/health/ |

---

## 🏗️ Architecture
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  React Frontend  │────▶│  Django REST API  │────▶│  PostgreSQL RDS │
│    (AWS S3)      │     │  (AWS EC2+Docker) │     │   (AWS RDS)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
             ┌──────▼──────┐            ┌────────▼───────┐
             │ Redis Cache  │            │    AWS S3      │
             │(ElastiCache) │            │ (Media Files)  │
             └─────────────┘            └────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Django 4.2 | Web framework |
| Django REST Framework | REST API |
| PostgreSQL | Primary database |
| Redis | Caching + Celery broker |
| Celery | Background tasks |
| JWT (simplejwt) | Authentication |
| Gunicorn | WSGI server |
| Nginx | Reverse proxy |
| Docker | Containerization |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| React Router | Client-side routing |
| Axios | HTTP client |
| Recharts | Data visualization |
| React Hot Toast | Notifications |

### DevOps / Cloud
| Service | Purpose |
|---------|---------|
| AWS EC2 | Application server |
| AWS RDS | Managed PostgreSQL |
| AWS S3 | Static + media storage |
| AWS ElastiCache | Managed Redis |
| AWS CloudWatch | Logging + monitoring |
| AWS ECR | Docker image registry |
| GitHub Actions | CI/CD pipeline |
| Docker Compose | Container orchestration |

---

## ✨ Features

- ✅ User registration and JWT authentication
- ✅ Add, edit, delete income and expense transactions
- ✅ 13 spending categories (Food, Transport, Housing, etc.)
- ✅ Monthly dashboard with bar and pie charts
- ✅ Category-wise budget limits and usage tracking
- ✅ Filter expenses by date, category, type, amount
- ✅ Paginated REST API with search
- ✅ Request logging with correlation IDs
- ✅ Docker + Gunicorn + Nginx production setup
- ✅ GitHub Actions CI/CD pipeline
- ✅ Environment-based configuration
- ✅ Swagger API documentation

---

## 📁 Project Structure
```
expense-tracker-app/
│
├── apps/                          # Django applications
│   ├── users/                     # Authentication app
│   │   ├── models.py              # Custom User model
│   │   ├── serializers.py         # User serializers
│   │   ├── views.py               # Auth views
│   │   └── urls.py                # Auth routes
│   │
│   └── expenses/                  # Core expense app
│       ├── models.py              # Expense + Budget models
│       ├── serializers.py         # API serializers
│       ├── views.py               # CRUD + Dashboard views
│       ├── filters.py             # Query filters
│       ├── tasks.py               # Celery tasks
│       └── urls.py                # Expense routes
│
├── config/                        # Django project config
│   ├── settings/
│   │   ├── base.py                # Shared settings
│   │   ├── development.py         # Local dev settings
│   │   └── production.py          # AWS production settings
│   ├── urls.py                    # Root URL config
│   ├── middleware.py              # Request logging
│   ├── pagination.py              # API pagination
│   └── celery.py                  # Celery config
│
├── frontend/                      # React frontend
│   ├── src/
│   │   ├── api/axios.js           # Axios + JWT interceptors
│   │   ├── context/AuthContext.js # Auth state management
│   │   ├── pages/
│   │   │   ├── Login.js           # Login page
│   │   │   ├── Register.js        # Register page
│   │   │   └── Dashboard.js       # Main dashboard
│   │   └── utils/PrivateRoute.js  # Protected routes
│   └── package.json
│
├── nginx/
│   └── nginx.conf                 # Nginx reverse proxy config
│
├── scripts/
│   └── entrypoint.sh              # Docker entrypoint
│
├── .github/
│   └── workflows/
│       └── deploy.yml             # CI/CD pipeline
│
├── Dockerfile                     # Multi-stage Docker build
├── docker-compose.yml             # Local development
├── docker-compose.prod.yml        # Production deployment
├── gunicorn.conf.py               # Gunicorn config
├── requirements.txt               # Python dependencies
└── manage.py                      # Django management
```

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker Desktop
- Git

### Backend Setup
```bash
# Clone the repo
git clone https://github.com/rutuja-rakshe/expense-tracker-app.git
cd expense-tracker-app

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

### Frontend Setup
```bash
cd frontend
npm install
echo "REACT_APP_API_URL=http://127.0.0.1:8000" > .env
npm start
```

Frontend runs at: `http://localhost:3000`

### Docker Setup (Full Stack Local)
```bash
docker-compose up -d
python manage.py migrate
python manage.py createsuperuser
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register/` | Register new user |
| POST | `/api/v1/auth/login/` | Login and get JWT tokens |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| POST | `/api/v1/auth/logout/` | Logout and blacklist token |
| GET/PATCH | `/api/v1/auth/profile/` | View and update profile |
| POST | `/api/v1/auth/change-password/` | Change password |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/expenses/` | List expenses with filters |
| POST | `/api/v1/expenses/` | Create new expense |
| GET | `/api/v1/expenses/{id}/` | Get single expense |
| PUT/PATCH | `/api/v1/expenses/{id}/` | Update expense |
| DELETE | `/api/v1/expenses/{id}/` | Delete expense |

### Dashboard and Budgets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/?year=2026&month=4` | Monthly summary |
| GET/POST | `/api/v1/budgets/` | List and create budgets |
| PUT/DELETE | `/api/v1/budgets/{id}/` | Update and delete budget |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health/` | Health check with DB ping |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/redoc/` | ReDoc documentation |
| GET | `/admin/` | Django admin panel |

### Filtering Examples
```
GET /api/v1/expenses/?category=food
GET /api/v1/expenses/?type=expense
GET /api/v1/expenses/?date_from=2026-04-01&date_to=2026-04-30
GET /api/v1/expenses/?search=grocery
GET /api/v1/expenses/?amount_min=100&amount_max=5000
GET /api/v1/expenses/?ordering=-amount
```

---

## ☁️ AWS Deployment

### Infrastructure
```
EC2 (t2.micro)     → Django + Gunicorn + Nginx via Docker
RDS (db.t3.micro)  → PostgreSQL 16
S3                 → React frontend and media files
ElastiCache        → Redis cache and Celery broker
CloudWatch         → Logs and monitoring
ECR                → Docker image registry
```

### Deployment Steps

**1. EC2 Setup**
```bash
sudo apt update && sudo apt install -y docker.io docker-compose git
sudo systemctl start docker
git clone https://github.com/rutuja-rakshe/expense-tracker-app.git
cd expense-tracker-app
```

**2. Environment**
```bash
cat > .env << EOF
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_IP
DATABASE_URL=postgres://postgres:password@RDS_ENDPOINT:5432/expense_tracker
REDIS_URL=redis://localhost:6379/0
USE_S3=False
SECURE_SSL_REDIRECT=False
EOF
```

**3. Run**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

**4. Frontend on S3**
```bash
cd frontend
REACT_APP_API_URL=http://YOUR_EC2_IP:8000 npm run build
# Upload build/ folder to S3 with static website hosting enabled
```

### CI/CD Pipeline
Push to `main` branch automatically triggers:
1. Run pytest test suite
2. Build Docker image
3. Push to AWS ECR
4. Deploy to EC2 via AWS SSM

---

## 🔐 Environment Variables
```bash
# Django Core
SECRET_KEY=                    # Django secret key (required)
DEBUG=False                    # Never True in production
ALLOWED_HOSTS=                 # EC2 IP or your domain

# Database
DATABASE_URL=postgres://user:pass@rds-endpoint:5432/expense_tracker

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Tokens
JWT_ACCESS_MINUTES=60
JWT_REFRESH_DAYS=7

# AWS S3 (production only)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1
USE_S3=True

# Email via AWS SES (production only)
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Error Tracking
SENTRY_DSN=
```

---

## 🧪 Running Tests
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests with coverage report
pytest --cov=apps --cov-report=term-missing -v

# Lint check
flake8 apps config --max-line-length=120

# Format code
black apps config
isort apps config
```

---

## 📊 Database Models

### User
```
id, email (unique), first_name, last_name,
currency, is_active, is_staff, date_joined, updated_at
```

### Expense
```
id, user (FK), title, amount, category, type,
date, notes, receipt_url, is_recurring, tags,
created_at, updated_at
```

### Budget
```
id, user (FK), category, monthly_limit,
created_at, updated_at
```

### Category Choices
```
food, transport, housing, utilities, healthcare,
entertainment, shopping, education, travel,
salary, freelance, investment, other
```

---

## 🎯 Resume Highlights

- Designed and deployed full-stack web application on AWS using EC2, RDS (PostgreSQL), S3, and ElastiCache (Redis)
- Built automated CI/CD pipeline with GitHub Actions → Docker → AWS ECR → EC2 with zero-downtime deployments
- Containerized Django application using multi-stage Docker builds
- Implemented JWT authentication with refresh token rotation and blacklisting
- Configured request logging middleware with unique correlation IDs for distributed tracing
- Built REST API with filtering, pagination, and search supporting 13 expense categories
- Secured production environment with HTTPS headers, environment-based secrets, and CORS configuration

---

## 👤 Author

**Rutuja Rakshe**
- GitHub: [@rutuja-rakshe](https://github.com/rutuja-rakshe)
- LinkedIn: [https://www.linkedin.com/in/rutuja-rakshe]

---

## 📄 License

MIT License — free to use for learning and portfolio purposes.

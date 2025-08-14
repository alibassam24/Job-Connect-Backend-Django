# CareerConnect -> Job Posting & Application Management API

A Django REST Framework backend for managing job postings, employee/employer profiles, applications, and skills — designed for a modern recruitment platform.

---

## Features

### User Management
- Register new users (Employee or Employer role)
- Login & Logout
- Update or delete accounts
- Role-based user profiles

### Employee Features
- Create and edit employee profiles
- Upload CVs and introduction text
- Add and remove skills
- Add, edit, and delete work experiences

### Employer Features
- Create and edit employer profiles
- Post jobs with details like experience level, workplace type, location
- Manage job postings (view, edit, delete)

### Job Management
- Post new jobs
- Search jobs & search by title,location,experience
- View job details
- Delete jobs
- API responses use **PageNumberPagination** (5 items per page) for job listings


### Application Management
- Employees can apply to jobs with a cover letter and CV
- Employers can view all applications for their posted jobs
- Edit or delete applications

---

## Tech Stack
- **Python 3.10+**
- **Django 4.x**
- **Django REST Framework**
- **SQLite**
- **Token Authentication:** 
- **PageNumberPagination**
---

## Setup Instructions


``` bash
# Clone the repo

# Create virtual environment
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

#Create Superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```
## API Endpoints Overview 🗂

### 👤 User Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/register-user/` | Register a new user |
| POST | `/login-user/` | Login user |
| POST | `/logout-user/` | Logout user |
| PATCH | `/update-user/<id>/` | Update user by ID |
| DELETE | `/delete-user/<id>/` | Delete user by ID |

### 🧑‍💼 Employee Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/create-employee-profile/` | Create employee profile |
| GET | `/view-employee-profile/<id>/` | View employee profile by ID |
| PATCH | `/edit-employee-profile/<id>/` | Edit employee profile by ID |
| POST | `/add-skills/` | Add skills to profile |
| DELETE | `/remove-skills/<id>/` | Remove a skill by ID |
| POST | `/add-experience/` | Add work experience |
| GET | `/get-experiences/` | Get all experiences |
| GET | `/get-experience-of-employee/<employee_id>/` | Get experiences of a specific employee |
| PATCH | `/edit-experience/<experience_id>/` | Edit experience by ID |
| DELETE | `/remove-experience/<experience_id>/` | Remove experience by ID |

### 🏢 Employer Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/create-employer-profile/` | Create employer profile |
| GET | `/view-employer-profile/<id>/` | View employer profile by ID |
| PATCH | `/edit-employer-profile/<id>/` | Edit employer profile by ID |
| POST | `/post-job/` | Post a new job |
| GET | `/search-jobs/<title>` | Search jobs |
| GET | `/view-job/<job_id>/` | View job details by job ID |
| DELETE | `/delete-job/<job_id>/` | Delete job by job ID |

### 📝 Application Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/send-application/<job_id>/` | Send job application |
| PATCH | `/edit-application/<application_id>/` | Edit an application by ID |
| GET | `/view-all-application/<job_id>/` | View all applications for a job |
| DELETE | `/delete-application/<application_id>/` | Delete an application by ID |



## 🙋‍♂️ Author
Ali Bassam
📧 alibassam063@gmail.com
🔗 https://www.linkedin.com/in/alibassam1
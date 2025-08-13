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
- Search jobs
- View job details
- Delete jobs

### Application Management
- Employees can apply to jobs with a cover letter and CV
- Employers can view all applications for their posted jobs
- Edit or delete applications

---

## Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite (default, can switch to PostgreSQL/MySQL)
- **Authentication:** Token-based authentication (DRF `TokenAuthentication`)
- **Media Handling:** Django `FileField` / `ImageField` with `MEDIA_URL` and `MEDIA_ROOT`

---

## Getting Started

### 1. Create a virtual environment & install dependencies
``` bash
Edit
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
```
### 2. Run migrations
```bash

python manage.py makemigrations
python manage.py migrate
```
### 3. Create a superuser
```bash
python manage.py createsuperuser
```
### 4. Run the development server
```
python manage.py runserver
```
## API Endpoints Overview
Method	Endpoint	Description
POST	/register-user/	Register a new user
POST	/login-user/	Login user
POST	/logout-user/	Logout user
PATCH	/update-user/<id>/	Update user
DELETE	/delete-user/<id>/	Delete user
POST	/create-employee-profile/	Create employee profile
GET	/view-employee-profile/<id>/	View employee profile
POST	/add-skills/	Add skills to profile
DELETE	/remove-skills/<id>/	Remove a skill
POST	/post-job/	Post a job
GET	/search-jobs/	Search jobs
GET	/view-job/<job_id>/	View job details
DELETE	/delete-job/<job_id>/	Delete job
POST	/send-application/<job_id>/	Send job application
PATCH	/edit-application/<application_id>/	Edit an application
GET	/view-all-application/<job_id>/	View all applications for a job
DELETE	/delete-application/<application_id>/

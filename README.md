# Travel Platform

A full-stack travel blog platform built with Python and Django.

This project was developed as a portfolio project to practice building a complete Django web application with authentication, user profiles, author management, content management, comments, search, filtering, security, database optimization, and automated testing.

## Features

### Blog

- Create and manage travel blog posts
- Published and draft posts
- Scheduled publishing
- Featured posts
- Categories and tags
- Search functionality
- Category, tag, and author filtering
- Pagination
- Previous and next post navigation
- Post view counter
- Login-required posts

### Authentication & Profiles

- User registration
- Login and logout
- Protected views
- Safe `next` URL validation after login
- User profile management
- Custom avatar upload
- Preset avatar selection
- Social media profile links

### Author Dashboard

- Author-only dashboard
- Create posts
- Edit posts
- Delete posts
- Author-based permissions
- Rich text editor for post content

### Comments

- Guest and authenticated user comments
- Comment approval system
- Display of approved comments
- Automatic user information for authenticated commenters

### Newsletter & Contact

- Newsletter subscription
- Contact form
- Form validation
- CAPTCHA protection
- User feedback messages

### Security

- Django authentication and authorization
- Protected author functionality
- Permission checks
- Safe login redirect validation
- Avatar preset validation
- Environment-based secret key
- HTTP-only session cookies
- Production-oriented security configuration

### Performance

- Database query optimization
- `select_related()` for foreign-key relationships
- `prefetch_related()` for many-to-many relationships
- Query annotations for comment counts
- Optimized blog queries

### Testing

The project includes automated tests covering important application functionality, including authentication, profiles, forms, blog views, filtering, permissions, and validation.

Run the test suite with:

```bash
python manage.py test
```

## Technologies

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Django Templates
- django-taggit
- django-summernote
- django-simple-captcha
- django-debug-toolbar
- django-extensions
- django-robots
- Git
- GitHub

## Project Structure

```text
travel-platform/
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── blog/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── management/
│       └── commands/
│           └── seed_demo.py
│
├── website/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── statics/
├── templates/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## Demo Data

The project includes a custom Django management command for generating sample data.

Run:

```bash
python manage.py seed_demo
```

The command creates sample:

- Users
- Authors
- Profiles
- Categories
- Blog posts
- Tags
- Comments
- Newsletter subscribers

This makes it possible to explore the main functionality of the project without manually creating the initial data.

The demo accounts use:

```text
Password: DemoPass123!
```

The demo password is intended only for local development and demonstration purposes.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/nadia-mofidi/travel-platform.git
cd travel-platform
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Django secret key

Set the following environment variable:

```text
DJANGO_SECRET_KEY
```

For local development, use a development-only secret key.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create demo data

```bash
python manage.py seed_demo
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Development

The project was developed incrementally with a focus on:

- Django best practices
- Authentication and authorization
- Form validation
- Database relationships
- Query optimization
- Security
- Automated testing
- Maintainable project structure
- Git version control

## Future Improvements

Possible future improvements include:

- Production deployment
- PostgreSQL database
- Cloud media storage
- CI/CD pipeline
- Expanded test coverage
- Advanced search
- REST API development

## Author

Nadia Mofidi

GitHub:  
https://github.com/nadia-mofidi

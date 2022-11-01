<p align="center">
  <a href="" rel="noopener">
    <h1 align="center">Authenticator</h1>
  </a>
</p>

---

## 📝 Table of Contents

- [Idea](#idea)
- [Dependencies / Limitations](#limitations)
- [Future Scope](#future_scope)
- [Setting up a local environment](#getting_started)
- [Usage](#usage)
- [Technology Stack](#tech_stack)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## 💡 Idea <a name = "idea"></a>

The idea of this project is to create an easy authenticator/log-in structure for my future projects, and to show my backend experience with JWT, authentication tools, two-factor authentication and API Creations with Django Rest Framework

## 🚀 Future Scope <a name = "future_scope"></a>

- Evolve two-factor authentication
- Fix security issues
- Create user trought the admin website

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development
and testing purposes.

### Prerequisites

- Latest Python Version
- IDE of your choice

The remaining requirements are in the requirements.txt file

### Installing

Clone the repository
```
git clone https://github.com/g0d1-prog/Authenticator.git
```

Add the .env in the backend directory file with the following configurations:

- DEBUG: False or True
- SECRET_KEY
- ALLOWED_HOSTS: List of allowed url hosts
- EMAIL_HOST_PASSWORD: Email address password to the system send the token to the user

Install the requirements
```
cd Authenticator
pip install -r requirements.txt
```

Make all and apply all the migrations to create the SQlite Database
```
cd backend
python manage.py makemigrations
python manage.py migrate
```

Collect the static files
```
python manage.py collectstatic
```

Run the server
```
python manage.py runserver
```

## 🎈 Usage <a name="usage"></a>

This tool works as a complete structure for login/registration/retrieval of user data through endpoints of the created API.

Base URL: authenticator.herokuapp.com

Endpoints:

- Admin: **/admin/** (To create an administrator user, it is necessary to create it via terminal with the createsuperuser command)
- Get JWT Token: **/api/token/**
- Register user: **/api/create/**
- Confirm user and add remaining information:
**/api/user/**
- Login: **/api/login/**
- Logout: **/api/logout/**
- Create another token: **/api/createToken/**
- Send confirmation token for account release: **/api/sendConfirmationCode/**
- Recover Password: **/api/changePassword/**

Each endpoint has its request data needed to return the response:

- Get JWT Token: No data request needed
- Register User: email, password
- Confirm user: email(Registered before), name, about, age, phone, token_code(must be equal to the token sent and registered to the user), is_active(must be True)
- Login: email, password
- Logout: No data request needed
- Create another token: token_code
- Send confirmation token: email, token_code
- Recover password: email, password, token_code(must be equal to the token sent to the user e-mail and registred in the user)

## ⛏️ Built With <a name = "tech_stack"></a>

- [Python](https://www.python.org/) - Programming Language
- [Django](https://www.djangoproject.com/) - Server-side Framework
- [Django Rest Framework](https://www.django-rest-framework.org/) - API Framework
- [JWT](https://jwt.io/) - Web Token Authenticator
- [SQLite](https://www.sqlite.org/index.html) - Database
- [Heroku](https://www.heroku.com/) - Deploy Tool

## ✍️ Authors <a name = "authors"></a>

- [@g0d1-prog](https://github.com/g0d1-prog) - Idea & Development

## 🎉 Acknowledgments <a name = "acknowledgments"></a>

- CORS Security
- JWT Authentication
- Token Confirmation via E-mail
- Two-factor authentication
[Korean](./README.md)

## Introduction

This project serves as an example of implementing the basic functionalities and pages of a web application,
demonstrating the use of the commonly used Model-View-Controller (MVC) pattern and CRUD (Create, Read, Update, Delete)
the pattern in Flask.
The code included in this repository will greatly assist developers in understanding these patterns.
The MVC pattern is a software design pattern that separates an application into three components: Model, View, and
Controller.
This structure helps improve code reusability and maintainability.

- The Model represents and processes the information (data) of the application.
- The View is responsible for the user interface (UI) that is presented to the user.
- The Controller handles user input and coordinates the interactions between the Model and the View.

CRUD represents the four basic operations in data persistence: Create, Read, Update, Delete.
These operations are
typically required functionalities in all web applications

## Getting Started

### Prerequisites

First, you'll need to install dependencies:

```bash
pip install -r requirements.txt
```

### Running

#### First time once

Before you run the app for the first time, you'll need to init, migrate, and upgrade for DB.  
We use for here flask-sqlalchemy, flask-migrate and flask-wtf.

```bash
flask db init     # Initialize the database
flask db migrate  # Create the migration
flask db upgrade  # Apply the migration
```

#### After running

If you once run the init script, from now on you can just run the app:

```bash
flask run
```

### Endpoints

- 🤷 `/` - Nothing
- 📪 `/contact`
    - `/contact/us` - Contact us
    - `/contact/complete` - When send the contact us form, redirect to this page
    - `/contact/<id>` - Hello to the user(id), It will be main page after
- 🔐 `/auth` - Authentication
    - `/auth/signup` - Sign Up
    - `/auth/signin` - Sign In
    - Redirects
        - `/auth/register` -> `/auth/signup`
        - `/auth/login` -> `/auth/signin`
- 🗂️ `/crud`
    - `/crud/users` - Show and edit all users
    - `/crud/register` - Register a new user directly
    - `/crud/<id>` - Edit user
    - `/crud/<id>/delete` - Delete user

### 🗝️ How login works?

1. When you
    1. sign-up, password is hashed and stored in the database.
    2. sign-in, hashed p.w is compared to the p/w in the database.
2. If the hashes (p/w)
    1. match, you are logged in.
    2. don't match, you are not logged in.
3. If you are logged in, you can access the `/auth` endpoints.

### 📚 Libraries

- 🗃️ SQL ㅣ DataBase
    - Flask SQLAlchemy > For simplify the use of SQLAlchemy with powerful ORM
    - Flask Migrate > For handles SQLAlchemy database migrations
- 🔐 Authentication
    - Flask WTF > For integrate Flask and WTForms, including CSRF
    - Flask Login > For handles the user session management

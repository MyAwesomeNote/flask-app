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

### Libraries

- Flask Extensions
    - Flask SQLAlchemy > For simplify the use of SQLAlchemy with powerful ORM
    - Flask Migrate > For handles SQLAlchemy database migrations
    - Flask WTF > For integrate Flask and WTForms, including CSRF, file upload, and reCAPTCHA
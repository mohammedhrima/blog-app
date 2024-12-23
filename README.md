# Project Overview
This project is a Flask-based web application that serves as both the backend and the file server. It includes basic authentication pages (signup and login) and a home page with a section for displaying news articles fetched from the backend.

### Project Structure
```
.
├── app.py
├── requirements.txt
├── setup.sh
├── static
│   ├── home.css
│   ├── login.css
│   └── signup.css
└── templates
    ├── home.html
    ├── login.html
    └── signup.html
```


+ app.py: The main Flask application file that serves the templates and API endpoints.
+ requirements.txt: Contains the list of Python dependencies required for the project.
+ setup.sh: A shell script to set up and manage the project environment.
+ static/: Contains the CSS files for styling the HTML templates.
+ templates/: Contains the HTML templates for the project (home, login, and signup pages).

### How to Use the Project

#### Step 1: Setup Environment

+ To set up the project environment, run the following command:
```bash
    source setup.sh
```

+ This script will:
    + Initialize a virtual environment.
    + Install required dependencies from requirements.txt.
    + Activate the virtual environment.

#### Step 2: Running the Project

+ To start the project, ensure the virtual environment is active and then start the Flask application run the following command:

```bash
    run
```
+ After starting the project, navigate to http://127.0.0.1:5000 in your web browser to access the application.
#### Step 3: Exiting the Environment

+ To clean up and deactivate the virtual environment, use the following command:

```bash
    clean && out
```

### Additional Setup Script Commands

+ `install package_name` : Install additional Python packages and update requirements.txt.
+ `run` : Start the Flask application (shortcut for running the app).
+ `freeze` : Update requirements.txt with the current environment dependencies.
+ `clean` : Remove temporary files, the virtual environment, and database files.

### Features

+ Signup Page: Allows users to create an account.
+ Login Page: Allows users to log into their account.
+ Home Page: Displays a list of news articles fetched from the /news API endpoint.

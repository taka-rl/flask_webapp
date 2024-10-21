# About
This is a Flask web app example where I have been utilizing gained skills and knowledge in Flask, sqlalchemy, RESTful API and Python while learning them by myself.

## Stacked tech
- Python
- Flask
- HTML/CSS/Bootstrap
- Flask-WTF/WTForm
- sqlalchemy
- PosgreSQL (for deploy)
- Flask-Login
- Jinja


## Preparation to use
1. Make sure the config_name as an argument of create_app function in main.py  
      ```app = create_app(config_name='development')```  
   Since it is still under development, 'production' has not been supported yet.

2. Run the following command for the libraries:  
   On Windows type:
   ```python -m pip install -r requirements.txt```  
   On MacOS type:
   ```pip3 install -r requirements.txt```

3. Create API Keys if you would like to use "Useful Information function" in the useful_info.html.  
   OpenWeather API: https://openweathermap.org/api  
   ExchangeRate API: https://www.exchangerate-api.com/

4. Get an App password on Google if you would like to use email sender function in contact.html  
   How to create App password → https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237?hl=ja

5. Create .env file including the following variables:
   ```
   SECRET_KEY=Type Your Secret Key  # Flask Secret Key
   WEATHER_API_KEY = 'Replace Your API Key set at 2'  # OpenWeather API
   ExchangeRate_API_KEY = 'Replace Your API Key set at 2'  # ExchangeRate API
   MYEMAIL = 'Your Email Address set at 3'  
   EMAIL_PASSWORD = 'App Password set at 3'
   SUPER_ADMIN = 'admin@email.com'  # The SUPER_ADMIN is the one that can change user's role such as admin and user and delete users.
   ```
6. Run main.py
7. Use one of the accounts written as below to Login
   - Super admin user:  
      email: admin@email.com  
      password: admin  
   - user:     
      email:test@email.com  
      password: test@email.com
8. Register a new user

9. Change user's role and delete registered users on ('/admin-dashboard') route.

## Design
### Directory structure
    ├── .github                 # GitHub actions
    ├── instance                # database file
    ├── static                  # static files
    │   ├── assets              # img files
    │   ├── css                 # css file related to bootstrap
    │   ├── js                  # js file related to bootstrap
    │   └── translations        # language json files
    ├── templates               # route html files
    ├── tests                   # tests
    │   ├── conftest.py         # set up for testing
    │   ├── parameters.py       # parameters for test
    │   ├── test_about.py       # test for about route
    │   ├── test_admin.py       # test for admin route
    │   ├── test_auth.py        # test for auth route
    │   ├── test_blog.py        # test for blog route
    │   ├── test_collection.py  # test for collection route
    │   ├── test_contact.py     # test for contact route
    │   ├── test_error.py       # test for error route
    │   └── test_useful_info.py # test for useful_info route
    ├── flask_app               
    │   ├── __init__.py         # Initialize Flask app and extensions
    │   ├── forms.py            # Forms
    │   ├── models.py           # Database models
    │   ├── utils.py            # Utility functions such as decorators, email sender
    │   └── route               
    │       ├── about.py        # About-related routes
    │       ├── auth.py         # Auth-related routes
    │       ├── blog.py         # Blog-related routes
    │       ├── collection.py   # Collection-related routes
    │       ├── contact.py      # Contact-related routes
    │       ├── others.py       # Other (language switcher)
    │       ├── admin.py        # Admin routes
    │       └── useful_info.py  # Useful_info-related routes
    ├── main.py                 # Run the app
    ├── .gitignore
    ├── Procfile                 
    ├── requirements.txt
    └── README.md

### Database
The ERD is as follows:  
![image](https://github.com/user-attachments/assets/9d89c929-c464-4739-babe-ab8b95710c22)


### User Role
There are three roles:  
Super admin:
- It is the one set the email on .env file as "SUPER_ADMIN".
- It can switch user's role such as admin and user and delete users on ('/admin-dashboard') route.
- It also contains admin features.  

Admin:
- It can post a new post/place, edit a post/place and delete a post/place.
- It can comment on posts.

User: 
- When you register, the user role is user.
- It can see the web page
- It can comment on posts.


## Finished development:  
- Store my favorite cafes in the database(SQLAlchemy)
- Show you the weather information through OpenWeather API
- Get the currency exchange rate between JPY and HUF through ExchangeRate API
- Add pages such as Blog posts, hobby, contact, about, register/login/logout
- Show some posts/create a post
- Add register/login/logout function
- Design database considering Place, BlogPost, User and Comment
- Add user authentication function for adding/editing/deleting places (only admin can)
- Add a send_email function in the contact.html
- Add a language switcher
- Organize main.py (See Directory structure)
- Add Error handling
- Add functions to change user role and delete users by admin
 
## Current development
- Testing
- Documentation
- Add github actions, which is python-app.yml to execute pytest

## Future development:
- Improve the web page design
- CI/CD pipelines
- Introduce a chatbot
- Deploy the web page


## Testing
pytest-flask is used for testing. All the test files are stored in the tests folder.  
Testing is connect to GitHub actions and tests are executed when commit or pull request happen.  
GitHub actions is still under development because of some errors. 

### How to run testing on your local environment
1. run this command in the terminal: ```python -m pytest```  
   If you would like to see more details on the tests: ```python -m pytest -v```  

Here is the executed result of ```python -m pytest``` .
```
PS C:\folder path\flask_webapp> python -m pytest
========================================================================================================= test session starts =========================================================================================================
platform win32 -- Python 3.10.11, pytest-8.3.3, pluggy-1.5.0
rootdir: C:\folder path\flask_webapp
plugins: anyio-4.6.0, flask-1.3.0
collected 24 items                                                                                                                                                                                                                     

tests\test_about.py .                                                                                                                                                                                                            [  4%]
tests\test_admin.py ....                                                                                                                                                                                                         [ 20%]
tests\test_auth.py ......                                                                                                                                                                                                        [ 45%]
tests\test_blog.py ....                                                                                                                                                                                                          [ 62%]
tests\test_collection.py ....                                                                                                                                                                                                    [ 79%]
tests\test_contact.py .                                                                                                                                                                                                          [ 83%]
tests\test_useful_info.py .                                                                                                                                                                                                      [100%] 
''''
========================================================================================================== warnings summary =========================================================================================================== 

=================================================================================================== 24 passed, 2 warnings in 6.34s ==================================================================================================== 
```


Here is the executed result of ```python -m pytest -v``` .
```
========================================================================================================= test session starts =========================================================================================================
platform win32 -- Python 3.10.11, pytest-8.3.3, pluggy-1.5.0 -- C:-----\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe
cachedir: .pytest_cache
rootdir: C:\folder path\flask_webapp
plugins: anyio-4.6.0, flask-1.3.0
collected 24 items                                                                                                                                                                                                                     

tests/test_about.py::test_about_access PASSED                                                                                                                                                                                    [  4%]
tests/test_admin.py::test_check_super_admin_exist PASSED                                                                                                                                                                         [  8%]
tests/test_admin.py::test_admin_dashboard_access PASSED                                                                                                                                                                          [ 12%]
tests/test_admin.py::test_change_user_role PASSED                                                                                                                                                                                [ 16%]
tests/test_admin.py::test_delete_user PASSED                                                                                                                                                                                     [ 20%]
tests/test_auth.py::test_register_page PASSED                                                                                                                                                                                    [ 25%]
tests/test_auth.py::test_register_form PASSED                                                                                                                                                                                    [ 29%]
tests/test_auth.py::test_duplicated_email_register PASSED                                                                                                                                                                        [ 33%]
tests/test_auth.py::test_login_page PASSED                                                                                                                                                                                       [ 37%]
tests/test_auth.py::test_login_form PASSED                                                                                                                                                                                       [ 41%]
tests/test_auth.py::test_logout PASSED                                                                                                                                                                                           [ 45%]
tests/test_blog.py::test_create_new_post PASSED                                                                                                                                                                                  [ 50%]
tests/test_blog.py::test_edit_post PASSED                                                                                                                                                                                        [ 54%]
tests/test_blog.py::test_delete_post PASSED                                                                                                                                                                                      [ 58%]
tests/test_blog.py::test_add_comment PASSED                                                                                                                                                                                      [ 62%]
tests/test_collection.py::test_access_collection_page PASSED                                                                                                                                                                     [ 66%]
tests/test_collection.py::test_add_place PASSED                                                                                                                                                                                  [ 70%]
tests/test_collection.py::test_edit_place PASSED                                                                                                                                                                                 [ 75%]
tests/test_collection.py::test_delete_place PASSED                                                                                                                                                                               [ 79%]
tests/test_contact.py::test_access_contact_page PASSED                                                                                                                                                                           [ 83%]
tests/test_error.py::test_500_page PASSED                                                                                                                                                                                        [ 87%]
tests/test_error.py::test_404_page PASSED                                                                                                                                                                                        [ 91%]
tests/test_useful_info.py::test_access_useful_info_page PASSED                                                                                                                                                                   [100%] 

========================================================================================================== warnings summary =========================================================================================================== 

=================================================================================================== 24 passed, 2 warnings in 6.46s ==================================================================================================== 
```
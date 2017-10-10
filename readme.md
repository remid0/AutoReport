App Server:
Go to the "Server" folder
    - Create a virtual environnement : mkvirtualenv --python=python3 testenv
    - Install dependencies : pip install -r requirements.txt
    - Setup th database : ./manage.py migrate
    - Create a superuser to administrate the server : ./manage.py createsuperuser
    - Run the Server ./manage.py runserver
    - Access to the admin page : http://localhost:8000/admin/

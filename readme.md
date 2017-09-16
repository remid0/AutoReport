
For the server side:
    Go to the "Server" folder
    I highly encourage to use a virtual env.
    Whith virtualenvwrapper, you can use:
        mkvirtualenv --python=python3 testenv

    To install the project : 
    pip3 install requirements.txt
        ./manage.py migrate
        ./manage.py createsuperuser
        ./manage.py runserver

    Then you can go to the admin page :
        http://localhost:8000/admin/

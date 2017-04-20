# Instatllation
```sh
# Go to the project root.
# Use a python virtual env or work on global env.

# For virtual env:
$ pip install -r requirements.txt

# For global env:
$ sudo pip install -r requirements.txt

# Make makemigrations
$ python manage.py makemigrations

# Migrate them to sqlite3
$ python manage.py migrate

# Create a superuser/admin
$ python manage.py createsuperuser

# run the server
$ python manage.py runserver
```

Visit http://localhost:8000 with browser.
Signup for accounts, you can also login using the admin credentials.  
Add codechef or Quora usernames to get the account data, data is retrived using web scrapping.
Admin can see the stats page which shows all the User details ranked.

Visit http://localhost:8000/admin/ and login with the admin credentials, to see the admin panel from where all the models can be managed.

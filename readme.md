# PyPresents

This app was written to allow randomize a receiver of Xmass gift in my family :)
Everybody can log in using users created in admin panel, describe the present they want to find under the Christmass tree,
and draw another family member to buy gift for. <br>
Basically it is e-letter for Santa :)

# Running app
0) Ensure python 3.4 is installed and used as interpreter
1) Download source code
2) Create migrations and migrate db (uses sqlite)

```
python manage.py makemigrations
python manage.py migrate
```

3) Create superuser
```
python manage.py createsuperuser
```

4) Install requirements
```
pip install -r requirements.txt
```

5. Run server
```
python manage.py runserver
```

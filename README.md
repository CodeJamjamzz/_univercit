Create venv
```
python -m venv venv
```
Install libraries
```
pip install -r requirements.txt
```

Database name: **univercit**
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'univercit',
        'USER': {username},
        'PASSWORD': {password},
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'init_command': "SET SQL_MODE='STRICT_TRANS_TABLES'"},
    }
}
```

Create branch on each app <3

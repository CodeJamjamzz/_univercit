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

# How to add tailwind and Daisy UI library

Clone the repository
```
git clone https://github.com/Smoll05/CSIT321_F1-UniverCIT.git
```

In the root directory **CSIT321_F1-UniverCIT**> input below in the terminal to install node packages
```
npm install
```
After the install the tailwind library
```
npm install tailwindcss @tailwindcss/cli
```
After installling the tailwind library install Daisy UI
```
npm i -D daisyui@latest
```
After that create a directory and a css file in the directory if it still does not exist <br> ->
``univercit/static/css/src/input.css`` <br>
Copy this and paste inside input.css
```
@import "tailwindcss";
@plugin "daisyui";
```
Put this code inside the ``package.json`` file
```
"scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "watch": "tailwindcss -i ./univercit/static/css/src/input.css -o ./univercit/static/css/src/output.css --watch"
},
```
Put this in ``univercit/settings.py`` - needed so that when you put ``{% load static %}`` in the html file it will know that the css is in the ``univercit/static/css/src/input.css``
```
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```
When you create an HTML file put this in the head tag
```
{% load static %}
<link href="{% static 'css/src/output.css' %}" rel="stylesheet" type="text/css" />
```
After that you can then type this in the terminal to run the tailwind
```
npm run watch
```
You will get a response like this
```
> djangotailwind@1.0.0 watch
> tailwindcss -i ./myapp/static/css/src/input.css -o ./myapp/static/css/src/output.css --watch

≈ tailwindcss v4.1.14

/*! 🌼 daisyUI 5.3.7 */
```
This means that tailwind and daisyUI is now ready. <br><br>
After that create another terminal, then run django
```
py manage.py runserver
```
Violaaaa magic!
# ReactBlog

This is a simple blog-like app built with Flask (as backend) and React.js (as frontend).

The main target of this app is to learn the basics of these two frameworks.

## Requirements

The only requirements are **Python** and **Pip**

## Install


```
# If you want a virtualenv
mkvirtualenv -a `pwd` -r requirements.txt flask
# otherwise
pip install -r requirements.txt
```

## Run the server

```
python server.py
```

At the first run a new SQLite db is created (file `test.db`).

## Enjoy!

Edit `server.py` to play with Flask and `static/scripts/app.js` to play with React.js

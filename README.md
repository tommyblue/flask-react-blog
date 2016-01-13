# ReactBlog

This is a simple blog-like app built with Flask (as backend) and React.js (as frontend).

The main target of this app is to learn the basics of these two frameworks.

## Docker

A `Dockerfile` is ready to build a docker image. The current folder is linked
with it so you can edit local files and the docker image will update automatically.

To use the docker image you only need to have docker installed locally, then type:

```
docker build -t tommyblue/react-blog .
docker run --name react-pg -d postgres
docker run -d -p 3500:3500 -v `pwd`:/srv:ro --name react-blog --link react-pg:postgres tommyblue/react-blog python /srv/server.py
```

You can verify that the container is running (and that it's using the right port) with `docker ps -l`.

Connect to the app pointing your browser to `http://localhost:3500/`

**Note:**

If you want to protect the access to the database with a password, use this:

```
docker run --name react-pg -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
The app will automatically use it.

## Manual install

### Requirements

The only requirements are **Python** and **Pip**

### Install


```
# If you want a virtualenv
mkvirtualenv -a `pwd` -r requirements.txt flask
# otherwise
pip install -r requirements.txt
```

### Run the server

```
python server.py
```

At the first run a new SQLite db is created (file `test.db`).

## Enjoy!

Edit `server.py` to play with Flask and `static/scripts/app.js` to play with React.js

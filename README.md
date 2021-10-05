# Scoreboard API

A RESTful API to manage a scoreboard for a particular tournament.

![Python Version](https://img.shields.io/badge/python-3.9.7-blue.svg)

### Deploy on Heroku

[![Heroku](https://img.shields.io/badge/heroku-blue.svg)](https://heroku.com/deploy)

### Environment Variables:

* `SECRET`: The secret key to generate hashes. Get one using:

```shell
openssl rand -hex 32
```

* `DATABASE_URL`: The URL of relational database. (Automatic for Heroku)

Async, non-blocking Flask & SQLAlchemy example
==============================================

## Overview

This code shows how to use the following menagerie of compontents
together in a completely non-blocking manner:

* [Flask](http://flask.pocoo.org/), for the web application framework;
* [SQLAlchemy](http://www.sqlalchemy.org/), for the object relational mapper (via [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy));
* [Postgresql](http://www.postgresql.org/), for the database;
* [Psycopg2](http://initd.org/psycopg/), for the SQLAlchemy-Postgresql adapter;
* [Gunicorn](http://gunicorn.org/), for the WSGI server; and,
* [Gevent](http://www.gevent.org/), for the networking library.

The file `server.py` defines a small Flask application that has
two routes: one that triggers a `time.sleep(5)` in Python and one that
triggers a `pg_sleep(5)` in Postgres.  Both of these sleeps are normally
blocking operations.  By running the server using the Gevent
worker for Gunicorn, we can make the Python sleep non-blocking.
By configuring Psycopg2's co-routine support (via
[psycogreen](https://bitbucket.org/dvarrazzo/psycogreen)) we 
can make the Postgres sleep non-blocking.


## Installation

Clone the repo:

	git clone https://github.com/kljensen/async-flask-sqlalchemy-example.git

Install the requirements

	pip install -r requirements.txt

Make sure you've got the required database

	createdb fsppgg_test

Create the required tables in this database

	python ./server.py -c


## Running the code

You can test three situations with this code:
 * Gunicorn blocking with SQLAlchemy/Psycopg2 blocking;
 * Gunicorn non-blocking with SQLAlchemy/Psycopg2 blocking; and,
 * Gunicorn non-blocking with SQLAlchemy/Psycopg2 non-blocking.

### Gunicorn blocking with SQLAlchemy blocking

Run the server (which is the Flask application) like

	gunicorn server:app

Then, in a separate shell, run the client like

	python ./client.py

You should see output like

	Sending 5 requests for http://localhost:8000/sleep/python/...
		@  5.05s got response [200]
		@ 10.05s got response [200]
		@ 15.07s got response [200]
		@ 20.07s got response [200]
		@ 25.08s got response [200]
		= 25.09s TOTAL
	Sending 5 requests for http://localhost:8000/sleep/postgres/...
		@  5.02s got response [200]
		@ 10.02s got response [200]
		@ 15.03s got response [200]
		@ 20.04s got response [200]
		@ 25.05s got response [200]
		= 25.05s TOTAL
	------------------------------------------
	SUM TOTAL = 50.15s


### Gunicorn non-blocking with SQLAlchemy blocking

Run the server like

	gunicorn server:app -k gevent

and run the client again.   You should see output like

	Sending 5 requests for http://localhost:8000/sleep/python/...
		@  5.05s got response [200]
		@  5.06s got response [200]
		@  5.06s got response [200]
		@  5.06s got response [200]
		@  5.07s got response [200]
		=  5.08s TOTAL
	Sending 5 requests for http://localhost:8000/sleep/postgres/...
		@  5.01s got response [200]
		@ 10.02s got response [200]
		@ 15.04s got response [200]
		@ 20.05s got response [200]
		@ 25.06s got response [200]
		= 25.06s TOTAL
	------------------------------------------
	SUM TOTAL = 30.14s
	 

### Gunicorn non-blocking with SQLAlchemy non-blocking

Run the server like

	PSYCOGREEN=true gunicorn server:app  -k gevent 

and run the client again.   You should see output like

	Sending 5 requests for http://localhost:8000/sleep/python/...
		@  5.03s got response [200]
		@  5.03s got response [200]
		@  5.03s got response [200]
		@  5.04s got response [200]
		@  5.03s got response [200]
		=  5.04s TOTAL
	Sending 5 requests for http://localhost:8000/sleep/postgres/...
		@  5.02s got response [200]
		@  5.03s got response [200]
		@  5.03s got response [200]
		@  5.03s got response [200]
		@  5.03s got response [200]
		=  5.03s TOTAL
	------------------------------------------
	SUM TOTAL = 10.07s


## Results

Stuff gets faster, shizzle works fine.  Your mileage may vary in production.  


## License (MIT)

Copyright (c) 2013 Kyle L. Jensen (kljensen@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
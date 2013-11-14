bitcoin_eshop
=============

Simple bitcoin eshop. Does not use private keys.

Prerequisites
* Installed Python and Virtualenv, see http://docs.python-guide.org/en/latest/starting/install/linux/

Install
* clone rep `git clone git@github.com:davidbarton/bitcoin_eshop.git` and cd `cd bitcoin_eshop`
* build local environment `virtualenv venv --distribute`
* use app context `source venv/bin/activate`
* install dependencies `pip install -r requirements.txt`
* create dev database dir `mkdir -p bitcoin_eshop/db` and file `touch bitcoin_eshop/db/development.db`
* create db tables and superuser`python manage.py syncdb`
* start server `python manage.py runserver`

Database migration [South]
* see [The Basics](http://south.readthedocs.org/en/0.7.6/tutorial/part1.html) and [Converting An App](http://south.readthedocs.org/en/0.7.6/convertinganapp.html)

Dev database data
* open and login at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* insert master public keys and products
* dev product image: [http://www.freegreatpicture.com/files/104/20309-christmas-food.jpg](http://www.freegreatpicture.com/files/104/20309-christmas-food.jpg)

bitcoin_eshop
=============

Simple bitcoin eshop. Does not use private keys.

Prerequisites
* Installed Python and Virtualenv, see http://docs.python-guide.org/en/latest/starting/install/linux/
* ???

Install

```
git clone git@github.com:davidbarton/bitcoin_eshop.git
cd bitcoin_eshop
virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
mkdir -p bitcoin_eshop/db
touch bitcoin_eshop/db/development.db
python manage.py syncdb
python manage.py runserver
```

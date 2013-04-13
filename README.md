bitcoin_eshop
=============

Simple bitcoin eshop. Does not use private keys.

Prerequisites
* Installed Python and Virtualenv, see http://docs.python-guide.org/en/latest/starting/install/linux/

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

start python shell
```
python manage.py shell
```
type commands
```
from web.models import *
k = MasterPublicKeys(master_public_key="YOUR_MASTER_PUBLIC_KEY")
k.save()
p1 = Products(title="chleba",img="http://www.freegreatpicture.com/files/104/20309-christmas-food.jpg",base_price="3",stock=10,master_public_key=k)
p2 = Products(title="pastika",img="http://www.freegreatpicture.com/files/104/20309-christmas-food.jpg",base_price="3.5",stock=15,master_public_key=k)
p3 = Products(title="pivo",img="http://www.freegreatpicture.com/files/104/20309-christmas-food.jpg",base_price="4",stock=30,master_public_key=k)
p1.save()
p2.save()
p3.save()
```

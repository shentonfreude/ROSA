=========
 Install
=========

Checkout code::

  git clone git@github.com:shentonfreude/ROSA.git
  cd ROSA.git

Virtualenv::

  /usr/local/python/2.7.2/bin/virtualenv --distribute .
  source bin/activate

Install::

  pip install -r requirements.txt

Setup DB::

  python rosa/manage.py syncdb

Run::

  python rosa/manage.py runserver

You should get a nice view but no data. 

See the 'import' doc for info on how to populate the data from
production ROSA.





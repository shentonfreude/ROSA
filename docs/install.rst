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

You should get a nice view but there's no data yet.

You can use the sanitized data by loading the fixture::

  python rosa/manage.py loaddata fixtures/application.json.gz

Or see the 'import' doc for info on how to populate the data from
production ROSA.







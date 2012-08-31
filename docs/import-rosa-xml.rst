==================
 Import ROSA Data
==================

Prodution ROSA XML
==================

ROSA developers added an XML export so that BIANCA could retrieve and
process data.

Go to the URL:

https://merope.hq.nasa.gov/rosa/ws/hdmsrosa/all/main/RosaExportXml

I click Token login, then give my username and pin+token code.

It will deliver you to a differnet page; enter the same URL again.

The file should download in about 3 minutes and at this writing is 21.5 MB.

Convert to JSON
===============

TBD: see the rosa/application/rosa_parse.py file


Importing JSON into Django ROSA
===============================

We have to dork with directories and Django enviornment to pull this
off, I'm sure there's a better way. 

Change into the dir that has the rosa_import.py::

  cd rosa

Set an environment variable so Django can find settings.py::

  export DJANGO_SETTINGS_MODULE=settings

Run the importer, specifying the path to the JSON file::

  ./rosa_import.py ~/Dropbox/rosaExport.json  

This took a few minutes on my laptop; it displays apps and percent
progress as it imports.

You can run it from here with::

  ./manage.py runserver


Sanitizing Data
===============

If you need to sanitize the data, you can use the `lorem-rosa.sh`
script in the top-level of this distribution. It depends on the Lorem
tool from https://github.com/koansys/lorem

You will have to set the PATH to include whereever you downloaded Lorem.

posterwall
==========

Development
-----------
Get ready:

    mkvirtualenv -p `python3` posterwall
    sudo apt-get install libjpeg-dev
    pip install -r requirements/dev.txt
    npm install
    bower install
    grunt build

Link up your front+backend:

    util/bootstrap.sh

Then in one tab spin up the frontend workflow:

    grunt serve

And in another the backend workflow:

    ./manage.py runserver_plus


Production
----------
Everything the same, except:

    pip install -r requirements/prod.txt
    util/boostrap.sh prod

Or use the prod brunch:

    grunt publish
    cd prod
    git checkout prod
    ./manage.py runserver

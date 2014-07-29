Google Proxy
============

Installation - Application
--------------------------

Using a separate unprivileged user for running the application:

1. Create the new user::

    # useradd -m bpa

2. Install required packages (fabric, rsync, virtualenv)::

    # apt-get install fabric rsync virtualenv

3. Create an SSH key for your account, if you don't already have one.
   Then add this key to ``bpa``'s list of authorized keys.

4. Setup deployment tree::

    $ fab venv setup

5. Deploy::

    $ fab venv deploy

6. Start the application:

    $ fab venv restart

7. Install nginx::

    $ apt-get install nginx

8. Copy or merge supplied ``google-proxy-nginx.conf`` into your
   nginx configuration::

    # cp /path/to/google-proxy-nginx.conf /etc/nginx/sites-available
    # ln -s ../sites-available/google-proxy-nginx.conf /etc/nginx/sites-enabled

9. Restart nginx::

    # /etc/init.d/nginx reload

10. Add ``gs`` to ``/etc/hosts``::

    # vi /etc/hosts

If you now go to http://gs you should see Google's adjusted home page.


Installation - Firefox/Iceweasel
--------------------------------

Use supplied ``adjust-firefox-search-engine.py`` script to modify
Firefox or Iceweasel to use google proxy.

1. Install lxml::

    # apt-get install python-lxml

2. Find out where your search plugins are installed::

    $ dpkg -L iceweasel |grep searchplugins

   If the above command produces no results, try a less restrictive
   spelling::

    $ dpkg -L iceweasel |grep search

3. Use the script to adjust google search plugin::

    $ python adjust-firefox-search-engine.py /etc/iceweasel/searchplugins/locale/en-US/google.xml > /tmp/adjusted
    # mv /tmp/adjusted /etc/iceweasel/searchplugins/locale/en-US/google.xml

4. Delete cached search configuration::

    $ rm ~/.mozilla/**/search.json

5. Restart Firefox/Iceweasel.

Searching via google should now use google proxy.

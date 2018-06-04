# Linux Server Configuration  
A custom Flask application that stores and displays a variety of video games with assorted categories. Includes functionality to create, edit, and delete games, along with user login and authentication.  
[View Item Catalog Web App](http://lightsail.melvin.io/)  
[View setup guide](GUIDE.md)

### Amazon Lightsail  
**IP:** 35.182.139.132  
**Domain Name:** lightsail.melvin.io  
**SSH Port:** 2200  
**Item Catalog**: http://lightsail.melvin.io/  
**SSH User:** grader *(SSH key only)*  
**SSH Password:** udacityudacity *(SSH key only)*  
**PostgreSQL User**: catalog *(local only)*  
**PostgreSQL Password**: I8vke78B9a *(local only)*  

### Installed Software  
* apache2  
* libapache2-mod-wsgi  
* postgresql  
* python-psycopg2  
* python-flask  
* python-sqalchemy  
* python-pip  

### Other Changes  
* Adjusted UFW to only accept incoming connections on ports 80, 123, and 2200  
* Changed default SSH port to 2200
* Created `grader` user account with SSH key, to be provided in project submission notes  
* Set default timezone to `UTC`  
* Changed SQLite database to PostgreSQL (`postgresql://user:password@localhost/database')` in `database_setup.py`, `lotsofgames.py`, and `__init__.py`
* Updated `client_secrets.json` path to `/var/www/UdacityItemCatalog` in `__init__.py`
* Updated packages with `apt-get update`, `apt-get upgrade`, and `apt-get dist-upgrade`

### Credits
* https://github.com/hicham-alaoui/ha-linux-server-config/
* https://github.com/callforsky/udacity-linux-configuration
* https://github.com/petergns/linux_server_catalog

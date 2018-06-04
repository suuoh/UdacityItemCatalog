# Udacity Linux Server Configuration Guide
### This guide is from @hicham-alaoui. [Link to original guide.](https://github.com/hicham-alaoui/ha-linux-server-config)


## Step A: The Lightsail instance  
### 1. Create a Lightsail instance in AWS
* Click on the “Services” link in the top navbar
* Under the “Compute section, select Lightsail
* Inside the Lightsail page, click on “Create instance” page
* Under “Select Blueprint” section click on “OS Only”
* Select “Ubuntu”
* Select a plan. Usually the first basic plan, free for the first month then $5 afterwards
* Under “Name your instance”, rename your instance if you wish to
* Click the “Create” button. The instance will take few moments to appear on the instances page  
### 2. Download the Lightsail default private key to local device
* In the instances page click on the instance name to open the settings page.
* Scroll all the way down to the bottom of the page and click on the blue “Account page” link
* Click on “download” at the bottom of the page, name and save the file on your local device then ssh into your Lightsail server : sudo ssh ubuntu@35.178.90.82 -i lightsail_key.pem)  
### 3. Add ports 2200/tcp and 123/udp
* On your instance page click on the “Networking” tab,
* Under “Firewall” section, click on “+Add another” at the bottom of the ports list,
* Add ports as follow: Custom: TCP:2200, and Custom:UDP:123. (after adding these two ports the list should include at least four ports, 22, 80, 2200, and 123)
* Click “Save”

### 4. Update your Linux server
* Connect to the linux server via either the Lightsail page ssh connect link or local gitbash as explained above. 
* Update server packages using the command: $ sudo apt-get update
* Upgrade the packages: $ sudo apt-get upgrade
* Remove un-used packages: $ sudo apt-get autoremove
* enable unattended updates: $ sudo apt install unattended-upgrades
* You can also install the user identifier package “finger” : $ sudo apt-get install finger

### 5. Change ssh port from 22 to 2200
* Open the sshd_config file: $ sudo nano /etc/ssh/ssdh_config
* Change the ssh port from 22 to 2200
* Save the change
* Restart the ssh service: $ sudo sevice ssh restart 

### 6. Update ufw ports and status
* Allow the new port 2200: $ sudo ufw allow 2200/tcp
* Allow existing port 22: $ sudo ufw allow 80/tcp
* All UDP port 123: $ sudo ufw allow 123/udp
* Check if the ufw is active. If not, do so using the command: $ sudo ufw enable
* Restart the ssh service: $ sudo service ssh restart

### 7. Configure the local timezone to UTC
* Configure the time zone: $ sudo dpkg-reconfigure tzdata

===========================================================================

## Step B: The “grader” user
### 1. Create the grader user
* Switch role to root using the command: sudo su -
* Create the grader user: sudo adduser grader
* Assign sudo status to grader: $ sudo nano /etc/sudoers.d/grader, and type grader ALL=(ALL:ALL) ALL.


### 2. Create a keypair for grader user
* ssh into the grader user account: $ ssh grader@35.178.90.82 -p 2200 (plus password if any)
* Create a directory .ssh: $ sudo mkdir .ssh
* Create a file with the name authorized_keys inside the .ssh directory: $ sudo touch /.ssh/authorized_keys.
* Change the permission for the .ssh folder: $ sudo chmod 700 .ssh
* Change the permissions for the authorized_keys file: $ sudo chmod 644 /.ssh/authorized_keys
* Open a new gitbash window on your device and type the command: $ ssh-keygen
* Create the file in which to save the key (/c/Users/Hicham/.ssh/id_rsa): c/Users/Hicham/.ssh/authorized_keys
* The command will create two files in the specified directory. Open the one with the extension PUB using the command: $ sudo cat ~/.ssh/authorized_keys.pub
* Copy the content
* Open the authorized_keys file created for the grader user: $ sudo nano /.ssh/authorized_keys
* Paste the content
* Reopen the sshd_config file (sudo nano /etc/ssh/sshd_config) and change password authentication from “yes” to “no”.

### 3. Change PermitRootLogin property property
* Change the PermitRootLogin property to "no" in the sshd_config file: $ sudo /etc/ssh/sshd_config

### 4. Restart the ssh service
* Restart the ssh service: $ sudo service ssh restart 

===========================================================================

## Step C: Apache2, mod-wsgi, and Git
### 1. Install Apache2
* Connect to your instance with the grader account: $ ssh grader@35.178.90.82 -p 2200 -i ~/.ssh/authorized_keys
* Install apache2: $ sudo apt-get install apache2.

### 2. Add mod-wsgi for python environment
* use the command: $ sudo apt-get install libapache2-mod-wsgi python-dev
### 3. Install git 
* Install git: $ sudo apt-get install git

===========================================================================

## Step D: Clone the app into Apache2
### 1. Clone the catalog app (properties app in this example) 
* Create a new folder under the /www directory: $ sudo mkdir FlaskApp
* cd into the new FlaskApp directory: $ cd /var/www/FlaskApp
* Clone you catalog app with the new name "FlaskApp": $ sudo git clone[ https://github.com/hicham-alaoui/properties-catalog.git](http://github.com) FlaskApp. The path to the catalog app should be:/var/www/FlaskApp/FlaskApp. 

### 2. Add the packages used in your app to enable them inside the new environment
* Install pip: $ sudo apt-get install python-pip.
* Install Flask and the rest of the packages
*$ sudo apt-get install python-pip
* $ sudo pip install Flask
* $ sudo pip install httplib2
* $ sudo pip install sqlalchemy
* $ sudo pip install oauth2client
* $ sudo pip install --upgrade oauth2client
* $ sudo pip install sqlalchemy
* $ sudo pip install sqlalchemy_utils
* $ sudo pip install requests
* $ sudo pip install render_template
* $ sudo pip install redirect  
The above list is not exhaustive and varies from one project to the other

### 3. Rename and edit the application python file
* Rename the cloned application python file from its current name(e.g., project.py or catalog.py)  to __init__py
* In the __init__.py edit the client_secrects.json file path to : /var/www/FlaskApp/FlaskApp/client_secrets.json 

### 4. Set up the database  
* Install PostgreSQL : $ sudo apt-get install postgresql
* Check if no remote connections are allowed:  sudo nano /etc/postgresql/9.5/main/pg_hba.conf
* Login as user "postgres": $ sudo su - postgres
* Get into postgreSQL shell: psql
* Create a new database named "catalog" and create a new user named "catalog" in postgreSQL shell: postgres=# CREATE DATABASE catalog;
* postgres=# CREATE USER catalog
* Set a password for user catalog: postgres=# ALTER ROLE catalog WITH PASSWORD 'password'
* Give user "catalog" permission to "catalog" application database: postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog
* Quit postgreSQL: postgres=# \q
* Exit from user "postgres": exit
* Change the path to the database in the `__init__.py` and the database_setup.py (properties_db.py in this project) files to : create_engine('postgresql://catalog:password@localhost/catalog')
* Install psycopg2: sudo apt-get -qqy install postgresql python-psycopg2
* Create database schema: sudo python database_setup.py

===========================================================================

## Final step: Fire the app to the web
### 1. Create a new Virtual Host
* Create the FlaskApp.conf file: $ sudo nano /etc/apache2/sites-available/FlaskApp.conf
* Paste the text below inside the FlaskApp.conf file:  

	```  
	<VirtualHost *:80>  
		ServerName 35.178.90.82 
		ServerAdmin [ha@mail.com](mail.com)  
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi  
		<Directory /var/www/FlaskApp/FlaskApp/>  
			Order allow,deny  
			Allow from all  
		</Directory>  
		Alias /static /var/www/FlaskApp/FlaskApp/static  
		<Directory /var/www/FlaskApp/FlaskApp/static/>  
			Order allow,deny  
			Allow from all  
		</Directory>  
		ErrorLog ${APACHE_LOG_DIR}/error.log  
		LogLevel warn  
		CustomLog ${APACHE_LOG_DIR}/access.log combined  
	</VirtualHost>  
	```  
	*Remember to change the ServerName and ServiceAdmin details to yours. 

* Disable the default virtual host:  $ sudo a2dissite 000-default.conf
* Enable the new virtual host: $ sudo a2ensite FlaskApp.conf

### 2. Create a wsgi file for the app. 
* The wsgi file sits inside the parent FlaskApp directory: $ sudo nano /var/www/FlaskApp/flaskapp.wsgi
* Paste the text below inside the flaskapp.wsgi file:

	```  
	#!/usr/bin/python  
	import sys  
	import logging  
	logging.basicConfig(stream=sys.stderr)  
	sys.path.insert(0,"/var/www/FlaskApp/")  

	from FlaskApp import app as application  
	application.secret_key = 'Add your secret key'  
	```
### 3. Change the secret key credentials for Google sign in
* Get the Host Name for the public IP address (e.g., 35.178.90.82)
* Update the oauth2 credentials for the app in the Google Console
* Update the client_secrets.json file with the new “Authorised Javascript origins” and “Authorised redirect URIs” details

### 4. Restart the Apache server
* Start Apache2 service with the command: $ sudo service apache2 restart

### 5. Launch the app in the browser
* Use the Host Name address [http://ec2-35-178-90-82.eu-west-2.compute.amazonaws.com]( amazonaws.com) (not just the public IP e.g., 35.178.90.82).

## References:
* [https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps](https://www.digitalocean.com/)
* [https://github.com/kongling893/Linux-Server-Configuration-UDACITY](https://github.com)
* [https://stackoverflow.com/](https://stackoverflow.com)

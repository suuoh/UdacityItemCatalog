# Udacity Linux Server Configuration Guide
### Based on [this guide](https://github.com/hicham-alaoui/ha-linux-server-config) by [@hicham-alaoui](https://github.com/hicham-alaoui).
**NOTE:** Modified details to my situation and process, but did not change order of steps.

## Step A: The Lightsail instance  
### 1. Create a Lightsail instance in AWS
* Go to [Amazon Lightsail](https://lightsail.aws.amazon.com/ls/webapp)
* Inside the Lightsail page, click on “Create instance” page
* Under “Select Blueprint” section click on “OS Only” and select “Ubuntu”
* Select a plan. The first plan is free for the first month then $5 afterwards
* Click the “Create” button. The instance will take few moments to appear on the instances page  

### 2. Download the Lightsail default private key to local device
* On the dashboard, click on the instance name to open the settings page.
* Scroll all the way down to the bottom of the page and click on the blue “Account page” link
* Click on “download” at the bottom of the page, name and save the file on your local device
* SSH into your Lightsail server: `sudo ssh ubuntu@35.182.139.132 -i lightsail_key.pem` 

### 3. Add ports 2200/tcp and 123/udp
* On your instance page click on the “Networking” tab
* Under “Firewall” section, click on “Add another” at the bottom of the ports list
* Add ports as follow: Custom TCP 2200 and Custom UDP 123. (There should already be HTTP TCP 80 and SSH TCP 22)
* Click “Save”

### 4. Update your Linux server
* SSH into the server
* Update the packages list with `sudo apt-get update`
* Upgrade packages with `sudo apt-get upgrade` and `sudo apt-get dist-upgrade`
* Remove unused packages with `sudo apt-get autoremove`
* Enable unattended updates: `sudo apt install unattended-upgrades`

*Make a snapshot of the server, before changing the SSH and firewall settings.*

### 5. Change ssh port from 22 to 2200
* Open the sshd_config file with `sudo nano /etc/ssh/ssdh_config`
* Change the ssh port from 22 to 2200
* Save the change and restart the ssh service with `sudo sevice ssh restart`

### 6. Update UFW ports and status
* Block all incoming with `sudo ufw deny incoming`
* Allow all outgoing with `sudo ufw allow outgoing`
* Allow the new ssh port 2200 with `sudo ufw allow 2200/tcp`
* Delete existing ssh port with `sudo ufw delete allow 22/tcp`
* Allow http port with `sudo ufw allow 80/tcp`
* All UDP port 123 with `sudo ufw allow 123/udp`
* Enable UFW with `sudo ufw enable`
* Restart the ssh service with `sudo service ssh restart`

### 7. Configure the local timezone to UTC
* Change timezone with `sudo timedatectl set-timezone UTC`

===========================================================================

## Step B: The “grader” user
### 1. Create the grader user
* Create the grader user with `sudo adduser grader`
* Assign sudo status to grader with `sudo nano /etc/sudoers.d/grader`
* Enter `grader ALL=(ALL:ALL) ALL` and save the file

### 2. Create a keypair for grader user
* SSH into the grader user account with `ssh grader@35.182.139.132 -p 2200` (plus password if any)
* Create a directory .ssh with `sudo mkdir .ssh`
* Create a file with the name authorized_keys with `sudo touch /.ssh/authorized_keys`
* Change the permission for the .ssh folder with `sudo chmod 700 .ssh`
* Change the permissions for the authorized_keys file with `sudo chmod 644 /.ssh/authorized_keys`
* Open a new gitbash window on your device and generate a new key pair `ssh-keygen`
* Save the key to a file such as `/c/Users/Melvin/.ssh/lightsail_grader`
* The command will create two files in the specified directory.
* Open the one with the `.pub` extension with `sudo cat /c/Users/Melvin/.ssh/lightsail_grader.pub`
* Copy the content
* On the server, open the authorized_keys file for the grader user with `sudo nano /.ssh/authorized_keys`
* Paste the content and save

*Either make another snapshot at this point or try logging in with the key file first.*

### 3. Disable password authentication and remote root login
* Reopen the sshd_config file with `sudo nano /etc/ssh/sshd_config`
* Set `PasswordAuthentication no`
* Set `PermitRootLogin no`
* Restart the ssh service with `sudo service ssh restart`

===========================================================================

## Step C: Apache2, mod-wsgi, and Git
### 1. Install packages
* Connect as the grader account with `ssh grader@35.182.139.132 -p 2200 -i /c/Users/Melvin/.ssh/authorized_keys`
* Install apache2 with `sudo apt-get install apache2`
* Install wsgi and python with `sudo apt-get install libapache2-mod-wsgi python`
* Install git with `sudo apt-get install git`

===========================================================================

## Step D: Clone the item catalog app
### 1. Clone the repository
* cd into /var/www/ directory: `cd /var/www/`
* Clone the repository with `sudo git clone https://github.com/suuoh/UdacityItemCatalog [alternate name, if desired]`
* The path to the item catalog app should be `/var/www/UdacityItemCatalog`

### 2. Add the Python packages used in your app
* Install pip with `sudo apt-get install python-pip`
* Install Flask and the rest of the packages
* `sudo pip install Flask`
* `sudo pip install httplib2`
* `sudo pip install sqlalchemy`
* `sudo pip install psycopg2`
* `sudo pip install oauth2client`
* `sudo pip install --upgrade oauth2client`
* `sudo pip install sqlalchemy`
* `sudo pip install sqlalchemy_utils`
* `sudo pip install requests`
* `sudo pip install render_template`
* `sudo pip install redirect`
*The above list is not exhaustive and varies from one project to the other*

### 3. Rename and edit the application python file
* Rename the main application  file from its current name (e.g. application.py or catalog.py) to `__init__.py`
* In the `__init__.py`, edit the `client_secrects.json` file path to `/var/www/UdacityItemCatalog/client_secrets.json`

### 4. Set up the database  
* Install PostgreSQL with `sudo apt-get install postgresql`
* Check if no remote connections are allowed `sudo nano /etc/postgresql/9.5/main/pg_hba.conf`
* Login as the database user postgres with `sudo su - postgres`
* Get into PostgreSQL shell with `psql`
* Create a new "catalog" user with `CREATE USER catalog WITH PASSWORD [password];`
* Set permissions with `ALTER USER catalog CREATEDB;`
* Create a new "itemcatalog" database with `CREATE DATABASE itemcatalog WITH OWNER catalog;`
* Give user "catalog" permission to "itemcatalog" application database with `GRANT ALL PRIVILEGES ON DATABASE itemcatalog TO catalog;`
* Quit PostgreSQL with `\q`
* Exit the postgres user and switch back to your original user with `exit`
* Change the database path in `__init__.py`, `database_setup.py`, and `lotsofitems.py` to `create_engine('postgresql://catalog:password@localhost/itemcatalog')`
* Set up the database schema with `sudo python database_setup.py`
* Add initial items with `sudo python lotsofitems.py`

===========================================================================

## Step E: Configure the web app
### 1. Create a new Virtual Host
* Create the itemcatalog.conf file with `sudo nano /etc/apache2/sites-available/itemcatalog.conf`
* Paste the text below inside the itemcatalog.conf file:  
	```  
	<VirtualHost *:80>  
		ServerName 35.182.139.132
		ServerAlias [domain]
		ServerAdmin [email]
		WSGIDaemonProcess itemcatalog user=grader group=grader threads=5
		WSGIScriptAlias / /var/www/UdacityItemCatalog/itemcatalog.wsgi  
		<Directory /var/www/UdacityItemCatalog/>  
			Order allow,deny  
			Allow from all  
		</Directory>  
		Alias /static /var/www/UdacityItemCatalog/static  
		<Directory /var/www/UdacityItemCatalog/static/>  
			Order allow,deny  
			Allow from all  
		</Directory>  
		ErrorLog ${APACHE_LOG_DIR}/error.log  
		LogLevel warn  
		CustomLog ${APACHE_LOG_DIR}/access.log combined  
	</VirtualHost>  
	```  
	*Remember to change the ServerName, ServerAlias, and ServiceAdmin details to yours, as well as the paths.*

* Disable the default virtual host with `sudo a2dissite 000-default.conf`
* Enable the new virtual host `sudo a2ensite itemcatalog.conf`

### 2. Create a wsgi file for the app. 
* The wsgi file sits inside the parent directory: `sudo nano /var/www/UdacityItemCatalog/itemcatalog.wsgi`
* Paste the text below inside the itemcatalog.wsgi file:
	```  
	#!/usr/bin/python  
	import sys  
	import logging  
	logging.basicConfig(stream=sys.stderr)  
	sys.path.insert(0,"/var/www/")  

	from UdacityItemCatalog import app as application  
	application.secret_key = 'Add your secret key'  
	```
### 3. Change the secret key credentials for Google sign in
* Set up a domain for your Lightsail IP or reverse lookup the host name
* Go to the [Credentials section of the Google Developers Console](https://console.developers.google.com/apis/credentials)
* Update the `Authorised JavaScript origins` for the app
* `Authorised redirect URIs` is not used, but you can update it as well
* Update the `client_secrets.json` file with the new `Authorised Javascript origins` and `Authorised redirect URIs` details

### 4. Restart the Apache server
* Restart the Apache2 service with `sudo service apache2 restart`

### 5. Launch the app in the browser
* Visit your app using the domain name, not the IP Address

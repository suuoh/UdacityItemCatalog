# Linux Server Configuration 
A custom Flask application that stores and displays a variety of video games with assorted categories. Includes functionality to create, edit, and delete games, along with user login and authentication.  
[View Item Catalog Web App](http://lightsail.melvin.io/)  

### Amazon Lightsail
**IP:** 35.182.139.132  
**Domain Name:** lightsail.melvin.io
**SSH Port:** 2200
**Item Catalog**: http://lightsail.melvin.io/
**PostgreSQL User**: catalog

### Installed Software
* apache2
* libapache2-mod-wsgi
* postgresql

### Other Changes
* Adjusted UFW to only accept incoming connections on ports 80, 123, and 2200
* Created `grader` user account with SSH key, to be provided in project submission notes
* Set default timezone to `UTC`

**Deploying Flash + Gunicorn + Nginx + https + domain**

Created by Javier Ideami - March 2, 2020

**The jupyter notebook to train the model used by the flask app can be accessed here:**
[Jupyter Notebook to train the model with Fastai v2](https://github.com/javismiles/bear-detector-flask-deploy/blob/master/resources/model.ipynb)
![Image of cute bear](https://github.com/javismiles/bear-detector-flask-deploy/blob/master/resources/bears/cutebear.jpg?raw=true)

**The jupyter notebook to train the model used by the flask app can be accessed here:**
[Jupyter Notebook to train the model with Fastai v2](https://github.com/javismiles/bear-detector-flask-deploy/blob/master/resources/model.ipynb)


The objective of this project is to deploy a Flask app that uses a model trained with the Fast.ai v2 library following an example in the upcoming book &quot;Deep Learning for Coders with fastai and PyTorch: AI Applications Without a PhD&quot; by Jeremy Howard and Sylvain Gugger.

The most important part of the project is testing a deployment process that combines a Flask app, the Gunicorn server, the Nginx server and a custom domain name with an SSL certificate, all installed on a dedicated server.

Below I explain the different deployment stages to deploy this repo combining the pieces mentioned above.

This workflow has been tested on:

**Server OS:** Centos 7

**Name of your flask app:** app

**User installing this:** root (you can use any other)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Install Python and nginx**

If python and ningx have not been installed:

sudo yum install epel-release

sudo yum install python-pip python-devel gcc nginx

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Install virtualenv**

sudo pip install virtualenv

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Clone our repo or create it**

Create your flask app, or clone a repo where you already have it

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Create a virtual environment inside the repo**

virtualenv myprojectenv

source myprojectenv/bin/activate

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Install flask, Gunicorn and any other dependencies**

pip install gunicorn flask

Or more generally: pip install -r requirements.txt

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Give instructions to the Gunicorn server to find our app**

Create a wsgi entry point, file wsgi.py in the root of the repo

The file contains just this:

_from myproject import application_

_if \_\_name\_\_ == &quot;\_\_main\_\_&quot;:_

_    application.run()_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Create a service to automatically start the gunicorn server and our app when server starts**

Create a systemd unit file called app.service in /etc/systemd/system

It contains this:

_[Unit]_

_Description=Gunicorn instance to serve my app_

_After=network.target_

_[Service]_

_User=root_

_Group=nginx_

_WorkingDirectory=path-to-your-app_

_Environment=&quot;PATH=path-to-your-app/myprojectenv/bin&quot;_

_ExecStart=path-to-your-app/myprojectenv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi_

_[Install]_

_WantedBy=multi-user.target_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Start the system process which will create a unix socket file in our app folder and bind to it.**

sudo systemctl start myproject

sudo systemctl enable myproject

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Configure nginx to proxy web requests**

If you are using plesk, go to the nginx settings of the domain where you want to install the app, and select the option that makes nginx not work as a proxy of apache, so that it works standalone.

Open the nginx configuration file of your server, or of the domain where you want to put the app.

**If you are using plesk, you will find the file here:**

/var/www/vhosts/system/domain/conf/nginx.conf

**You can add a brand new section above the standard one:**

_server {_

_    listen 80;_

_    server\_name server\_domain\_or\_IP;_

_    location / {_

_        proxy\_set\_header Host $http\_host;_

_        proxy\_set\_header X-Real-IP $remote\_addr;_

_        proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;_

_        proxy\_set\_header X-Forwarded-Proto $scheme;_

_        proxy\_pass http://unix:path-to-your-app/app.sock;_

_    }_

_}_

**Or you can also just add the location section to an existing server section.**

**This would be the beginning of a server section for the https ssl access of the domain:**

_server {_

_        listen x.x.x.x:443 ssl http2;_

_        server\_name whatever.com;_

_        server\_name www.whatever.com;_

_        server\_name ipv4.whatever.com;_

_…………………._

**And this would be the beginning of a server section for the http access of the domain:**

_server {_

_        listen x.x.x.x:80;_

_        server\_name whatever.com;_

_        server\_name www.whatever.com;_

_        server\_name ipv4.whatever.com;_

_…………………._

**And you could add just the location part inside one of them:**

_location / {_

_        proxy\_set\_header Host $http\_host;_

_        proxy\_set\_header X-Real-IP $remote\_addr;_

_        proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;_

_        proxy\_set\_header X-Forwarded-Proto $scheme;_

_        proxy\_pass http://unix:path-to-your-app/app.sock;_

_    }_

This way you point either the root of the domain or another path within the domain to the flask app.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Give nginx permissions if necessary**

If you are not using the root user, you may have to give permissions to nginx by doing:

sudo usermod -a -G user nginx

chmod 710 /home/user (or wherever the app is installed)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Test nginx conf file**

Test that the syntax of your conf file changes are correct: sudo nginx -t

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Launch or relaunch nginx**

sudo systemctl stop nginx

sudo systemctl start nginx

sudo systemctl enable nginx

sudo systemctl status nginx

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Now you can go to your domain address and access the app**

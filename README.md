
## Objective

The aim of this project is to deploy  Django Pur Beurre app on server

## Create A Digital Ocean Droplet

Use [this link](https://docs.digitalocean.com/products/droplets/how-to/create/) to create a droplet in Digital Ocean

### Creating SSH keys (Optional)

You can choose to create SSH keys to login if you want. If not, you will get the password sent to your email to login via SSH

To generate a key on your local machine

```
$ ssh-keygen
```

Hit enter all the way through and it will create a public and private key at

```
~/.ssh/id_rsa
~/.ssh/id_rsa.pub
```

You want to copy the public key (.pub file)

```
$ cat ~/.ssh/id_rsa.pub
```

Copy the entire output and add as an SSH key for Digital Ocean

### Login To Your Server

If you setup SSH keys correctly the command below will let you right in. If you did not use SSH keys, it will ask for a password. This is the one that was mailed to you

```
$ ssh root@YOUR_SERVER_IP
```

### Create a new user

It will ask for a password, use something secure. You can just hit enter through all the fields. I used the user "djangoadmin" but you can use anything

```
# adduser djangoadmin
```

### Give root privileges

```
# usermod -aG sudo djangoadmin
```

### SSH keys for the new user

Now we need to setup SSH keys for the new user. You will need to get them from your local machine

### Exit the server

You need to copy the key from your local machine so either exit or open a new terminal

```
# exit
```

You can generate a different key if you want but we will use the same one so lets output it, select it and copy it

```
$ cat ~/.ssh/id_rsa.pub
```

### Log back into the server

```
$ ssh root@YOUR_SERVER_IP
```

### Add SSH key for new user

Navigate to the new users home folder and create a file at '.ssh/authorized_keys' and paste in the key

```
# cd /home/djangoadmin
# mkdir .ssh
# cd .ssh
# nano authorized_keys
Paste the key and hit "ctrl-x", hit "y" to save and "enter" to exit
```

### Login as new user

You should now get let in as the new user

```
$ ssh djangoadmin@YOUR_SERVER_IP
```

### Disable root login

```
# sudo nano /etc/ssh/sshd_config
```

### Change the following

```
PermitRootLogin no
PasswordAuthentication no
```

### Reload sshd service

```
# sudo systemctl reload sshd
```

## Software

## Update packages

```
# sudo apt update
# sudo apt upgrade
```

## Install Python 3, Postgres & NGINX

```
# sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

## Clone the project into the app folder on your server (Either HTTPS or setup SSH keys)
```
# git clone yourdepot.git
```

# Vitrual Environment

You need to install the python3-venv package

```
# sudo apt install python3-venv
```

### Create project directory

```
# mkdir yourapp
# cd yourapp
```

### Create venv

```
# python3 -m venv ./venv
```

### Activate the environment

```
# source venv/bin/activate
```
# Postgres Database & User Setup

Log in as administrator to the PostgreSQL console by typing the command 

```
# sudo -u postgres psql
```

You should now be logged into the pg shell

### Create a database

```
CREATE DATABASE db_name;
```

### Create user

```
CREATE USER db_user WITH PASSWORD db_password;
```

### Set default encoding, tansaction isolation scheme (Recommended from Django)

```
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE db_user SET timezone TO 'UTC';
```

### Give User access to database

```
GRANT ALL PRIVILEGES ON DATABASE db_name TO db_user;
```

### Quit out of Postgres

```
\q
```

## Create static files

```
python manage.py collectstatic
```
## Migrations

```
# python manage.py makemigrations
# python manage.py migrate
```
you can load the data from your dump file as well

```
# python manage.py loaddata path_to_the_dump_file
```

## Create super user

```
# python manage.py createsuperuser
```
# NGINX Setup

install NGINX
```
# sudo apt-get install nginx
```

### Create project folder

```
# sudo nano /etc/nginx/sites-available/your_project
```
### Copy this code and paste into the file

```
server {

    listen 80;
    server_name YOUR_IP_ADDRESS;;
    root PATH_TO_ROOT;

    location /static {
        alias PATH_TO_STATICFILES ;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
        }
    }

}
```
### Enable the file by linking to the sites-enabled dir

```
# sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled
```
### Test NGINX config

```
# sudo nginx -t
```

### Restart NGINX

```
# sudo systemctl restart nginx
```

# Gunicorn and Supervisor Setup

Install gunicorn and supervisor 

```
# pip install gunicorn

# sudo apt-get install supervisor
```

### Test Gunicorn serve

```
# gunicorn your_project.wsgi:application
```
Just like Nginx, Supervisor reads a configuration file located in  etc/supervisor. Each file ending in  .conf and located in the path  /etc/supervisor/conf.d represents a process that is monitored by Supervisor. Create a new one:
```
sudo vi /etc/supervisor/conf.d/your_project-gunicorn.conf
```
### Copy this code and past into the file your_project_gunicorn.conf

```
[program:your_project-gunicorn.conf]
command = /home/your_user/env/bin/gunicorn your_project-gunicorn.conf.wsgi:application
user = your_user
directory = /home/your_user/your_project
environment = ENV="PRODUCTION",SECRET_KEY="your_screct_key"
autostart = true
autorestart = true
```
###  Supervisor commands to start the processes
```
# sudo supervisorctl reread
# sudo supervisorctl update
# sudo supervisorctl status
```



## Acknowledgment
I would like to thank my mentor Dimitri Ségard, for all the help and advices he gave to me to accomplish this project.

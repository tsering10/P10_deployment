
## Objective

The aim of this project is to deploy the Pur Beurre app on server

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

## Acknowledgment
I would like to thank my mentor Dimitri Ségard, for all the help and advices he gave to me to accomplish this project.

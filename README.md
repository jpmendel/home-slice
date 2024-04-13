# HomeSlice

A Raspberry Pi Zero home server application built using Python, Django, HTMX and SQLite.

## Project Setup

1. Install Python 3.9 with `brew install python@3.9` on MacOS, or by visiting [python.org](https://www.python.org/downloads/).
2. Run the `setup.sh` script to create the virtual environment and install packages.
3. Create a file named `.env` and copy the keys from `.env.default` into it. Then fill in your desired configuration.

## Raspberry Pi Setup

1. Use the Raspberry Pi Imager to install Raspbian onto a device. Set up the device to connect to your network and create SSH keys to securely connect.
2. Connect to the Raspberry Pi using `ssh`.
4. Install the required packages:
```
sudo apt-get install nginx python3-venv libopenblas-dev
```
5. Create a file named `.pienv` and copy the keys from `.pienv.default` into it. Then fill in your desired configuration.
6. Run the `deploy/update.sh` script to sync project files to the Raspberry Pi.
7. Copy the configuration files into the system directory:
```
sudo cp config/app.socket /etc/systemd/system/
sudo cp config/app.service /etc/systemd/system/
```
8. Run the following code to enable the application:
```
sudo systemctl start app.socket
sudo systemctl enable app.socket
sudo systemctl daemon-reload
sudo systemctl restart app
```
9. Copy the NGINX config into the NGINX available sites directory and enable it:
```
sudo cp config/app.nginx /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/app.nginx /etc/nginx/sites-enabled/
```
10. Verify the NGINX config is valid and then restart NGINX:
```
nginx -t
sudo systemctl restart nginx
```

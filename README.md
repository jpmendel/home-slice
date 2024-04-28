# HomeSlice

A Raspberry Pi Zero home server application built using Python, Django, HTMX and SQLite.

## Project Setup

1. Install Python 3.9 with your system package manager, or by visiting [python.org](https://www.python.org/downloads/).
2. Run the `setup.sh` script to create the virtual environment and install packages.
3. Fill your desired configuration into the `.env` file.

## Run (development)

1. Activate the Python virtual environment: `source .venv/bin/activate`
2. Change into the `src` directory: `cd src`
3. If needed, migrate the database: `python manage.py migrate`
4. Run the Django application in development mode: `python manage.py runserver`

## Raspberry Pi Setup

1. Use the Raspberry Pi Imager to install Raspbian onto a device. Set up the device to connect to your network and create SSH keys to securely connect.
2. Connect to the Raspberry Pi using `ssh`.
4. Install the required packages:
```
sudo apt-get install nginx python3-venv libopenblas-dev
```
5. Return to the project on your development machine.
6. Create a file named `.pienv` and copy the keys from `.pienv.default` into it. Then fill in your desired configuration.
7. Run the `deploy/update.sh` script to sync project files to the Raspberry Pi.
8. SSH back into the Raspberry Pi, then follow the `Project Setup` steps using the `prod.txt` requirements.
9. Copy the configuration files into the system directory:
```
sudo cp config/app.socket /etc/systemd/system/
sudo cp config/app.service /etc/systemd/system/
```
10. Run the following code to enable the application:
```
sudo systemctl start app.socket
sudo systemctl enable app.socket
sudo systemctl daemon-reload
sudo systemctl restart app
```
11. Copy the NGINX config into the NGINX available sites directory and enable it:
```
sudo cp config/app.nginx /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/app.nginx /etc/nginx/sites-enabled/
```
12. Verify the NGINX config is valid and then restart NGINX:
```
nginx -t
sudo systemctl restart nginx
```

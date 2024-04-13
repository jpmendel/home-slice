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
sudo apt-get install python3-venv nginx libopenblas-dev
```
5. Create a file named `.pienv` and copy the keys from `.pienv.default` into it. Then fill in your desired configuration.
6. Run the `deploy/update.sh` script to sync project files to the Raspberry Pi.

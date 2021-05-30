- [1. Setup the board on macOS](#1-setup-the-board-on-macos)
  - [1.1. Conda](#11-conda)
    - [1.1.1. Python 3.8](#111-python-38)
    - [1.1.2. MDT (Mendel Development Tool)](#112-mdt-mendel-development-tool)
  - [1.2. Boot up the board](#12-boot-up-the-board)
  - [1.3. Install OpenSSH key on the board](#13-install-openssh-key-on-the-board)
  - [1.4. Connect the board to WiFi](#14-connect-the-board-to-wifi)
  - [1.5. Connect to the board with MDT shell](#15-connect-to-the-board-with-mdt-shell)
  - [1.6. Update the Mendel software](#16-update-the-mendel-software)

# 1. Setup the board on macOS
> * Tested on Catalina (10.15)
> * Caution: currently doesn't work on Big Sur

## 1.1. Conda

Create a new environment
```sh
conda create -n coralboard
conda activate coralboard
```

### 1.1.1. Python 3.8
> Until [TensorFlow 2](https://www.tensorflow.org/install) supports Python 3.9

```sh
conda install python=3.8
```

### 1.1.2. MDT (Mendel Development Tool)
> Official guide [here](https://www.coral.ai/docs/dev-board-mini/get-started/)

The package is not available in the Anaconda repo, so we'll use pip to install in the conda environment [(blog)](https://www.anaconda.com/blog/using-pip-in-a-conda-environment)

```sh
pip install mendel-development-tool
```

## 1.2. Boot up the board
* Left: Phone charger (USB-C) - 5V2A
* Right: Computer (USB-C)

## 1.3. Install OpenSSH key on the board
> Beginning with macOS Catalina (10.15), we cannot create an MDT (or other SSH) connection over USB

Make sure the Mac can recognize the board <-- I've tried a few cables and **only the one come with MacBook power adapter** works.
```sh
ls /dev/cu.usbmodem*

# my board is called zippy_zebra1
# /dev/cu.usbmodemzippy_zebra1
```

Connect to the serial console
```sh
screen /dev/cu.usbmodemzippy_zebra1 115200

# Mendel GNU/Linux (eagle) zippy-zebra ttyGS0
#
# zippy-zebra login: 
```
> Factory credential is mendel/mendel

Generate a keypair on Mac with empty passphrase
```sh
ssh-keygen -t rsa -m PEM

# Generating public/private rsa key pair.
# Enter file in which to save the key (/Users/leesiu/.ssh/id_rsa): mendel
# Enter passphrase (empty for no passphrase): 
```

Move the private key to the expected path
```sh
chmod 600 mendel
mkdir -p ~/.config/mdt/keys && mv mendel ~/.config/mdt/keys/mdt.key
```

Copy the content of the public key `mendel.pub` to the board
```sh
# Replace xxxxxx
echo "ssh-rsa xxxxxx" > /home/mendel/.ssh/authorized_keys
```

## 1.4. Connect the board to WiFi

```sh
nmtui
```

If using Windows, `nmtui` may complain about the screen. use `nmcli` instead

```
nmcli device wifi rescan
nmcli device wifi list
nmcli device wifi connect <SSID> --ask
```

Exit the serial console, and unplug the OTG cable.

## 1.5. Connect to the board with MDT shell

Search for mendel devices in the same WiFi
```sh
mdt devices

# zippy-zebra  (IP.ADDRESS)
```

```sh
mdt shell

# Connected to the board as user mendel
```

## 1.6. Update the Mendel software
The board most probably has an outdated software, so it's a good idea to upgrade it. 

Check the Mendel version
```sh
cat /etc/mendel_version

# 5.2
```

The version is even newer than in the [official webpage](https://www.coral.ai/software/#mendel-dev-board-mini), so I'll just update the packages
```sh
sudo apt-get update
sudo apt-get dist-upgrade
```

If everything goes well,
```sh
sudo reboot now
```

# Notes install DMI-TCAT

Github: https://github.com/digitalmethodsinitiative/dmi-tcat/wiki

## On vagrant

Install Virtual Box and Vagrant:
- `Virtual Box`: https://www.virtualbox.org/
- `Oracle VM VirtualBox Extension Pack`: https://www.virtualbox.org/
- `Vagrant`: https://www.vagrantup.com/downloads.html


Copy `config_tcat.txt` and name it `config_tcat_completed.txt`, and fill the section (from your twitter account):
- CONSUMERKEY=
- CONSUMERSECRET=
- USERTOKEN=
- USERSECRET=

From the main folder with `Vagrantfile`, set up the vagrant machine:

    vagrant up

The server should be running in the guest machine (vagrant), and should be accessible from your host machine at:
- http://172.28.128.2/capture/
- http://172.28.128.2/analysis/

TCAT administrator login (for capture setup and analysis):
  Username: admin
  Password: admin

TCAT standard login (for analysis only):
  Username: tcat
  Password: tcat

**Note**: The vagrant machine is setup to take ip: 172.28.128.2 (set in `Vagrantfile`), and dmi_tcat is setup to run the server on the same ip (set in `config_tcat.txt`) in the vagrant machine, so it should be accessible from the host.

## Use

### Capture

From http://172.28.128.2/capture/, you can set a query that will fetch data in the background (based on hashtag, etc)

### Analysis

From  http://172.28.128.2/analysis/, you can use data fetched by the capture process to extract stats, export csv, etc.
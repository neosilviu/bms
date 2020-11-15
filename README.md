# bms

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
git clone https://github.com/karulis/pybluez.git
cd /pybluez
sudo python setup.py install
cd /examples/simple
nano getbms-ant.py



sudo apt-get upgrade
sudo bluetoothctl
scan on
pair AA:BB:CC:B1:23:45
1234
exit

sudo crontab -e
   sudo rfcomm bind /dev/rfcomm1 AA:BB:CC:B1:23:45
   sudo python ~/bms/getbms-ant.py


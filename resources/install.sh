#!/bin/bash

cd ../../

rm -rf hearingaid-prototype
git clone https://github.com/liketohear/hearingaid-prototype.git
cd hearingaid-prototype
./make.sh

cd ../
git clone https://github.com/ppisa/rpi-utils.git
sudo cp rpi-utils/init-overlay/sbin/* /sbin
sudo mkdir /overlay
sudo cp -r rpi-utils/init-overlay/overlay /
cd liketohear/resources 
sudo cp cmdline.txt /boot/cmdline.txt

sudo apt-get install python3-tornado 
cp bashrc  ~/.bashrc
sudo cp systemd-udevd.service /lib/systemd/system/systemd-udevd.service
sudo cp dhcpcd.conf /etc/dhcpcd.conf


echo "system needs to be restarted, press y to continue"

read message
if [[ $message == y* ]];
then
    sudo reboot
else
    echo "please reboot later"
fi

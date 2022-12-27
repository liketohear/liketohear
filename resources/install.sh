#!/bin/bash
sudo apt-get update -y
cd ~

#locale=de_DE.UTF-8
#kb_layout=de
new_password=liketohear

sudo sed -i 's/^dtparam.*/#dtparam=audio=on/' /boot/config.txt
sudo echo 'dtoverlay=audioinjector-wm8731-audio' | sudo tee -a /boot/config.txt
sudo echo 'force_turbo=1' | sudo tee -a /boot/config.txt

#sudo raspi-config nonint do_change_locale $locale
#sudo raspi-config nonint do_configure_keyboard $layout
sudo raspi-config nonint do_ssh 1
sudo raspi-config nonint do_wifi_country DE
sudo raspi-config nonint do_change_timezone Europe/Berlin
(echo raspberry ; echo $new_password ; echo $new_password) | passwd

sudo apt install -y hostapd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo apt install -y dnsmasq
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

sudo touch /etc/sysctl.d/routed-ap.conf
sudo sudo echo 'net.ipv4.ip_forward=0' /etc/sysctl.d/routed-ap.conf
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo netfilter-persistent save

#instead of sudo nano /etc/dnsmasq.conf
sudo sed -i 's/^#interface.*/interface=wlan0 #listening interface/' /etc/dnsmasq.conf 			# Listening interface
sudo echo 'dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h' | sudo tee -a /etc/dnsmasq.conf	# Pool of IP addresses served via DHCP
sudo echo 'domain=wlan' | sudo tee -a /etc/dnsmasq.conf 						# Local wireless DNS domain
sudo echo 'address=/gw.wlan/192.168.4.1' | sudo tee -a /etc/dnsmasq.conf 				# Alias for this router

#
sudo rfkill unblock wlan

#instead sudo nano /etc/hostapd/hostapd.conf
sudo echo 'country_code=DE' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'interface=wlan0' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'ssid=liketohear-wifi-2' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'hw_mode=g' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'channel=7' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'macaddr_acl=0' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'auth_algs=1' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'ignore_broadcast_ssid=0' | sudo tee -a /etc/hostapd/hostapd.conf  
sudo echo 'wpa=2' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'wpa_passphrase=liketohear-wifi-2' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'wpa_key_mgmt=WPA-PSK' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'wpa_pairwise=TKIP' | sudo tee -a /etc/hostapd/hostapd.conf 
sudo echo 'rsn_pairwise=CCMP' | sudo tee -a /etc/hostapd/hostapd.conf 

#sudo apt dist-upgrade
sudo apt install -y build-essential haveged ssh mosh byobu tig htop nmon libncurses-dev
sudo apt-get install -y jackd2 libjack-jackd2-dev qjackctl openjdk-11-jdk
sudo apt-get install -y libsndfile-dev
sudo apt-get install -y portaudio19-dev 

wget https://sourceforge.net/projects/njconnect/files/njconnect-1.6.tar.xz
sudo tar -xf njconnect-1.6.tar.xz
cd njconnect-1.6
make
cd ..

wget https://github.com/HoerTech-gGmbH/openMHA/archive/v4.8.1.zip
unzip v4.8.1.zip
mv openMHA-4.8.1 openMHA
cd openMHA
./configure
make
make install VERBOSE=1
cd ..

#octave macht feedback-noise für hearingaid-prototype 
sudo apt-get install -y octave
sudo apt-get install -y python3
sudo apt-get install -y python3-tornado
git clone https://github.com/liketohear/hearingaid-prototype


cd hearingaid-prototype
./make.sh
sudo cp example-configuration/etc/dbus-1/system-local.conf /etc/dbus-1/system-local.conf
cd ../

# if you wan't a write protected filesystem uncomment the following lines
#git clone https://github.com/ppisa/rpi-utils.git
#sudo cp rpi-utils/init-overlay/sbin/* /sbin
#sudo mkdir /overlay
#sudo cp -r rpi-utils/init-overlay/overlay /
#cd liketohear/resources
#sudo cp cmdline.txt /boot/cmdline.txt

cd liketohear/resources
cp bashrc  ~/.bashrc
#sudo cp dhcpcd.conf /etc/dhcpcd.conf


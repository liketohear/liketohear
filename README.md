
# liketohear

![Image](https://user-images.githubusercontent.com/10296132/103158804-75c4ee80-47c2-11eb-974d-b154d96e24b3.jpg)

This repository holds the information for a framework with intuitive gui control via web app for self-fitting the [mobile openMHA hearing aid prototype](https://github.com/m-r-s/hearingaid-prototype). The framework includes a web app for sound control, logs audio level analysis and self-fitting parameters. 

The liketohear prototype is developed in he framework of the citizen science project ["Hear How You Like To Hear"  at the Fraunhofer IDMT Oldenburg](https://www.idmt.fraunhofer.de/de/institute/projects-products/projects/liketohear.html), funded by the [BMBF](https://www.bmbf.de/). 

Corresponding author: Peggy Sylopp  
Contributing author: Tobias Bruns, Paul Maanen

# Aims
The prototype was designed for intuitive app control in everyday acoustic environments, accessible and operable for everyone.
This is realized by using affordable consumer hardware and open source software. The aim is to lower the entry barrier for self-fitting hearing aid development and facilitate any interested person to get actively involved in testing and improving hearing devices; to empowering power-users. 

# Warning and disclaimer
First, a few words of warning:
Hearing aids are medical products! You use these instructions and the software at you own risk. The described device can produce very high sound levels. Exposure to high sound levels can permanently damage your hearing! You are responsible for the configuration of the device and the protection of your hearing.
Please read about the consequences of noise induced hearing loss before proceeding to the fun part: https://www.nidcd.nih.gov/health/noise-induced-hearing-loss

# Installing
* Download sd card image [here](https://seafile.idmt.fraunhofer.de/f/c1def76f9ab04495b421/?dl=1)
* write the image to sd card (e.g. using on Ubuntu `dd if=liketohear-04_shrink.img of=/dev/sdb bs=1M`)
* plug USB stick: SanDisk Cruzer Fit USB
* Put the SD-Card in your Raspberry Pi Model 3 and boot (username: pi. password: like2hear)
* connect your smartphone to the raspberry wifi (SSID: like2hear-4, password: like2hear-4)
* open browser and type http://172.24.1.1:8888

OR (unstable app connection)

* Download the raspbian buster distribution [here](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2020-08-24/2020-08-20-raspios-buster-armhf-lite.zip):
* Unzip and write the image to sd card (e.g. using `dd if=2020-08-20-raspios-buster-armhf-lite.img of=/dev/sdb bs=1M` )
* Put the SD-Card in your Raspberry Pi Model 3 or higher and connect ethernet 
* Boot (default username: pi, password: raspberry) and install git (`sudo apt-get install git`)
* Get the sources:  `git clone https://github.com/liketohear/liketohear'
* Change directory to `liketohear/resources` and run `./install.sh`
* Confirm realtime mode with jackd2
* Reboot (username: pi, password: liketohear)
* connect your smartphone to the raspberry wifi (SSID: liketohear-wifi-2, password: liketohear-wifi-2)
* open browser and type http://172.24.1.1:8888

# Main ingredients
Hardware:

* Binaural Microphones/Earphones
* Microphone pre-amplifier
* Raspberry Pi 3 model B
* Low-latency sound card
* USB power bank
* USB stick

Third party software:
 * [A mobile hearing aid prototype based on openMHA](https://github.com/m-r-s/hearingaid-prototype)
 * [openMHA](https://github.com/HoerTech-gGmbH/openMHA/)
 * [Raspbian](https://www.raspbian.org/)
 * [JACK](https://github.com/jackaudio)
 * hostapd
 * OpenSSH

# Main characteristics
Free software: Control is yours, you can change every single bit of it!
Efficient real-time implementations of research-approved hearing algorithms (c.f. openMHA at Github)
Competitively low delays: Less than 5ms
Looks like wearing in-ear headphones
Model for 3d print available

# Some cool features
  * very intuitive control by web app - no technical affinity necessary
  * self-fitting
  * logging of binaurals sound sceneries on USB stick
  * based on presets
  * Pre-configured SD-card image (~500 Mb) available for download
  * No proper shut down of OS necessary: Overlay makes power cut possible without affecting the software installation
  * Pre-calibrated for most "transparent" acoustic impression
  * Autostart on boot
  * Several hours of autonomy
  * Connect via WiFi to the hearing aid prototype
  * Fit it to your hearing thresholds
  * Combine it with any jack-based software (play, process, or record) 

# Documentation & Instructions
Further documentation and instructions can be found in the corresponding [Wiki](https://github.com/liketohear/liketohear/wiki). Feel free to test them and contribute. 
Please also see documentation of the [openMHA](http://www.openmha.org/documentation/) if you want to dig deeper into hearing aid signal processing.


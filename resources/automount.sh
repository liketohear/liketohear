#!/bin/bash

# mount last SanDisk usb stick entry in /dev/disk/by-id to /media
sudo mount -o uid=$UID '/dev/'$(ls -l /dev/disk/by-id | grep SanDisk | tail -1 | awk -F'/' '{print $3}') /media

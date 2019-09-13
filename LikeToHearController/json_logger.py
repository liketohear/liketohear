'''
Copyright 2019 Fraunhofer IDMT
All rights reserved

This file is part of the like2hear project

like2hear is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

like2hear is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with like2hear.  If not, see <http://www.gnu.org/licenses/>.

'''

'''

@author: Tobias Bruns <tobias.bruns@idmt.fraunhofer.de
@date: 19.11.2019
@version 1.0

@package like2hear

This file contains a class for logging user settings and octave levels to a connected usb-drive

'''

import json
import time
import os

class JsonLoggerHandler():
    _timediff = {}

    # initializing logger with standard user name and given logfile name
    def __init__(self,userid = "standard",filename = "/media/user_interface.log", usb_log=True):
        self._userid = userid
        if usb_log:
            # check if usb stick is inserted
            while not os.path.ismount("/media"):
                print("No usb stick detected for logging: retry...")
                time.sleep(1) 
            # open file
            try:
                self._fid = open(filename,'a')
            except:
                print("No logging folder available on device")
                exit()

    # closing logging    
    def close(self):
        # close file
        self._fid.close()
        
    # write to logfile    
    def write(self,date,uid,msg,log_data = []):
        # saving log info in python dict
        
        log_info = {'date': date, 'msg': msg, 'data': log_data, 'userid': uid}
        # encode python dict to json string    
        self._fid.write(json.dumps(log_info) + '\n')
        # flush fid to update file, so data is also logged before program crash
        self._fid.flush()

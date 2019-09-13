#!/usr/bin/python
# -*- utf-8 -*-

'''
Copyright 2019 Fraunhofer IDMT, Oldenburg
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

##@package like2hear
#
# Control Class for the openMHA TCP/IP Interface
#
# @author Tobias Bruns <tobias.bruns@idmt.fraunhofer.de>
# @version 0.1
# @date 03.04.2019
# 2019 Fraunhofer IDMT, Oldenburg




import socket, time




class OpenMhaCalibration(object):
    '''
    classdocs
    '''
    _openMhaAddr = "127.0.0.1"; #standard address
    _openMhaPort = 33337; #standard port
    _openMhaGainPresets = {};
    _normalUCL = 85; # normal value for loud voice
    _normalMCL = 65; # normal vlaue for loud voice
    _debug = True;
    
    def __init__(self):
        # starting socket connection
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            self._conn.connect((self._openMhaAddr,self._openMhaPort))
            print('New connection to openMHA established')
        except Exception: 
            print('error: Cannot establish connection to open MHA')

        
    def close(self):
        self.setLog = False
    
        
    def ShowCalibrationLevels(self,dur_sec=30):
        msg = 'mha.calib_in.rmslevel?\n'
        time_intervall = 4 # Hz
        
        for idx in range(int(dur_sec*time_intervall)):
            self._conn.send(msg.encode('utf-8'))
            print(self._conn.recv(1024).decode('utf-8'))
            time.sleep(1/time_intervall)
        
            
    
if __name__ == "__main__":

    openMHACalibration = OpenMhaCalibration();
    openMHACalibration.ShowCalibrationLevels(60);

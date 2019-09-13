#!/usr/bin/python
# -*- utf-8 -*-

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
@package liketohear

Control Class for the openMHA TCP/IP Interface

@author Tobias Bruns <tobias.bruns@idmt.fraunhofer.de>
@version 1.0
@date 26.04.2019
2019 Fraunhofer IDMT, Oldenburg

'''

import socket, json, os.path, json_logger, threading, time, datetime

class openMHACtrl(object):
    '''
    classdocs
    '''
    _openMhaAddr = "127.0.0.1"   #standard address
    _openMhaPort = 33337         #standard port
    _openMhaGainPresets = {}
    _timediff = datetime.timedelta()
    _debug = False # if set to true no connection to openMHA ist established
    _network_lock = threading.Lock()
	
    def __init__(self):
        '''
        Constructor
        '''
        self._presetx = 5
        self._presety = 5
        
        self.userName = "DefaultUser"
        self.setLog = True
        
        # loading presets from file
        if os.path.exists('gains.json'):
            fh_gains = open('gains.json', 'r')
            self._openMhaGainPresets = json.load(fh_gains)
            fh_gains.close()
        else:
            return -1;
        
        if self._debug is False:
            # starting socket connection
            self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._conn.settimeout(1.0)
            try: 
                self._conn.connect((self._openMhaAddr,self._openMhaPort))
                print('New connection to openMHA established')
            except socket.timeout:
                print ('timeout')
                
        self.setGeneralGains()
        self.setGainsfromPreset(self._presetx,self._presety)
        if self.setLog is True:
            self.user_log = json_logger.JsonLoggerHandler()
            self.user_log._timediff = self._timediff
            self.log_thread = threading.Thread(target=self.log_loop)
            self.log_thread.start()
            print("started logging")
        
    def close(self):
        self.setLog = False
    
    def log_loop(self):
        self.user_log.write(time.asctime(),self.userName,'openMHACtrl started')
        msg = 'mha.transducers.mhachain.analysis.plug.mhachain.rms.level_db?\n'
        
        while self.setLog:
            new_time = datetime.datetime.now() + self._timediff
            if self._debug == False:
                with self._network_lock:
                    self._conn.send(msg.encode('utf-8'))
                    ret = self._conn.recv(1024)
                    self.user_log.write(new_time.ctime(),self.userName,ret.decode('utf_8'))
                    
            self.user_log.write(new_time.ctime(),self.userName,'current preset',{"presetx": self._presetx, "presety": self._presety})
            time.sleep(1)
            
        self.user_log.write(time.asctime(),self.userName,'openMHACtrl stopped')
        self.user_log.close()
        
        
    def setGeneralGains(self):
        msg = 'mha.transducers.mhachain.altplugs.dynamiccompression.mhachain.dc.gtstep = ' + str(self._openMhaGainPresets['step_size']) + '\n'
        
        if self._debug is False:
            with self._network_lock:
                try:
                    self._conn.send(msg.encode('utf-8'))
                    ret = self._conn.recv(1024)
                    print(ret.decode('utf-8'))
                except socket.timeout:     
                    print('connection timed out')
		
        msg = 'mha.transducers.mhachain.altplugs.dynamiccompression.mhachain.dc.gtmin = ' + str(self._openMhaGainPresets['min_gain']) + '\n'
        
        if self._debug is False:
            with self._network_lock:
                try:
                    self._conn.send(msg.encode('utf-8'))
                    ret = self._conn.recv(1024)
                    print(ret.decode('utf-8'))
                except socket.timeout:     
                    print('connection timed out')
		
    def setGainsfromPreset(self,presetx,presety):
        if presetx is not self._presetx:
            self._presetx = presetx
            msg = 'mha.transducers.mhachain.altplugs.dynamiccompression.mhachain.dc.gtdata = ' + self._openMhaGainPresets['gain_presets'][presetx-1] + '\n'

            if self._debug is False:
                with self._network_lock:
                    try:
                        self._conn.send(msg.encode('utf-8'))
                        ret = self._conn.recv(1024)
                        print(ret.decode('utf-8'))
                    except socket.timeout:     
                        print('connection timed out')
            else:
                print(msg)
                
        if presety is not self._presety:
            self._presety = presety
            msg = 'mha.transducers.mhachain.altplugs.dynamiccompression.mhachain.gain.bbgain = ' + str(self._openMhaGainPresets['gain_offsets'][presety-1]) + '\n'

            if self._debug is False:
                with self._network_lock:
                    try:
                        self._conn.send(msg.encode('utf-8'))
                        ret = self._conn.recv(1024)
                        print(ret.decode('utf-8'))
                    except socket.timeout:     
                        print('connection timed out')
            else:
                print(msg)

    def	setOnOff(self,onoff):
        if onoff == 1:
            msg = 'mha.transducers.mhachain.altplugs.select = dynamiccompression \n'
        else:
            msg = 'mha.transducers.mhachain.altplugs.select = (none) \n'

        if self._debug is False:
            with self._network_lock:
                try:
                    self._conn.send(msg.encode('utf-8'))
                    ret = self._conn.recv(1024)
                except socket.timeout:     
                    print('connection timed out')
                    
    def setUserID(self,uid):
        self.userName = uid
        
    def setTime(self,ts):
        client_time = datetime.datetime.fromtimestamp(ts)
        self._timediff = client_time - datetime.datetime.now()
        print("timedelay between client and Server:" + str(self._timediff))
        
if __name__ == "__main__":
    
    openMHACtrlInstance = openMHACtrl()
    openMHACtrlInstance.setGainsfromPreset(5, 5)
    openMHACtrlInstance.setLog = False
    

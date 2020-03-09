'''
Created on 23.04.2018

@author: bns
'''

import json
import time
import re
import matplotlib.pyplot as plt


class read_log():
    def __init__(self,select_data = "levels",user_id='DefaultUser',filename = "user_interface.log"):
        self._fid = open(filename,'r')
        self._user_id = user_id;
        self._select_data = select_data;
    def close(self):
        self._fid.close()
        
    def readlines(self):
        # First open file      
        for msg in self._fid.readlines():
            line_object = json.loads(re.sub('\n','',msg))
            
            if self._user_id in line_object['userid']: 
                if "levels" in self._select_data:
                    nummatch= re.search('\[[0-9 .-]+\]', line_object['msg'], flags=0)
                    if(nummatch):
                        numstrs = re.findall('[0-9.-]+', nummatch.group(0))
                        nums = list( map( float, numstrs ))
                        yield nums
                if 'presets' in self._select_data and 'current preset' in line_object['msg']:
                        yield [line_object['data']['presetx'], line_object['data']['presety']]
        
if __name__ == '__main__':
    user_levels = read_log('levels',[],'user_interface.log')
    user_presets = read_log('presets',[],'user_interface.log')
    dataset = 0
    idx = 0
    out = []
    out_presets = []

    for dataset in user_levels.readlines():
        out.append(dataset)
        
    for dataset in user_presets.readlines():
        out_presets.append(dataset)
                    
            
    plt.plot(out_preset,'o')
    plt.show()
    

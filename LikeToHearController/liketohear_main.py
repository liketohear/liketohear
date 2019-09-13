#!/usr/bin/python3
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
@author Tobias Bruns <tobias.bruns@idmt.fraunhofer.de>
@version 1.0
@date 26.04.2019
2019 Fraunhofer IDMT, Oldenburg

@package liketohear

This is the like2hear project main script containing a http server for WEB GUI and
a simple web socket server for asynchronously controlling the like to hear hearable
parameters

'''

SOCKETTIMEOUT = 2
SOCKETBUF = 128
SRV_PORT = 2000


import os, json
from liketohear_ctrl import openMHACtrl
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import signal
import logging
import time
from functools import partial


nCli = 0                                # number of connected consoles
debug = 0;                              # if debug is set to 1 no connection to openMHA_2DCtrl is established
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3    # seconds to wait after term signal
openMHAInstance =  openMHACtrl()        # initializing openMHA_2DCtrl.py instance
onoffFlag = 1
commander = "/home/pi/hearingaid-prototype/commandqueue"

# html handler for showing the whole webpage
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("../html")
        self.write(loader.load("index.html").generate())
    
    def post(self):
        username = self.get_argument('user_id')
        self.render("../html/2dtouch.html", user_id=username)
        
# websocket handler 
class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self,user_id):
        global nCli
        self.write_message("Connected to ""like to hear"" websocket")
        print("New user connection connection established ...")
        openMHAInstance.setUserID(user_id)
    def on_message(self, message):
        global onoffFlag
        #message = message.encode('utf-8','ignore')
        try:
            mObj = json.loads(message)
            self.write_message("message accepted")

            # catching command SET to send preset and volume data to openMHACtrl
            if mObj['cmd'] == 'SET':
                if debug is 0:
                    openMHAInstance.setGainsfromPreset(mObj['pre'], mObj['vol'])
                else:
                    print("Debug: received preset: " + str(mObj['pre']) + " and level: " + str(mObj['vol']))

            # catching command REG for registrating new user to openMHACtrl
            if mObj['cmd'] == 'REG':
                if debug is 0:
                    # time from milliseconds (js) to deconds (python)
                    openMHAInstance.setTime(mObj['data']/1000)
                else:
                    print("Set new time:" + str( mObj['data']))
                    
            # catching command RESET for resetting feedback reduction
            if mObj['cmd'] == 'RESET':
                if debug is 0:
                    msg = "feedback 3\n"
                    print('Received reset')
                    pipeout = os.open(commander, os.O_WRONLY)
                    os.write(pipeout, msg.encode('utf-8')) 
                    os.close(pipeout)
                else:
                    print('Received reset')

            if mObj['cmd'] == 'ONOFF':
                print("Set onoff:" + str(mObj['data']))
                if debug is 0:
                    onoffFlag = int(mObj['data'])
                    # set onoff flag
                    openMHAInstance.setOnOff(onoffFlag)
                else:
                    print("Set onoff:" + str(mObj['data']))
                
                
        except ValueError:
            # if no valid JSON was coming in interprete as text
            print("no JSON, just chatting")
            self.write_message("You said: " + message)
            

    def on_close(self):
        global nCli
        if nCli >= 1:
            nCli -= 1

        print('Connection to like to hear websocket closed...')
        
# application initialisation for html and websocket        
application = tornado.web.Application([
(r'/ws/(.*)', WSHandler),
(r'/', MainHandler),
(r"/(.*)", tornado.web.StaticFileHandler, {"path": "../html"}),
],debug=True)


## Signal Handler
# 
# Callback function handling system term and interrupt signals 
# # @param sig: unix signal code  
def sig_handler(server, sig, frame):
    openMHAInstance.close()
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop(deadline):
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            logging.info('Waiting for next tick')
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()
            logging.info('Shutdown finally')

    def shutdown():
        logging.info('Stopping http server')
        server.stop()
        logging.info('Will shutdown in %s seconds ...',
                     MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        stop_loop(time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)

    logging.warning('Caught signal: %s', sig)
    io_loop.add_callback_from_signal(shutdown)
#


# Starting websocket.py as standalone application
if __name__ == "__main__":
       
    print("Starting Websocket...")
    print ("Navigate to localhost:8888")
    # starting tornado http server
    http_server = tornado.httpserver.HTTPServer(application)
    
    # registering signal handler
    signal.signal(signal.SIGTERM, partial(sig_handler, http_server))
    signal.signal(signal.SIGINT, partial(sig_handler, http_server))
    
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    



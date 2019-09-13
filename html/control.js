/*
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
*/

/*

2DTouch GUI Control Class and Websocket Connnection to Like To Hear Framework

@author Stephanus Volke <stephanus.volke@idmt.fraunhofer.de>
@version 1.0
@date 19.11.2018
2019 Fraunhofer IDMT, Oldenburg

*/

class Socket {

constructor(host, port, user_id, soundhandle) {
	this.socket = new WebSocket(`ws://${host}:${port}/ws/${user_id}`);
	this.socket.onopen = this.onopen.bind(this);
	this.socket.onmessage = this.onmessage;
	this.soundhandle = soundhandle;

	this.soundhandle.addEventListener('soundchange', this.sound_change_handler.bind(this));
}

sound_change_handler(ev) {
	let vol = ev.target.vol;
	let freq = ev.target.freq;
	this.send_sounddata(vol, freq);
}

onopen() {
	console.log('ws open');
	this.send_command('REG',Date.now())
}

onmessage(msg) {
	
}

send_sounddata(vol, pre) {
	var obj = {
	cmd: "SET",
	receiver: '',
	pre: pre,
	vol: vol,
	algo: "1"
	};				
	this.socket.send(JSON.stringify(obj));
}

send_command(cmd, data) {
	var obj = {
	cmd: cmd,
	data: data,
	};
	this.socket.send(JSON.stringify(obj));
}
}

class Soundformer {

constructor(box, handle) {
	this.box = box;
	this.handle = handle;

	this.grab_handler = this.grab_handler.bind(this)
	this.drop_handler = this.drop_handler.bind(this)
	this.drag_handler = this.drag_handler.bind(this)
	this.click_handler = this.click_handler.bind(this)

	this.handle.addEventListener('mousedown', this.grab_handler);
	this.handle.addEventListener('touchstart', this.grab_handler);
	this.box.addEventListener('click', this.click_handler);

	this.handle.vol = 5;
	this.handle.freq = 5;

	this.event = new Event('soundchange');
}

init_box() {
	this._bounds = this.box.getBoundingClientRect();
	this._handlebounds = this.handle.getBoundingClientRect();
}

click_handler(ev) {
	this.init_box()
	ev.stopPropagation();
	let mouse = {x:ev.clientX, y:ev.clientY};
	let left = mouse.x - this.lim.xmin - this._handlebounds.width / 2;
	let top = mouse.y - this.lim.ymin - this._handlebounds.height / 2;
	left = (left < 0) ? 0 : ((left > this.lim.width - this._handlebounds.width) ? this.lim.width - this._handlebounds.width : left);
	top = (top < 0) ? 0 : ((top > this.lim.height - this._handlebounds.height) ? this.lim.height - this._handlebounds.height : top);
	this.handle.style.top = `${top}px`;
	this.handle.style.left = `${left}px`;
	this._set_values(left, top);
	
}

grab_handler(ev) {
	this.init_box()
	if (ev.type == 'mousedown') {
	document.addEventListener('mouseup', this.drop_handler);
	document.addEventListener('mousemove', this.drag_handler);
	} else if (ev.type == 'touchstart') {
	document.addEventListener('touchend', this.drop_handler);
	document.addEventListener('touchmove', this.drag_handler);
	}
}

drag_handler(ev) {
	let mouse = undefined;
	if (ev.type == 'mousemove') {
	mouse = {x:ev.clientX, y:ev.clientY};
	} else if (ev.type == 'touchmove') {
	ev.preventDefault();
	mouse = {x:ev.touches[0].clientX, y:ev.touches[0].clientY}
	}
	let left = mouse.x - this.lim.xmin - this._handlebounds.width / 2;
	let top = mouse.y - this.lim.ymin - this._handlebounds.height / 2;
	left = (left < 0) ? 0 : ((left > this.lim.width - this._handlebounds.width) ? this.lim.width - this._handlebounds.width : left);
	top = (top < 0) ? 0 : ((top > this.lim.height - this._handlebounds.height) ? this.lim.height - this._handlebounds.height : top);
	this.handle.style.top = `${top}px`;
	this.handle.style.left = `${left}px`;
	this._set_values(left, top);
	ev.preventDefault();
}

_set_values(x, y) {
	let new_vol = 10-  Math.round(9 / (this.lim.height - this._handlebounds.height) * y);
	let new_freq = 1+ Math.round(9 / (this.lim.width - this._handlebounds.width) * x);
	if ((new_vol != this.handle.vol) || (new_freq != this.handle.freq)) {
	this.handle.vol = new_vol;
	this.handle.freq = new_freq;
	this.handle.dispatchEvent(this.event)
	}
}

set_values(freq, vol) {
	this.init_box()
	freq = (freq < 1) ? 1 : ((freq > 10) ? 10 : freq)
	vol = (vol < 1) ? 1 : ((vol > 10) ? 10 : vol)
	this.handle.vol = vol;
	this.handle.freq = freq;
	let top = (this.lim.height - this._handlebounds.height) / 9 * (10-vol);
	let left = (this.lim.width - this._handlebounds.width) / 9 * (freq-1);
	this.handle.style.top = `${top}px`;
	this.handle.style.left = `${left}px`;
}

drop_handler(ev) {
	if (ev.type == 'mouseup') {
	document.removeEventListener('mouseup', this.drop_handler);
	document.removeEventListener('mousemove', this.drag_handler);
	} else if (ev.type == 'touchend') {
	document.removeEventListener('touchend', this.drop_handler);
	document.removeEventListener('touchmove', this.drag_handler);
	}
}

get lim() {
	return {
	xmin: this._bounds.left,
	xmax: this._bounds.left + this._bounds.width,
	ymin: this._bounds.top,
	ymax: this._bounds.top + this._bounds.max,
	width: this._bounds.width,
	height: this._bounds.height,
	};
}

}

class Menu {
	constructor(onoffswitch, resetswitch, socket) {
		this.onoff = onoffswitch;
		this.reset = resetswitch;

		this.resethandler = this.resethandler.bind(this);
		this.onoffhandler = this.onoffhandler.bind(this);

		this.onoff.addEventListener('click', this.onoffhandler);
		this.reset.addEventListener('click', this.resethandler);
	    
        	this.socket=socket;
	    
	}

	onoffhandler(ev) {	     
		this.socket.send_command('ONOFF', this.onoff.checked);
	}

	resethandler(ev) {
		this.socket.send_command('RESET', this.reset.checked);
	}
}

var soundbox = document.getElementById("sound-box");
var soundhandle = document.getElementById("sound-handle");
var resethandle = document.getElementById("reset-handle");
var onoffhandle = document.getElementById("onoff-handle");
var user_id = document.getElementById("main").dataset.userid;

//var socket = new Socket("172.24.1.1", '8888', user_id, soundhandle);
var socket = new Socket("127.0.0.1", '8888', user_id, soundhandle); 
var sound = new Soundformer(soundbox, soundhandle);
var menu = new Menu(onoffhandle,resethandle, socket);

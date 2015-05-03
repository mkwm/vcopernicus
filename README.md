# vCopernicus
Simple tool that makes it possible to write code for Internet of Things without actual things available.

## How it works
This tool is fairly simple. It consists of three parts written in Python:
* management helper tool
* coordinating webserver
* serial port handler

Management helper tool allows to conveniently perform actions such as spawning new node or starting coordinating webserver.

Coordinating webserver serves as "hub" for whole cluster of virtualized Copernicus devices - it provides both GUI for user input (buttons, motion, knob rotation) or presenting device state (LEDs, servo dashboard) and API for communicating between web browser (which serves as GUI client) and serial port handler.

Serial port handler translates API events to serial port data and vice versa. At the moment, it works only with serial port (physical or virtual) exposed using UNIX sockets.

Both webserver and handler make extensive use of HTML5 Server-Sent Events mechanism.

## Requirements
You have to use virtualized device in the same way as with physical Copernicus in Mode 2 (via serial port). Mode 1 (direct GPIO access) is currently not supported, sorry.

## Usage
Use of Linux operating system is required (at the moment).

First of all, you should create new Python 2.7 virtualenv. Installing vCopernicus system-wide is not recommended, as this requires superuser rights - also for updating already installed version. It also easier to completely remove virtualenv than to clean every bit of package installed system-wide.

If you use virtualenvwrapper, creating new virtualenv is as simple as writing:
```
mkvirtualenv -p /usr/bin/python2.7 vcopernicus
```

Before using vCopernicus tools, you will need to enter virtualenv:
```
workon vcopernicus
```

Entering virtualenv to run "device code" is not required - just make sure pySerial module is available and run your script as you would do on real Copernicus device (of course, you will need to specify proper virtual serial port path).

You don't have to run nodes and coordinating webserver on single machine (that means you don't have to install webserver module on node - and vice versa). Helper tool is common for both node and coordinator - it automatically detects available commands. If you want to use helper, install vCopernicus egg from this repository:
```
pip install -e 'git+https://github.com/mkwm/iot-vcopernicus.git@develop#egg=vCopernicus&subdirectory=vCopernicus'
```

On the nodes, you have to install vCopernicus-device egg:
```
pip install -e 'git+https://github.com/mkwm/iot-vcopernicus.git@develop#egg=vCopernicus-device&subdirectory=vCopernicus-device'
```

Similar command goes for coordinating webserver:
```
pip install -e 'git+https://github.com/mkwm/iot-vcopernicus.git@develop#egg=vCopernicus-coordinator&subdirectory=vCopernicus-coordinator'
```

#### Coordinating webserver
In order to start coordinating webserver, just invoke ```vcopernicus-coordinator``` comand. You'll be able to see all currently registered devices at http://localhost:8080/. Accessing http://localhost:8080/devices/FOO will create node named __FOO__.

#### Serial port handler
Serial port handler is started using command ```vcopernicus-device```. In order to use it, you need some serial port access/emulation method. In vCopernicus, such method is called transport. Each transport has its unique name and set of parameters. There are also some global parameters:
- ```-c COORDINATOR```, ```--coordinator COORDINATOR``` - specifies coordinating webserver location; it defaults to ```IOT_HYPERVISOR``` environment variable or to ```localhost:8080``` if not set
- ```-n NAME```, ```--name NAME``` - specifies node name; it defaults to ```IOT_NODENAME``` environment variable or to local hostname as returned by ```gethostname()``` call
- ```TRANSPORT_TYPE``` - required; specifies which transport method would be used

Example: to connect as node ```pusheen``` to coordinator ```drogon:5000``` and to use ```magic``` transport method, you should call:
```
vcopernicus-device -n pusheen -c drogon:5000 magic
```

Available transports and their specific arguments are described below.

#### Available transports

##### File descriptor (FD) transport
Transport which serves as base to other transports. It assumes that ```vcopernicus-device``` command would be provided with some already opened file descriptor, which should be used to communicate with device-side code.
- ```-f FD_NUMBER```, ```--fd-number FD_NUMBER``` - file descriptor number

Describing how one can do this is beyound the scope of this documentation. In most cases, this transport method won't be used directly. Check PTY or UNIX socket transport instead.

##### Pseudoterminal (PTY) transport
This method provides device-side code with pseudoterminal. They accept same ioctls as real serial ports do, so device code won't be able to see any difference. This is recommended method of running vCopernicus (if you are not running device operating system separately inside VirtualBox or VMware).
- ```-p PTY_PATH```, ```--pty_path PTY_PATH``` - path of "serial port" to create; **WARNING:** if file with given path exists, it would be removed!

Example:
```
vcopernicus-device pty -p /tmp/ttyS0
```

(Then, use ```Serial('/tmp/ttyS0')``` in your code)

##### UNIX socket transport
Method dedicated for interaction with virtual machines which expose their serial port as UNIX socket (you'll find instructions how to set this up with VirtualBox or VMware). It connects to specified socket as client, so it needs to be created by the other side first.
- ```-p SOCKET_PATH```, ```--socket_path SOCKET_PATH``` - path of UNIX socket to connect to

Example:
```
vcopernicus-device unix -p /tmp/vm_ttyS0.sock
```

###### VirtualBox VM
You can easily connect your virtual machine serial port to UNIX socket outside:

1. Open your VM settings
2. Choose "Serial Ports"
3. Select "Port 1" tab (or "Port 2", if you need...)
4. Check "Enable Serial Port"
5. Select "COM1" as "Port Number" (you can choose different number, but you'll need to adjust serial port path in your code if you do so)
6. Choose "Host Pipe" as "Port Mode"
7. Tick checkbox next to "Create Pipe"
8. Enter whatever path in "Port/File Path" - I suggest using something like ```/tmp/vm_ttyS0.sock```. Make sure you have write permission to this location and you remember it when running serial port handler!
9. Click "OK"
10. Start your VM

###### VMware Player/Workstation
**Note**: By default, VMware adds virtual printer to newly created virtual machines. This printer occupies first serial port. Make sure to change serial port name in your code or to remove virtual printer before following these steps:

1. Open your VM settings
2. Go to "Hardware" tab
3. Click "Add" and select "Serial Port" when wizard appears
4. When asked, select "Output to socket" as serial port type
5. Enter whatever path in blank text input - I suggest using something like ```/tmp/vm_ttyS0.sock```. Make sure you have write permission to this location and you remember it when running serial port handler! Choose "From Server" and "To An Application".
6. Click "Finish" to close wizard and "Save" to commit changes to your VM configuration.
7. Start your VM

## Bugs
Yes.

## See also
* [Copernicus](http://home.agh.edu.pl/~tszydlo/copernicus/) - platform for IoT classes by Tomasz Szydło and Robert Brzoza-Woch
* [Copernicus API](https://github.com/gronostajo/copernicus-api) - convenient Python API for Copernicus by Krzysztof "gronostaj" Śmiałek

## License
vCopernicus itself is provided under the terms of [Creative Commons Attribution-NonCommercial 4.0 International](http://creativecommons.org/licenses/by-nc/4.0/) license.

## External components
vCopernicus includes jQuery, jQuery Knob and gauge.js, all of which are provided under the terms of MIT license:

    The MIT License (MIT)
   
    jQuery: Copyright (c) jQuery Foundation and other contributors
    jQuery Knob: Copyright (c) 2013 Anthony Terrien
    gauge.js: Copyright (c) Bernard Kobos
   
    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# vCopernicus
Simple tool that makes it possible to write code for Internet of Things without actual things available.

## How it works
This tool is fairly simple. It consists of two parts written in Python:
* coordinating webserver
* serial port handler

Coordinating webserver serves as "hub" for whole cluster of virtualized Copernicus devices - it provides both GUI for user input (buttons, motion, knob rotation) or presenting device state (LEDs, servo dashboard) and API for communicating between web browser (which serves as GUI client) and serial port handler.

Serial port handler translates API events to serial port data and vice versa. At the moment, it works only with serial port (physical or virtual) exposed using UNIX sockets.

Both webserver and handler make extensive use of HTML5 Server-Sent Events mechanism.

## Requirements
You have to use virtualized device in the same way as with physical Copernicus in Mode 2 (via serial port). Mode 1 (direct GPIO access) is currently not supported, sorry.

## Usage
Use of Linux operating system is required (at the moment). If you are experienced enough, you can try running real Intel Galileo filesystem image using LXC and PTY serial port emulation.

First of all, clone this repository:

    git clone https://github.com/mkwm/iot-vcopernicus.git

Now you can choose whether you want to use it quickly or to customize your environment.

### Quick
1. Install required modules
   ```
   pip install -r requirements.txt
   ```
   
2. Run coordinating webserver
   ```
   python manager.py start
   ```
   
3. Create your first node
   ```
   python manager.py create_node NODE01
   ```
   
4. Start your first node
   ```
   python manager.py start_node NODE01
   ```
5. Write your code, starting from bootstrap template in ```NODE01/home/code.py```
6. Open your web browser at http://localhost:8080/devices/NODE01
7. Run your code and have fun!
8. When you've finished, stop your node...
   ```
   python manager.py stop_node NODE01
   ```
   
9. And the coordinating webserver
   ```
   python manager.py stop NODE01
   ```

### Customized

#### Coordinating webserver
1. Enter __hypervisor__ directory
   ```
   cd lib/hypervisor
   ```
   
2. Install required modules
   ```
   pip install -r requirements.txt
   ```
   
3. Run webserver
   ```
   python hypervisor.py
   ```

4. At http://localhost:8080/ you can see all currently registered devices. Accessing http://localhost:8080/devices/FOO will create node named __FOO__.

#### Serial port handler
1. Enter __device__ directory
   ```
   cd lib/device
   ```
   
2. Install required modules
   ```
   pip install -r requirements.txt
   ```
   
3. Set ```IOT_HYPERVISOR``` (if different than ```localhost:8080```) and ```IOT_NODENAME``` (if different than hostname) environment variables
   ```
   export IOT_HYPERVISOR=localhost:1234
   export IOT_NODENAME=ETH01
   ```
   
4. Create UNIX socket which emulates serial port (various methods to do it are described in section "Serial port emulation")
5. Run serial port handler
   ```
   python runner.py /tmp/ttyS0.sock
   ```
   
5. Open web browser at http://localhost:8080/devices/ETH01
6. Run your code and have fun! vCopernicus tastes the best with [copernicus-api](https://github.com/gronostajo/copernicus-api) wrapper.

## Serial port emulation
Serial port handler requires you to provide it with path of UNIX socket that emulates serial port. There are several ways to do it.

### PTY serial port emulation
You can (ab)use the way pseudoterminals work - they accept same ioctls as real serial ports do. With simple ```socat``` tool invocation you can attach UNIX socket to PTY created in place of ```/dev/ttyS0``` (you may need to use ```sudo```):
```
socat PTY,link=/dev/ttyS0,mode=666,unlink-close=0 UNIX-LISTEN:/tmp/ttyS0.sock,fork,mode=666
```
This will create appropriate socket at ```/tmp/ttyS0.sock```. If you want to run multiple virtual Copernicus devices on single host, just make sure to substitute ```ttyS0``` with ```ttyS1```, ```ttyS2```... and to run several instances of serial port handler with different ```IOT_NODENAME``` set. Of course, you have to change serial port name in your code for second and next devices; if you are using __copernicus-api__ wrapper, you'll need to construct it like that:
```
from serial import Serial
api = Copernicus(Serial('/dev/ttyS1', 38400))
```

### VirtualBox VM
You can easily connect your virtual machine serial port to UNIX socket outside:

1. Open your VM settings
2. Choose "Serial Ports"
3. Select "Port 1" tab (or "Port 2", if you need...)
4. Check "Enable Serial Port"
5. Select "COM1" as "Port Number" (you can choose different number, but you'll need to adjust serial port path in your code if you do so)
6. Choose "Host Pipe" as "Port Mode"
7. Tick checkbox next to "Create Pipe"
8. Enter whatever path in "Port/File Path" - I suggest using something like ```/tmp/ttyS0.sock```. Make sure you have write permission to this location and you remember it when running serial port handler!
9. Click "OK"
10. Start your VM

### VMware Player/Workstation
**Note**: By default, VMware adds virtual printer to newly created virtual machines. This printer occupies first serial port. Make sure to change serial port name in your code or to remove virtual printer before following these steps:

1. Open your VM settings
2. Go to "Hardware" tab
3. Click "Add" and select "Serial Port" when wizard appears
4. When asked, select "Output to socket" as serial port type
5. Enter whatever path in blank text input - I suggest using something like ```/tmp/ttyS0.sock```. Make sure you have write permission to this location and you remember it when running serial port handler! Choose "From Server" and "To An Application".
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



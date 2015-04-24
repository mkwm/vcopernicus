# vCopernicus
Simple tool that makes it possible to write code for Internet of Things without actual things available.

## How it works
At the moment, this tool is extermely simple. It consists of two parts:
* coordinating webserver
* Python module which mocks ```serial``` module behavior

Coordinating webserver serves as "hub" for whole cluster of virtualized Copernicus devices - it provides both GUI for user input (buttons, motion, knob rotation) or presenting device state (LEDs, servo dashboard) and API for communicating between web browser (which serves as GUI client) and code "on device".

Python module translates API events to serial port data and vice versa.

Both webserver and Python module make extensive use of HTML5 Server-Sent Events mechanism.

## Requirements
You have to use virtualized device in the same way as with physical Copernicus in Mode 2, using Python ```serial``` module). Mode 1 and other means of interaction are currently not supported, sorry.

## Usage
Use of Linux operating system is recommended. If you are experienced enough, you can try running real Intel Galileo filesystem image using LXC, with ```serial``` module replaced.

First of all, clone this repository:

    git clone https://github.com/mkwm/iot-vcopernicus.git

### Coordinating webserver
1. Enter __hypervisor__ directory
       cd hypervisor
2. Install required modules
       pip install requirements.txt
3. Run webserver
       python hypervisor.py
4. At http://localhost:5000/ you can see all currently registered devices. Accessing http://localhost:5000/FOO will create node named __FOO__.

### Python module
1. Enter __device__ directory
       cd device
2. Install required modules
       pip install requirements.txt
3. Write your code making sure you use mocked ```serial``` module
4. Set ```IOT_HYPERVISOR``` and ```ION_NODENAME``` environment variables
       export IOT_HYPERVISOR=localhost:5000
       export IOT_NODENAME=ETH01
4. Open web browser at http://localhost:5000/ETH01
5. Run your code and have fun!

## Bugs
Yes.

Because of the way mocked module works (spawning additional thread in background), you will need to forcefully close script as ```Ctrl+C``` would be (probably) ineffective. Sending SIQUIT (```Ctrl+Shift+\```)  should work.

Note that current code was created mostly as proof-of-concept. It would be rewritten from scratch, probably.

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

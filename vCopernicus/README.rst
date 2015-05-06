vCopernicus Management Helper Tool
==================================

This is simple tool which helps with management of vCopernicus coordinator and nodes. Other vCopernicus modules may register their commands and they would be available using this tool.

Installation
------------
You should use pip package manager: ::

    pip install -e "git+https://github.com/mkwm/iot-vcopernicus.git@develop#egg=vCopernicus&subdirectory=vCopernicus"

Usage
-----
Simply invoke ``vcopernicus`` command. You will be greeted with: ::

   Welcome to vCopernicus management shell
   To see list of available commands, type 'help'
   >>> 

Now, you may enter your commands. To see list of currently registered commands, type ``help`` as instructed. To exit interactive shell, type ``quit`` or press Ctrl+C/Ctrl+D (any of these would do the trick). 

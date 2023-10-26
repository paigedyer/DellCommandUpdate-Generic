This program automates the process of updating Dell PCs and laptops using Dell Command | Update.

I uploaded this version as a generic program that would require some adjustments to the code. Inluding adding in file paths to DCU.py and adding an administrator account to startInstall.bat. Administrators will also need to include the Dell Command | Update installer on a file server. It can be found by extracting the contents from Dell's website and copy-pasting the .msi file.

Additionally, the program was run using EV Reach's Process Automation tool, but will successfully run when ran with administrative permissions.

The program checks for the presence of Dell Command | Update in either Program Files or Program Files (x86). If it's not installed, it installs the file from a network file server. The program then checks for updates and installs any available updates. 

I am currently in the process of ironing bumps and adding more error handling processes, but this program already works great if you have many computers to administrate remotely.

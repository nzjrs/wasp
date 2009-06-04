from distutils.core import setup

setup(name = "libppz",
    version = "0.1",
    description = "Module for interfacing with paparazzi UAV",
    author = "John Stowers",
    author_email = "john.stowers@gmail.com",
    packages = ["ppz", "ppz.ui"],
    scripts = ["booz-serial-monitor.py"],
    long_description = "Module for interfacing with paparazzi UAV" 
) 


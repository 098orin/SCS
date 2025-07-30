import os
import requests
import ctypes
import value
import tools

tools.install_if_not_exists("cryptography")
tools.install_if_not_exists("scratchattach")
tools.install_if_not_exists("rich")

path = value.path

#!/usr/bin/python

import time
import explorerhat

explorerhat.motor.two.forward(100)

time.sleep(1)

explorerhat.motor.two.stop()

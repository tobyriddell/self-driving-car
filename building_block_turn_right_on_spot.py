#!/usr/bin/python

import time
import explorerhat

explorerhat.motor.two.forward(20)
explorerhat.motor.one.backward(20)

time.sleep(1)

explorerhat.motor.two.stop()

#!/usr/bin/env python

try:
	from PyDect200 import PyDect200
except:
	print(u'PyDect200 is not installed!')
	print(u'run: pip install PyDect200')
	exit()
import getpass

print(u"Welcome to PyDect200, the Python AVM-DECT200 API")
fritzbox_pw = getpass.getpass(prompt='Please insert your fritzbox-password: ', stream=None)
print(u'Thank you, please wait few seconds...')
f = PY_DECT200(fritzbox_pw)
try:
	info = f.get_info()
	power = f.get_power_all()
	names = f.get_device_names()
except Exception, e:
    print(u'HTTP-Error, wrong password?')
    exit()
    
print(u'')
for dev_id in info.keys():
	print(u"Device ID:    %s" % dev_id)
	print(u"Device Name:  %s" % names.get(dev_id))
	print(u"Device State: %s" % ('ON' if info.get(dev_id) == '1' else 'OFF'))
	print(u"Device Power: %sW" % (float(power.get(dev_id)) / 1000))
	print(u'')

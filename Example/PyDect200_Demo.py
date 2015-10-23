#!/usr/bin/env python
# -- coding: utf-8 --

try:
        from PyDect200 import PyDect200
except:
        print(u'PyDect200 is not installed!')
        print(u'run: pip install PyDect200')
        exit()
import getpass


print(u"Welcome to PyDect200 v%s, the Python AVM-DECT200 API" % PyDect200.__version__)
fritzbox_pw = getpass.getpass(prompt='Please insert your fritzbox-password: ', stream=None)
print(u'Thank you, please wait few seconds...')
f = PyDect200(fritzbox_pw)
try:
        info = f.get_info()
        power = f.get_power_all()
        names = f.get_device_names()
except Exception:
    print(u'HTTP-Error, wrong password?')
    exit()

print(u'')
for dev_id in info.keys():
        print(u"Device ID:           %s" % dev_id)
        dev_name = names.get(dev_id)
        try:
            print(u"Device Name:         %s" % dev_name.decode('utf-8'))
        except:
            print(u"Device Name:         %s" % unicode(dev_name, errors='ignore'))
        print(u"Device State:        %s" % ('ON' if info.get(dev_id) == '1' else 'OFF'))
        dev_power = power.get(dev_id)
        if dev_power.isdigit():
            dev_power = float(dev_power) / 1000
        print(u"Device Power:        %sW" % dev_power)
        print(u"Device Energy:       %sWh" % f.get_energy_single(dev_id))
        print(u"Device Temperature:  %s degree Celsius  " % (f.get_temperature_single(dev_id)))
        print(u'')

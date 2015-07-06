try:
	from fritzl.fritzl import Fritzl
except:
	print(u'Fritzl is not installed!')
	print(u'run: pip install fritzl')
	exit()
import getpass

print(u"Welcome to Fritzl, the Python AVM-DECT200 API")
fritzbox_pw = getpass.getpass(prompt='Please insert your fritzbox-password: ', stream=None)
print(u'Thank you, please wait few seconds...')
f = Fritzl(fritzbox_pw)
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

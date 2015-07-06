Fritzl
======

[![Download format](https://pypip.in/format/Fritzl/badge.png)](https://pypi.python.org/pypi/Fritzl/)
[![Downloads](https://pypip.in/download/Fritzl/badge.png)](https://pypi.python.org/pypi/Fritzl/)
[![Egg Status](https://pypip.in/egg/Fritzl/badge.png)](https://pypi.python.org/pypi/Fritzl/)
[![License](https://pypip.in/license/Fritzl/badge.png)](https://pypi.python.org/pypi/Fritzl/)
[![Latest Version](https://pypip.in/version/Fritzl/badge.png)](https://pypi.python.org/pypi/Fritzl/)
[![Wheel Status](https://pypip.in/wheel/Fritzl/badge.png)](https://pypi.python.org/pypi/Fritzl/)


Control the Fritz-AVM DECT200 (switch a electric socket)

### Install

```
pip install Fritzl
```


### Example

```
In [1]: from Fritzl.Fritzl import Fritzl
In [2]: f = Fritzl('fitzbox_password')
In [3]: f.get_device_names()
Out[3]: {'16': 'Beleuchtung', '17': 'Fernseher'}
In [4]: f.get_info()
Out[4]: {u'16': u'0', u'17': u'0'}
In [5]: f.switch_onoff(16,1)
Out[5]: 
		{u'DeviceID': u'16',
		 u'RequestResult': u'1',
		 u'Value': u'0',
		 u'ValueToSet': u'1'}
In [6]: f.get_power()
Out[6]: {u'16': 68.95, u'17': 0.0}
```

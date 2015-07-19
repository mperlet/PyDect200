PY_DECT200 ( renamed Fritzl-Package)
======

[![Download format](http://img.shields.io/pypi/format/PY_DECT200.svg)](https://pypi.python.org/pypi/PY_DECT200/)
[![Downloads](http://img.shields.io/pypi/dm/PY_DECT200.svg)](https://pypi.python.org/pypi/PY_DECT200/)
[![License](http://img.shields.io/pypi/l/PY_DECT200.svg)](https://pypi.python.org/pypi/PY_DECT200/)
[![Latest Version](http://img.shields.io/pypi/v/PY_DECT200.svg)](https://pypi.python.org/pypi/PY_DECT200/)


Control the Fritz-AVM DECT200 (switch a electric socket)

### Install

```
pip install PY_DECT200
```

### Demo

```
git clone git@github.com:mperlet/PY_AVMDECT200.git

./PY_AVMDECT200/Example/PY_DECT200_Demo.py
```

### Example Code

```
In [1]: from PY_DECT200 import PY_DECT200
In [2]: f = PY_DECT200('fitzbox_password')
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

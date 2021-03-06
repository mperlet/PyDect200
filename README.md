PyDect200
======
[![Build Status](https://travis-ci.org/mperlet/PyDect200.svg?branch=master)](https://travis-ci.org/mperlet/PyDect200)
![pylint Score](https://mperlet.github.io/pybadge/badges/9.12.svg)
[![Download format](http://img.shields.io/pypi/format/PyDect200.svg)](https://pypi.python.org/pypi/PY_DECT200/)
[![Downloads](http://img.shields.io/pypi/dm/PyDect200.svg)](https://pypi.python.org/pypi/PY_DECT200/)
[![License](http://img.shields.io/pypi/l/PyDect200.svg)](https://pypi.python.org/pypi/PY_DECT200/)
[![Latest Version](http://img.shields.io/pypi/v/PyDect200.svg)](https://pypi.python.org/pypi/PY_DECT200/)


Control the Fritz-AVM DECT200 (switch a electric socket)
and Fritz-AVM PowerLine 546E

### Install

```
pip install PyDect200
```

### Demo

#### Demo (Github Style)

```
curl https://raw.githubusercontent.com/mperlet/PyDect200/master/Example/PyDect200_Demo.py | python
```

#### Demo (git clone)

```
git clone git@github.com:mperlet/PyDect200.git

./PyDect200/Example/PyDect200_Demo.py
```

### Example Code

```
from PyDect200 import PyDect200
f = PyDect200('fitzbox_password')
# or with username PyDect200('fritzbox_password', username='fritzbox_username')

f.get_device_names()
# {'16': 'Beleuchtung', '17': 'Fernseher'}

f.get_info()
# {u'16': u'0', u'17': u'0'}

f.switch_onoff(16,1)
#		{u'DeviceID': u'16',
#		 u'RequestResult': u'1',
#		 u'Value': u'0',
#		 u'ValueToSet': u'1'}

f.get_power()
# {u'16': 68.95, u'17': 0.0}
```

### Tested with

* Python2.7 / Python3.4
* Fritzbox 7270
* FRITZ!OS: 06.05
* AVM Dect200

******************

* Python2.7
* Fritzbox 7490
* FRITZ!OS: 6.36 Labor
* Dect200
* PowerLine 546E

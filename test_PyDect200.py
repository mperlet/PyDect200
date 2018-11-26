from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import unittest

from PyDect200.PyDect200 import PyDect200

try:
    from unittest.mock import patch, MagicMock  # Py3
except Exception:
    from mock import patch, Mock  # Py2

PY2 = 2
PY3 = 3


def run(python_version):
    def run_decorator(func):
        def function_wrapper(x):
            if (sys.version_info > (3, 0)) and python_version == PY3:
                func(x)
            elif (sys.version_info < (3, 0)) and python_version == PY2:
                func(x)
            else:
                return True

        return function_wrapper

    return run_decorator


class TestPyDect200(unittest.TestCase):

    @run(PY2)
    @patch('PyDect200.urllib2.urlopen')
    def test_basic_commands_py2(self, mock_urlopen):
        cm = Mock()
        cm.read.side_effect = ['<Challenge>1234</Challenge>',
                               '<SID>caffeaffe1234</SID>',
                               'device1,device2,device3', 'true']
        mock_urlopen.return_value = cm

        instance = PyDect200("testtest")

        self.assertEqual(instance.sid, 'caffeaffe1234')

        self.assertEqual(instance.get_device_ids(),
                         ['device1', 'device2', 'device3'])
        self.assertEqual(instance.switch_onoff('device1', True), 'true')

    @run(PY2)
    @patch('PyDect200.PyDect200.get_sid')
    def test_session_id_py2(self, mock_sid):
        mock_sid.return_value = "hey"

        instance = PyDect200("testtest")
        instance.sid = 'caffeaffe1234'
        self.assertEqual(instance.sid, 'caffeaffe1234')

    @run(PY3)
    @patch('urllib.request.urlopen')
    def test_basic_commands_py3(self, mock_urlopen):
        cm = MagicMock()
        cm.read.side_effect = ['<Challenge>1234</Challenge>'.encode(),
                               '<SID>caffeaffe1234</SID>'.encode(),
                               'device1,device2,device3'.encode(),
                               'true'.encode()]
        mock_urlopen.return_value = cm

        instance = PyDect200("testtest")

        self.assertEqual(instance.sid, 'caffeaffe1234')

        self.assertEqual(instance.get_device_ids(),
                         ['device1', 'device2', 'device3'])
        self.assertEqual(instance.switch_onoff('device1', True), 'true')


if __name__ == '__main__':
    unittest.main()

# -- coding: utf-8 --

"""
Module to Control the AVM DECT200 Socket
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import hashlib, sys
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

class PyDect200(object):
    """
    Class to Control the AVM DECT200 Socket
    """
    __version__ = u'0.0.15'
    __author__ = u'Mathias Perlet'
    __author_email__ = u'mathias@mperlet.de'
    __description__ = u'Control Fritz AVM DECT200'

    __fritz_url = u'http://fritz.box'
    __homeswitch = u'/webservices/homeautoswitch.lua'

    __debug = False

    def __init__(self, fritz_password):
        """The constructor"""
        self.__password = fritz_password
        self.get_sid()


    def set_url(self, url):
        """Set alternative url"""
        self.__fritz_url = url


    def __homeauto_url_with_sid(self):
        """Returns formatted uri"""
        return u'%s%s?sid=%s' % (self.__fritz_url,
                                 self.__homeswitch,
                                 self.sid)

    @classmethod
    def __query(cls, url):
        """Reads a URL"""
        try:
            return urllib2.urlopen(url).read().decode('utf-8').replace('\n', '')
        except urllib2.HTTPError:
            _, exception, _ = sys.exc_info()
            if cls.__debug:
                print('HTTPError = ' + str(exception.code))
        except urllib2.URLError:
            _, exception, _ = sys.exc_info()
            if cls.__debug:
                print('URLError = ' + str(exception.reason))
        except Exception:
            _, exception, _ = sys.exc_info()
            if cls.__debug:
                print('generic exception: ' + str(exception))
                raise
            pass
        return "inval"



    def __query_cmd(self, command, device=None):
        """Calls a command"""
        url = u'%s&switchcmd=%s' % (self.__homeauto_url_with_sid(), command)
        if device is None:
            return self.__query(url)
        else:
            return self.__query('%s&ain=%s' % (url, device))

    def get_sid(self):
        """Returns a valid SID"""
        base_url = u'%s/login_sid.lua' % self.__fritz_url
        get_challenge = None
        try:
            get_challenge = urllib2.urlopen(base_url).read().decode('ascii')
        except urllib2.HTTPError as exception:
            print('HTTPError = ' + str(exception.code))
        except urllib2.URLError as  exception:
            print('URLError = ' + str(exception.reason))
        except Exception as exception:
            print('generic exception: ' + str(exception))
            raise


        challenge = get_challenge.split(
            '<Challenge>')[1].split('</Challenge>')[0]
        challenge_b = (
            challenge + '-' + self.__password).encode().decode('iso-8859-1').encode('utf-16le')

        md5hash = hashlib.md5()
        md5hash.update(challenge_b)

        response_b = challenge + '-' + md5hash.hexdigest().lower()
        get_sid = urllib2.urlopen('%s?response=%s' % (base_url, response_b)).read().decode('utf-8')
        self.sid = get_sid.split('<SID>')[1].split('</SID>')[0]

    def get_info(self):
        """Returns device info"""
        return self.get_state_all()

    def switch_onoff(self, device, status):
        """Switch a Socket"""
        if status == 1 or status == True or status == '1':
            return self.switch_on(device)
        else:
            return self.switch_off(device)

    def switch_toggle(self, device):
        """Toggles the current state of the given device"""
        state = self.get_state(device)
        if(state == '1'):
            return self.switch_off(device)

        elif(state == '0'):
            return self.switch_on(device)
        else:
            return state

    def get_power(self):
        """Returns the Power in Watt"""
        power_dict = self.get_power_all()
        for device in power_dict.keys():
            power_dict[device] = float(power_dict[device]) / 1000.0
        return power_dict

    def get_device_ids(self):
        """Returns a list of device id strings"""
        return self.__query_cmd('getswitchlist').split(',')

    def get_device_names(self):
        """Returns a Dict with devicenames"""
        dev_names = {}
        for device in self.get_device_ids():
            dev_names[device] = self.get_device_name(device)
        return dev_names

    def get_device_name(self, device):
        """Returns the name for a single device"""
        return self.__query_cmd('getswitchname', device)

    def get_power_single(self, device):
        """Returns the power in mW for a single device"""
        return self.__query_cmd('getswitchpower', device)

    def get_energy_single(self, device):
        """Returns the energy in Wh for a single device"""
        return self.__query_cmd('getswitchenergy', device)

    def get_temperature_single(self, device):
        """Returns the temperature in 0.1 °C for a single device"""
        temp_str = self.__query_cmd('gettemperature', device)
        if temp_str.lstrip('-').isdigit():
            return float(temp_str) / 10.0
        return 'inval'

    def get_power_all(self):
        """Returns the power in mW for all devices"""
        power_dict = {}
        for device in self.get_device_names().keys():
            power_dict[device] = self.get_power_single(device)
        return power_dict

    def switch_on(self, device):
        """Switch device on"""
        return self.__query_cmd('setswitchon', device)


    def switch_off(self, device):
        """Switch device off"""
        return self.__query_cmd('setswitchoff', device)


    def get_state(self, device):
        """Returns the device state"""
        return self.__query_cmd('getswitchstate', device)

    def get_state_all(self):
        """Returns all device states"""
        state_dict = {}
        for device in self.get_device_names().keys():
            state_dict[device] = self.get_state(device)
        return state_dict

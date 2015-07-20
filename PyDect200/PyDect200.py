"""
Module to Control the AVM DECT200 Socket
"""
from __future__ import print_function
import hashlib, urllib2


class PyDect200(object):
    """
    Class to Control the AVM DECT200 Socket
    """
    __version__ = u'0.0.8'
    __author__ = u'Mathias Perlet'
    __author_email__ = u'mathias@mperlet.de'
    __description__ = u'Control Fritz AVM DECT200'

    __fritz_url = u'http://fritz.box'
    __homeswitch = u'/webservices/homeautoswitch.lua'

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

    def get_sid(self):
        """Returns a valid SID"""
        base_url = u'%s/login_sid.lua' % self.__fritz_url
        get_challenge = None
        try:
            get_challenge = urllib2.urlopen(base_url).read()
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
            challenge + '-' + self.__password).decode('iso-8859-1').encode('utf-16le')

        md5hash = hashlib.md5()
        md5hash.update(challenge_b)

        response_b = challenge + '-' + md5hash.hexdigest().lower()
        get_sid = urllib2.urlopen('%s?response=%s' % (base_url, response_b)).read()
        self.sid = get_sid.split('<SID>')[1].split('</SID>')[0]

    def get_info(self):
        """Returns device info"""
        return self.get_state_all()

    def switch_onoff(self, device, status):
        """Switch a Socket"""
        if status == 1:
            return self.switch_on(device)
        else:
            return self.switch_off(device)

    def get_power(self):
        """Returns the Power in Watt"""
        power_dict = self.get_power_all()
        for device in power_dict.keys():
            power_dict[device] = float(power_dict[device]) / 1000.0
        return power_dict

    def get_device_names(self):
        """Returns a Dict with devicenames"""
        url = u'%s&switchcmd=getswitchlist' % (self.__homeauto_url_with_sid())
        url_names = u'%s&switchcmd=getswitchname&ain=' % (self.__homeauto_url_with_sid())
        dev_names = {}
        devices = self.__query(url).split(',')
        for device in devices:
            dev_names[device] = self.__query(url_names + device)
        return dev_names

    def get_power_single(self, device):
        """Returns the power in mW for a single device"""
        cmd = u'%s&switchcmd=getswitchpower&ain=%s' % (self.__homeauto_url_with_sid(), device)
        return self.__query(cmd)

    def get_power_all(self):
        """Returns the power in mW for all devices"""
        power_dict = {}
        for device in self.get_device_names().keys():
            power_dict[device] = self.get_power_single(device)
        return power_dict

    def switch_on(self, device):
        """Switch device on"""
        cmd = u'%s&switchcmd=setswitchon&ain=%s' % (self.__homeauto_url_with_sid(), device)
        return self.__query(cmd)

    def switch_off(self, device):
        """Switch device off"""
        cmd = u'%s&switchcmd=setswitchoff&ain=%s' % (self.__homeauto_url_with_sid(), device)
        return self.__query(cmd)

    #def switch_toggle(self, device):
    #    cmd = u'%s&switchcmd=setswitchtoggle&ain=%s' % (self.__homeauto_url_with_sid(), device)
    #    return self.__query(cmd)

    def get_state(self, device):
        """Returns the device state"""
        cmd = u'%s&switchcmd=getswitchstate&ain=%s' % (self.__homeauto_url_with_sid(), device)
        return self.__query(cmd)

    def get_state_all(self):
        """Returns all device states"""
        state_dict = {}
        for device in self.get_device_names().keys():
            state_dict[device] = self.get_state(device)
        return state_dict

    @classmethod
    def __query(cls, url):
        """Reads a URL"""
        return urllib2.urlopen(url).read().replace('\n', '')

import hashlib, urllib, sys, urllib2, json


class Fritzl(object):
	
	__fritz_url = u'http://fritz.box'
	__homeswitch = u'/webservices/homeautoswitch.lua'
	
	def __init__(self, fritz_password):
		self.__password = fritz_password
		self.get_sid()
		
		
	def set_url(self, url):
		self.__fritz_url = url

	
	def __homeauto_url_with_sid(self):
		return u'%s%s?sid=%s' % (self.__fritz_url,
						 self.__homeswitch,
						 self.sid)

	def get_sid(self):
		base_url = u'%s/login_sid.lua' % self.__fritz_url
		try:
			get_challenge = urllib2.urlopen(base_url).read()
		except:
			print(u'error: host not found')

		
		challenge = get_challenge.split(
						'<Challenge>')[1].split('</Challenge>')[0]
		challenge_b = (challenge + '-' + self.__password).decode(
						'iso-8859-1').encode('utf-16le')
		
		m = hashlib.md5()
		m.update(challenge_b)
		
		response_b = challenge + '-' + m.hexdigest().lower()
		get_sid = urllib2.urlopen(
					'%s?response=%s' % (base_url, response_b)).read()
		self.sid = get_sid.split('<SID>')[1].split('</SID>')[0]
	
	def get_info(self):
		return self.get_state_all()

	def switch_onoff(self, device, status):
		if status == 1:
			return self.switch_on(self, device)
		else:
			return self.switch_off(self, device)
		
	def get_power(self):
		power_dict = self.get_power_all()
		for device in power_dict.keys():
			print power_dict[device]
			power_dict[device] = float(power_dict[device]) / 1000.0
		return power_dict
		
	def get_device_names(self):
		url = u'%s&switchcmd=getswitchlist' % (self.__homeauto_url_with_sid())
		url_names = u'%s&switchcmd=getswitchname&ain=' % (self.__homeauto_url_with_sid())
		dev_names = {}
		devices = self.__query(url).split(',')
		for device in devices:
			dev_names[device] = self.__query(url_names + device)
		return dev_names
		
	def get_power_single(self, device):
		cmd = u'%s&switchcmd=getswitchpower&ain=%s' % (self.__homeauto_url_with_sid(), device)
		return self.__query(cmd)
	
	def get_power_all(self):
		power_dict = {}
		for device in self.get_device_names().keys():
			power_dict[device] = self.get_power_single(device)
		return power_dict
	
	def switch_on(self, device):
		cmd = u'%s&switchcmd=setswitchon&ain=%s' % (self.__homeauto_url_with_sid(), device)
		return self.__query(cmd)
	
	def switch_off(self, device):
		cmd = u'%s&switchcmd=setswitchoff&ain=%s' % (self.__homeauto_url_with_sid(), device)
		return self.__query(cmd)
	
	#def switch_toggle(self, device):
	#	cmd = u'%s&switchcmd=setswitchtoggle&ain=%s' % (self.__homeauto_url_with_sid(), device)
	#	return self.__query(cmd)
	
	def get_state(self, device):
		cmd = u'%s&switchcmd=getswitchstate&ain=%s' % (self.__homeauto_url_with_sid(), device)
		return self.__query(cmd)

	def get_state_all(self):
		state_dict = {}
		for device in self.get_device_names().keys():
			state_dict[device] = self.get_state(device)
		return state_dict
	
	def __query(self, url):
		return urllib2.urlopen(url).read().replace('\n', '')

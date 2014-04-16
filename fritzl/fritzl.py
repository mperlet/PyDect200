import hashlib, urllib, sys, urllib2, json


class Fritzl(object):
	
	__fritz_url = u'http://fritz.box'
	__lua_script = u'/net/home_auto_query.lua'

	def __init__(self, fritz_password):
		self.__password = fritz_password
		self.get_sid()
		
		
	def set_url(self, url):
		self.__fritz_url = url
	
	def __lua_url_with_sid(self):
		return u'%s%s?sid=%s' % (self.__fritz_url,
								 self.__lua_script,
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
		command = u'AllOutletStates'
		pre = u'xhr=1&t1390731922458=nocache'
		url = u'%s&command=%s&%s' % (self.__lua_url_with_sid(),
									 command,pre)
		response = json.loads(urllib2.urlopen(url).read())
		result = {}
		for key in response.keys():
			if key.startswith('DeviceID'):
				dev_number = key.split('_')[1]
				status = response['DeviceSwitchState_%s' % dev_number]
				result[response[key]] = status
		return result

	def switch_onoff(self, device_nr, status):
		url = u'%s%s' % (self.__fritz_url, self.__lua_script)
		http_header = {
			"Origin" : self.__fritz_url,
			"Referer": self.__lua_url_with_sid(),
			}
						
		params = {
		  'command' : 'SwitchOnOff',
		  'id' : device_nr,
		  'value_to_set' : status,
		  'xhr' : '1',
		  'sid' : self.sid,
		}

		req = urllib2.Request(url,
							  urllib.urlencode(params),
							  http_header)
		return json.loads(urllib2.urlopen(req).read())

	def get_power(self):
		watts = {}
		for device in self.get_info().keys():
						
			command = u'EnergyStats_10&id=%s' % device
			pre = u'xhr=1&t1390731922458=nocache'
			url = u'%s&command=%s&%s' % (self.__lua_url_with_sid(),
									   command,
									   pre)
			response = json.loads(urllib2.urlopen(url).read())
			watt_float = float(response['EnStats_max_value']) / 100
			watts[device] = watt_float
		return watts

	def get_device_names(self):
		def get_element(obj):
			return obj.pop().getchildren().pop()
		
		try:
			from pyquery import PyQuery as pq
		except ImportError:
			print('ImportError: please install pyquery')

		doc = pq(url=u'	%s/net/home_auto_overview.lua?sid=%s' % (
					 self.__fritz_url, self.sid))
					 
		dev_count = doc('.zebra > tr').size()
		
		return_dict = {}
		
		for dev_id in range(2, dev_count + 1):
			id_sel = '.zebra > tr:nth-child(%s) > td.c1 > nobr' % (
					 dev_id)
			name_sel = '.zebra > tr:nth-child(%s) > td.c2 > nobr' % (
					 dev_id)
			
			dev_nr = get_element(doc(id_sel)).attrib['id']
			name = get_element(doc(name_sel)).attrib['title']
			
			return_dict[dev_nr.split('_')[1]] = name
		
		return return_dict

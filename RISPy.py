#!python3
'''
Implementation of the RIS interface to Cisco Unified Communications Manager.
'''

import base64
import urllib.request
import xml.etree.ElementTree as etree
import json

''' Specifies what variables/functions are available '''
__all__ = ["cmserver", "cmport", "username", "password", "SOAPAction", "selectCmDeviceExt"]

''' *** SET UP DEBUG *** '''
DEBUG = False
if DEBUG:
	from http.client import HTTPConnection
	HTTPConnection.debuglevel = 1


''' *** SET UP VARIABLES *** '''
cmserver = '172.16.7.41'
cmport = '8443'
RIS70wsdl = 'https://' + cmserver + ':' + cmport + '/realtimeservice2/services/RISService70?wsdl'
RIS70location = 'https://' + cmserver + ':' + cmport + '/realtimeservice2/services/RISService70'
username = 'risuser'
password = 'password'
SOAPAction = 'CUCM:DB ver=9.1'

credentials = username + ':' + password
credentialsbytes = credentials.encode('utf8')
base64EncodedCredentials = base64.encodebytes(credentialsbytes)
 




def selectCmDeviceExt(selectItems, nodeName='', selectBy='Name', deviceClass='Phone', model='255', status ='Any', protocol='Any', downloadStatus='Any'):
	'''
	Allows clients to perform Unified CM device-related queries and provides the latest device status eliminating duplicates if any

	Parameters: 
		deviceClass - Specifies the device class type that needs to be queried for the real-time status. 
			The following options are available: 
			- Any 
			- Phone (Default)
			- Gateway
			- H323
			- Cti
			- VoiceMail
			- MediaResources
			- SIP Trunk
			- HuntList
			- Unknown
		model - Model of the device. 255 (Default) specifies all models.
		status - Specifies the status of the device. The following options are available:
			- Any 
			- Registered (Default)
			- UnRegistered
			- Rejected
			- PartiallyRegistered
			- Unknown
		nodeName - Specifies the server name where search is performed. If no name is specified, 
			then all the servers within the cluster will be searched 
		selectItems - Specifies the array of items for which you can specify the search criteria.
		selectBy - Specifies the Unified CM selection types during the search to RISDC. 
			The following options are available:
			- Name (Default)
			- IPV4Address
			- IPV6Address
			- DirNumber
			- Description
			- SIPStatus for SIP Trunk
		protocol - Specifies the protocol name in the search criteria. The following options are available:
			- Any (Default)
			- SCCP
			- SIP
			- Unknown
		downloadStatus - Specifies the download status of the application. The following options are available:
			- Any (Default)
			- Upgrading
			- Successful
			- Failed
			- Unknown

	Returns   : List of servers and devices
	'''

	''' Set up variables, in case they were changed '''
	RIS70wsdl = 'https://' + cmserver + ':' + cmport + '/realtimeservice2/services/RISService70?wsdl'
	RIS70location = 'https://' + cmserver + ':' + cmport + '/realtimeservice2/services/RISService70'
	credentials = username + ':' + password
	credentialsbytes = credentials.encode('utf8')
	base64EncodedCredentials = base64.encodebytes(credentialsbytes)
 	

	''' *** SOAP Envelope *** '''
	selectCmDeviceExtSOAP =  '<SOAP-ENV:Envelope xmlns:ns0="http://schemas.cisco.com/ast/soap" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">'
	selectCmDeviceExtSOAP += '<SOAP-ENV:Header/>'
	selectCmDeviceExtSOAP += '<ns1:Body>'
	selectCmDeviceExtSOAP += '<ns0:selectCmDeviceExt>'
	selectCmDeviceExtSOAP += '<ns0:StateInfo></ns0:StateInfo>'
	selectCmDeviceExtSOAP += '<ns0:CmSelectionCriteria>'
	selectCmDeviceExtSOAP += '<ns0:MaxReturnedDevices>1000</ns0:MaxReturnedDevices>'
	selectCmDeviceExtSOAP += '<ns0:DeviceClass>' + deviceClass + '</ns0:DeviceClass>'
	selectCmDeviceExtSOAP += '<ns0:Model>' + model + '</ns0:Model>'
	selectCmDeviceExtSOAP += '<ns0:Status>' + status + '</ns0:Status>'
	selectCmDeviceExtSOAP += '<ns0:NodeName>' + nodeName + '</ns0:NodeName>'
	selectCmDeviceExtSOAP += '<ns0:SelectBy>' + selectBy + '</ns0:SelectBy>'
	selectCmDeviceExtSOAP += '<ns0:SelectItems>'
	for item in selectItems:
		selectCmDeviceExtSOAP += '<ns0:item>'
		selectCmDeviceExtSOAP += '<ns0:Item>' + item + '</ns0:Item>'
		selectCmDeviceExtSOAP += '</ns0:item>'

	# selectCmDeviceExtSOAP += '<ns0:item>'
	# selectCmDeviceExtSOAP += '<ns0:Item>CSFEE</ns0:Item>'
	# selectCmDeviceExtSOAP += '</ns0:item>'
	# selectCmDeviceExtSOAP += '<ns0:item>'
	# selectCmDeviceExtSOAP += '<ns0:Item>SEPF84F5794022A</ns0:Item>'
	# selectCmDeviceExtSOAP += '</ns0:item>'
	# selectCmDeviceExtSOAP += '<ns0:item>'
	# selectCmDeviceExtSOAP += '<ns0:Item>SEP001E136BF578</ns0:Item>'
	# selectCmDeviceExtSOAP += '</ns0:item>'

	selectCmDeviceExtSOAP += '</ns0:SelectItems>'
	selectCmDeviceExtSOAP += '<ns0:Protocol>' + protocol + '</ns0:Protocol>'
	selectCmDeviceExtSOAP += '<ns0:DownloadStatus>' + downloadStatus + '</ns0:DownloadStatus>'
	selectCmDeviceExtSOAP += '</ns0:CmSelectionCriteria>'
	selectCmDeviceExtSOAP += '</ns0:selectCmDeviceExt>'
	selectCmDeviceExtSOAP += '</ns1:Body>'
	selectCmDeviceExtSOAP += '</SOAP-ENV:Envelope>'

	binary_data = selectCmDeviceExtSOAP.encode('utf8')

	try:
		req = urllib.request.Request(RIS70location, binary_data)
		req.add_header('Content-Type', 'text/xml; charset=utf-8')
		req.add_header('SOAPAction', SOAPAction)
		req.add_header('Authorization', 'Basic ' + base64EncodedCredentials.decode('utf-8')[:-1]) # the [:-1] removes the \n -- there is almost certainly a better way to do this.
		f = urllib.request.urlopen(req)
		xmlResponse = f.read().decode('utf-8')
		#return xmlResponse
		return format_ris_response(xmlResponse)
	except urllib.error.HTTPError as e:
	    print(e.headers['www-authenticate'])
	    print(e)

def format_ris_response(xmlResponse):
	result = []
	ns0 = "{http://schemas.xmlsoap.org/soap/envelope/}"
	ns1 = "{http://schemas.cisco.com/ast/soap}"
	root = etree.fromstring(xmlResponse)
	totalDevicesFound = root.findall('.//{0}TotalDevicesFound'.format(ns1))[0].text
	#print(totalDevicesFound)
	if int(totalDevicesFound) > 0:
		cmNodes = root.findall('.//{0}CmNodes'.format(ns1))
		for node in cmNodes:
			cmNodeItems = node.findall('{0}item'.format(ns1))
			for nodeItem in cmNodeItems:
				serverDict = {}
				serverDict['server'] = nodeItem.find('{0}Name'.format(ns1)).text
				devicesArray = []
				cmDevices = nodeItem.findall('{0}CmDevices'.format(ns1))
				for cmDevice in cmDevices:
					cmDeviceItems = cmDevice.findall('{0}item'.format(ns1))
					for detail in cmDeviceItems:
						deviceDict = {}
						for thing in detail:
							deviceDict[thing.tag.split(ns1)[1]] = thing.text
						devicesArray.append(deviceDict)
				#print(devicesArray)
					serverDict['devices'] = devicesArray
					#print(json.dumps(serverDict, indent=1))
					result.append(serverDict)

	#print(json.dumps(result, indent=1))





							#print(thing.tag.split(ns1)[1], thing.text)
							#print(thing.tag.split(ns1,1)[1], thing.text)
						#print(detail.text)
						# name = detail.find('{0}Name'.format(ns1)).text
						# activeLoadID = detail.find('{0}ActiveLoadID'.format(ns1)).text
						# print(name, activeLoadID)
	return(result)

if __name__ == '__main__':
	print('Please use as a module and use help(RISPy) to see usage instructions.')
	print(selectCmDeviceExt(["CSFEE","SEPF84F5794022A","SEP001E136BF578"]))





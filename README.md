RISPy
=====

Implementation of the RIS interface to Cisco Unified Communications Manager.

This is the first draft of this library which only implements the 'selectCmDeviceExt' at present.

## Example Usage

```
import RISPy
RISPy.username = 'someuser'
RISPy.password = 'somepassword'
RISPy.cmserver = '172.16.7.41'
result = RISPy.selectCmDeviceExt(["CSFAA","SEP123456789012","CSFBB"], deviceClass='Any')

for item in result:
    for device in item['devices']:
        print(device['Name'], device['ActiveLoadID'])

```

You can also get help and more information by using `>>> help(RISPy)` 

## Variables

The following shows the available variables and their default settings:

```
    SOAPAction = 'CUCM:DB ver=9.1'
    cmport = '8443'
    cmserver = ''
    password = 'risuser'
    username = 'rispassword'

```

## Functions

The following shows the implemented functions of the RIS interface at this time:

### selectCmDeviceExt

>Allows clients to perform Unified CM device-related queries and provides the latest device status eliminating duplicates if any

```
selectCmDeviceExt(selectItems, nodeName='', selectBy='Name', deviceClass='Phone', model='255', status='Any', protocol='Any', downloadStatus='Any')
```


_Parameters_:

* deviceClass - Specifies the device class type that needs to be queried for the real-time status. The following options are available:  
    * Any    
    * Phone (Default)  
    * Gateway  
    * H323  
    * Cti  
    * VoiceMail  
    * MediaResources  
    * SIP Trunk  
    * HuntList  
    * Unknown  
* model - Model of the device. 255 (Default) specifies all models.
    status - Specifies the status of the device. The following options are available:
    * Any 
    * Registered (Default)
    * UnRegistered
    * Rejected
    * PartiallyRegistered
    * Unknown
* nodeName - Specifies the server name where search is performed. If no name is specified, then all the servers within the cluster will be searched 
* selectItems - Specifies the array of items for which you can specify the search criteria.
* selectBy - Specifies the Unified CM selection types during the search to RISDC. The following options are available:
    * Name (Default)
    * IPV4Address
    * IPV6Address
    * DirNumber
    * Description
    * SIPStatus for SIP Trunk
* protocol - Specifies the protocol name in the search criteria. The following options are available:
    * Any (Default)
    * SCCP
    * SIP
    * Unknown
* downloadStatus - Specifies the download status of the application. The following options are available:
    * Any (Default)
    * Upgrading
    * Successful
    * Failed
    * Unknown

Returns   : Array of devices by server with details.

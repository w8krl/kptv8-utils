import pandas as pd
import glob 
import datetime
import json
import time
import requests
from requests.auth import HTTPBasicAuth

###Function to fetch array of object IDs from the source
def getObjects(url):
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'X-Api-Key' : 'xxx',
		'client-version':'4.9'
	}
	resp = requests.get(url, headers=headers)
	return resp.json


log = 'C:/Users/xxx/OneDrive/Desktop/xxx.txt'
fh = open(log, 'w')

#ES basic security settings
user = 'xxx'
key = 'xxx'

esHeaders = {
    'Content-Type': 'application/json'
}


#Function to process each ID and return JSON object
def getSiteDetails(id):
    data = False
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Api-Key' : 'xxx',
        'client-version':'4.9'
    }
    url="https://api.com?id=" + str(id)

    try:
        data = requests.get(url, headers=headers)
        data = data.json()
        data = data['resources']['chargepoint_locations_placecards']['data'][0]
    except:
        print(f"ID: {id} failed")
    return data

###Call object ID function
evData = getObjects("url")

#Set counter
c = 0

###Iterate object IDs
for i in evData:

	###Call main API function to get lower level detail
	siteData = getSiteDetails(i['id'])
	fh.write(json.dumps(siteData))
	
	###If true, write send the retrieved object for ingestion into elasticsearch
	if (siteData):
		siteData = json.dumps(siteData)
		resp = requests.post('https://xxx.xxx.xxx.xxx:9200/ev/_doc/' + str(i['id']), headers=esHeaders, data=siteData, auth=(user,key), verify=False)
		print(resp)
	c +=1
	print(f"{c} processed\t-\t{len(evData) - c} remaining!")

###Close log file - useful to store downloaded objects and reindex offline
fh.close

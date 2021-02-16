
import requests as req
import urllib.request
import re
import os
import json
import sys
import shutil
import progressbar

def getClienId():
	try:
	  data = req.get("https://m.soundcloud.com")
	  client_id = re.search(r'clientId":"(.*?)",', data.text).group(1)
	  return client_id
	except:
	  print("An exception occurred")
	  sys.exit()


print("Welcome to Python Soundcloud downloader using stream/hls (chunk not progressive links)")
track_link = input("Please give a track url:") 
respo = req.get("https://w.soundcloud.com/player/?url="+track_link)
respo = respo.text.encode('utf-8').decode('ascii', 'ignore')
_result = re.search(r'}}\)},\[(.*?)}]}]', respo).group(1)
_result = _result+"}]}"
_result = json.loads(_result)

stream_url = _result['data'][0]['media']['transcodings'][0]['url']+"?client_id="+getClienId()
print(_result['data'][0]['media']['transcodings'][0]['url'])
title = _result['data'][0]['title']
print(_result['data'][0]['title'])
stream_resp = req.get(stream_url)
stream_resp = stream_resp.json()
stream_mp3 = req.get(stream_resp['url'])
dirName = "temp"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")
result = re.findall(r',(.*?)#', stream_mp3.text, re.DOTALL)
result = [i.replace('\n','') for i in result]
bar = progressbar.ProgressBar(maxval=len(result), \
widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range(len(result)):
	urllib.request.urlretrieve(result[i],  'temp/'+str("{:04d}".format(i)) +'.mp3')
	bar.update(i+1)
bar.finish()
cmd = "cat temp/*.mp3 | \"tools\\ffmpeg\"  -i pipe: -c:a copy -c:v copy \""+title+".mp3\""
os.system(cmd)
shutil.rmtree('temp/')


	
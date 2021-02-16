
import requests as req
import urllib.request
import re
import os
import json
import sys
import shutil
import progressbar
# from PyQt5.QtGui import *

class Handler:

	def getClienId(self):
		try:
		  data = req.get("https://m.soundcloud.com")
		  client_id = re.search(r'clientId":"(.*?)",', data.text).group(1)
		  return client_id
		except:
		  print("An exception occurred")
		  sys.exit()

	def getMp3Track(self,url,bara,QApplication):
		respa = req.get("https://w.soundcloud.com/player/?url="+url)

		respa = respa.text.encode('utf-8').decode('ascii', 'ignore')

		resulta = re.search(r'}}\)},\[(.*?)}]}]', respa).group(1)
		resulta = resulta+"}]}"
		resulta = json.loads(resulta)
		stream_url = resulta['data'][0]['media']['transcodings'][0]['url']+"?client_id="+self.getClienId()
		print(resulta['data'][0]['media']['transcodings'][0]['url'])
		title = resulta['data'][0]['title']
		print(resulta['data'][0]['title'])

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
		jj = 0
		inc = float(100)/len(result)
		for i in range(len(result)):
			urllib.request.urlretrieve(result[i],  'temp/'+str("{:04d}".format(i)) +'.mp3')
			bar.update(i+1)
			jj = jj+inc
			# print(jj)
			bara.setValue(round(jj,0))
			QApplication.processEvents() #  to prevent progressbar and app from freezing
		bar.finish()
		cmd = "cat temp/*.mp3 | \"tools\\ffmpeg\"  -i pipe: -c:a copy -c:v copy \""+title+".mp3\""
		os.system(cmd)

		shutil.rmtree('temp/')  #remove no empty directory



	
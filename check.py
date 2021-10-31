import requests
import schedule
import time
import subprocess
def check():
	try:
		resp = requests.get('http://chal8.web.letspentest.org/screen?url=file:///etc/passwd').json().get('status')
	except:
		subprocess.run(['sudo', 'docker', 'restart', '3f1115475f19'])
	if resp == "Timeout" or resp is None:
		subprocess.run(['sudo', 'docker', 'restart', '3f1115475f19'])

schedule.every(3).minutes.do(check)

while 1:
	schedule.run_pending()
	time.sleep(1)
import requests
import schedule
import time
import subprocess
def check():
	try:
		resp = requests.get('http://chal8.web.letspentest.org/screen?url=file:///etc/passwd', verify=False, timeout=10).json().get('status')
	except:
		print("crash app")
		subprocess.run(['sudo', 'docker', 'restart', '3f1115475f19'])
	print(resp)
	if resp == "Timeout" or resp is None:
		print("timeout")
		subprocess.run(['sudo', 'docker', 'restart', '3f1115475f19'])

schedule.every(3).minutes.do(check)

while 1:
	schedule.run_pending()
	time.sleep(1)
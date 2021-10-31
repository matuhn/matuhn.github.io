from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
import os 
import time 
from concurrent.futures import ThreadPoolExecutor, as_completed

FLAG = "FLAG{10c802c9c6afc26769764b5b986d708a}"

options = Options()
options.headless = True


def define_driver_path():
	if os.name == "nt":
		path = "geckodriver.exe"
	else:
		path = "./geckodriver_linux"
	return path

def botcheck(url, i):
	path = define_driver_path()
	driver = webdriver.Firefox(executable_path=path, options=options)
	driver.get(url)
	try:
		alert = Alert(driver)
		alert.accept()
	except:
		print("no alert")
	driver.add_cookie({'name':'Flag','value': FLAG,'path':'/'})
	driver.get(url)
	try:
		alert = Alert(driver)
		alert.accept()
	except:
		print("no alert")
	driver.quit()
	return i

# def check():
# 	while True:
# 		path = "question"
# 		files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
# 		if len(files) == 0:
# 			pass
# 		else:
# 			for i in files:
# 				url = "http://localhost:8012/question_secret_path_for_admin127637162uyqweudbUWEYQWUIE6843586093uqwyeuqwyeu_khoabdapromax?q=" + i 
# 				print(url)
# 				botcheck(url)
# 				os.remove(path + "/" +i)

def multi_thread():
	while True:
		threads = []
		with ThreadPoolExecutor(max_workers=20) as executor:
			path = "question"
			files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
			if len(files) == 0:
				pass
			else:
				for i in files:
					url = "http://localhost:8012/check?q=" + i 
					print(url)
					threads.append(executor.submit(botcheck, url, i))
					print("[+] Done")
				for task in as_completed(threads):
					i = task.result()
					os.remove(path + "/" +i)

if __name__ == '__main__':
	multi_thread()

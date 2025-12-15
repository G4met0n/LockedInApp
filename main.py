import psutil
import json
import time
from datetime import datetime, timedelta


with open("apps.json", "r") as f:
    apps = json.load(f)
with open("websites.json", "r") as f:
    websites = json.load(f)

def kill_process_by_name(process_name):
    """Kill a process by its name."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                print(f"Killing process {process_name} with PID {proc.info['pid']}")
                proc.kill()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Process {process_name} not found.")
    return False

def block_websites():

    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect_ip = "127.0.0.1"

    with open(hosts_path, "r+") as file:
        content = file.read()
        for site in websites:
            if site not in content:
                file.write(f"\n{redirect_ip} {site}")

def unblock_websites():
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

    with open(hosts_path, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(site in line for site in websites):
                file.write(line)
        file.truncate()

#select how long the program will run
def user_input():
    user_time = int(float(input("Enter time in minutes: "))*60)
    start_time = time.time()
    end_time = start_time + user_time
    time.time() >= end_time
    return end_time




if __name__ == "__main__":
    # returns
    end_time = user_input()

    # Block websites once at the start
    block_websites()
    print("Locked in mode activated. Websites blocked. Applications terminated.")
    
    try:
        # main loop
        while not (time.time() >= end_time):
            for process_to_kill in apps:
                print(f"Checking and killing process: {process_to_kill}")
                kill_process_by_name(process_to_kill)
            time.sleep(5)
    finally:
        # Unblock websites after the loop ends
        unblock_websites()
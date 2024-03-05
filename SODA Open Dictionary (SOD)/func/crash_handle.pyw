import psutil
import subprocess
import os
from necessary_function import get_config
settings=get_config()

with open("func/main_pid.txt", encoding="utf-8") as fi:
    process = psutil.Process(int(fi.read()))
while process.is_running():
    if not process.is_running() and os.path.exists('func/main_pid.txt'):
        settings["boost performance"]="True"
        with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
            for i in settings: fo.write(f"{i}: {settings[i]}\n")
        subprocess.run(["py", "UI.py"], start_new_session=True)
        break

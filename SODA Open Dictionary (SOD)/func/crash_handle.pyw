import subprocess
import sys
import os
from necessary_function import get_config
settings=get_config()

try:
    import psutil
except:
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} -m pip install psutil")
    os.system("py crash_handle.pyw")
else:
    with open("func/main_pid.txt", encoding="utf-8") as fi:
        process = psutil.Process(int(fi.read()))
    while process.is_running():
        if not process.is_running() and os.path.exists('func/main_pid.txt'):
            if process.pid!=int(open("func/main_pid.txt", encoding="utf-8").read()):
                settings["boost performance"]="True"
                with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
                    for i in settings: fo.write(f"{i}: {settings[i]}\n")
                subprocess.run(["py", f"-{sys.version_info.major}.{sys.version_info.minor}", "UI.py"], start_new_session=True)
                break

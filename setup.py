import os
import zipfile
import io
import shutil
import sys
print(f"Python {sys.version_info.major}.{sys.version_info.minor}")

def backup_user_data(data_dir, setting_dir, backup_dir):
    if os.path.exists(setting_dir):
        shutil.copytree(setting_dir, os.path.join(backup_dir, 'setting'))

def restore_user_data(setting_dir, backup_dir):
    if os.path.exists(os.path.join(backup_dir, 'setting')):
        if os.path.exists(setting_dir):
            shutil.rmtree(setting_dir)
            shutil.copytree(os.path.join(backup_dir, 'setting'), setting_dir)
            shutil.rmtree(backup_dir)

try:
    import requests
    import winshell
except:
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} -m pip install pywin32 winshell requests pyinstaller")
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} setup.py")
else:
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} -m pip install kivymd==1.2.0 kivy googletrans==4.0.0rc1 eng-to-ipa pyttsx3 psutil --upgrade pip")
try:
    repo_url = "https://github.com/soda2611/Whoop/archive/refs/heads/main.zip"

    repo_dir = "Whoop-main"

    sod_dir = "Whoop"
    setting_dir = os.path.join(sod_dir, 'func', 'setting')
    backup_dir = os.path.expanduser('~/.whoop_backup')
    
    backup_user_data(data_dir, setting_dir, backup_dir)

    response = requests.get(repo_url)

    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    zip_file.extractall()

    os.system(f"rmdir /S /Q {sod_dir}")

    shutil.move(os.path.join(repo_dir, sod_dir), sod_dir)

    os.system(f"rmdir /S /Q {repo_dir}")

    restore_user_data(data_dir, setting_dir, backup_dir)

    python_file = os.path.abspath(f"{sod_dir}/UI.py")

    icon_file = os.path.abspath(f"{sod_dir}/func/setting/img/Logo.ico")

    desktop = winshell.desktop()

    shortcut_name = "Whoop"

    shortcut = os.path.join(desktop, shortcut_name + ".lnk")

    with winshell.shortcut(shortcut) as link:
        link.path = python_file
        link.description = "An open dictionary for everyone"
        link.arguments = python_file
        link.icon_location = (icon_file, 0)
        link.working_directory = os.path.abspath(sod_dir)
     
except Exception as ex:
    print(ex)


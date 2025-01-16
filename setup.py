import os, zipfile, io, shutil, sys

print(f"Python {sys.version_info.major}.{sys.version_info.minor}")

def backup_user_data(setting_dir, backup_dir):
    if os.path.exists(setting_dir):
        shutil.copytree(setting_dir, os.path.join(backup_dir, 'setting'))

def restore_user_data(setting_dir, backup_dir):
    backup_setting_dir = os.path.join(backup_dir, 'setting')
    if os.path.exists(backup_setting_dir):
        if not os.path.exists(setting_dir):
            os.makedirs(setting_dir)
        for root, dirs, files in os.walk(backup_setting_dir):
            relative_path = os.path.relpath(root, backup_setting_dir)
            target_dir = os.path.join(setting_dir, relative_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
        shutil.rmtree(backup_dir)

def get_data(setting_dir):
    setting_file = os.path.join(setting_dir, 'setting.txt')
    if os.path.exists(setting_file):
        with open(setting_file, "r", encoding="utf-8") as fi:
            setting=fi.readlines()
        settings={}
        for index in setting:
            option, properties=index.strip().split(": ")
            settings[option]=properties
        
        return settings
    return {}
    
def write_data(setting_dir, settings):
    setting_file = os.path.join(setting_dir, 'setting.txt')
    if os.path.exists(setting_file):
        with open(setting_file, "w", encoding="utf-8") as fo:
            for i in settings:
                fo.write(f"{i}: {str(settings[i])}\n")

try:
    import requests
    import winshell
except:
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} -m pip install pywin32 winshell requests pyinstaller")
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} setup.py")
else:
    os.system(f"py -{sys.version_info.major}.{sys.version_info.minor} -m pip install kivymd==1.2.0 kivy googletrans==4.0.0rc1 eng-to-ipa pyttsx3 psutil gtts --upgrade pip")

try:
    repo_url = "https://github.com/soda2611/Whoop/archive/refs/heads/main.zip"
    repo_dir = "Whoop-main"
    sod_dir = "Whoop"
    repo_setup_path = os.path.join(repo_dir, "setup.py")
    setting_dir = os.path.join(sod_dir, 'func', 'setting')
    backup_dir = os.path.expanduser('~/.whoop_backup')
    static_value=['version', 'released date', 'pattern']
    
    settings=get_data(setting_dir)
    backup_user_data(setting_dir, backup_dir)

    response = requests.get(repo_url)

    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    zip_file.extractall()

    os.system(f"rmdir /S /Q {sod_dir}")
    
    with open(repo_setup_path, 'r') as repo_setup_file:
        repo_setup_content = repo_setup_file.read()
    
    with open("setup.py", 'w') as local_setup_file:
        local_setup_file.write(repo_setup_content)

    shutil.move(os.path.join(repo_dir, sod_dir), sod_dir)

    os.system(f"rmdir /S /Q {repo_dir}")

    new_setting=get_data(setting_dir)
    restore_user_data(setting_dir, backup_dir)

    for i in settings:
        if i in new_setting and i not in static_value:
            new_setting[i]=settings[i]

    write_data(setting_dir, new_setting)

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

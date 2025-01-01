import os, zipfile, io, shutil, sys
print(f"Python {sys.version_info.major}.{sys.version_info.minor}")

def backup_user_data(setting_dir, backup_dir):
    if os.path.exists(setting_dir):
        shutil.copytree(setting_dir, os.path.join(backup_dir, 'setting'))

def restore_user_data(setting_dir, backup_dir):
    if os.path.exists(os.path.join(backup_dir, 'setting')):
        if os.path.exists(setting_dir):
            shutil.rmtree(setting_dir)
            shutil.copytree(os.path.join(backup_dir, 'setting'), setting_dir)
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

def write_data(setting_dir, settings):
    setting_file = os.path.join(setting_dir, 'setting.txt')
    with open(setting_file, "w", encoding="utf-8") as fo:
        for i in settings:
            fo.write(f"{i}: {str(settings[i])}\n")

try:
    import requests, psutil
except:
    os.system(f"pip install requests psutil")
    os.system(f"python setup.py")
else:
    os.system(f"pip install kivymd==1.2.0 googletrans==4.0.0rc1 eng-to-ipa pyttsx3 gtts psutil")
try:
    repo_url = "https://github.com/soda2611/Whoop/archive/refs/heads/main.zip"
    repo_dir = "Whoop-main"
    sod_dir = "Whoop"
    repo_setup_path = os.path.join(repo_dir, "setup-for-Pydroid.py")
    setting_dir = os.path.join(sod_dir, 'func', 'setting')
    backup_dir = os.path.expanduser('~/.whoop_backup')
    static_value=['version', 'released date']
    
    settings=get_data(setting_dir)
    backup_user_data(setting_dir, backup_dir)

    response = requests.get(repo_url)

    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    zip_file.extractall()

    os.system(f"rm -rf {sod_dir}")
    
    with open(repo_setup_path, 'r') as repo_setup_file:
        repo_setup_content = repo_setup_file.read()

    with open("setup-for-Pydroid.py", 'w') as local_setup_file:
        local_setup_file.write(repo_setup_content)

    shutil.move(os.path.join(repo_dir, sod_dir), sod_dir)

    os.system(f"rm -rf {repo_dir}")
    
    new_setting=get_data(setting_dir)
    restore_user_data(setting_dir, backup_dir)
    
    for i in settings:
        if i in new_setting and i not in static_value:
            new_setting[i]=settings[i]

    write_data(setting_dir, new_setting)

except Exception as ex:
    print(ex)
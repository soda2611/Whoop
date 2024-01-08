import os
import zipfile
import io
import shutil
try:
    import requests
    import winshell
except:
    os.system("pip install pywin32 winshell requests")
    os.system("setup.py")
else:
    os.system("pip install https://github.com/KivyMD/kivymd/archive/master.zip kivy googletrans==4.0.0rc1 eng-to-ipa pyttsx3 notify-py")

    try:
        repo_url = "https://github.com/soda2611/SODA_Open_Dictionary/archive/refs/heads/main.zip"

        repo_dir = "SODA_Open_Dictionary-main"

        sod_dir = "SODA Open Dictionary"

        response = requests.get(repo_url)

        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        zip_file.extractall()

        shutil.move(os.path.join(repo_dir, sod_dir), sod_dir)

        os.system(f"rmdir /S /Q {repo_dir}")

        python_file = os.path.abspath(f"{sod_dir}/UI.py")

        icon_file = os.path.abspath(f"{sod_dir}/func/Logo.ico")

        desktop = winshell.desktop()

        shortcut_name = "SODA Open Dictionary"

        shortcut = os.path.join(desktop, shortcut_name + ".lnk")

        with winshell.shortcut(shortcut) as link:
            link.path = python_file
            link.description = "An open dictionary for everyone"
            link.arguments = python_file
            link.icon_location = (icon_file, 0)
            link.working_directory = os.path.abspath(sod_dir)
        
    except Exception as ex:
        print(ex)

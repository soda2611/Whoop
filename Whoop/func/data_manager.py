import requests, base64, os

# Thay thế bằng token và URL repo của bạn
token = "g%h%p%_%l%6%b%z%c%z%t%j%6%Q%R%0%q%e%i%W%k%S%l%h%W%U%8%U%4%H%s%6%r%K%0%n%I%K%U%9".replace("%", "")
repo_url = "https://api.github.com/repos/soda2611/Whoop"

def download_file(file_path, name):
    url = f"{repo_url}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        download_url = content["download_url"]
        response = requests.get(download_url)
        with open(name, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error downloading file: {response.text}")

def upload_file(file_path, name):
    url = f"{repo_url}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha']
    else:
        print(f"Error retrieving file SHA: {response.status_code} - {response.text}")
        return

    with open(name, 'rb') as f:
        content = f.read()
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    data = {
        'message': 'Update file',
        'content': encoded_content,
        'sha': sha
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print("File uploaded successfully")
    elif response.status_code == 200:
        print("File updated successfully")
    else:
        print(f"Error uploading file: {response.status_code} - {response.text}")

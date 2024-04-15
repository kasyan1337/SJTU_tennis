import requests

def fetch_github_content(url):
    """
    Fetches the content of a file from GitHub.
    :param url: URL of the file on GitHub.
    :return: Content of the file if successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch file content from GitHub: {e}")
        return None

def is_update_available(local_file_name, remote_content):
    """
    Checks if the local file is different from the remote content.
    :param local_file_name: Name of the local file to compare.
    :param remote_content: Content fetched from the remote repository.
    :return: True if an update is available, False otherwise.
    """
    try:
        with open(local_file_name, 'r', encoding='utf-8') as file:
            local_content = file.read()
        return local_content != remote_content
    except FileNotFoundError:
        print(f"Local file {local_file_name} not found. Assuming update is needed.")
        return True

def update_file(file_name, content):
    """
    Writes the provided content to the file, overwriting it.
    :param file_name: Name of the file to update.
    :param content: New content to write into the file.
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"File {file_name} has been updated to the latest version.")

def update_file_from_github(file_name):
    """
    Checks for updates and asks the user if they want to update the file.
    :param file_name: Name of the file to check and potentially update.
    """
    base_url = "https://raw.githubusercontent.com/kasyan1337/SJTU_tennis/master/"
    url = f"{base_url}{file_name}"

    remote_content = fetch_github_content(url)
    if remote_content is None:
        print("Could not retrieve the file from GitHub. Update aborted.")
        return

    if is_update_available(file_name, remote_content):
        user_decision = input("An update is available. Do you want to update? [y/n]: ")
        if user_decision.lower() in ['y', 'yes']:
            update_file(file_name, remote_content)
        else:
            print("Update canceled by the user.")
    else:
        print(f"File {file_name} is already up to date.")

file_name = "tennis_macos.py"
update_file_from_github(file_name)

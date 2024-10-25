import dropbox
import logging
import requests
from dotenv import load_dotenv
import os
from collections import defaultdict

load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("dropbox").disabled = True

class InvalidResponseError(Exception):
    pass


class ApiHandle:
    def __init__(self, url="dbackup-proxy.vercel.app"):
        self.url = url
    
    def get_auth_url(self):
        response = requests.get(f"https://{self.url}/api/get-auth-url")
        try:
            data = response.json()["auth_url"]
        except AttributeError:
            raise InvalidResponseError("Invalid response from server. Please try again.")
        return data
    
    def finish_auth(self, auth_code):
        response = requests.post(f"https://{self.url}/api/get-access-token", json={"auth_code": auth_code})
        try:
            data = response.json()[0]["access_token"]
        except AttributeError:
            raise InvalidResponseError("Invalid response from server. Please try again.")
        return data


class DropboxClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.initialised = False
        self.connected = False
        self.authenticated = False

        try:
            self.instance = dropbox.Dropbox(self.access_token)
            logging.info(f"Connected to Dropbox with access token {self.access_token}!")
            self.initialised = True
            self.connected = True
        except dropbox.exceptions.AuthError:
            logging.error(
                "Error connecting to Dropbox with access token: " + self.access_token
            )
            self.initialised = True
        except:
            raise

        try:
            self.account = self.instance.users_get_current_account()
            logging.info(
                f"Connected to Dropbox with account {self.account.name.display_name}"
            )
            self.authenticated = True
        except dropbox.exceptions.AuthError:
            logging.error("Failed to get current account")
        except:
            raise

    def explore(self, path, folders_only=True):
        folders = []
        try:
            for entry in self.instance.files_list_folder(path).entries:
                if folders_only:
                    if isinstance(entry, dropbox.files.FolderMetadata):
                        folders.append(entry)
                else:
                    folders.append(entry)
            return folders
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                logging.error(f"Folder {path} not found")
            else:
                raise
    
    def get_directories(self, path):
        self.tree = {}
        self.full_paths = []
        base = self.explore(path, folders_only=False)
        
        for item in base:
            if isinstance(item, dropbox.files.FolderMetadata):
                self.tree[item.name] = self.get_directories(item.path_display)
            else:
                self.full_paths.append(item.path_lower)
        
        return self.tree, self.full_paths

    def download(self, file, destination):
        try:
            # for 
            self.instance.files_download_to_file(file, destination)
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                print(f"File {file} not found")
            else:
                raise


if __name__ == "__main__":
    handle = ApiHandle()
    # print(handle.get_auth_url())
    # print(handle.finish_auth(input("Paste auth code: ")))
    # print(os.getenv("DBX_KEY"))
    client = DropboxClient(os.getenv("DBX_KEY"))
    print(client.get_directories(""))

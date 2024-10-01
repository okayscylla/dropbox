import dropbox
import logging

logging.basicConfig(level=logging.DEBUG)


with open("secrets.txt", "r") as f:
    ACCESS_TOKEN=f.read()


class DropboxClient:
    def __init__(self,access_token):
        self.access_token = access_token
        try:
            self.instance = dropbox.Dropbox(self.access_token)
            logging.info(f"Connected to Dropbox with access token {self.access_token}!")
        except dropbox.exceptions.AuthError:
            logging.error("Error connecting to Dropbox with access token: " + self.access_token)
        except:
            raise
        
        try:
            self.account = self.instance.users_get_current_account()
            logging.info(f"Connected to Dropbox with account {self.account.name.display_name}")
        except dropbox.exceptions.AuthError:
            logging.error("Failed to get current account")
        except:
            raise
        
    def explore(self, path):
        try:
            return self.instance.files_list_folder(path).entries
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                logging.error(f"Folder {path} not found")
            else:
                raise
    
    def download(self, file, destination):
        try:
            self.instance.files_download_to_file(file, destination)
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                print(f"File {file} not found")
            else:
                raise 


if __name__ == "__main__":
    client = DropboxClient(ACCESS_TOKEN)

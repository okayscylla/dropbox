import widgets
import customtkinter as ctk
import api
import logging
import dotenv
import os

ctk.set_default_color_theme("theme.json") # based on default dark-blue theme
ctk.set_appearance_mode("dark")


class MainWindow(ctk.CTk):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = key
        
        self.title("DBackup")
        self.resizable(False, False)
        self.geometry("1200x740")
        logging.info("Main window initialized")
        self.tab_init()
    
    def tab_init(self):
        self.tabs = ctk.CTkTabview(self, anchor="nw")
        self.tabs.add("Overview")
        self.tabs.add("Backup")
        self.tabs.add("Settings")
        self.tabs.pack(expand=True, fill="both")
    
    def api_init(self):
        self.handle = api.DropboxClient(self.api_key)
        self.startup_test()

    def startup_test(self):
        if not self.handle.initialised:
            logging.error("Handle not initialised")
            return 0  # Handle not initialised
        elif not self.handle.connected:
            logging.error("Handle not connected")
            return -1  # Handle not connected
        elif not self.handle.authenticated:
            logging.error("Handle not authenticated")
            return -2  # Handle not authenticated

        logging.info(
            f"Startup test passed: initialised: {self.handle.initialised}, connected: {self.handle.connected}, authenticated: {self.handle.authenticated}"
        )
        return True

if __name__ == "__main__":
    dotenv.load_dotenv()

    key = os.getenv("DBX_KEY")

    root = MainWindow(key)

    root.mainloop()
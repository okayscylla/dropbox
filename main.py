import widgets
import customtkinter as ctk
import api
import duplicates
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
        self.scopes = []
        self.tab_init()
        
    
    def reload_vars(self):
        self.days_since_last_backup = "20"
        # self.scopes = ["Home", "Pictures", "Videos", "Documents", "Downloads", "Music"]
    
    def tab_init(self):
        self.tabs = ctk.CTkTabview(self, anchor="nw")
        self.tabs.add("Overview")
        self.tabs.add("Settings")
        self.tabs._segmented_button.configure(font=ctk.CTkFont(size=18))
        self.tabs.pack(expand=True, fill="both")
        
        self.api_init()
        self.init_backup()
    
    def init_backup(self):
        self.reload_vars()
        root = self.tabs.tab("Overview")
        
        self.title = ctk.CTkLabel(root, text="DBackup", font=ctk.CTkFont(size=30))
        self.title.pack(anchor="nw", padx=(15, 0), pady=(10, 0))
        
        self.browse = widgets.BrowseFrame(root, self.handle, self)
        self.browse.refresh()
        self.browse.pack(expand=True, fill="both")
        
        # last = ctk.CTkLabel(root, text=f"Last Backup:\t{self.days_since_last_backup} days ago", font=ctk.CTkFont(size=20))
        # last.pack(anchor="nw", padx=(15, 0))
        self.status = ctk.CTkLabel(root, text="Current Status: \tNone", font=ctk.CTkFont(size=20))
        self.status.pack(anchor="nw", padx=(15, 0))
        
        self.location = widgets.EntryField(root, "Save Location:\t", ctk.CTkFont(size=20))
        self.location.pack(anchor="nw", padx=(15, 0), pady=10, side="left")
                
        self.submit = ctk.CTkButton(root, text="Submit", font=ctk.CTkFont(size=20), command=lambda: self.begin_backup())
        self.submit.pack(anchor="se", padx=(0, 15), pady=10, side="right")
            
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
    
    def begin_backup(self):
        save_dir = self.location.entry.get()
        if save_dir == "":
            return
        
        for folder in self.scopes:
            dirs, paths = self.handle.get_directories(folder)
            
            for dir in dirs:
                if not os.path.exists(os.path.join(save_dir, dir)):
                    os.mkdir(os.path.join(save_dir, dir))
            
            for path in paths:
                if not os.path.exists(os.path.join(save_dir, path)):
                    self.handle.download(path, os.path.join(save_dir, path))
        
        duplicates_files = duplicates.duplicate_finder(self.scopes)
        
        for duplicate in duplicates_files:
            try:
                os.remove(duplicate)
            except OSError:
                pass

if __name__ == "__main__":
    dotenv.load_dotenv()

    key = os.getenv("DBX_KEY")

    root = MainWindow(key)

    root.mainloop()
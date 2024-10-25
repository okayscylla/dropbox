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
    
    def reload_vars(self):
        self.days_since_last_backup = "20"
        # self.scopes = ["Home", "Pictures", "Videos", "Documents", "Downloads", "Music"]
    
    def tab_init(self):
        self.tabs = ctk.CTkTabview(self, anchor="nw")
        self.tabs.add("Overview")
        self.tabs.add("Settings")
        self.tabs._segmented_button.configure(font=ctk.CTkFont(size=18))
        self.tabs.pack(expand=True, fill="both")
        
        self.overview_widgets = []
        self.settings_widgets = []
        self.api_init()
        self.init_backup()
    
    def init_backup(self):
        self.reload_vars()
        root = self.tabs.tab("Overview")
        
        title = ctk.CTkLabel(root, text="DBackup", font=ctk.CTkFont(size=30))
        title.pack(anchor="nw", padx=(15, 0), pady=(10, 0))
        
        self.overview_widgets.append(title)
        
        # sep1 = ttk.Separator(root, orient="vertical")
        # sep1.pack(anchor="nw", padx=15, pady=(0, 10), expand=True, fill="x")
        
        # self.overview_widgets.append(sep1)
        
        # scopes = ctk.CTkScrollableFrame(root)
        # for item in self.scopes:
        #     ctk.CTkLabel(scopes, text=item).pack(anchor="nw")
        # scopes.pack(fill="both", expand=True)
        
        browse = widgets.BrowseFrame(root, self.handle)
        browse.refresh()
        browse.pack(expand=True, fill="both")
        
        self.overview_widgets.append(browse)
        
        last = ctk.CTkLabel(root, text=f"Last Backup:\t{self.days_since_last_backup} days ago", font=ctk.CTkFont(size=20))
        last.pack(anchor="nw", padx=(15, 0))
        
        self.overview_widgets.append(last)
        
        file_types = widgets.EntryField(root, "File Types:\t", ctk.CTkFont(size=20))
        file_types.pack(anchor="nw", padx=(15, 0), pady=10)
        
        self.overview_widgets.append(file_types)
    
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
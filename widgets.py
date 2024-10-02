import customtkinter
import api as dbx
import logging
import os


class PopupWindow(customtkinter.CTk):
    def __init__(self, title, resolution=(430, 180), scale=1.0, *args, **kwargs): # TODO implement icons
        super().__init__(*args, **kwargs)
        
        self.title(title)
        self.scale = scale
        self.geometry(f"{int(resolution[0]*scale)}x{int(resolution[1]*scale)}")
        self.resizable(False, False)


class BrowseFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, handle, scale=1.0, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.handle = handle
        self.scale = scale
        self.directory = None
        
        if self.startup_test() is not True:
            raise Exception("There was an error with the handle")
        
        self.seek(str(), absolute=True)
        self.refresh()
    
    def startup_test(self):
        if not self.handle.initialised:
            logging.error("Handle not initialised")
            return 0 #Handle not initialised
        elif not self.handle.connected:
            logging.error("Handle not connected")
            return -1 #Handle not connected
        elif not self.handle.authenticated:
            logging.error("Handle not authenticated")
            return -2 #Handle not authenticated
        
        logging.info(f"Startup test passed: initialised: {self.handle.initialised}, connected: {self.handle.connected}, authenticated: {self.handle.authenticated}")
        return True

    def seek(self, path, absolute=False):
        logging.info(f"Leaving directory {self.directory.__repr__()}")
        
        if type(path) is not str:
            logging.error("Error while seeking: path must be a string")
            return False
        
        if absolute:
            logging.info(f"Seeking to absolute path: {path.__repr__()}")
            self.directory = path
        else:
            logging.info(f"Seeking to relative path: {path.__repr__()}")
            self.directory = os.path.join(self.directory, path)
        
        return True

    def refresh(self):
        pass

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Test")
    root.geometry("1200x740")
    root.resizable(False, False)
    
    handle = dbx.DropboxClient(dbx.ACCESS_TOKEN)
    
    frame = BrowseFrame(root, handle)
    frame.pack(expand=True, fill="both")

    root.mainloop()
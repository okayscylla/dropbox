import customtkinter as ctk
import api as dbx
import logging
import os


class PopupWindow(ctk.CTk):
    def __init__(
        self, title, resolution=(430, 180), scale=1.0, *args, **kwargs
    ):  # TODO implement icons
        super().__init__(*args, **kwargs)

        self.title(title)
        self.scale = scale
        self.geometry(f"{int(resolution[0]*scale)}x{int(resolution[1]*scale)}")
        self.resizable(False, False)


class ButtonRow(ctk.CTkFrame):
    def __init__(self, master, text, submit_text="Select", style=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.next_button = customtkinter.CTkButton(self, text=text)
        self.subcmd_button = customtkinter.CTkButton(self, text=submit_text)
        self.next_button.pack(side="left", fill="x", expand=True)
        self.subcmd_button.pack(side="right")


class BrowseFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, handle, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.handle = handle
        self.widgets = []
        self.directory = None

        if self.startup_test() is not True:
            raise Exception("There was an error with the handle")

        self.seek(str(), absolute=True)

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
    
    def add(self, display_name, destination):
        self.widgets.append(ButtonRow(self, display_name))

    def refresh(self):
        logging.info(f"Refreshing directory {self.directory.__repr__()}")
        for widget in self.widgets:
            widget.pack_forget()
            widget.pack(side="top", fill="x", expand=True)
        
        logging.info(f"Refreshed directory {self.directory.__repr__()}")


if __name__ == "__main__":
    import dotenv
    import os
    
    dotenv.load_dotenv()
    
    root = ctk.CTk()
    root.title("Test")
    root.geometry("1200x740")
    root.resizable(False, False)

    handle = dbx.DropboxClient(os.getenv("DBX_KEY"))

    frame = BrowseFrame(root, handle)
    frame.add("Test", "/test")
    frame.refresh()
    frame.pack(expand=True, fill="both")

    root.mainloop()

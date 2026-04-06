# main.py
import customtkinter as ctk
import pathlib
import parse_email
import ui_design
import os
from database import DatabaseOps
from ui_design import RecentFilesView


class App(ctk.CTk):
    def __init__(self):
        # setup theme
        project_root = pathlib.Path(__file__).parent
        theme_file = f"{project_root}/assets/theme.json"
        ctk.set_default_color_theme(theme_file)
        super().__init__()

        self.x=1180
        self.y=630
        self.title("Email Reader")
        self.geometry(f"{self.x}x{self.y}")
        self.db = DatabaseOps()

        # open file button
        open_file_btn = ctk.CTkButton(self, text="Open file", command=self.open_file)
        open_file_btn.pack(pady=10)

        # email view
        self.email_view = ui_design.EmailViewUI(self)
        self.email_view.pack()

        # recent files view
        self.recent_files_view = RecentFilesView(self, on_file_select=self.load_from_recent_files)
        self.recent_files_view.pack()

        self.refresh_recent_files()

    def open_file(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Email files", "*.eml")])
        if file_path:
            filename = os.path.basename(file_path)
            self.db.save_recent_files(filename, file_path)
            email_data = parse_email.parse_email(file_path)
            self.email_view.update_email(email_data)

    def load_from_recent_files(self, file_path):
        email_data = parse_email.parse_email(file_path)
        self.email_view.update_email(email_data)

    def refresh_recent_files(self):
        recent_files = self.db.get_recent_files()
        self.recent_files_view.populate_recent_files(recent_files)
app = App()
app.mainloop()
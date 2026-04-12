# main.py
import customtkinter as ctk
import pathlib
import parse_email
import ui_design
import os
from database import DatabaseOps


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

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.name_font = ctk.CTkFont(family="Roboto Mono", size=20, weight="bold")
        self.name = ctk.CTkLabel(self, text="Email Reader", fg_color="transparent", padx=10, font=self.name_font)
        self.name.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5, ipadx=10, ipady=5)

        # open file button
        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        open_file_btn = ctk.CTkButton(self, text="Open file", font=self.label_font, command=self.open_file)
        open_file_btn.grid(row=1, column=0, sticky="new", padx=10, pady=5, ipadx=10, ipady=5)

        # email view
        self.email_view = ui_design.EmailViewUI(self)
        self.email_view.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)

        # email headers button
        self.current_email_data = None
        headers_btn = ctk.CTkButton(self, text="Email Headers", font=self.label_font, command=lambda: ui_design.EmailHeadersWindow(self, self.current_email_data))
        headers_btn.grid(row=1, column=2, sticky="nsew", padx=10, pady=5, ipadx=10)

        # attachments view
        self.attachments_view = ui_design.AttachmentsView(self)
        self.attachments_view.grid(row=2, column=2, rowspan=3, sticky="nsew", padx=10, pady=5, ipadx=10)

        # recent files view
        self.recent_files_view = ui_design.RecentFilesView(self, on_file_select=self.load_from_recent_files)
        self.recent_files_view.grid(row=2, column=0, rowspan=1, sticky="nsew", padx=10, pady=5)

        self.refresh_recent_files()

        # about button
        about_btn = ctk.CTkButton(self, text="About", font=self.label_font, command=lambda: ui_design.AboutDialogue(self))
        about_btn.grid(row=3, column=0, sticky="nsew", padx=10, pady=5, ipadx=10)

    def open_file(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Email files", "*.eml")])
        if not file_path:
            return
        filename = os.path.basename(file_path)
        self.db.save_recent_files(filename, file_path)
        try:
            email_data = parse_email.parse_email(file_path)
        except FileNotFoundError:
            ui_design.ErrorDialogue(self, "File Not Found", f"{os.path.basename(file_path)} file not found")
            return
        self.email_view.update_email(email_data)
        self.attachments_view.get_attachments(email_data)
        self.current_email_data = email_data
        self.refresh_recent_files()

    def load_from_recent_files(self, file_path):
        try:
            email_data = parse_email.parse_email(file_path)
        except FileNotFoundError:
            ui_design.ErrorDialogue(self, "File Not Found", f"{os.path.basename(file_path)} file not found")
            return
        filename = os.path.basename(file_path)
        self.db.save_recent_files(filename, file_path)
        self.email_view.update_email(email_data)
        self.attachments_view.get_attachments(email_data)
        self.current_email_data = email_data
        self.refresh_recent_files()

    def refresh_recent_files(self):
        recent_files = self.db.get_recent_files()
        self.recent_files_view.populate_recent_files(recent_files)

app = App()
app.mainloop()
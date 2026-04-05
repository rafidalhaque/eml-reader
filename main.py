# main.py
import customtkinter as ctk
import pathlib
import parse_email
import ui_design


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.x=1180
        self.y=630
        self.title("Email Reader")
        self.geometry(f"{self.x}x{self.y}")

        # setup theme
        project_root = pathlib.Path(__file__).parent
        theme_file = f"{project_root}/assets/theme.json"
        ctk.set_default_color_theme(theme_file)

        # open file button
        open_file_btn = ctk.CTkButton(self, text="Open file", command=self.open_file)
        open_file_btn.pack(pady=100)

        # email view
        self.email_view = ui_design.EmailViewUI(self)
        self.email_view.pack()

    def open_file(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Email files", "*.eml")])
        if file_path:
            email_data = parse_email.parse_email(file_path)
            self.email_view.update_email(email_data)

app = App()
app.mainloop()
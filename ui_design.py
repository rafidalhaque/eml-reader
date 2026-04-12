# ui_design.py
from textwrap import wrap

import customtkinter as ctk
import webbrowser

from tkinterweb import HtmlFrame


class EmailViewUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.email_ui()

    def email_ui(self):
        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.subject_label = ctk.CTkLabel(self, text="Subject: ", font=self.label_font, anchor="w")
        self.subject_label.pack(fill="x", expand=True, padx=10)
        self.from_label = ctk.CTkLabel(self, text="From: ", font=self.label_font, anchor="w")
        self.from_label.pack(fill="x", expand=True, padx=10)
        self.to_label = ctk.CTkLabel(self, text="To: ", font=self.label_font, anchor="w")
        self.to_label.pack(fill="x", expand=True, padx=10)
        self.date_label = ctk.CTkLabel(self, text="Date: ", font=self.label_font, anchor="w")
        self.date_label.pack(fill="x", expand=True, padx=10)
        self.body_html = HtmlFrame(self, messages_enabled=False, on_link_click=self.open_external_link)
        self.body_html.pack(padx=10, pady=10, fill="both", expand=True)

    def update_email(self, email_data):
        self.subject_label.configure(text=f"Subject: {email_data["subject"]}")
        self.from_label.configure(text=f"From: {email_data["from"]}")
        self.to_label.configure(text=f"To: {email_data["to"]}")
        self.date_label.configure(text=f"Date: {email_data["date"]}")
        self.body_html.load_html(email_data["body_html"])

    def open_external_link(self, url):
        if not url:
            return
        if url.startswith(("http://", "https://", "mailto:")):
            webbrowser.open_new_tab(url)

class AttachmentsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.font_family = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.attachments_ui()

    def attachments_ui(self):
        self.attachments_frame = ctk.CTkScrollableFrame(self, label_text="Attachments", label_font=self.font_family)
        self.attachments_frame.pack(fill="both", expand=True)

    def make_filesize_readable(self, filesize):
        if filesize < 1024:
            return f"{filesize} B"
        elif filesize < 1024 * 1024:
            filesize = filesize / 1024
            return f"{filesize:.2f} KB"
        else:
            filesize = filesize / (1024 * 1024)
            return f"{filesize:.2f} MB"

    def get_attachments(self, email_data):
        for widget in self.attachments_frame.winfo_children():
            widget.destroy()
        attachments = email_data["attachments"]
        for attachment in attachments:
            filename, filesize = attachment
            attachment_text = ctk.CTkLabel(
                self.attachments_frame,
                text=f"File Name: {filename}\nFile Size: {self.make_filesize_readable(filesize)}\n",
                font=(self.font_family, 15, "normal"),
                wraplength=300,
                anchor="w",
                justify="left"
            )
            attachment_text.pack(fill="x", expand=True)

class RecentFilesView(ctk.CTkFrame):
    def __init__(self, master, on_file_select, **kwargs):
        super().__init__(master, **kwargs)
        self.on_file_select = on_file_select
        self.font_family = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.recent_files_frame = ctk.CTkScrollableFrame(self, label_text="Recent Files", fg_color="transparent", label_font=self.font_family, label_fg_color="transparent")
        self.recent_files_frame.pack(fill="both", expand=True)

    def populate_recent_files(self, recent_files):
        for widget in self.recent_files_frame.winfo_children():
            widget.destroy()

        for file in recent_files:
            id, filename, file_path, opened_at = file
            hidden_btn = ctk.CTkButton(
                self.recent_files_frame,
                text=f"{filename}\n{file_path}\n{opened_at}",
                font=(self.font_family, 13),
                anchor="w",
                command=lambda p=file_path: self.on_file_select(p)
            )
            hidden_btn.pack(fill="x", pady=5)

class AboutDialogue(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Email Reader")
        self.geometry("400x300")
        self.resizable(True, True)
        self.grab_set()

        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.heading = ctk.CTkLabel(self, text="About Email Reader", font=(self.label_font, 18), anchor="n", wraplength=250)
        self.heading.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        self.text = """
        Email Reader is a GUI software build with python3 and customtkinter. It allows user to read .eml file. 
        """
        self.about_text = ctk.CTkLabel(self, text=self.text, font=self.label_font, wraplength=250, anchor="n", justify="left")
        self.about_text.grid(row=1, column=0, columnspan=2, pady=(20, 10))
        self.developer_btn = self.hyperlink_btn(parent=self, text="Developer: rafidalhaque", fg_color="blue", url="https://rafidalhaque.github.io")
        self.developer_btn.grid(row=2, column=0, padx=20, pady=5)
        self.github_repo = self.hyperlink_btn(parent=self, text="GitHub Repository", fg_color="black", url="https://github.com/rafidalhaque/eml-reader")
        self.github_repo.grid(row=2, column=1, padx=20, pady=5)

    def hyperlink_btn(self, parent, text, url, fg_color, **kwargs):
        return ctk.CTkButton(parent, text=text, font=self.label_font, fg_color=fg_color, command=lambda: webbrowser.open(url), **kwargs)

class ErrorDialogue(ctk.CTkToplevel):
    def __init__(self, parent, title="Error", message="An Error Occured", **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()

        self.label_font = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.message_label = ctk.CTkLabel(self, text=message, font=self.label_font, anchor="w", wraplength=300)
        self.message_label.pack(padx=20, pady=(20, 5), expand=True)
        self.ok_button = ctk.CTkButton(self, text="OK", font=self.label_font, command=self.destroy)
        self.ok_button.pack(pady=(0, 20))

class EmailHeadersWindow(ctk.CTkToplevel):
    def __init__(self, parent, current_email_data, **kwargs):
        super().__init__(parent, **kwargs)
        self.x = 800
        self.y = 600
        self.title("Email Headers | Email Reader")
        self.geometry(f"{self.x}x{self.y}")
        self.font_family = ctk.CTkFont(family="Roboto Mono", size=15, weight="bold")
        self.resizable(False, False)
        self.columnconfigure(0, weight=0, minsize=200)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.headers_ui(parent=self)
        self.current_email_data = current_email_data
        self.get_headers_info(self.current_email_data)
        self.grab_set()

    def headers_ui(self, parent, **kwargs):
        self.header_frame = ctk.CTkScrollableFrame(parent, label_text="Email Headers", label_font=self.font_family)
        self.header_frame.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="nsew")
        self.header_frame.columnconfigure(0, weight=0, minsize=200)
        self.header_frame.columnconfigure(1, weight=1)
    def get_headers_info(self, email_data):
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        self.header_heading = ctk.CTkLabel(self.header_frame, text="Headers", font=self.font_family, anchor="center")
        self.header_heading.grid(row=1, column=0, pady=(20, 10))
        self.value_heading = ctk.CTkLabel(self.header_frame, text="Values", font=self.font_family, anchor="center")
        self.value_heading.grid(row=1, column=1, pady=(20, 10))
        headers = email_data["other_headers"]
        for index, header in enumerate(headers):
            name, value = header
            header_name = ctk.CTkTextbox(
                self.header_frame,
                font=(self.font_family, 13, "normal"),
                border_color="black",
                border_width=1,
                border_spacing=10,
                height=35
            )
            header_name.grid(row=index + 2, column=0, sticky="nsew", padx=5, pady=5)
            header_name.insert("0.0", name)
            header_name.configure(state="disabled")
            value_textbox = ctk.CTkTextbox(
                self.header_frame,
                font=(self.font_family, 13, "normal"),
                border_color="black",
                border_width=1,
                border_spacing=10,
                height=35
            )
            value_textbox.grid(row=index + 2, column=1, sticky="nsew", padx=5, pady=5)
            value_textbox.insert("0.0", value)
            value_textbox.configure(state="disabled")




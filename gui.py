import os
from tkinter import filedialog
from cryptography.fernet import Fernet
import customtkinter as CTk


class gui_app(CTk.CTk):
    
    def __init__(self):
        super().__init__()  
        self.title("Encryption Tool")  
        self.geometry("936x550")
        self.main_frame = CTk.CTkFrame(self,
                                fg_color="#FFDDDD", 
                                border_color="black",  
                                border_width=1,       
                                width=936,
                                height=550)
        self.main_frame.place(x=0, y=0)
        
        self.top_label()
        self.encrypt_button()
        self.decrypt_button()
        self.entry_key()
        self.left_frame()
        self.drop_button()
        self.file_path = ""  # Initialize file path
        
    def top_label(self):
        self.label=CTk.CTkButton(self, text="ENCRYPTION TOOL",
                                    width=936,
                                    height=95,
                                    fg_color="#D3DF9E",
                                    text_color="#1E1E1E",
                                    hover_color="#D3DF9E",
                                    border_color="#000000",
                                    corner_radius=0,
                                    border_width=0.5,
                                    font=("Roboto Mono", 32))
        self.label.pack(pady=0, anchor="n")

    def encrypt_button(self):
        self.encrypt_btn=CTk.CTkButton(self, text="Encrypt Data and \nGenerate a key",
                                    width=380,
                                    height=115,
                                    fg_color="#ffeae1",
                                    bg_color="#ffd6d6",
                                    text_color="#223A22",
                                    hover_color="#fae2d7",
                                    corner_radius=5,
                                    border_color="#eaab9c",
                                    border_width=1,
                                    font=("Roboto Mono", 20))
                                    #command=self.encrypt_file)
        self.encrypt_btn.pack(pady=50, padx=29, anchor="ne")

    def decrypt_button(self):
        self.decrypt_btn=CTk.CTkButton(self, text="Decrypt Data using a \npre-existing key",
                                    width=380,
                                    height=80,
                                    fg_color="#ffeae1",
                                    bg_color="#ffd6d6",
                                    text_color="#223A22",
                                    hover_color="#fae2d7",
                                    corner_radius=5,
                                    border_color="#eaab9c",
                                    border_width=1,
                                    font=("Roboto Mono", 20))
        self.decrypt_btn.pack(padx=29, pady=0, anchor="ne")

    def entry_key(self):
        self.entry_frame=CTk.CTkFrame(self,
                                fg_color="#FFDDDD", 
                                bg_color="#FFDDDD",
                                corner_radius=10,
                                height=60,
                                width=380)
        self.entry_frame.pack(padx=29, pady=0, anchor="ne")
        
        self.key_entry = CTk.CTkEntry(self, 
                            placeholder_text="Enter The Key",
                            width=380, 
                            height=60,
                            fg_color="#ffeae1",
                            bg_color="#ffeae1",
                            text_color="#223A22",
                            border_color="#eaab9c", 
                            border_width=1)
        self.key_entry.pack(padx=29, pady=0, anchor="ne")

    def left_frame(self):
        self.frame = CTk.CTkFrame(self,
                                fg_color="#FFCFCB",
                                bg_color="#FFDDDD",
                                corner_radius=4,
                                border_color="#eaa4b2",
                                border_width=0.9,
                                width=480,
                                height=400)
        self.frame.place(x=25, y=120)

        self.file_entry=CTk.CTkEntry(self,
                            placeholder_text="Paste the url/drop the file",
                            fg_color="#ffeae1",
                            bg_color="#F5CBC7",
                            text_color="#223A22",
                            border_color="#eaab9c", 
                                width=936,
                                height=550)
        self.main_frame.place(x=0, y=0)
        #self.label_border()
                           
        self.file_entry.place(x=39, y=435)

    def drop_button(self):
        self.drop_btn = CTk.CTkButton(self, 
                                text="🗂️\nDrop files here\nor click to browse",
                                font=("Roboto Mono", 20),
                                fg_color="#ffeae1",
                                bg_color="#ffddcf",
                                corner_radius=4,
                                hover_color="#ffeae1",
                                border_color="#eaa4b2",
                                border_width=0.9,
                                width=430,
                                height=285,
                                compound="top")
                                #command=self.browse_file
        self.drop_btn.place(x=50, y=130)
        
        # Set up drag and drop
        '''self.drop_btn.bind('<DragEnter>', self.on_drag_enter)
        self.drop_btn.bind('<DragLeave>', self.on_drag_leave)
        self.drop_btn.bind('<Drop>', self.on_drop)'''

    '''def browse_file(self):
        """Open file dialog to select a file"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.process_file(file_path)

    def on_drag_enter(self, event):
        """Visual feedback when dragging over the drop area"""
        self.drop_btn.configure(border_color="#4CC9F0", border_width=2)

    def on_drag_leave(self, event):
        """Reset drop area appearance"""
        self.drop_btn.configure(border_width=0.9)

    def on_drop(self, event):
        """Handle dropped files"""
        self.drop_btn.configure(border_width=0.9)
        # Get the file path (handles Windows path formatting)
        file_path = event.data.strip('{}')
        if os.path.exists(file_path):
            self.process_file(file_path)

    def process_file(self, file_path):
        """Handle the selected file"""
        self.file_path = file_path
        filename = os.path.basename(file_path)
        # Update the entry field
        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, file_path)
        # Visual feedback
        self.drop_btn.configure(text=f"🗂️\n{filename}\nReady for encryption!")

    def encrypt_file(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, "Please select a file first!")
            return
        
        try:
            # Generate key
            key = Fernet.generate_key().decode('utf-8')
            
            # Encrypt the file
            with open(self.file_path, 'rb') as f:
                data = f.read()
            
            fernet = Fernet(key.encode('utf-8'))
            encrypted = fernet.encrypt(data)
            
            # Save encrypted file
            encrypted_path = self.file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            
            # Save key to file
            key_path = os.path.splitext(self.file_path)[0] + '_KEY.txt'
            with open(key_path, 'w') as f:
                f.write(key)
            
            # Update UI
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, f"Encrypted! Key saved to {key_path}")
            self.drop_btn.configure(text=f"🗂️\nEncryption complete!\nKey saved to {os.path.basename(key_path)}")
            
        except Exception as e:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, f"Error: {str(e)}")'''


app = gui_app()
app.mainloop()

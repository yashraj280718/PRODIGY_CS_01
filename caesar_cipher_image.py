import tkinter as tk
from tkinter import ttk, messagebox
import string

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher - Encryption & Decryption")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Caesar Cipher Tool", 
                               style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input message section
        ttk.Label(main_frame, text="Enter Message:", 
                 style="Heading.TLabel").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_text = tk.Text(main_frame, height=4, width=50, wrap=tk.WORD,
                                 font=("Arial", 10))
        self.input_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                            pady=(0, 15))
        
        # Shift value section
        shift_frame = ttk.Frame(main_frame)
        shift_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                        pady=(0, 15))
        
        ttk.Label(shift_frame, text="Shift Value:", 
                 style="Heading.TLabel").grid(row=0, column=0, sticky=tk.W)
        
        self.shift_var = tk.StringVar(value="3")
        shift_spinbox = ttk.Spinbox(shift_frame, from_=1, to=25, 
                                   textvariable=self.shift_var, width=10)
        shift_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                          pady=(0, 15))
        
        self.preserve_case = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preserve letter case", 
                       variable=self.preserve_case).grid(row=0, column=0, sticky=tk.W)
        
        self.preserve_spaces = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preserve spaces and punctuation", 
                       variable=self.preserve_spaces).grid(row=1, column=0, sticky=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(0, 15))
        
        encrypt_btn = ttk.Button(buttons_frame, text="Encrypt", 
                               command=self.encrypt_message, style="Action.TButton")
        encrypt_btn.grid(row=0, column=0, padx=(0, 10))
        
        decrypt_btn = ttk.Button(buttons_frame, text="Decrypt", 
                               command=self.decrypt_message, style="Action.TButton")
        decrypt_btn.grid(row=0, column=1, padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="Clear All", 
                             command=self.clear_all)
        clear_btn.grid(row=0, column=2)
        
        # Output section
        ttk.Label(main_frame, text="Result:", 
                 style="Heading.TLabel").grid(row=6, column=0, sticky=tk.W, pady=(15, 5))
        
        self.output_text = tk.Text(main_frame, height=4, width=50, wrap=tk.WORD,
                                  font=("Arial", 10), state=tk.DISABLED,
                                  bg="#f0f0f0")
        self.output_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                             pady=(0, 10))
        
        # Copy button
        copy_btn = ttk.Button(main_frame, text="Copy Result", 
                            command=self.copy_result)
        copy_btn.grid(row=8, column=0, columnspan=2, pady=(5, 0))
        
        # Instructions
        instructions = """Instructions:
• Enter your message in the text area above
• Set the shift value (1-25)
• Choose your preferred options
• Click Encrypt or Decrypt
• Use the same shift value to decrypt an encrypted message"""
        
        inst_label = ttk.Label(main_frame, text=instructions, 
                             style="Instructions.TLabel", justify=tk.LEFT)
        inst_label.grid(row=9, column=0, columnspan=2, pady=(20, 0), sticky=tk.W)
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Title style
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        
        # Heading style
        style.configure("Heading.TLabel", font=("Arial", 11, "bold"))
        
        # Instructions style
        style.configure("Instructions.TLabel", font=("Arial", 9), 
                       foreground="gray")
        
        # Action button style
        style.configure("Action.TButton", font=("Arial", 10, "bold"))
    
    def caesar_cipher(self, text, shift, decrypt=False):
        """Perform Caesar cipher encryption or decryption"""
        if decrypt:
            shift = -shift
        
        result = ""
        
        for char in text:
            if char.isalpha():
                # Determine if uppercase or lowercase
                is_upper = char.isupper()
                char = char.lower()
                
                # Shift the character
                shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                
                # Preserve case if option is selected
                if self.preserve_case.get() and is_upper:
                    shifted = shifted.upper()
                
                result += shifted
            else:
                # Preserve spaces and punctuation if option is selected
                if self.preserve_spaces.get():
                    result += char
        
        return result
    
    def encrypt_message(self):
        """Encrypt the input message"""
        try:
            message = self.input_text.get("1.0", tk.END).strip()
            if not message:
                messagebox.showwarning("Warning", "Please enter a message to encrypt.")
                return
            
            shift = int(self.shift_var.get())
            encrypted = self.caesar_cipher(message, shift)
            
            self.display_result(encrypted)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid shift value.")
    
    def decrypt_message(self):
        """Decrypt the input message"""
        try:
            message = self.input_text.get("1.0", tk.END).strip()
            if not message:
                messagebox.showwarning("Warning", "Please enter a message to decrypt.")
                return
            
            shift = int(self.shift_var.get())
            decrypted = self.caesar_cipher(message, shift, decrypt=True)
            
            self.display_result(decrypted)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid shift value.")
    
    def display_result(self, result):
        """Display the result in the output text area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        self.output_text.config(state=tk.DISABLED)
    
    def copy_result(self):
        """Copy the result to clipboard"""
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Success", "Result copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No result to copy.")
    
    def clear_all(self):
        """Clear all text areas"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.shift_var.set("3")

def main():
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
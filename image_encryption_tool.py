import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import random

class ImageEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.current_image_path = None
        self.encryption_key = None
        
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Encryption Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Operations", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Select Image", 
                  command=self.load_image).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        # Encryption options frame
        options_frame = ttk.LabelFrame(main_frame, text="Encryption Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Encryption method
        ttk.Label(options_frame, text="Encryption Method:").grid(row=0, column=0, sticky=tk.W)
        self.method_var = tk.StringVar(value="XOR")
        method_combo = ttk.Combobox(options_frame, textvariable=self.method_var, 
                                   values=["XOR", "Pixel Swap", "Mathematical", "Color Channel Shift"],
                                   state="readonly", width=20)
        method_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Key/Seed input
        ttk.Label(options_frame, text="Encryption Key:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.key_var = tk.StringVar(value="12345")
        key_entry = ttk.Entry(options_frame, textvariable=self.key_var, width=20)
        key_entry.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(10, 0))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(control_frame, text="Encrypt Image", 
                  command=self.encrypt_image, style="Accent.TButton").grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="Decrypt Image", 
                  command=self.decrypt_image, style="Accent.TButton").grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="Save Result", 
                  command=self.save_image).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(control_frame, text="Reset", 
                  command=self.reset_images).grid(row=0, column=3)
        
        # Image display frame
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(4, weight=1)
        
        # Original image
        original_frame = ttk.LabelFrame(display_frame, text="Original Image", padding="10")
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.original_canvas = tk.Canvas(original_frame, width=300, height=300, 
                                        bg="white", relief=tk.SUNKEN, borderwidth=2)
        self.original_canvas.grid(row=0, column=0)
        
        # Processed image
        processed_frame = ttk.LabelFrame(display_frame, text="Processed Image", padding="10")
        processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.processed_canvas = tk.Canvas(processed_frame, width=300, height=300, 
                                         bg="white", relief=tk.SUNKEN, borderwidth=2)
        self.processed_canvas.grid(row=0, column=0)
        
        # Configure grid weights for image display
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, font=("Arial", 9))
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def load_image(self):
        """Load an image file"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                      ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert('RGB')
                self.current_image_path = file_path
                self.file_label.config(text=os.path.basename(file_path), foreground="black")
                
                # Display original image
                self.display_image(self.original_image, self.original_canvas)
                
                # Clear processed image
                self.processed_canvas.delete("all")
                self.processed_image = None
                
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, canvas):
        """Display image on canvas with proper scaling"""
        if image is None:
            return
        
        # Get canvas dimensions
        canvas_width = canvas.winfo_width() or 300
        canvas_height = canvas.winfo_height() or 300
        
        # Calculate scaling to fit canvas while maintaining aspect ratio
        img_width, img_height = image.size
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image for display
        display_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and display
        photo = ImageTk.PhotoImage(display_img)
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, image=photo)
        
        # Keep a reference to prevent garbage collection
        canvas.image = photo
    
    def generate_key_sequence(self, length, key_string):
        """Generate a deterministic sequence from key string"""
        random.seed(hash(key_string) % (2**32))
        return [random.randint(0, 255) for _ in range(length)]
    
    def xor_encryption(self, image_array, key_string, decrypt=False):
        """XOR-based encryption/decryption"""
        height, width, channels = image_array.shape
        key_sequence = self.generate_key_sequence(width * height * channels, key_string)
        
        flat_array = image_array.flatten()
        
        # XOR each pixel value with corresponding key value
        for i in range(len(flat_array)):
            flat_array[i] = flat_array[i] ^ key_sequence[i % len(key_sequence)]
        
        return flat_array.reshape(height, width, channels)
    
    def pixel_swap_encryption(self, image_array, key_string, decrypt=False):
        """Pixel position swapping encryption/decryption"""
        height, width, channels = image_array.shape
        total_pixels = height * width
        
        # Generate deterministic swap sequence
        random.seed(hash(key_string) % (2**32))
        swap_indices = list(range(total_pixels))
        random.shuffle(swap_indices)
        
        # Reshape to work with pixel positions
        flat_array = image_array.reshape(total_pixels, channels)
        result_array = flat_array.copy()
        
        if decrypt:
            # Reverse the swapping
            for i, j in enumerate(swap_indices):
                result_array[j] = flat_array[i]
        else:
            # Apply the swapping
            for i, j in enumerate(swap_indices):
                result_array[i] = flat_array[j]
        
        return result_array.reshape(height, width, channels)
    
    def mathematical_encryption(self, image_array, key_string, decrypt=False):
        """Mathematical operation-based encryption/decryption"""
        # Generate key values from string
        key_hash = hash(key_string) % 256
        multiplier = (key_hash % 127) + 1  # Ensure odd number for reversibility
        additive = key_hash % 256
        
        if decrypt:
            # Find modular multiplicative inverse
            inv_multiplier = self.mod_inverse(multiplier, 256)
            result = ((image_array.astype(np.int32) - additive) * inv_multiplier) % 256
        else:
            result = (image_array.astype(np.int32) * multiplier + additive) % 256
        
        return result.astype(np.uint8)
    
    def mod_inverse(self, a, m):
        """Calculate modular multiplicative inverse"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            return 1  # Fallback
        return (x % m + m) % m
    
    def color_channel_shift(self, image_array, key_string, decrypt=False):
        """Color channel shifting encryption/decryption"""
        key_hash = hash(key_string)
        
        # Generate shift values for each channel
        r_shift = (key_hash >> 0) % 256
        g_shift = (key_hash >> 8) % 256
        b_shift = (key_hash >> 16) % 256
        
        result = image_array.copy().astype(np.int32)
        
        if decrypt:
            result[:, :, 0] = (result[:, :, 0] - r_shift) % 256
            result[:, :, 1] = (result[:, :, 1] - g_shift) % 256
            result[:, :, 2] = (result[:, :, 2] - b_shift) % 256
        else:
            result[:, :, 0] = (result[:, :, 0] + r_shift) % 256
            result[:, :, 1] = (result[:, :, 1] + g_shift) % 256
            result[:, :, 2] = (result[:, :, 2] + b_shift) % 256
        
        return result.astype(np.uint8)
    
    def encrypt_image(self):
        """Encrypt the loaded image"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first.")
            return
        
        if not self.key_var.get().strip():
            messagebox.showwarning("Warning", "Please enter an encryption key.")
            return
        
        try:
            self.status_var.set("Encrypting image...")
            self.root.update()
            
            # Convert image to numpy array
            image_array = np.array(self.original_image)
            method = self.method_var.get()
            key_string = self.key_var.get()
            
            # Apply selected encryption method
            if method == "XOR":
                encrypted_array = self.xor_encryption(image_array, key_string)
            elif method == "Pixel Swap":
                encrypted_array = self.pixel_swap_encryption(image_array, key_string)
            elif method == "Mathematical":
                encrypted_array = self.mathematical_encryption(image_array, key_string)
            elif method == "Color Channel Shift":
                encrypted_array = self.color_channel_shift(image_array, key_string)
            
            # Convert back to PIL Image
            self.processed_image = Image.fromarray(encrypted_array.astype(np.uint8))
            
            # Display encrypted image
            self.display_image(self.processed_image, self.processed_canvas)
            
            self.status_var.set(f"Image encrypted using {method}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            self.status_var.set("Encryption failed")
    
    def decrypt_image(self):
        """Decrypt the processed image"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "Please encrypt an image first or load an encrypted image.")
            return
        
        if not self.key_var.get().strip():
            messagebox.showwarning("Warning", "Please enter the decryption key.")
            return
        
        try:
            self.status_var.set("Decrypting image...")
            self.root.update()
            
            # Convert processed image to numpy array
            image_array = np.array(self.processed_image)
            method = self.method_var.get()
            key_string = self.key_var.get()
            
            # Apply selected decryption method
            if method == "XOR":
                # XOR is symmetric
                decrypted_array = self.xor_encryption(image_array, key_string, decrypt=True)
            elif method == "Pixel Swap":
                decrypted_array = self.pixel_swap_encryption(image_array, key_string, decrypt=True)
            elif method == "Mathematical":
                decrypted_array = self.mathematical_encryption(image_array, key_string, decrypt=True)
            elif method == "Color Channel Shift":
                decrypted_array = self.color_channel_shift(image_array, key_string, decrypt=True)
            
            # Convert back to PIL Image
            decrypted_image = Image.fromarray(decrypted_array.astype(np.uint8))
            
            # Replace processed image with decrypted version
            self.processed_image = decrypted_image
            self.display_image(self.processed_image, self.processed_canvas)
            
            self.status_var.set(f"Image decrypted using {method}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
            self.status_var.set("Decryption failed")
    
    def save_image(self):
        """Save the processed image"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save processed image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                      ("JPEG files", "*.jpg"),
                      ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def reset_images(self):
        """Reset all images and clear canvases"""
        self.original_image = None
        self.processed_image = None
        self.current_image_path = None
        
        self.original_canvas.delete("all")
        self.processed_canvas.delete("all")
        
        self.file_label.config(text="No file selected", foreground="gray")
        self.status_var.set("Ready")

def main():
    root = tk.Tk()
    app = ImageEncryptionTool(root)
    
    # Configure style for better appearance
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 10, "bold"))
    
    root.mainloop()

if __name__ == "__main__":
    main()
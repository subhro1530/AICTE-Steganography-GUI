import tkinter as tk
from tkinter import filedialog, messagebox
from stegano import lsb
import os

# Create main application window
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        self.root.geometry("500x400")
        
        self.create_encode_page()
    
    def create_encode_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Encode Message into Image", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Select Image File (.PNG)").pack()
        self.image_entry = tk.Entry(self.root, width=40)
        self.image_entry.pack()
        tk.Button(self.root, text="Browse", command=self.load_image).pack()
        
        tk.Label(self.root, text="Select Text File (.TXT)").pack()
        self.text_entry = tk.Entry(self.root, width=40)
        self.text_entry.pack()
        tk.Button(self.root, text="Browse", command=self.load_text).pack()
        
        tk.Label(self.root, text="Enter Password").pack()
        self.password_entry = tk.Entry(self.root, width=40, show='*')
        self.password_entry.pack()
        
        tk.Button(self.root, text="Encode", command=self.encode_message).pack(pady=10)
        tk.Button(self.root, text="Go to Decode Page", command=self.create_decode_page).pack()
        
    def create_decode_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Decode Message from Image", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Select Encrypted Image").pack()
        self.decode_image_entry = tk.Entry(self.root, width=40)
        self.decode_image_entry.pack()
        tk.Button(self.root, text="Browse", command=self.load_decode_image).pack()
        
        tk.Label(self.root, text="Enter Password").pack()
        self.decode_password_entry = tk.Entry(self.root, width=40, show='*')
        self.decode_password_entry.pack()
        
        tk.Button(self.root, text="Decode", command=self.decode_message).pack(pady=10)
        tk.Button(self.root, text="Go to Encode Page", command=self.create_encode_page).pack()
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        self.image_entry.delete(0, tk.END)
        self.image_entry.insert(0, file_path)
    
    def load_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, file_path)
    
    def load_decode_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        self.decode_image_entry.delete(0, tk.END)
        self.decode_image_entry.insert(0, file_path)
    
    def encode_message(self):
        image_path = self.image_entry.get()
        text_path = self.text_entry.get()
        password = self.password_entry.get()
        
        if not image_path or not text_path or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        with open(text_path, "r") as file:
            secret_message = password + "::" + file.read()
        
        encoded_image = lsb.hide(image_path, secret_message)
        save_path = image_path.replace(".png", "_encoded.png")
        encoded_image.save(save_path)
        
        messagebox.showinfo("Success", f"Encoded Image saved at {save_path}")
    
    def decode_message(self):
        image_path = self.decode_image_entry.get()
        password = self.decode_password_entry.get()
        
        if not image_path or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            extracted_message = lsb.reveal(image_path)
            stored_password, secret_message = extracted_message.split("::", 1)
            
            if stored_password != password:
                messagebox.showerror("Error", "Incorrect Password!")
                return
            
            os.makedirs("output", exist_ok=True)
            output_path = os.path.join("output", "decoded_message.txt")
            with open(output_path, "w") as file:
                file.write(secret_message)
            
            messagebox.showinfo("Success", f"Message extracted and saved at {output_path}")
        except:
            messagebox.showerror("Error", "Failed to decode message!")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

# gui_rgb_change_stego.py

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os

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
        
        tk.Label(self.root, text="Select Image File").pack()
        self.image_entry = tk.Entry(self.root, width=40)
        self.image_entry.pack()
        tk.Button(self.root, text="Browse", command=self.load_image).pack()
        
        tk.Label(self.root, text="Enter Secret Message").pack()
        self.msg_entry = tk.Entry(self.root, width=40)
        self.msg_entry.pack()
        
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
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        self.image_entry.delete(0, tk.END)
        self.image_entry.insert(0, file_path)
    
    def load_decode_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        self.decode_image_entry.delete(0, tk.END)
        self.decode_image_entry.insert(0, file_path)
    
    def encode_message(self):
        image_path = self.image_entry.get()
        msg = self.msg_entry.get()
        password = self.password_entry.get()
        
        if not image_path or not msg or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        img = cv2.imread(image_path)
        d = {chr(i): i for i in range(255)}
        
        n, m, z = 0, 0, 0
        for char in msg:
            img[n, m, z] = d[char]
            n += 1
            m += 1
            z = (z + 1) % 3
        
        save_path = image_path.replace(".png", "_encoded.png")
        save_path = image_path.replace(".jpg", "_encoded.jpg")
        cv2.imwrite(save_path, img)
        os.system(f'start "" "{save_path}"')
        messagebox.showinfo("Success", f"Encoded Image saved at {save_path}")
    
    def decode_message(self):
        image_path = self.decode_image_entry.get()
        password = self.decode_password_entry.get()
        
        if not image_path or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        img = cv2.imread(image_path)
        c = {i: chr(i) for i in range(255)}
        
        n, m, z = 0, 0, 0
        message = ""
        for _ in range(len(password)):
            message += c[img[n, m, z]]
            n += 1
            m += 1
            z = (z + 1) % 3
        
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            messagebox.showerror("Error", "Output folder is required!")
            return
        
        output_path = os.path.join(output_folder, "decrypted_message.txt")
        with open(output_path, "w") as f:
            f.write(message)
        
        messagebox.showinfo("Success", f"Decrypted message saved at {output_path}")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

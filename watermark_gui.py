import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from watermark_bot import WatermarkBot

class WatermarkBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Bot")
        self.root.geometry("600x500")
        
        # Initialize watermark bot
        self.bot = WatermarkBot()
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.author_name = tk.StringVar(value="Your Name")
        self.website = tk.StringVar(value="your-website.com")
        self.visible_text = tk.StringVar(value="© 2024")
        self.top_left = tk.BooleanVar(value=False)
        self.top_right = tk.BooleanVar(value=False)
        self.bottom_left = tk.BooleanVar(value=False)
        self.bottom_right = tk.BooleanVar(value=True)  # Default to bottom-right
        self.center = tk.BooleanVar(value=False)
        self.font_size = tk.IntVar(value=24)
        self.opacity = tk.IntVar(value=70)
        self.add_invisible = tk.BooleanVar(value=True)
        self.add_visible = tk.BooleanVar(value=True)
        self.add_metadata = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Watermark Bot", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        ttk.Label(main_frame, text="Input Image:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=1, column=2)
        
        ttk.Label(main_frame, text="Output Image:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=2, column=2)
        
        # Author information
        author_frame = ttk.LabelFrame(main_frame, text="Author Information", padding="10")
        author_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(author_frame, text="Author Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(author_frame, textvariable=self.author_name, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(author_frame, text="Website:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(author_frame, textvariable=self.website, width=30).grid(row=1, column=1, padx=5)
        
        # Watermark options
        watermark_frame = ttk.LabelFrame(main_frame, text="Watermark Options", padding="10")
        watermark_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Checkboxes
        ttk.Checkbutton(watermark_frame, text="Add Invisible Watermark", 
                       variable=self.add_invisible).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(watermark_frame, text="Add Visible Watermark", 
                       variable=self.add_visible).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(watermark_frame, text="Add Metadata", 
                       variable=self.add_metadata).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Visible watermark settings
        visible_frame = ttk.Frame(watermark_frame)
        visible_frame.grid(row=0, column=1, rowspan=3, padx=20)
        
        ttk.Label(visible_frame, text="Visible Text:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(visible_frame, textvariable=self.visible_text, width=20).grid(row=0, column=1, padx=5)
        
        # Position checkboxes
        ttk.Label(visible_frame, text="Positions:").grid(row=1, column=0, sticky=tk.W, pady=2)
        positions_frame = ttk.Frame(visible_frame)
        positions_frame.grid(row=1, column=1, padx=5)
        
        ttk.Checkbutton(positions_frame, text="Top-Left", variable=self.top_left).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(positions_frame, text="Top-Right", variable=self.top_right).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(positions_frame, text="Bottom-Left", variable=self.bottom_left).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(positions_frame, text="Bottom-Right", variable=self.bottom_right).grid(row=1, column=1, sticky=tk.W)
        ttk.Checkbutton(positions_frame, text="Center", variable=self.center).grid(row=2, column=0, sticky=tk.W)
        
        ttk.Label(visible_frame, text="Font Size:").grid(row=2, column=0, sticky=tk.W, pady=2)
        font_size_spinbox = ttk.Spinbox(visible_frame, from_=8, to=100, textvariable=self.font_size, 
                                       width=10, increment=1)
        font_size_spinbox.grid(row=2, column=1, padx=5)
        
        ttk.Label(visible_frame, text="Opacity (%):").grid(row=3, column=0, sticky=tk.W, pady=2)
        opacity_spinbox = ttk.Spinbox(visible_frame, from_=1, to=100, textvariable=self.opacity, 
                                     width=10, increment=5)
        opacity_spinbox.grid(row=3, column=1, padx=5)
        
        # Process button
        process_button = ttk.Button(main_frame, text="Process Image", command=self.process_image)
        process_button.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to process images")
        self.status_label.grid(row=6, column=0, columnspan=3)
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.input_path.set(filename)
            # Auto-generate output filename
            if not self.output_path.get():
                base_name = os.path.splitext(filename)[0]
                self.output_path.set(f"{base_name}_watermarked.png")
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def process_image(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input image")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output image")
            return
        
        if not self.add_invisible.get() and not self.add_visible.get() and not self.add_metadata.get():
            messagebox.showerror("Error", "Please select at least one watermark option")
            return
        
        try:
            # Update bot with current settings
            self.bot.author_name = self.author_name.get()
            self.bot.website = self.website.get()
            
            # Process image
            self.status_label.config(text="Processing image...")
            self.root.update()
            
            # Build positions list from checkboxes
            positions = []
            if self.top_left.get():
                positions.append('top-left')
            if self.top_right.get():
                positions.append('top-right')
            if self.bottom_left.get():
                positions.append('bottom-left')
            if self.bottom_right.get():
                positions.append('bottom-right')
            if self.center.get():
                positions.append('center')
            
            # Default to bottom-right if no positions selected
            if not positions:
                positions = ['bottom-right']
            
            self.bot.process_image(
                input_path=self.input_path.get(),
                output_path=self.output_path.get(),
                add_invisible=self.add_invisible.get(),
                add_visible=self.add_visible.get(),
                add_metadata=self.add_metadata.get(),
                visible_text=self.visible_text.get(),
                visible_positions=positions,
                font_size=self.font_size.get(),
                opacity=self.opacity.get()
            )
            
            self.status_label.config(text="Image processed successfully!")
            messagebox.showinfo("Success", f"Image processed successfully!\nSaved to: {self.output_path.get()}")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error processing image:\n{str(e)}")

def main():
    root = tk.Tk()
    app = WatermarkBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
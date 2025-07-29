import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import glob
from watermark_bot import WatermarkBot

class WatermarkBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Bot")
        self.root.geometry("700x675")
        
        # Initialize watermark bot
        self.bot = WatermarkBot()
        
        # Variables
        self.processing_mode = tk.StringVar(value="single")  # "single" or "batch"
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.mark_postfix = tk.StringVar(value="_watermarked")
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
        
        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Processing Mode", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="Single Image", variable=self.processing_mode, 
                       value="single", command=self.on_mode_change).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(mode_frame, text="Batch Processing (Directory)", variable=self.processing_mode, 
                       value="batch", command=self.on_mode_change).grid(row=0, column=1, padx=10)
        
        # File/Directory selection frame
        self.selection_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        self.selection_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Single file widgets
        self.single_widgets = []
        self.single_widgets.append(ttk.Label(self.selection_frame, text="Input Image:"))
        self.single_widgets.append(ttk.Entry(self.selection_frame, textvariable=self.input_path, width=50))
        self.single_widgets.append(ttk.Button(self.selection_frame, text="Browse", command=self.browse_input))
        self.single_widgets.append(ttk.Label(self.selection_frame, text="Output Image:"))
        self.single_widgets.append(ttk.Entry(self.selection_frame, textvariable=self.output_path, width=50))
        self.single_widgets.append(ttk.Button(self.selection_frame, text="Browse", command=self.browse_output))
        
        # Batch widgets
        self.batch_widgets = []
        self.batch_widgets.append(ttk.Label(self.selection_frame, text="Input Directory:"))
        self.batch_widgets.append(ttk.Entry(self.selection_frame, textvariable=self.input_dir, width=50))
        self.batch_widgets.append(ttk.Button(self.selection_frame, text="Browse", command=self.browse_input_dir))
        self.batch_widgets.append(ttk.Label(self.selection_frame, text="Output Directory:"))
        self.batch_widgets.append(ttk.Entry(self.selection_frame, textvariable=self.output_dir, width=50))
        self.batch_widgets.append(ttk.Button(self.selection_frame, text="Browse", command=self.browse_output_dir))
        self.batch_widgets.append(ttk.Label(self.selection_frame, text="File Postfix:"))
        self.batch_widgets.append(ttk.Entry(self.selection_frame, textvariable=self.mark_postfix, width=20))
        
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
        self.process_button = ttk.Button(main_frame, text="Process Image", command=self.process_image)
        self.process_button.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to process images")
        self.status_label.grid(row=6, column=0, columnspan=3)
        
        # Initialize mode
        self.on_mode_change()
        
    def on_mode_change(self):
        """Handle mode change between single file and batch processing"""
        if self.processing_mode.get() == "single":
            # Show single file widgets
            for i, widget in enumerate(self.single_widgets):
                widget.grid(row=i//3, column=i%3, sticky=tk.W if i%3==0 else tk.EW, pady=2, padx=2)
            # Hide batch widgets
            for widget in self.batch_widgets:
                widget.grid_remove()
            self.process_button.config(text="Process Image")
        else:
            # Hide single file widgets
            for widget in self.single_widgets:
                widget.grid_remove()
            # Show batch widgets
            for i, widget in enumerate(self.batch_widgets):
                widget.grid(row=i//3, column=i%3, sticky=tk.W if i%3==0 else tk.EW, pady=2, padx=2)
            self.process_button.config(text="Process Directory")
        
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
    
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir.set(directory)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def get_supported_image_files(self, input_dir):
        """Get all supported image files from input directory"""
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        image_files = []
        for ext in supported_formats:
            image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext}")))
            image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext.upper()}")))
        return image_files
    
    def process_image(self):
        if self.processing_mode.get() == "single":
            self.process_single_image()
        else:
            self.process_batch()
    
    def process_single_image(self):
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
    
    def process_batch(self):
        if not self.input_dir.get():
            messagebox.showerror("Error", "Please select an input directory")
            return
        
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        if not self.add_invisible.get() and not self.add_visible.get() and not self.add_metadata.get():
            messagebox.showerror("Error", "Please select at least one watermark option")
            return
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Get all image files
            image_files = self.get_supported_image_files(self.input_dir.get())
            
            if not image_files:
                messagebox.showerror("Error", f"No supported image files found in {self.input_dir.get()}")
                return
            
            # Update bot with current settings
            self.bot.author_name = self.author_name.get()
            self.bot.website = self.website.get()
            
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
            
            # Process each image
            successful = 0
            failed = 0
            
            self.status_label.config(text=f"Processing {len(image_files)} images...")
            self.root.update()
            
            for i, image_path in enumerate(image_files, 1):
                try:
                    # Generate output filename
                    filename = os.path.basename(image_path)
                    name, ext = os.path.splitext(filename)
                    output_filename = f"{name}{self.mark_postfix.get()}{ext}"
                    output_path = os.path.join(self.output_dir.get(), output_filename)
                    
                    # Update status
                    self.status_label.config(text=f"Processing {i}/{len(image_files)}: {filename}")
                    self.root.update()
                    
                    # Process the image
                    self.bot.process_image(
                        input_path=image_path,
                        output_path=output_path,
                        add_invisible=self.add_invisible.get(),
                        add_visible=self.add_visible.get(),
                        add_metadata=self.add_metadata.get(),
                        visible_text=self.visible_text.get(),
                        visible_positions=positions,
                        font_size=self.font_size.get(),
                        opacity=self.opacity.get()
                    )
                    
                    successful += 1
                    
                except Exception as e:
                    failed += 1
                    print(f"✗ Failed to process {filename}: {str(e)}")
            
            # Show results
            self.status_label.config(text=f"Batch processing completed! Successful: {successful}, Failed: {failed}")
            messagebox.showinfo("Batch Processing Complete", 
                              f"Batch processing completed!\n\nSuccessful: {successful}\nFailed: {failed}\n\nOutput directory: {self.output_dir.get()}")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error during batch processing:\n{str(e)}")

def main():
    root = tk.Tk()
    app = WatermarkBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
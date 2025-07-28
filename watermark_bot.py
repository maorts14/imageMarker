import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import piexif
from datetime import datetime
import argparse

class WatermarkBot:
    def __init__(self, author_name="Your Name", website="your-website.com"):
        """
        Initialize the watermark bot with author information
        
        Args:
            author_name (str): Your name for metadata
            website (str): Your website for metadata
        """
        self.author_name = author_name
        self.website = website
        
    def add_invisible_watermark(self, image_path, output_path, watermark_text="Protected"):
        """
        Add invisible watermark using LSB (Least Significant Bit) steganography
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save watermarked image
            watermark_text (str): Text to embed as invisible watermark
        """
        # Read image using PIL for better Hebrew path support
        try:
            pil_img = Image.open(image_path)
            img = np.array(pil_img)
            if len(img.shape) == 3 and img.shape[2] == 4:  # RGBA
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            elif len(img.shape) == 3:  # RGB
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # If grayscale, no conversion needed
        except Exception as e:
            raise ValueError(f"Could not read image from {image_path}: {str(e)}")
            
        # Convert text to binary
        binary_text = ''.join(format(ord(char), '08b') for char in watermark_text)
        binary_text += '00000000'  # Add null terminator
        
        # Check if image can hold the text
        if len(binary_text) > img.size:
            raise ValueError("Image too small to hold watermark text")
            
        # Flatten image
        flat_img = img.flatten()
        
        # Embed watermark in LSB
        for i, bit in enumerate(binary_text):
            if i < len(flat_img):
                flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
                
        # Reshape back to original dimensions
        watermarked_img = flat_img.reshape(img.shape)
        
        # Save watermarked image using PIL for better Hebrew path support
        if len(watermarked_img.shape) == 3:
            watermarked_img = cv2.cvtColor(watermarked_img, cv2.COLOR_BGR2RGB)
        pil_watermarked = Image.fromarray(watermarked_img)
        
        # Ensure output is PNG format
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + '.png'
        
        pil_watermarked.save(output_path, format='PNG')
        print(f"Invisible watermark added: {watermark_text}")
        
    def add_visible_watermark(self, image_path, output_path, watermark_text="© 2024", 
                            positions=None, opacity=70, font_size=24):
        """
        Add visible watermark to image
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save watermarked image
            watermark_text (str): Text to display as watermark
            position (str): Position of watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
            opacity (float): Opacity of watermark (0.0 to 1.0)
            font_size (int): Font size for watermark text
        """
        # Open image
        img = Image.open(image_path)
        
        # Create a copy for watermark
        watermarked = img.copy()
        
        # Create transparent overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Try to use a default font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Get image dimensions
        img_width, img_height = img.size
        
        # Calculate margin based on font size (minimum 10px, scales with font size)
        margin = max(10, font_size // 3)
        
        # Convert opacity from percentage to decimal (0-100 to 0-1)
        opacity_decimal = opacity / 100.0
        
        # Default to bottom-right if no positions specified
        if positions is None:
            positions = ['bottom-right']
        
        # Draw watermark text at each selected position
        for position in positions:
            if position == 'top-left':
                x, y = margin, margin
            elif position == 'top-right':
                x, y = img_width - text_width - margin, margin
            elif position == 'bottom-left':
                x, y = margin, img_height - text_height - margin
            elif position == 'bottom-right':
                x, y = img_width - text_width - margin, img_height - text_height - margin
            elif position == 'center':
                x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
            
            # Draw watermark text at this position
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, int(255 * opacity_decimal)))
        
        # Composite overlay onto image
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        watermarked = Image.alpha_composite(img, overlay)
        
        # Convert back to RGB if original was RGB
        if img.mode == 'RGB':
            watermarked = watermarked.convert('RGB')
        
        # Ensure output is PNG format
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + '.png'
        
        # Save watermarked image
        watermarked.save(output_path, format='PNG')
        print(f"Visible watermark added: {watermark_text}")
        
    def add_metadata(self, image_path, output_path):
        """
        Add metadata (EXIF) to image with author information
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save image with metadata
        """
        # Open image
        img = Image.open(image_path)
        
        # Prepare EXIF data
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        
        # Add artist (author name)
        exif_dict["0th"][piexif.ImageIFD.Artist] = self.author_name.encode('utf-8')
        
        # Add copyright
        copyright_text = f"© {datetime.now().year} {self.author_name}"
        exif_dict["0th"][piexif.ImageIFD.Copyright] = copyright_text.encode('utf-8')
        
        # Add software
        exif_dict["0th"][piexif.ImageIFD.Software] = "WatermarkBot".encode('utf-8')
        
        # Add website in user comment
        user_comment = f"Website: {self.website}".encode('utf-8')
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment
        
        # Add date/time
        current_time = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
        exif_dict["0th"][piexif.ImageIFD.DateTime] = current_time.encode('utf-8')
        
        # Convert to EXIF bytes
        exif_bytes = piexif.dump(exif_dict)
        
        # Ensure output is PNG format
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + '.png'
        
        # Save image with EXIF data
        img.save(output_path, format='PNG', exif=exif_bytes)
        print(f"Metadata added: Author={self.author_name}, Website={self.website}")
        
    def process_image(self, input_path, output_path, add_invisible=True, add_visible=True, 
                     add_metadata=True, visible_text="© 2024", visible_positions=None, font_size=24, opacity=70):
        """
        Process image with all watermark types
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save processed image
            add_invisible (bool): Whether to add invisible watermark
            add_visible (bool): Whether to add visible watermark
            add_metadata (bool): Whether to add metadata
            visible_text (str): Text for visible watermark
            visible_position (str): Position of visible watermark
            font_size (int): Font size for visible watermark
        """
        temp_path = input_path
        
        try:
            # Add invisible watermark
            if add_invisible:
                temp_invisible = f"temp_invisible_{os.path.basename(input_path)}"
                self.add_invisible_watermark(temp_path, temp_invisible)
                temp_path = temp_invisible
            
            # Add visible watermark
            if add_visible:
                temp_visible = f"temp_visible_{os.path.basename(input_path)}"
                self.add_visible_watermark(temp_path, temp_visible, visible_text, visible_positions, font_size=font_size, opacity=opacity)
                temp_path = temp_visible
            
            # Add metadata
            if add_metadata:
                self.add_metadata(temp_path, output_path)
            else:
                # If no metadata, just copy the last temp file to output
                import shutil
                shutil.copy2(temp_path, output_path)
                
            # Clean up temp files
            if add_invisible and os.path.exists(f"temp_invisible_{os.path.basename(input_path)}"):
                os.remove(f"temp_invisible_{os.path.basename(input_path)}")
            if add_visible and os.path.exists(f"temp_visible_{os.path.basename(input_path)}"):
                os.remove(f"temp_visible_{os.path.basename(input_path)}")
                
            print(f"Image processed successfully: {output_path}")
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            # Clean up temp files on error
            for temp_file in [f"temp_invisible_{os.path.basename(input_path)}", 
                            f"temp_visible_{os.path.basename(input_path)}"]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def main():
    # Set up proper encoding for Windows with Hebrew characters
    import sys
    if sys.platform.startswith('win'):
        import locale
        # Try to set UTF-8 encoding for better Hebrew support
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    parser = argparse.ArgumentParser(description='Watermark Bot - Add watermarks and metadata to images')
    parser.add_argument('--input', required=True, help='Path to input image')
    parser.add_argument('--output', required=True, help='Path to output image')
    parser.add_argument('--author', default='Your Name', help='Author name for metadata')
    parser.add_argument('--website', default='your-website.com', help='Website for metadata')
    parser.add_argument('--no-invisible', action='store_true', help='Skip invisible watermark')
    parser.add_argument('--no-visible', action='store_true', help='Skip visible watermark')
    parser.add_argument('--no-metadata', action='store_true', help='Skip metadata')
    parser.add_argument('--visible-text', default='© 2024', help='Text for visible watermark')
    parser.add_argument('--top-left', action='store_true', help='Add watermark to top-left position')
    parser.add_argument('--top-right', action='store_true', help='Add watermark to top-right position')
    parser.add_argument('--bottom-left', action='store_true', help='Add watermark to bottom-left position')
    parser.add_argument('--bottom-right', action='store_true', help='Add watermark to bottom-right position')
    parser.add_argument('--center', action='store_true', help='Add watermark to center position')
    parser.add_argument('--font-size', type=int, default=24, help='Font size for visible watermark')
    parser.add_argument('--opacity', type=int, default=70, help='Opacity percentage for visible watermark (0-100)')
    
    args = parser.parse_args()
    
    # Create watermark bot
    bot = WatermarkBot(author_name=args.author, website=args.website)
    
    # Build positions list from command line arguments
    positions = []
    if args.top_left:
        positions.append('top-left')
    if args.top_right:
        positions.append('top-right')
    if args.bottom_left:
        positions.append('bottom-left')
    if args.bottom_right:
        positions.append('bottom-right')
    if args.center:
        positions.append('center')
    
    # Default to bottom-right if no positions specified
    if not positions:
        positions = ['bottom-right']
    
    # Process image
    bot.process_image(
        input_path=args.input,
        output_path=args.output,
        add_invisible=not args.no_invisible,
        add_visible=not args.no_visible,
        add_metadata=not args.no_metadata,
        visible_text=args.visible_text,
        visible_positions=positions,
        font_size=args.font_size,
        opacity=args.opacity
    )

if __name__ == "__main__":
    main() 
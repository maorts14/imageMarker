#!/usr/bin/env python3
"""
Batch processor for watermarking multiple images at once.
This script processes all images in a directory and saves them to an output directory.
"""

import os
import glob
from watermark_bot import WatermarkBot
import argparse

class BatchWatermarkProcessor:
    def __init__(self, author_name="Your Name", website="your-website.com"):
        self.bot = WatermarkBot(author_name=author_name, website=website)
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
    def get_image_files(self, input_dir):
        """Get all supported image files from input directory"""
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext}")))
            image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext.upper()}")))
        return image_files
    
    def process_directory(self, input_dir, output_dir, mark_postfix, **kwargs):
        """
        Process all images in input directory and save to output directory
        Args:
            input_dir (str): Input directory path
            output_dir (str): Output directory path
            mark_postfix (str): Postfix to add to marked images
            **kwargs: Arguments to pass to process_image method
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all image files
        image_files = self.get_image_files(input_dir)
        
        if not image_files:
            print(f"No supported image files found in {input_dir}")
            return
        
        print(f"Found {len(image_files)} images to process")
        
        # Process each image
        successful = 0
        failed = 0
        
        for i, image_path in enumerate(image_files, 1):
            try:
                # Generate output filename
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}{mark_postfix}{ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                print(f"Processing {i}/{len(image_files)}: {filename}")
                
                # Process the image
                self.bot.process_image(
                    input_path=image_path,
                    output_path=output_path,
                    **kwargs
                )
                
                successful += 1
                print(f"✓ Successfully processed: {filename}")
                
            except Exception as e:
                failed += 1
                print(f"✗ Failed to process {filename}: {str(e)}")
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"Batch processing completed!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Output directory: {output_dir}")
        print(f"{'='*50}")

def main():
    parser = argparse.ArgumentParser(description='Batch watermark processor (directory version of watermark_bot.py)')
    parser.add_argument('--input_dir', required=True, help='Input directory containing images')
    parser.add_argument('--output_dir', required=True, help='Output directory for processed images')
    parser.add_argument('--mark_postfix', default='_watermarked', help='Postfix to add to marked images (default: _watermarked)')
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

    # Validate input directory
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return

    # Create batch processor
    processor = BatchWatermarkProcessor(
        author_name=args.author,
        website=args.website
    )

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

    # Process directory
    processor.process_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        mark_postfix=args.mark_postfix,
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
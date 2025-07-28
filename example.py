#!/usr/bin/env python3
"""
Example script demonstrating how to use the WatermarkBot class programmatically.
This script shows different ways to add watermarks to images.
"""

from watermark_bot import WatermarkBot
import os

def main():
    # Create a watermark bot instance with your information
    bot = WatermarkBot(
        author_name="John Doe",
        website="johndoe.com"
    )
    
    # Example 1: Add all types of watermarks
    print("Example 1: Adding all types of watermarks")
    try:
        bot.process_image(
            input_path="sample_image.jpg",  # Replace with your image path
            output_path="watermarked_full.jpg",
            add_invisible=True,
            add_visible=True,
            add_metadata=True,
            visible_text="© 2024 John Doe",
            visible_position="bottom-right"
        )
        print("✓ Full watermarking completed")
    except FileNotFoundError:
        print("⚠ Sample image not found - skipping example 1")
    
    # Example 2: Add only visible watermark
    print("\nExample 2: Adding only visible watermark")
    try:
        bot.process_image(
            input_path="sample_image.jpg",  # Replace with your image path
            output_path="watermarked_visible.jpg",
            add_invisible=False,
            add_visible=True,
            add_metadata=False,
            visible_text="PROTECTED",
            visible_position="center"
        )
        print("✓ Visible watermark completed")
    except FileNotFoundError:
        print("⚠ Sample image not found - skipping example 2")
    
    # Example 3: Add only metadata
    print("\nExample 3: Adding only metadata")
    try:
        bot.process_image(
            input_path="sample_image.jpg",  # Replace with your image path
            output_path="watermarked_metadata.jpg",
            add_invisible=False,
            add_visible=False,
            add_metadata=True
        )
        print("✓ Metadata embedding completed")
    except FileNotFoundError:
        print("⚠ Sample image not found - skipping example 3")
    
    # Example 4: Custom invisible watermark
    print("\nExample 4: Custom invisible watermark")
    try:
        bot.add_invisible_watermark(
            image_path="sample_image.jpg",  # Replace with your image path
            output_path="watermarked_invisible.jpg",
            watermark_text="This image belongs to John Doe"
        )
        print("✓ Invisible watermark completed")
    except FileNotFoundError:
        print("⚠ Sample image not found - skipping example 4")
    
    print("\n" + "="*50)
    print("To test these examples:")
    print("1. Place a sample image named 'sample_image.jpg' in this directory")
    print("2. Run this script: python example.py")
    print("3. Check the generated output files")
    print("="*50)

if __name__ == "__main__":
    main() 
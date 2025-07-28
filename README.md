# Watermark Bot

A Python bot that adds invisible watermarks, visible watermarks, and metadata to images. Perfect for protecting your digital assets and adding copyright information.

## Features

### 1. Invisible Watermark
- Uses LSB (Least Significant Bit) steganography to embed hidden text
- Completely invisible to the human eye
- Can be extracted with specialized tools
- Perfect for copyright protection and ownership verification

### 2. Visible Watermark
- Adds visible text overlay to images
- Customizable text, position, and opacity
- Multiple position options: top-left, top-right, bottom-left, bottom-right, center
- Professional appearance with semi-transparent overlay

### 3. Metadata Embedding
- Adds EXIF metadata to images
- Includes author name, copyright information, and website
- Preserves image quality while adding ownership information
- Compatible with standard image viewers and metadata readers

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The bot can be used from the command line with various options:

```bash
# Basic usage with all features enabled
python watermark_bot.py input_image.jpg output_image.jpg

# Customize author information
python watermark_bot.py input.jpg output.jpg --author "John Doe" --website "johndoe.com"

# Customize visible watermark
python watermark_bot.py input.jpg output.jpg --visible-text "© 2024 John Doe" --visible-position center

# Skip specific features
python watermark_bot.py input.jpg output.jpg --no-invisible --no-visible --no-metadata

# Help
python watermark_bot.py --help
```

### Command Line Options

- `input_image`: Path to the input image
- `output_image`: Path to save the processed image
- `--author`: Your name for metadata (default: "Your Name")
- `--website`: Your website for metadata (default: "your-website.com")
- `--no-invisible`: Skip invisible watermark
- `--no-visible`: Skip visible watermark
- `--no-metadata`: Skip metadata embedding
- `--visible-text`: Text for visible watermark (default: "© 2024")
- `--visible-position`: Position of visible watermark (choices: top-left, top-right, bottom-left, bottom-right, center)

### Graphical User Interface

For easier use, run the GUI version:

```bash
python watermark_gui.py
```

The GUI provides:
- File browser for selecting input and output images
- Form fields for author information
- Checkboxes to enable/disable features
- Dropdown for visible watermark position
- Real-time status updates

## Examples

### Example 1: Basic Watermarking
```bash
python watermark_bot.py photo.jpg watermarked_photo.jpg --author "Jane Smith" --website "janesmith.com"
```

This will:
- Add invisible watermark with text "Protected"
- Add visible watermark "© 2024" in bottom-right corner
- Add metadata with Jane Smith as author and janesmith.com as website

### Example 2: Custom Visible Watermark
```bash
python watermark_bot.py logo.png protected_logo.png --visible-text "© 2024 My Company" --visible-position center
```

### Example 3: Metadata Only
```bash
python watermark_bot.py image.jpg image_with_metadata.jpg --no-invisible --no-visible
```

## Supported Image Formats

- **Input**: JPG, JPEG, PNG, BMP, TIFF
- **Output**: JPG, PNG (depending on your choice)

## Technical Details

### Invisible Watermark Implementation
- Uses LSB steganography in the blue channel
- Embeds text as binary data in the least significant bits
- Adds null terminator for proper text extraction
- Checks image capacity before embedding

### Visible Watermark Implementation
- Creates transparent overlay with specified text
- Uses system fonts with fallback to default
- Supports RGBA and RGB image modes
- Maintains original image quality

### Metadata Implementation
- Uses EXIF format for maximum compatibility
- Embeds artist name, copyright, software info, and user comments
- Includes timestamp of processing
- Preserves existing metadata when possible

## Requirements

- Python 3.7+
- Pillow (PIL) for image processing
- OpenCV for invisible watermark
- piexif for EXIF metadata
- numpy for numerical operations

## Troubleshooting

### Common Issues

1. **"Image too small to hold watermark text"**
   - Use shorter text for invisible watermark
   - Use larger images

2. **Font not found**
   - The bot will automatically fall back to default font
   - No action required

3. **Permission errors**
   - Ensure you have write permissions for the output directory
   - Close the output file if it's open in another application

### Performance Tips

- For batch processing, use the command line interface
- Large images may take longer to process
- PNG files are typically larger than JPG for output

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the repository. 
# Image Encryption Tool

A powerful desktop application for encrypting and decrypting images using multiple algorithms. Built with Python, Tkinter, and PIL, this tool provides an intuitive graphical interface for secure image processing.

## ✨ Features

- **User-friendly GUI** with side-by-side image preview
- **Four encryption algorithms**:
  - **XOR Encryption** - Bitwise XOR operations with key-generated sequences
  - **Pixel Swap** - Deterministic pixel position shuffling
  - **Mathematical** - Modular arithmetic operations with multiplicative inverses
  - **Color Channel Shift** - RGB channel value shifting
- **Supports multiple formats**: JPG, JPEG, PNG, BMP, TIFF
- **Custom encryption keys** for personalized security
- **Real-time preview** of original and processed images
- **Save functionality** for encrypted/decrypted results
- **Reset option** to clear all images and start fresh

## 🖼️ Screenshot

The application features a clean, organized interface with:
- File selection panel
- Encryption method dropdown
- Key input field
- Control buttons (Encrypt, Decrypt, Save, Reset)
- Side-by-side image display
- Status bar for operation feedback

## 🚀 Installation

### Prerequisites

Make sure you have Python 3.7+ installed on your system.

### Required Dependencies

Install the required packages using pip:

```bash
pip install pillow numpy
```

Or install from requirements.txt (if available):

```bash
pip install -r requirements.txt
```

### Clone the Repository

```bash
git clone https://github.com/yourusername/image-encryption-tool.git
cd image-encryption-tool
```

## 🎯 Usage

### Running the Application

```bash
python image_encryption_tool.py
```

### Step-by-Step Guide

1. **Load an Image**
   - Click "Select Image" button
   - Choose your image file from the file dialog
   - The original image will appear in the left panel

2. **Choose Encryption Method**
   - Select from the dropdown menu:
     - XOR (default)
     - Pixel Swap
     - Mathematical
     - Color Channel Shift

3. **Set Encryption Key**
   - Enter your custom key in the text field
   - Default key is "12345"
   - Use the same key for decryption

4. **Encrypt the Image**
   - Click "Encrypt Image" button
   - Encrypted result appears in the right panel

5. **Decrypt the Image**
   - Click "Decrypt Image" button (with the same key)
   - Decrypted result replaces the processed image

6. **Save Results**
   - Click "Save Result" to export the processed image
   - Choose location and format (PNG/JPG)

7. **Reset**
   - Click "Reset" to clear all images and start over

## 🔐 Encryption Algorithms

### XOR Encryption
- Uses bitwise XOR operations with a deterministic key sequence
- Symmetric algorithm (same process for encryption/decryption)
- Fast and simple implementation

### Pixel Swap
- Rearranges pixel positions based on key-generated shuffle sequence
- Maintains image data integrity while scrambling appearance
- Reversible with the correct key

### Mathematical
- Applies modular arithmetic operations (multiplication and addition)
- Uses modular multiplicative inverse for decryption
- Ensures mathematical reversibility

### Color Channel Shift
- Shifts RGB channel values by key-derived amounts
- Preserves image structure while altering colors
- Lightweight and efficient

## 📁 Project Structure

```
image-encryption-tool/
│
├── image_encryption_tool.py    # Main application file
├── README.md                   # This file
├── requirements.txt            # Python dependencies (optional)
└── examples/                   # Sample images (optional)
    ├── sample1.jpg
    └── sample2.png
```

## 🛠️ Technical Details

### Dependencies
- **tkinter**: GUI framework (built into Python)
- **PIL (Pillow)**: Image processing library
- **numpy**: Numerical operations and array manipulation
- **random**: Pseudorandom number generation for key sequences

### Key Features Implementation
- **Deterministic key generation**: Uses hash() function for reproducible results
- **Image scaling**: Automatic resizing to fit display canvases
- **Error handling**: Comprehensive try-catch blocks with user-friendly messages
- **Memory management**: Proper image reference handling to prevent memory leaks

## ⚠️ Security Notes

- This tool is designed for **educational and demonstration purposes**
- The encryption methods provided are **not cryptographically secure** for sensitive data
- For production security needs, use established cryptographic libraries
- Always keep your encryption keys secure and private

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- Large images may take longer to process
- Some image formats might require conversion to RGB
- Application window is resizable but images maintain aspect ratio

## 🔮 Future Enhancements

- [ ] Additional encryption algorithms (AES, DES)
- [ ] Batch processing for multiple images
- [ ] Password strength indicator
- [ ] Image compression options
- [ ] Drag-and-drop file support
- [ ] Dark mode theme
- [ ] Progress bar for large files
- Python Software Foundation for the excellent Tkinter GUI toolkit
- PIL/Pillow team for robust image processing capabilities
- NumPy developers for efficient numerical computing tools

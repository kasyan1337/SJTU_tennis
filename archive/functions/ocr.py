import pytesseract
from PIL import Image

# Function to perform OCR
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    # Use the Image.open to open an image from the path provided
    text = pytesseract.image_to_string(Image.open(filename))
    return text

# Example usage
# Adjust the path to where your 'captcha.jpg' is located within the 'captchas' directory
image_path = 'captchas/captcha.jpeg'
extracted_text = ocr_core(image_path)
print(extracted_text)

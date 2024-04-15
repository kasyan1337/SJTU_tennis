from playwright.sync_api import sync_playwright
import base64
from PIL import Image
import pytesseract

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://my.sjtu.edu.cn/ui/me")
    page.wait_for_selector('img#captcha-img')

    # Get the Data URI of the captcha image
    image_data_uri = page.evaluate("""() => {
        const img = document.querySelector('img#captcha-img');
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        ctx.drawImage(img, 0, 0);
        return canvas.toDataURL('image/jpeg');
    }""")

    # Extract base64 data from URI
    base64_data = image_data_uri.split(',')[1]
    image_data = base64.b64decode(base64_data)

    # Save the image to the 'captchas' directory
    image_path = '../captchas/captcha.jpg'
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)

    context.close()
    browser.close()

    # Perform OCR on the saved image
    def ocr_core(filename):
        text = pytesseract.image_to_string(Image.open(filename))
        return text

    # Use the saved image path
    extracted_text = ocr_core(image_path)
    print(extracted_text)

with sync_playwright() as playwright:
    run(playwright)

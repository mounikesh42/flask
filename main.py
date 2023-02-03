from flask import Flask, request
import easyocr
import re
import io
from PIL import Image

app = Flask(__name__)

@app.route('/api/image', methods=['POST'])
def process_image():
    image = request.files['image']
    print(image)
    image = Image.open(image)
    image = image.convert('RGB')
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()
    reader = easyocr.Reader(['te','en'])
    text = reader.readtext(image_bytes) 
    txt = [item[1] for item in text if re.search(r'[\u0C00-\u0C7F]|[a-zA-Z+,]|[\d+\(\)\+\-\*/=]', str(item[1]))]
    return {"text": txt}

if __name__ == '__main__':
    app.run(debug=True)

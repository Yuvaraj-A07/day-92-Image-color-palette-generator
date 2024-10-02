from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from collections import Counter
import webcolors

app = Flask(__name__)


def get_top_colors(image_path, num_colors=10):
    image = Image.open(image_path)
    image = image.resize((100, 100))  # Resize for faster processing
    pixels = list(image.getdata())
    most_common_colors = Counter(pixels).most_common(num_colors)
    hex_colors = [webcolors.rgb_to_hex(color[0]) for color in most_common_colors]
    return hex_colors


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = f"./static/{file.filename}"
            file.save(file_path)
            top_colors = get_top_colors(file_path)
            return render_template('index.html', top_colors=top_colors, image_path=file_path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

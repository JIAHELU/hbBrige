from flask import Flask, render_template, request, send_from_directory
import qrcode
import time
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            # 保存上传的图片
            image_path = 'static/uploaded_image.png'
            image.save(image_path)

            # 生成二维码
            url = request.url_root + image_path
            timestamp = str(int(time.time()))  # 使用时间戳生成唯一的文件名
            qrcode_path = 'static/qrcode_{}.png'.format(timestamp)
            qr_image = qrcode.make(url)
            qr_image.save(qrcode_path)

            return render_template('qrcode.html', qrcode_path=qrcode_path)

    return "Image not provided or invalid."


# 注册静态文件 MIME 类型
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True)
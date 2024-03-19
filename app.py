import base64
import io
import os
import time
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from flask import Flask, request, Response, render_template, jsonify
import torch
import matplotlib.pyplot as plt
import torchvision

app = Flask(__name__, template_folder='static')

# 加载模型
torch.hub.set_dir('./')
use_gpu = True if torch.cuda.is_available() else False

# trained on high-quality celebrity faces "celebA" dataset
# this model outputs 512 x 512 pixel images
model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub',
                       'PGAN', model_name='celebAHQ-512',
                       pretrained=True, useGPU=use_gpu)


@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    num_images = int(data["num_images"])
    # start_time = data["start_time"]
    # print(start_time)
    start_time = time.time()
    if num_images <= 0:
        num_images = 1
    noise, _ = model.buildNoiseData(num_images)
    with torch.no_grad():
        generated_images = model.test(noise)
    grid = torchvision.utils.make_grid(generated_images.clamp(min=-1, max=1), scale_each=True, normalize=True)
    generated_images = grid.permute(1, 2, 0).cpu().numpy()

    plt.imshow(generated_images)
    plt.axis('off')

    img_io = io.BytesIO()
    plt.savefig(img_io, format='PNG', bbox_inches='tight', pad_inches=0)
    img_io.seek(0)
    img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return jsonify({"src": img_data, "time": (time.time() - start_time) * 1000})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

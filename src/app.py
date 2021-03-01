from flask import Flask, render_template, redirect, request
from PIL import Image
import random
from flask_cors import CORS
from detect_defect import detect

app = Flask(__name__)
CORS(app)
model = None
model_id = 0

@app.route('/')
def index():
    # return "hello world"
    # return render_template("/home/lby/face-mask-detection-app/dist/index.html")
    return render_template("index.html")

@app.route("/upload", methods=['post', 'get'])
def upload():
    global model

    f = request.files['file']
    print(f.filename)
    f.save('./static/'+f.filename)
    img_dir = f.filename
    # load_path = '/home/lby/RetinaNet_Pytorch110/checkpoints/retinanet_1e-5/retinanet_15.pth'
    random_num = str(random.random())
    save_path = './static/result'+random_num+'.png'
    # if model is None:
    #     model = load_model(load_path)
    # if model_id == 0:
    #     retinanet_inference_only(model, img_dir, save_path)
    # elif model_id == 1:
    #     ssd_inference_only(model, img_dir, save_path)
    # else:
    #     yolo3_inference_only(model, img_dir, save_path)
    
    # return 'http://166.111.180.117:8000/static/result'+random_num+'.png'
    return 'http://166.111.180.117:8000/static/'+str(img_dir)

@app.route("/detectresult", methods=['post', 'get'])
def detectresult():
    global model
    # f = request.files['file']
    # print(f.filename)
    # f.save('./static/'+f.filename)
    # img_dir = f.filename
    random_num = str(random.random())
    # save_path = './static/result'+random_num+'.png'
    # print(request.form)
    frameid = request.form.get('id')#, '/home/lby/lace-defect-detection-app/src/static/1.mp4')
    viddir = request.form.get('videosrc')
    # viddir = request.form['id']
    # viddir = '/home/lby/lace-defect-detection-app/defect_fabric.MTS'
    print(viddir)
    print(frameid)
    detect(viddir, int(float(frameid))*25, random_num)
    img_dir = 'result.png'
    return random_num

@app.route("/playvideo", methods=['post', 'get'])
def playvideo():
    global model
    viddir = request.form['id']#, 'http://166.111.180.117:8000/static/油污.MP4')
    print(viddir)
    return 'http://166.111.180.117:8000/static/油污.MP4'

@app.route("/getmodel", methods=['post', 'get'])
def getmodel():
    global model
    global model_id
    model_id = request.form.get('id', False)
    print(model_id)
    # if model_id == 0:
    #     load_path = '/home/lby/RetinaNet_Pytorch110/checkpoints/retinanet_15.pth'
    #     model = retinanet_load_model(load_path)
    # elif model_id == 1:
    #     load_path = '/home/lby/SSD_Pytorch/checkpoints/ssd_1e-4_8/ssd_21.pth'
    #     model = ssd_load_model(load_path)
    # else:
    #     load_path = '/home/lby/YOLO3_Pytorch/checkpoints/yolo3_5e-4/yolo3_11.pth'
    #     model = yolo3_load_model(load_path)
    return 'success'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

import numpy as np
import cv2
import glob
from fastai.vision import *
from fastai import *
from flask import Flask, request, jsonify
import posixpath
import base64-*

app = Flask(__name__)

# from fastai.callbacks import *

colors = np.loadtxt('labels.txt', delimiter='\n', dtype=str)

path_images = "train"
path_valid = "val"
fnames = get_image_files(path_images)


def get_y_fn(x): return (posixpath.join('train_masks', f'{x.stem}{x.suffix}')) if (
    x.parent.stem == 'train') else (posixpath.join('val_masks', f'{x.stem}{x.suffix}'))


class SegLabelListCustom(SegmentationLabelList):
    def open(self, fn): return open_mask(fn, div=False)


class SegItemListCustom(SegmentationItemList):
    _label_cls = SegLabelListCustom


"""Run this for training as during training size is 1/2 nd testing size is same as original (480,640)"""
src = (SegItemListCustom.from_folder(Path(''))
       .split_by_folder(train='train', valid='val')
       .label_from_func(get_y_fn, classes=colors)
       # tfms_y=True because transforms we r applying on trainset,will be also applied on train_masks
       .transform(get_transforms(), tfm_y=True, size=(256, 256))
       # since test_masks are empty we dont need tfms on ground truth here so tfm_y=False
       )

data = (src
        .databunch(bs=8)
        .normalize(imagenet_stats))

learn = unet_learner(data, models.resnet34)

learn.load("w2_cloth")


def evaluate(img_string):
    imgdata = base64.b64decode(img_string)
    test_image = PIL.Image.open(io.BytesIO(imgdata))
    test_image = Image(pil2tensor(test_image, dtype=np.float32).div_(255))
    img_segment = learn.predict(test_image)[0]
    mask = img_segment.data.permute(1, 2, 0).numpy()
    mask = (np.squeeze(mask, axis=2))*85
    mask = cv2.resize(mask, (512, 512), interpolation=cv2.INTER_NEAREST)
    return mask


@app.route("/", methods=["POST", "GET"])
def home():
    return "your api is working"


@app.route("/api", methods=["POST", "GET"])
def api_func():
    img_string = request.json["img_string"]
    mask = evaluate(img_string)
    print(mask.shape)
    retval, buffer = cv2.imencode('.png', mask)
    mask_string = base64.b64encode(buffer)
    return jsonify({
        "mask_string": mask_string.decode("utf-8")
    })


if '__main__' == __name__:
    app.run(host='0.0.0.0', port=8080)

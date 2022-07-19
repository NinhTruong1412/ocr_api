from fastapi import FastAPI, Depends, File
from segmentations import get_yolov5, get_info, last_check, get_image_from_bytes
from starlette.responses import Response
from PIL import Image
import json
from fastapi.middleware.cors import CORSMiddleware
import os
import io

cred = "composed-garden-355604-dab98e218271.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred


model = get_yolov5()

app = FastAPI(
    title="Custom YOLOV5 Machine Learning API",
    description="""Obtain object value out of image
                    and return image and json result""",
    version="0.0.1",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/notify/v1/health')
def get_health():
    """
    Usage on K8S
    readinessProbe:
        httpGet:
            path: /notify/v1/health
            port: 80
    livenessProbe:
        httpGet:
            path: /notify/v1/health
            port: 80
    :return:
        dict(msg='OK')
    """
    return dict(msg='OK')

@app.post("/v1/ocr")
async def detect_food_return_json_result(file: bytes = File(...)):
    info_result = get_info(file)
    img_temp = get_image_from_bytes(file)
    results = model(img_temp)
    img = results.crop()
    for i in img:
        if (i["cls"] == 0):
            img = Image.fromarray(i["im"], 'RGB')
            b = io.BytesIO()
            img.save(b, 'jpeg')
            im_bytes = b.getvalue()
        else:
            im_bytes = file
            print("This happen")
    coor_Result = last_check(im_bytes)
    return {"info": info_result, "coor": coor_Result}



# @app.post("/object-to-img")
# async def detect_food_return_base64_img(file: bytes = File(...)):
#     input_image = get_image_from_bytes(file)
#     results = model(input_image)
#     results.render()
#     for img in results.imgs:
#         bytes_io = io.BytesIO()
#         img_base64 = Image.fromarray(img)
#         # print(img_base64)
#         # a.append(img_base64)
#         img_base64.save(bytes_io, format="jpeg")
#     return Response(content=bytes_io.getvalue(), media_type="image/jpeg")
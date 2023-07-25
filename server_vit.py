import torch
import io

from typing import Annotated
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torchvision.transforms as T

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model
model = torch.jit.load("model_vit.script.pt")
model = model.eval()

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

@app.get("/infer")
async def infer(image: Annotated[bytes, File()]):
    if image is None:
            print('no image found!')
            return None
    
    img: Image.Image = Image.open(io.BytesIO(image))
    img = img.convert("RGB")
    img = img.resize((32, 32))
    img_t =  T.ToTensor()(img).unsqueeze(0)
    preds = model.forward_jit(img_t)
    preds = preds[0].tolist()

    return {classes[i]: preds[i] for i in range(10)}

@app.get("/health")
async def health():
    return {"message": "ok"}
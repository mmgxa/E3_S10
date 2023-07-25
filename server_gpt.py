import torch
import tiktoken

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Text(BaseModel):
    text: str
    max_tokens: int = 32
    temperature: float = 1.0
    

# tokenizer
cl100k_base = tiktoken.get_encoding("cl100k_base")

# In production, load the arguments directly instead of accessing private attributes
# See openai_public.py for examples of arguments for specific encodings
tokenizer = tiktoken.Encoding(
    # If you're changing the set of special tokens, make sure to use a different name
    # It should be clear from the name what behaviour to expect.
    name="cl100k_im",
    pat_str=cl100k_base._pat_str,
    mergeable_ranks=cl100k_base._mergeable_ranks,
    special_tokens={
        **cl100k_base._special_tokens,
        "<|im_start|>": 100264,
        "<|im_end|>": 100265,
    }
)

# load model
model = torch.jit.load("model_gpt.script.pt")
model = model.eval()

@app.get("/infer")
# async def infer(text: Annotated[Text, Body(embed=True)]):
async def infer(text: Text):
    input_enc = torch.tensor(tokenizer.encode(text.text))
    with torch.inference_mode():
        out_gen = model.model.generate(input_enc.unsqueeze(0).long(), 
                                                max_new_tokens=text.max_tokens,
                                                temperature=text.temperature)
    decoded = tokenizer.decode(out_gen[0].cpu().numpy().tolist())

    return {'text': decoded}

@app.get("/health")
async def health():
    return {"message": "ok"}
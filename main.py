from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Union

from bilibili.search import bvid_to_music


app = FastAPI()

class Status(BaseModel):
    status_code: int
    msg: str

class BasicResp(BaseModel):
    status: Status

@app.get("/", description="keep alive API", response_model=BasicResp)
async def root():
    resp = {
        "status": {
            "status_code": 200,
            "msg": "ok"
        }
    }
    return resp

class MusicInfo(BaseModel):
    name: str
    author: str
    source: str
    duration: int
    cover_image_url: str

class BproxyResp(BaseModel):
    data: MusicInfo
    status: Status

@app.get("/bproxy", description="a proxy service to fetch music info by BVid", response_model=Union[BproxyResp, BasicResp])
async def bproxy(request: Request, bvid: str=""):
    try:
        matched, name, author, source, duration, cover_image_url = await bvid_to_music(BVid=bvid)
        resp = {
            "data": {
                "name": name,
                "author": author,
                "source": source,
                "duration": duration,
                "cover_image_url": cover_image_url,
            },
            "status": {
                "status_code": 200,
                "msg": "ok",
            }
        }
    except Exception as e:
        resp = {
            "data": {},
            "status": {
                "status_code": 500,
                "msg": str(e)
            }
        }
    return resp


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
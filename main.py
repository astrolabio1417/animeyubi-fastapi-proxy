from typing import Union
from kwikscript import get_video
from fastapi import FastAPI

app = FastAPI()


@app.get("/kwik")
def kwik_video(url: Union[str, None] = None):
    if url is None:
        return {"error": "url is required"}

    return {"url": get_video(url)}

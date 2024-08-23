from typing import Union
from kwikscript import get_video
from fastapi import FastAPI

app = FastAPI()


@app.get("/kwik")
def kwik_video(url: Union[str, None] = None):
    if url is None:
        return {"error": "url is required"}

    return {"url": get_video(url)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="debug")

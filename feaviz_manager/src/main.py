from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from src.manager.data_manager import create_image_data_visualization, create_tablular_data_visualization
from fastapi.logger import logger
from fastapi.responses import RedirectResponse


class DataPath(BaseModel):
    path: str


app = FastAPI(title='Feaviz - Feature visualization using Astra', debug=True)


@app.post("/tables/")
def create_tabular_feature_visualization(tabular_data_path: DataPath):
    status = create_tablular_data_visualization(tabular_data_path.path, settings.keyspace)
    if status>=1:
        return RedirectResponse("http://localhost:8088/superset/dashboard/"+str(status))
    else:
        return RedirectResponse("http://localhost:8088/dashboard/list/")

@app.post("/images")
def create_image_feature_visualization(images_data_path: DataPath):
    status = create_image_data_visualization(images_data_path.path, settings.keyspace, settings.http_server_url,
                                    settings.model_label_path, settings.model_weights_path,
                                    settings.model_cfg_path)
    if status >= 1:
        return RedirectResponse("http://localhost:8088/superset/dashboard/"+str(status))
    else:
        return RedirectResponse("http://localhost:8088/dashboard/list/")

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    logger.info("Starting uvicorn server ")
    uvicorn.run(app, host="0.0.0.0",
                port=5120)
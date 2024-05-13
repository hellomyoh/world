
from fastapi import FastAPI
import uvicorn
from one_api.aliexpress_collector import ali
from one_api.vvic_collector import vvic
from fastapi.middleware.cors import CORSMiddleware
from oneloader_runner.modules.api_description import Oneloader_api_desc

app = FastAPI(openapi_tags=Oneloader_api_desc())

# CORS 시작
origins = [
    "http://localhost:8090/",
    "http://localhost:8000/",
    "http://10.98.25.72:8090",
    "http://211.37.147.213:8090"
    "http://211.37.147.213:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# CORS 끝₩

# include route for each sites
app.include_router(ali)
app.include_router(vvic)


@app.get('/')
def root():
    return {'status': True}

if __name__ == '__main__':
    uvicorn.run("one_api_root:app", host= "0.0.0.0", port=8000,
                reload=True, reload_dirs="../oneloader_runner/modules/",
                reload_includes= ["oneloader_runner/**/*.py"])
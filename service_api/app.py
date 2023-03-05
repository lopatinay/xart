from fastapi import FastAPI


from service_api.router.system import system_router
from service_api.router.v1 import api_v1


fast_app = FastAPI()
fast_app.include_router(system_router)
fast_app.include_router(api_v1)

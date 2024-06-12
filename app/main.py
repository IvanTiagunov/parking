 #!/usr/bin/env python
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router


def start_up():
    init_db()


app = FastAPI(on_startup=start_up())


app.include_router(auth_router)
app.include_router(user_router)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)

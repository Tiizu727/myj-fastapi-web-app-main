from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.extra_modules.auth import routers as auth
# from api.routers import done, task, user
# from api.routers import done, task, user, exp_get_post
# from api.routers import done, task, user, article
from api.routers import parts, products, user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(task.router)
# app.include_router(done.router)
app.include_router(user.router)
app.include_router(auth.router)
# # app.include_router(exp_get_post.router)
# app.include_router(article.router)
app.include_router(parts.router)
app.include_router(products.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

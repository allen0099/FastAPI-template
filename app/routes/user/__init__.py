from fastapi import APIRouter

router: APIRouter = APIRouter(prefix="/user", tags=["使用者"])


@router.get("/me")
def get_me():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

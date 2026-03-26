from fastapi import APIRouter
router=APIRouter()

@router.get("/test")
def users_test():
    return {"message": "Hello, Users!"}

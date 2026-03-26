from fastapi import APIRouter
router=APIRouter()
@router.get("/test")
def questions_test():
    return {"message": "Hello, Questions!"}
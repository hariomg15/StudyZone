from fastapi import APIRouter
router=APIRouter()
@router.get("/test")
def enrollements_test():
    return {"message": "Hello, Enrollements!"}
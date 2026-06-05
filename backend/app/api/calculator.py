from fastapi import APIRouter

from ..database.schemas import CalculatorRequest
from ..tools.calculator import calculate

router = APIRouter()


@router.post("/calculator")
def calculator(request: CalculatorRequest):
    return calculate(request.expression)

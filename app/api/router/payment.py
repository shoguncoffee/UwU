from .base import *

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)


@router.post("/{method}")
async def pay(
    method: PaymentMethod,
    
):
    """
    """
    
    return 
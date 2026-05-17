from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.models.user_extended import Order, UserCode
from app.services.payment_service import PaymentService
from pydantic import BaseModel

router = APIRouter(prefix="/api/orders", tags=["支付"])


class CreateOrderRequest(BaseModel):
    subscription_type: str  # monthly/yearly/permanent


class OrderResponse(BaseModel):
    order_no: str
    subject: str
    amount: float
    payment_status: str
    subscription_type: str


@router.post("/create")
def create_order(
    request: CreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        order = PaymentService.create_order(db, str(current_user.id), request.subscription_type)
        
        return {
            "order": {
                "order_no": order.order_no,
                "subject": order.subject,
                "amount": float(order.amount),
                "payment_status": order.payment_status,
                "subscription_type": order.subscription_type
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/alipay")
async def create_alipay_payment(
    order_no: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter_by(order_no=order_no, user_id=current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.payment_status == "paid":
        raise HTTPException(status_code=400, detail="订单已支付")
    
    payment_data = await PaymentService.create_alipay_payment(order)
    
    return {
        "payment_url": payment_data['payment_url'],
        "qr_code": payment_data['qr_code']
    }


@router.post("/wechat")
async def create_wechat_payment(
    order_no: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter_by(order_no=order_no, user_id=current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.payment_status == "paid":
        raise HTTPException(status_code=400, detail="订单已支付")
    
    payment_data = await PaymentService.create_wechat_payment(order)
    
    return {
        "payment_url": payment_data['payment_url'],
        "qr_code": payment_data['qr_code']
    }


@router.get("/history")
def get_order_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "orders": [
            {
                "order_no": order.order_no,
                "subject": order.subject,
                "amount": float(order.amount),
                "payment_status": order.payment_status,
                "payment_method": order.payment_method,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "payment_time": order.payment_time.isoformat() if order.payment_time else None
            }
            for order in orders
        ]
    }


@router.get("/{order_no}")
def get_order(
    order_no: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter_by(order_no=order_no, user_id=current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    return {
        "order": {
            "order_no": order.order_no,
            "subject": order.subject,
            "amount": float(order.amount),
            "payment_status": order.payment_status,
            "payment_method": order.payment_method,
            "subscription_type": order.subscription_type,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "payment_time": order.payment_time.isoformat() if order.payment_time else None
        }
    }


@router.get("/subscription/status")
def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    return {
        "is_subscribed": current_user.is_subscribed,
        "subscription_type": current_user.subscription_type,
        "subscription_expire_at": current_user.subscription_expire_at.isoformat() if current_user.subscription_expire_at else None
    }

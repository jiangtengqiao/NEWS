import uuid
from datetime import datetime, timedelta
from typing import Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.user_extended import Order
from app.schemas.order import OrderCreate


class PaymentService:
    """支付服务 - 支持支付宝和微信支付"""
    
    # 订阅价格配置
    SUBSCRIPTION_PRICES = {
        'monthly': {
            'name': '月度订阅',
            'price': Decimal('19.90'),
            'months': 1,
            'description': '可享受平台全部功能一个月'
        },
        'yearly': {
            'name': '年度订阅',
            'price': Decimal('199.00'),
            'months': 12,
            'description': '可享受平台全部功能一年，省省省'
        },
        'permanent': {
            'name': '永久会员',
            'price': Decimal('599.00'),
            'months': 999,  # 永久
            'description': '一次购买，永久享受全部功能'
        }
    }
    
    @staticmethod
    def generate_order_no() -> str:
        """生成唯一订单号"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = uuid.uuid4().hex[:6].upper()
        return f"ORDER{timestamp}{random_str}"
    
    @staticmethod
    def calculate_amount(subscription_type: str) -> Decimal:
        """计算订单金额"""
        price_info = PaymentService.SUBSCRIPTION_PRICES.get(subscription_type)
        if not price_info:
            raise ValueError(f"未知的订阅类型: {subscription_type}")
        return price_info['price']
    
    @staticmethod
    def create_order(db: Session, user_id: str, subscription_type: str) -> Order:
        """创建订单"""
        amount = PaymentService.calculate_amount(subscription_type)
        price_info = PaymentService.SUBSCRIPTION_PRICES[subscription_type]
        
        order = Order(
            user_id=user_id,
            order_no=PaymentService.generate_order_no(),
            subject=f"临桂资讯{price_info['name']}",
            amount=amount,
            subscription_type=subscription_type,
            subscription_months=price_info['months']
        )
        
        db.add(order)
        db.commit()
        db.refresh(order)
        
        return order
    
    @staticmethod
    async def create_alipay_payment(order: Order) -> dict:
        """创建支付宝支付"""
        # 支付宝支付逻辑（实际需要接入支付宝SDK）
        # 此处为模拟实现
        payment_url = f"https://openapi.alipay.com/gateway.do?_input_charset=utf-8&out_trade_no={order.order_no}&total_amount={order.amount}&subject={order.subject}"
        
        return {
            'order_no': order.order_no,
            'payment_url': payment_url,
            'qr_code': f"https://qr.alipay.com/{order.order_no}",
            'payment_method': 'alipay'
        }
    
    @staticmethod
    async def create_wechat_payment(order: Order, openid: str = None) -> dict:
        """创建微信支付"""
        # 微信支付逻辑（实际需要接入微信支付SDK）
        # 此处为模拟实现
        payment_url = f"https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id={order.order_no}"
        
        return {
            'order_no': order.order_no,
            'payment_url': payment_url,
            'qr_code': f"weixin://wxpay/bizpayurl?pr={order.order_no}",
            'payment_method': 'wechat'
        }
    
    @staticmethod
    def verify_alipay_callback(params: dict) -> bool:
        """验证支付宝回调"""
        # 实际需要验证签名
        # 此处为模拟实现
        return params.get('trade_status') == 'TRADE_SUCCESS'
    
    @staticmethod
    def verify_wechat_callback(params: dict) -> bool:
        """验证微信支付回调"""
        # 实际需要验证签名
        # 此处为模拟实现
        return params.get('result_code') == 'SUCCESS'
    
    @staticmethod
    def process_payment_success(db: Session, order_no: str, payment_method: str) -> bool:
        """处理支付成功"""
        order = db.query(Order).filter_by(order_no=order_no).first()
        if not order or order.payment_status == 'paid':
            return False
        
        # 更新订单状态
        order.payment_status = 'paid'
        order.payment_method = payment_method
        order.payment_time = datetime.now()
        
        # 更新用户订阅状态
        user = order.user
        if order.subscription_type == 'permanent':
            user.is_subscribed = True
            user.subscription_type = 'permanent'
            user.subscription_expire_at = datetime(2099, 12, 31)
        else:
            user.is_subscribed = True
            user.subscription_type = order.subscription_type
            
            if user.subscription_expire_at and user.subscription_expire_at > datetime.now():
                # 累加订阅时间
                new_expire = user.subscription_expire_at + timedelta(days=30 * order.subscription_months)
            else:
                new_expire = datetime.now() + timedelta(days=30 * order.subscription_months)
            
            user.subscription_expire_at = new_expire
        
        db.commit()
        return True
    
    @staticmethod
    def process_payment_refund(db: Session, order_no: str) -> bool:
        """处理退款"""
        order = db.query(Order).filter_by(order_no=order_no).first()
        if not order or order.payment_status != 'paid':
            return False
        
        # 更新订单状态
        order.payment_status = 'refunded'
        
        # 更新用户订阅状态
        user = order.user
        
        # 取消订阅
        if order.subscription_type == 'permanent':
            user.is_subscribed = False
            user.subscription_type = 'free'
            user.subscription_expire_at = None
        else:
            # 退还剩余天数
            if user.subscription_expire_at:
                refund_days = 30 * order.subscription_months
                user.subscription_expire_at = user.subscription_expire_at - timedelta(days=refund_days)
                
                if user.subscription_expire_at <= datetime.now():
                    user.is_subscribed = False
                    user.subscription_type = 'free'
                    user.subscription_expire_at = None
        
        db.commit()
        return True

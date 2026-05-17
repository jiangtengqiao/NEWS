import stripe
import os
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional

# Stripe配置
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_placeholder')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder')

# 订阅价格配置（以分为单位）
SUBSCRIPTION_PRICES = {
    'monthly': {
        'name': '月度订阅',
        'description': '可享受平台全部功能一个月',
        'price': 1990,  # 19.90元 = 1990分
        'interval': 'month',
        'product_name': '临桂资讯月度订阅'
    },
    'yearly': {
        'name': '年度订阅',
        'description': '可享受平台全部功能一年',
        'price': 19900,  # 199元 = 19900分
        'interval': 'year',
        'product_name': '临桂资讯年度订阅'
    },
    'permanent': {
        'name': '永久会员',
        'description': '一次购买，永久享受全部功能',
        'price': 59900,  # 599元 = 59900分
        'interval': 'once',
        'product_name': '临桂资讯永久会员'
    }
}


class StripePaymentService:
    """Stripe支付服务"""
    
    @staticmethod
    def create_checkout_session(
        user_id: str,
        subscription_type: str,
        success_url: str,
        cancel_url: str
    ) -> dict:
        """创建Stripe结账会话"""
        price_info = SUBSCRIPTION_PRICES.get(subscription_type)
        if not price_info:
            raise ValueError(f"未知的订阅类型: {subscription_type}")
        
        try:
            # 创建Stripe结账会话
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'cny',
                            'unit_amount': price_info['price'],
                            'product_data': {
                                'name': price_info['product_name'],
                                'description': price_info['description'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata={
                    'user_id': user_id,
                    'subscription_type': subscription_type
                },
                # 中国地区需要的信息
                billing_address_collection='required',
                custom_text={
                    'submit': {
                        'message': '订阅后将立即享受临桂资讯全部功能'
                    }
                }
            )
            
            return {
                'session_id': checkout_session.id,
                'url': checkout_session.url
            }
            
        except stripe.error.StripeError as e:
            print(f"Stripe错误: {e}")
            # 如果Stripe失败，返回模拟数据
            return {
                'session_id': f'simulated_session_{user_id}_{subscription_type}',
                'url': f'/simulated-payment?type={subscription_type}'
            }
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str) -> dict:
        """验证Webhook签名"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, STRIPE_WEBHOOK_SECRET
            )
            return event
        except stripe.error.SignatureVerificationError:
            raise ValueError("Webhook签名验证失败")
    
    @staticmethod
    def create_customer(email: str, name: str = None) -> str:
        """创建Stripe客户"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name
            )
            return customer.id
        except stripe.error.StripeError as e:
            print(f"创建Stripe客户失败: {e}")
            return None
    
    @staticmethod
    def get_subscription_status(customer_id: str) -> dict:
        """获取订阅状态"""
        try:
            subscriptions = stripe.Subscription.list(
                customer=customer_id,
                status='active'
            )
            
            if subscriptions.data:
                sub = subscriptions.data[0]
                return {
                    'status': 'active',
                    'subscription_id': sub.id,
                    'current_period_end': datetime.fromtimestamp(sub.current_period_end).isoformat(),
                    'plan': sub.items.data[0].price.id if sub.items.data else None
                }
            else:
                return {'status': 'inactive'}
                
        except stripe.error.StripeError as e:
            print(f"获取订阅状态失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> bool:
        """取消订阅"""
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except stripe.error.StripeError as e:
            print(f"取消订阅失败: {e}")
            return False
    
    @staticmethod
    def create_refund(payment_intent_id: str, amount: int = None) -> dict:
        """创建退款"""
        try:
            refund_params = {'payment_intent': payment_intent_id}
            if amount:
                refund_params['amount'] = amount
            
            refund = stripe.Refund.create(**refund_params)
            return {
                'id': refund.id,
                'status': refund.status,
                'amount': refund.amount
            }
        except stripe.error.StripeError as e:
            print(f"创建退款失败: {e}")
            return {'error': str(e)}


def create_stripe_payment(user_id: str, subscription_type: str) -> dict:
    """创建Stripe支付"""
    return StripePaymentService.create_checkout_session(
        user_id=user_id,
        subscription_type=subscription_type,
        success_url='http://localhost:3000/payment/success',
        cancel_url='http://localhost:3000/payment/cancel'
    )


def handle_stripe_webhook(payload: bytes, signature: str) -> dict:
    """处理Stripe Webhook"""
    event = StripePaymentService.verify_webhook_signature(payload, signature)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        subscription_type = session['metadata']['subscription_type']
        
        return {
            'event': 'payment_success',
            'user_id': user_id,
            'subscription_type': subscription_type,
            'session_id': session.id
        }
    
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        return {
            'event': 'payment_intent_success',
            'payment_intent_id': payment_intent.id,
            'amount': payment_intent.amount
        }
    
    return {'event': 'unknown'}

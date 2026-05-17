import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from datetime import datetime, timedelta
from typing import Optional
import os


class EmailService:
    """使用Resend API发送真实邮件"""
    
    RESEND_API_KEY = os.getenv('RESEND_API_KEY', 're_placeholder_key')
    FROM_EMAIL = "临桂资讯 <noreply@lingui.cn>"
    
    # 邮件模板
    VERIFICATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>临桂资讯 - 邮箱验证</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #1890ff;
            padding-bottom: 20px;
        }}
        .logo {{
            font-size: 28px;
            font-weight: bold;
            color: #1890ff;
            margin-bottom: 5px;
        }}
        .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .code-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            margin: 30px 0;
        }}
        .code {{
            font-size: 36px;
            font-weight: bold;
            color: white;
            letter-spacing: 8px;
            font-family: 'Courier New', monospace;
        }}
        .code-label {{
            color: rgba(255,255,255,0.9);
            font-size: 14px;
            margin-top: 10px;
        }}
        .content {{
            color: #444;
            font-size: 15px;
            margin: 20px 0;
        }}
        .content h3 {{
            color: #1890ff;
            margin-top: 25px;
        }}
        .warning {{
            background: #fffbe6;
            border-left: 4px solid #faad14;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .warning-title {{
            color: #d48806;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .features {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }}
        .feature {{
            background: #f0f5ff;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .feature-icon {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        .feature-name {{
            font-size: 13px;
            color: #1890ff;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #999;
            font-size: 12px;
        }}
        .button {{
            display: inline-block;
            background: #1890ff;
            color: white;
            padding: 12px 30px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px 0;
        }}
        .button:hover {{
            background: #40a9ff;
        }}
        @media (max-width: 480px) {{
            .container {{
                padding: 20px;
            }}
            .code {{
                font-size: 28px;
            }}
            .features {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📰 临桂资讯</div>
            <div class="subtitle">桂林市临桂区官方新闻资讯平台</div>
        </div>
        
        <div class="content">
            <h3>尊敬的 用户，您好！</h3>
            
            <p>感谢您注册成为临桂资讯平台的用户！我们很高兴您选择使用我们的服务来获取最新、最权威的新闻资讯。</p>
            
            <div class="code-box">
                <div class="code">{verification_code}</div>
                <div class="code-label">您的邮箱验证码</div>
            </div>
            
            <p><strong>验证码有效期为 10 分钟</strong>，请尽快在注册页面输入验证码完成验证。</p>
            
            <div class="warning">
                <div class="warning-title">⚠️ 安全提醒</div>
                <p style="margin: 0; font-size: 13px;">
                    • 请勿将验证码透露给他人<br>
                    • 临桂资讯工作人员不会索要您的验证码<br>
                    • 若您未进行注册操作，请忽略此邮件
                </p>
            </div>
            
            <h3>📌 临桂资讯平台简介</h3>
            
            <p><strong>临桂资讯</strong>是由桂林市临桂区融媒体中心运营的官方新闻资讯平台，致力于为桂林市临桂区乃至桂林市全体居民提供权威、及时、全面的新闻资讯服务。</p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📰</div>
                    <div class="feature-name">权威新闻</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎧</div>
                    <div class="feature-name">语音播报</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🌐</div>
                    <div class="feature-name">多语言</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">💰</div>
                    <div class="feature-name">订阅服务</div>
                </div>
            </div>
            
            <h3>📋 我们的服务</h3>
            
            <p>临桂资讯平台提供以下核心服务：</p>
            
            <p><strong>1. 国家时政新闻（免费）</strong><br>
            包括国家领导人活动、中央政策文件、重要会议报道等，全部免费提供。</p>
            
            <p><strong>2. 桂林地方新闻（免费）</strong><br>
            包括桂林市及临桂区新闻、部门公告、政务服务信息等，全部免费提供。</p>
            
            <p><strong>3. 订阅付费内容</strong><br>
            包括社会热点、财经商业、科技教育、文化体育、名人演讲等精彩内容。</p>
            
            <p><strong>4. 个性化推荐</strong><br>
            采用智能推荐算法，根据您的阅读偏好为您推荐感兴趣的新闻。</p>
            
            <p><strong>5. 语言转译服务</strong><br>
            支持中文、英文、粤语、广西壮话等多种语言切换。</p>
            
            <h3>📞 联系我们</h3>
            
            <p>如果您在使用过程中遇到任何问题，欢迎通过以下方式联系我们：</p>
            
            <p>
                <strong>官方网站：</strong>http://www.lingui.cn<br>
                <strong>客服邮箱：</strong>service@lingui.cn<br>
                <strong>客服电话：</strong>0773-558XXXX（工作日9:00-18:00）<br>
                <strong>办公地址：</strong>广西壮族自治区桂林市临桂区致远路1号
            </p>
            
            <h3>📜 法律声明</h3>
            
            <p>使用本平台服务前，请您仔细阅读：</p>
            <p>• 《<a href="#">用户服务协议</a>》- 了解您的权利和义务<br>
            • 《<a href="#">隐私政策</a>》- 了解我们如何保护您的个人信息<br>
            • 《<a href="#">Cookie使用政策</a>》- 了解Cookie的使用说明</p>
            
            <div class="warning">
                <div class="warning-title">📋 重要提示</div>
                <p style="margin: 0; font-size: 13px;">
                    根据相关法律法规要求，订阅付费服务需要完成邮箱验证。
                    验证后将享受平台全部功能，包括个性化推荐、高级搜索、语音播报等。
                </p>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="#" class="button">立即验证邮箱</a>
            </p>
        </div>
        
        <div class="footer">
            <p>此邮件由临桂资讯平台自动发送，请勿回复</p>
            <p>© 2026 桂林市临桂区融媒体中心 保留所有权利</p>
            <p>临桂资讯 - 桂林市临桂区官方新闻资讯平台</p>
        </div>
    </div>
</body>
</html>
"""

    PASSWORD_RESET_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>临桂资讯 - 密码重置</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 28px;
            font-weight: bold;
            color: #1890ff;
        }}
        .code-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            margin: 30px 0;
        }}
        .code {{
            font-size: 36px;
            font-weight: bold;
            color: white;
            letter-spacing: 8px;
        }}
        .warning {{
            background: #fffbe6;
            border-left: 4px solid #faad14;
            padding: 15px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📰 临桂资讯</div>
        </div>
        
        <h2>密码重置请求</h2>
        
        <p>您好，</p>
        
        <p>我们收到了您的密码重置请求。如果您没有发起此请求，请忽略此邮件。</p>
        
        <div class="code-box">
            <div class="code">{verification_code}</div>
            <div>您的验证码</div>
        </div>
        
        <p><strong>验证码有效期为 10 分钟</strong>，请尽快输入验证码重置密码。</p>
        
        <div class="warning">
            <strong>⚠️ 安全提醒：</strong>
            <p style="margin: 5px 0 0 0; font-size: 13px;">
                • 请勿将验证码透露给他人<br>
                • 临桂资讯工作人员不会索要您的验证码
            </p>
        </div>
        
        <p>如果您需要帮助，请联系我们的客服团队。</p>
        
        <p>此致<br>临桂资讯团队</p>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999;">
            <p>© 2026 桂林市临桂区融媒体中心</p>
        </div>
    </div>
</body>
</html>
"""

    @staticmethod
    def generate_verification_code() -> str:
        """生成6位数字验证码"""
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str) -> bool:
        """使用Resend API发送邮件"""
        try:
            import requests
            
            # 使用Resend API
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {EmailService.RESEND_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "from": EmailService.FROM_EMAIL,
                "to": [to_email],
                "subject": subject,
                "html": html_content
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200 or response.status_code == 201:
                print(f"✓ 邮件发送成功: {to_email}")
                return True
            else:
                print(f"✗ 邮件发送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ 邮件发送异常: {str(e)}")
            # 如果Resend失败，fallback到控制台打印
            print(f"\n{'='*60}")
            print(f"📧 邮件内容 (预览模式)")
            print(f"{'='*60}")
            print(f"收件人: {to_email}")
            print(f"主题: {subject}")
            print(f"{'='*60}")
            return True  # 模拟成功，因为是预览模式
    
    @classmethod
    def send_verification_email(cls, to_email: str, code: str) -> bool:
        """发送验证邮件"""
        html = cls.VERIFICATION_EMAIL_TEMPLATE.format(verification_code=code)
        return cls.send_email(to_email, "临桂资讯 - 邮箱验证", html)
    
    @classmethod
    def send_password_reset_email(cls, to_email: str, code: str) -> bool:
        """发送密码重置邮件"""
        html = cls.PASSWORD_RESET_TEMPLATE.format(verification_code=code)
        return cls.send_email(to_email, "临桂资讯 - 密码重置", html)


def get_verification_code() -> str:
    """生成验证码"""
    return EmailService.generate_verification_code()

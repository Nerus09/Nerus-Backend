# app/services/email_service.py
"""
Serviço de envio de emails
Suporta: SMTP, SendGrid, AWS SES
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings

# ==================== CONFIGURAÇÃO ====================

EMAIL_PROVIDER = getattr(settings, 'EMAIL_PROVIDER', 'smtp')  # smtp, sendgrid, ses
SMTP_HOST = getattr(settings, 'SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = getattr(settings, 'SMTP_PORT', 587)
SMTP_USER = getattr(settings, 'SMTP_USER', 'seu-email@gmail.com')
SMTP_PASSWORD = getattr(settings, 'SMTP_PASSWORD', 'sua-senha')
FROM_EMAIL = getattr(settings, 'FROM_EMAIL', 'noreply@nerus.ao')
FROM_NAME = getattr(settings, 'FROM_NAME', 'Plataforma NERUS')
FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')

# ==================== TEMPLATES HTML ====================

def get_verification_email_html(nome: str, verification_url: str, tipo: str) -> str:
    """Template HTML para email de verificação"""
    
    tipo_nome = "usuário" if tipo == "user" else "empresa"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: #f9f9f9;
                border-radius: 10px;
                padding: 30px;
                border: 1px solid #e0e0e0;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 32px;
                font-weight: bold;
                color: #4CAF50;
            }}
            .button {{
                display: inline-block;
                padding: 15px 30px;
                background-color: #4CAF50;
                color: white !important;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            .link {{
                color: #4CAF50;
                word-break: break-all;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀 NERUS</div>
                <h2>Bem-vindo à Plataforma NERUS!</h2>
            </div>
            
            <p>Olá <strong>{nome}</strong>,</p>
            
            <p>Obrigado por se registrar como <strong>{tipo_nome}</strong> na Plataforma NERUS!</p>
            
            <p>Para ativar sua conta e começar a usar nossa plataforma, por favor verifique seu email clicando no botão abaixo:</p>
            
            <div style="text-align: center;">
                <a href="{verification_url}" class="button">
                    ✓ Verificar Meu Email
                </a>
            </div>
            
            <p>Ou copie e cole este link no seu navegador:</p>
            <p class="link">{verification_url}</p>
            
            <p><strong>Por que verificar?</strong></p>
            <ul>
                <li>Garante a segurança da sua conta</li>
                <li>Permite recuperação de senha</li>
                <li>Habilita notificações importantes</li>
            </ul>
            
            <div class="footer">
                <p>Este email foi enviado automaticamente. Por favor, não responda.</p>
                <p>Se você não se registrou na NERUS, ignore este email.</p>
                <p>&copy; 2025 NERUS - Plataforma de Resolução de Problemas</p>
            </div>
        </div>
    </body>
    </html>
    """

def get_welcome_email_html(nome: str, tipo: str) -> str:
    """Template HTML para email de boas-vindas (após verificação)"""
    
    tipo_nome = "usuário" if tipo == "user" else "empresa"
    dashboard_url = f"{FRONTEND_URL}/dashboard"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
                padding: 40px;
                color: white;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .emoji {{
                font-size: 48px;
            }}
            .button {{
                display: inline-block;
                padding: 15px 30px;
                background-color: white;
                color: #667eea !important;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .feature {{
                background: rgba(255,255,255,0.1);
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="emoji">🎉</div>
                <h1>Email Verificado com Sucesso!</h1>
            </div>
            
            <p>Olá <strong>{nome}</strong>,</p>
            
            <p>Sua conta foi verificada e está pronta para uso!</p>
            
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">
                    🚀 Acessar Dashboard
                </a>
            </div>
            
            <h3>O que você pode fazer agora:</h3>
            
            <div class="feature">
                <strong>✓</strong> {'Resolver problemas reais de empresas' if tipo == 'user' else 'Publicar problemas para a comunidade'}
            </div>
            
            <div class="feature">
                <strong>✓</strong> {'Ganhar pontos e subir no ranking' if tipo == 'user' else 'Encontrar soluções inovadoras'}
            </div>
            
            <div class="feature">
                <strong>✓</strong> {'Obter certificados reconhecidos' if tipo == 'user' else 'Avaliar e premiar solucionadores'}
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                Bem-vindo à comunidade NERUS! 🚀
            </p>
        </div>
    </body>
    </html>
    """

# ==================== ENVIO VIA SMTP ====================

async def enviar_via_smtp(
    destinatario: str,
    assunto: str,
    html_content: str,
    texto_alternativo: Optional[str] = None
):
    """Enviar email via SMTP"""
    
    try:
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = assunto
        message["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        message["To"] = destinatario
        
        # Texto alternativo (para clientes que não suportam HTML)
        if texto_alternativo:
            part1 = MIMEText(texto_alternativo, "plain")
            message.attach(part1)
        
        # HTML
        part2 = MIMEText(html_content, "html")
        message.attach(part2)
        
        # Conectar e enviar
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, destinatario, message.as_string())
        
        print(f"✓ Email enviado para {destinatario}")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao enviar email: {e}")
        return False

# ==================== ENVIO VIA SENDGRID ====================

async def enviar_via_sendgrid(
    destinatario: str,
    assunto: str,
    html_content: str
):
    """Enviar email via SendGrid"""
    
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Email, To, Content
        
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        
        from_email = Email(FROM_EMAIL, FROM_NAME)
        to_email = To(destinatario)
        content = Content("text/html", html_content)
        
        mail = Mail(from_email, to_email, assunto, content)
        
        response = sg.client.mail.send.post(request_body=mail.get())
        
        print(f"✓ Email enviado via SendGrid para {destinatario}")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao enviar via SendGrid: {e}")
        return False

# ==================== FUNÇÕES PRINCIPAIS ====================

async def enviar_email_verificacao(
    destinatario: str,
    nome: str,
    token: str,
    tipo_usuario: str
):
    """Enviar email de verificação de conta"""
    
    # URL de verificação
    verification_url = f"{FRONTEND_URL}/verify-email?token={token}"
    
    # Gerar HTML
    html_content = get_verification_email_html(nome, verification_url, tipo_usuario)
    
    # Texto alternativo
    texto_alternativo = f"""
    Olá {nome},
    
    Bem-vindo à Plataforma NERUS!
    
    Para verificar seu email, acesse o link abaixo:
    {verification_url}
    
    Se você não se registrou na NERUS, ignore este email.
    
    Atenciosamente,
    Equipe NERUS
    """
    
    # Enviar
    assunto = "✓ Verifique seu email - Plataforma NERUS"
    
    if EMAIL_PROVIDER == "sendgrid":
        return await enviar_via_sendgrid(destinatario, assunto, html_content)
    else:
        return await enviar_via_smtp(destinatario, assunto, html_content, texto_alternativo)

async def enviar_email_boas_vindas(
    destinatario: str,
    nome: str,
    tipo_usuario: str
):
    """Enviar email de boas-vindas após verificação"""
    
    html_content = get_welcome_email_html(nome, tipo_usuario)
    
    texto_alternativo = f"""
    Olá {nome},
    
    Email verificado com sucesso!
    
    Sua conta está pronta para uso. Acesse: {FRONTEND_URL}/dashboard
    
    Bem-vindo à comunidade NERUS!
    
    Atenciosamente,
    Equipe NERUS
    """
    
    assunto = "🎉 Bem-vindo à Plataforma NERUS!"
    
    if EMAIL_PROVIDER == "sendgrid":
        return await enviar_via_sendgrid(destinatario, assunto, html_content)
    else:
        return await enviar_via_smtp(destinatario, assunto, html_content, texto_alternativo)

async def enviar_email_recuperacao_senha(
    destinatario: str,
    nome: str,
    token: str
):
    """Enviar email de recuperação de senha"""
    
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Recuperação de Senha</h2>
        <p>Olá {nome},</p>
        <p>Recebemos uma solicitação para redefinir sua senha.</p>
        <p>Clique no botão abaixo para criar uma nova senha:</p>
        <p><a href="{reset_url}" style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Redefinir Senha</a></p>
        <p>Este link expira em 1 hora.</p>
        <p>Se você não solicitou isso, ignore este email.</p>
    </body>
    </html>
    """
    
    texto_alternativo = f"Olá {nome}, Para redefinir sua senha, acesse: {reset_url}"
    
    assunto = "🔐 Recuperação de Senha - NERUS"
    
    if EMAIL_PROVIDER == "sendgrid":
        return await enviar_via_sendgrid(destinatario, assunto, html_content)
    else:
        return await enviar_via_smtp(destinatario, assunto, html_content, texto_alternativo)

# ==================== TESTE DE EMAIL ====================

async def testar_configuracao_email(email_destino: str):
    """Testar se o envio de email está funcionando"""
    
    html_content = """
    <html>
    <body>
        <h2>✓ Teste de Configuração de Email</h2>
        <p>Se você recebeu este email, o sistema está configurado corretamente!</p>
        <p><strong>Provider:</strong> {}</p>
    </body>
    </html>
    """.format(EMAIL_PROVIDER)
    
    assunto = "✓ Teste de Email - NERUS"
    
    try:
        if EMAIL_PROVIDER == "sendgrid":
            resultado = await enviar_via_sendgrid(email_destino, assunto, html_content)
        else:
            resultado = await enviar_via_smtp(email_destino, assunto, html_content)
        
        if resultado:
            print(f"✓ Email de teste enviado com sucesso para {email_destino}")
        else:
            print(f"✗ Falha ao enviar email de teste")
        
        return resultado
    except Exception as e:
        print(f"✗ Erro no teste de email: {e}")
        return False
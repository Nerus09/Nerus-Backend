# app/api/v1/endpoints/auth.py (ATUALIZADO COM ESTRUTURA ANINHADA)
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Body
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime, timedelta
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import (
    UserRegister, 
    EmpresaRegister, 
    LoginRequest, 
    LoginResponse,
    UserInfo,  # 🔥 NOVO IMPORT
    EmailVerification,
    EmailVerificationResponse
)
import secrets
import json

router = APIRouter()

# ==================== REGISTRO DE USUÁRIO ====================

@router.post("/register/user", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    background_tasks: BackgroundTasks,
    cursor = Depends(get_db)
):
    """Registrar novo usuário"""
    
    try:
        # Verificar se email já existe
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (user_data.email,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Verificar se username já existe
        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            (user_data.username,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso"
            )
        
        # Gerar token de verificação
        verification_token = secrets.token_urlsafe(32)
        
        # Hash da senha
        senha_hash = hash_password(user_data.senha)
        
        # Inserir usuário
        query = """
        INSERT INTO users (
            nome, username, email, senha_hash, data_nascimento,
            nivel_educacao, token_verificacao, email_verificado
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
        """
        
        cursor.execute(query, (
            user_data.nome,
            user_data.username,
            user_data.email,
            senha_hash,
            user_data.data_nascimento,
            user_data.nivel_educacao,
            verification_token
        ))
        
        user_id = cursor.lastrowid
        
        # Enviar email de verificação (background)
        background_tasks.add_task(
            send_verification_email,
            email=user_data.email,
            nome=user_data.nome,
            token=verification_token,
            tipo="user"
        )
        
        return {
            "message": "Usuário criado com sucesso! Verifique seu email.",
            "user_id": user_id,
            "email": user_data.email
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no registro de usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor"
        )

# ==================== REGISTRO DE EMPRESA ====================

@router.post("/register/empresa", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_empresa(
    empresa_data: EmpresaRegister,
    background_tasks: BackgroundTasks,
    cursor = Depends(get_db)
):
    """Registrar nova empresa"""
    
    try:
        print(f"🔍 DEBUG - Dados da empresa recebidos: {empresa_data}")
        
        # Verificar se email já existe
        cursor.execute(
            "SELECT id FROM empresas WHERE email = %s",
            (empresa_data.email_corporativo,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Verificar se NIF já existe (se fornecido)
        if empresa_data.nif:
            cursor.execute(
                "SELECT id FROM empresas WHERE nif = %s",
                (empresa_data.nif,)
            )
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="NIF já cadastrado"
                )
        
        # Gerar token de verificação
        verification_token = secrets.token_urlsafe(32)
        
        # Hash da senha
        senha_hash = hash_password(empresa_data.senha)
        
        print(f"🔍 DEBUG - Inserindo empresa no banco...")
        
        # Inserir empresa
        query = """
        INSERT INTO empresas (
            nome, email, senha_hash, nif, setor_atuacao,
            token_verificacao, email_verificado
        ) VALUES (%s, %s, %s, %s, %s, %s, FALSE)
        """
        
        cursor.execute(query, (
            empresa_data.nome_empresa,
            empresa_data.email_corporativo,
            senha_hash,
            empresa_data.nif,
            empresa_data.setor_atuacao,
            verification_token,
        ))
        
        empresa_id = cursor.lastrowid
        
        print(f"✅ DEBUG - Empresa criada com ID: {empresa_id}")
        
        # Enviar email de verificação
        background_tasks.add_task(
            send_verification_email,
            email=empresa_data.email_corporativo,
            nome=empresa_data.nome_empresa,
            token=verification_token,
            tipo="empresa"
        )
        
        return {
            "message": "Empresa criada com sucesso! Verifique seu email.",
            "empresa_id": empresa_id,
            "email": empresa_data.email_corporativo
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no registro de empresa: {e}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no servidor: {str(e)}"
        )

# ==================== VERIFICAR EMAIL ====================

@router.post("/verify-email", response_model=EmailVerificationResponse)
def verify_email(
    verification_data: EmailVerification,
    cursor = Depends(get_db)
):
    """Verificar email com token"""
    
    token = verification_data.token
    
    # Buscar em usuários
    cursor.execute(
        "SELECT id, email, nome FROM users WHERE token_verificacao = %s",
        (token,)
    )
    user = cursor.fetchone()
    
    if user:
        # Verificar se já está verificado
        cursor.execute(
            "SELECT email_verificado FROM users WHERE id = %s",
            (user['id'],)
        )
        user_status = cursor.fetchone()
        
        if user_status['email_verificado']:
            return {
                "message": "Email já verificado anteriormente",
                "email_verificado": True
            }
        
        # Atualizar usuário
        cursor.execute(
            "UPDATE users SET email_verificado = TRUE, token_verificacao = NULL WHERE id = %s",
            (user['id'],)
        )
        
        return {
            "message": f"Email verificado com sucesso! Bem-vindo, {user['nome']}!",
            "email_verificado": True
        }
    
    # Buscar em empresas
    cursor.execute(
        "SELECT id, email, nome FROM empresas WHERE token_verificacao = %s",
        (token,)
    )
    empresa = cursor.fetchone()
    
    if empresa:
        # Verificar se já está verificado
        cursor.execute(
            "SELECT email_verificado FROM empresas WHERE id = %s",
            (empresa['id'],)
        )
        empresa_status = cursor.fetchone()
        
        if empresa_status['email_verificado']:
            return {
                "message": "Email já verificado anteriormente",
                "email_verificado": True
            }
        
        # Atualizar empresa
        cursor.execute(
            "UPDATE empresas SET email_verificado = TRUE, token_verificacao = NULL WHERE id = %s",
            (empresa['id'],)
        )
        
        return {
            "message": f"Email verificado com sucesso! Bem-vindo, {empresa['nome']}!",
            "email_verificado": True
        }
    
    # Token inválido
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token de verificação inválido ou expirado"
    )

# ==================== REENVIAR EMAIL DE VERIFICAÇÃO ====================

class ResendVerificationRequest(BaseModel):
    """Request para reenviar verificação"""
    email: EmailStr
    tipo_usuario: str = Field(..., pattern="^(user|empresa)$")

@router.post("/resend-verification", response_model=dict)
async def resend_verification(
    request: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    cursor = Depends(get_db)
):
    """Reenviar email de verificação"""
    
    if request.tipo_usuario == "user":
        cursor.execute(
            "SELECT id, nome, email_verificado FROM users WHERE email = %s",
            (request.email,)
        )
        entity = cursor.fetchone()
        table = "users"
    else:
        cursor.execute(
            "SELECT id, nome, email_verificado FROM empresas WHERE email = %s",
            (request.email,)
        )
        entity = cursor.fetchone()
        table = "empresas"
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email não encontrado"
        )
    
    if entity['email_verificado']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já verificado"
        )
    
    # Gerar novo token
    new_token = secrets.token_urlsafe(32)
    
    cursor.execute(
        f"UPDATE {table} SET token_verificacao = %s WHERE id = %s",
        (new_token, entity['id'])
    )
    
    # Enviar email
    background_tasks.add_task(
        send_verification_email,
        email=request.email,
        nome=entity['nome'],
        token=new_token,
        tipo=request.tipo_usuario
    )
    
    return {
        "message": "Email de verificação reenviado com sucesso!",
        "email": request.email
    }

# ==================== LOGIN ====================

@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,  # Só recebe email e senha
    cursor = Depends(get_db)
):
    """
    Login para usuário ou empresa
    """
    
    # 1️⃣ TENTAR BUSCAR NOS USUÁRIOS
    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (login_data.email,)
    )
    user = cursor.fetchone()
    
    if user:
        # ✅ ENCONTROU NOS USUÁRIOS
        if not verify_password(login_data.senha, user['senha_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        if not user['ativo']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta desativada"
            )
        
        # Gerar token JWT
        access_token = create_access_token(
            data={
                "sub": user['id'],
                "email": user['email'],
                "tipo": "user"  # ✅ Backend define
            }
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserInfo(
                user_id=user['id'],
                nome=user['nome'],
                email=user['email'],
                tipo_usuario="user",  # ✅ Backend informa
                email_verificado=user['email_verificado']
            )
        )
    
    # 2️⃣ SE NÃO ENCONTROU, TENTAR NAS EMPRESAS
    cursor.execute(
        "SELECT * FROM empresas WHERE email = %s",
        (login_data.email,)
    )
    empresa = cursor.fetchone()
    
    if empresa:
        # ✅ ENCONTROU NAS EMPRESAS
        if not verify_password(login_data.senha, empresa['senha_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        if not empresa['ativo']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta desativada"
            )
        
        # Gerar token JWT
        access_token = create_access_token(
            data={
                "sub": empresa['id'],
                "email": empresa['email'],
                "tipo": "empresa"  # ✅ Backend define
            }
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserInfo(
                user_id=empresa['id'],
                nome=empresa['nome'],
                email=empresa['email'],
                tipo_usuario="empresa",  # ✅ Backend informa
                email_verificado=empresa['email_verificado']
            )
        )
    
    # 3️⃣ NÃO ENCONTROU EM NENHUMA TABELA
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorretos"
    )

# ==================== LOGOUT ====================

@router.post("/logout", response_model=dict)
def logout():
    """Logout (apenas informativo, token gerenciado no front-end)"""
    return {
        "message": "Logout realizado com sucesso. Remova o token do cliente."
    }

# ==================== FUNÇÃO AUXILIAR PARA ENVIO DE EMAIL ====================

async def send_verification_email(email: str, nome: str, token: str, tipo: str):
    """
    Envia email de verificação
    (Esta função será implementada em email_service.py)
    """
    try:
        # Tente importar, mas não falhe se não existir
        from app.services.email_service import enviar_email_verificacao
        await enviar_email_verificacao(
            destinatario=email,
            nome=nome,
            token=token,
            tipo_usuario=tipo
        )
        print(f"✓ Email enviado para {email}")
    except ImportError:
        print(f"⚠️  Email service não disponível. Token para {email}: {token}")
    except Exception as e:
        print(f"⚠️  Erro ao enviar email: {e}")
        print(f"📧 Token de verificação para {email}: {token}")
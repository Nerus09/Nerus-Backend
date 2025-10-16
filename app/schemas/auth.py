# Login, Registro e Tokens
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import date

# ==================== REGISTER ====================

class UserRegister(BaseModel):
    nome: str = Field(None, min_length=3, max_length=255)
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    senha: str = Field(..., min_length=6)
    data_nascimento: Optional[date] = None
    nivel_educacao: str

    class Config:
        extra = 'forbid'
        
class EmpresaRegister(BaseModel):
    """Schema para registro de empresa"""
    nome_empresa: str = Field(..., min_length=3, max_length=255)
    email_corporativo: EmailStr
    senha: str = Field(..., min_length=6)
    nif: Optional[str] = None
    setor_atuacao: Optional[str] = None

# ==================== USER INFO ====================

class UserInfo(BaseModel):
    """Informações do usuário/empresa para resposta de login"""
    user_id: int
    nome: str
    email: str
    tipo_usuario: str
    email_verificado: bool

# ==================== LOGIN ====================

class LoginRequest(BaseModel):
    """Schema para login"""
    email: EmailStr
    senha: str
    
class LoginResponse(BaseModel):
    """Schema de resposta do login com estrutura aninhada"""
    access_token: str
    token_type: str = "bearer"
    user: UserInfo  # Objeto aninhado com informações do usuário

# ==================== TOKEN ====================

class TokenPayload(BaseModel):
    """Payload do JWT Token"""
    sub: int  # user_id ou empresa_id
    email: str
    tipo: str  # user ou empresa
    exp: Optional[int] = None

# ==================== EMAIL VERIFICATION ====================

class EmailVerification(BaseModel):
    """Schema para verificação de email"""
    token: str

class EmailVerificationResponse(BaseModel):
    """Resposta da verificação"""
    message: str
    email_verificado: bool
# Login, Registro e Tokens
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import date

# ==================== REGISTER ====================

class UserRegister(BaseModel):
    nome_completo: Optional[str] = Field(None, min_length=3, max_length=255)
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    senha: str = Field(..., min_length=6)
    data_nascimento: Optional[date] = None
    nivel_educacao: str
    palavras_chave: Optional[str] = None

    @model_validator(mode='after')
    def validate_nome_fields(self):
        if not self.nome and not self.nome_completo:
            raise ValueError('Either "nome" or "nome_completo" must be provided')
        
        # Se nome_completo foi fornecido mas nome não, use nome_completo como nome
        if self.nome_completo and not self.nome:
            self.nome = self.nome_completo
        
        return self

    class Config:
        extra = 'forbid'
        
class EmpresaRegister(BaseModel):
    """Schema para registro de empresa"""
    nome_empresa: str = Field(..., min_length=3, max_length=255)
    email_corporativo: EmailStr
    senha: str = Field(..., min_length=6)
    nif: Optional[str] = None
    telefone: Optional[str] = None
    setor_atuacao: Optional[str] = None
    tamanho_empresa: Optional[str] = "pequena"

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
    tipo_usuario: str = Field(..., pattern="^(user|empresa)$")  # user ou empresa

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
#Configuracoes (DB, secrets, etc)
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    
    """Configurações da aplicação"""
    
    # Ambiente
    ENVIRONMENT: str = "development"
    
    # Database
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    # Segurança JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 dias
    
    
   # ==================== AI CONFIGURATION ====================
    
    # Google Gemini (PRINCIPAL - GRATUITO)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Modelo gratuito e rápido
    
    # Groq (BACKUP - GRATUITO)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    
    # OpenAI (FUTURO - PAGO)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Anthropic Claude (FUTURO - PAGO)
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    
    # Configuração de provider padrão
    AI_PROVIDER: str = "gemini"  # gemini | groq | openai | anthropic
    AI_FALLBACK_PROVIDER: str = "groq"  # Provider de backup se o principal falhar
    
    # Configurações de análise
    AI_MAX_RETRIES: int = 3
    AI_TIMEOUT_SECONDS: int = 30
    AI_ENABLE_CACHE: bool = True
    AI_CACHE_TTL_HOURS: int = 24
    
    
     # Email - CAMPOS QUE ESTAVAM FALTANDO
    EMAIL_PROVIDER: str = "smtp"  # smtp, sendgrid, mailgun, etc
    FROM_EMAIL: str = "noreply@plataforma.ao"
    FROM_NAME: str = "Plataforma NERUS"
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@plataforma.ao"  # Mantive por compatibilidade
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "NERUS - Plataforma de Capacitação"
    
    # Logs
    LOG_LEVEL: str = "INFO"
    
    @property
    def DATABASE_URL(self) -> str:
        """Retorna URL de conexão com o MySQL"""
        return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()
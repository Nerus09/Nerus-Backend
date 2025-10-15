# Router principal V1
from fastapi import APIRouter
from app.api.v1.endpoints import ai_test, auth, user, problemas, solucoes, ranking, empresas

# Router principal da API v1
api_router = APIRouter()

# Incluir todos os endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(user.router, prefix="/users", tags=["Usuários"])
api_router.include_router(empresas.router, prefix="/empresas", tags=["Empresas"])  # ✅ DESCOMENTADO
api_router.include_router(problemas.router, prefix="/problemas", tags=["Problemas"])
api_router.include_router(solucoes.router, prefix="/solucoes", tags=["Soluções"])
api_router.include_router(ranking.router, prefix="/ranking", tags=["Rankings"])

# Endpoint de teste de IA (REMOVER EM PRODUÇÃO)
api_router.include_router(ai_test.router, prefix="/ai-test", tags=["🤖 Testes de IA"])
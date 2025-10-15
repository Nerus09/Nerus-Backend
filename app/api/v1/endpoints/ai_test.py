"""
Endpoint de teste para IA (REMOVER EM PRODUÇÃO)
"""
from fastapi import APIRouter, Depends
from typing import Dict
from pydantic import BaseModel
from app.services.ai_service import analisar_solucao, get_ai_service, get_cache_stats, clear_cache

router = APIRouter()

class TesteAnaliseRequest(BaseModel):
    """Request para teste de análise"""
    problema_titulo: str
    problema_descricao: str
    solucao_texto: str

# ==================== TESTAR ANÁLISE ====================

@router.post("/testar-analise", response_model=Dict)
async def testar_analise(request: TesteAnaliseRequest):
    """
    Endpoint de teste para análise de IA
    ⚠️ REMOVER EM PRODUÇÃO
    """
    
    # Criar problema fake para teste
    problema_fake = {
        'id': 999,
        'titulo': request.problema_titulo,
        'descricao': request.problema_descricao,
        'area': 'Teste',
        'nivel_dificuldade': 'intermediario',
        'contexto_empresa': 'Ambiente de teste',
        'objetivos': 'Testar sistema de IA',
        'requisitos': 'Nenhum requisito específico'
    }
    
    # Analisar
    resultado = await analisar_solucao(
        problema=problema_fake,
        solucao_texto=request.solucao_texto,
        use_cache=False  # Não usar cache em teste
    )
    
    return {
        "sucesso": True,
        "analise": resultado
    }

# ==================== STATUS DOS PROVIDERS ====================

@router.get("/providers-status", response_model=Dict)
def get_providers_status():
    """
    Verifica status de todos os providers de IA
    """
    service = get_ai_service()
    providers = service.get_available_providers()
    
    return {
        "providers": providers,
        "primary": service.primary_provider,
        "fallback": service.fallback_provider,
        "total_available": sum(1 for p in providers.values() if p['available'])
    }

# ==================== ESTATÍSTICAS DO CACHE ====================

@router.get("/cache-stats", response_model=Dict)
def get_cache_statistics():
    """
    Estatísticas do cache de análises
    """
    return get_cache_stats()

# ==================== LIMPAR CACHE ====================

@router.post("/clear-cache", response_model=Dict)
def limpar_cache():
    """
    Limpa todo o cache de análises
    ⚠️ Use com cuidado!
    """
    clear_cache()
    return {
        "message": "Cache limpo com sucesso",
        "stats": get_cache_stats()
    }

# ==================== TESTE RÁPIDO ====================

@router.get("/health", response_model=Dict)
def health_check_ai():
    """
    Health check do sistema de IA
    """
    service = get_ai_service()
    providers = service.get_available_providers()
    
    algum_disponivel = any(p['available'] for p in providers.values())
    
    return {
        "status": "healthy" if algum_disponivel else "unhealthy",
        "providers_available": algum_disponivel,
        "primary_provider": service.primary_provider,
        "primary_available": providers.get(service.primary_provider, {}).get('available', False)
    }
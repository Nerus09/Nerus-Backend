"""
Serviço principal de análise com IA
Sistema com fallback automático e cache
"""
from typing import Dict, Any, Optional
import json
import hashlib
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.ai_providers.gemini_provider import GeminiProvider
from app.services.ai_providers.groq_provider import GroqProvider
from app.services.ai_prompts import get_analise_prompt

# Cache em memória (em produção, usar Redis)
_cache: Dict[str, Dict[str, Any]] = {}

class AIAnalysisService:
    """
    Serviço de análise com IA
    Implementa sistema de fallback e cache
    """
    
    def __init__(self):
        self.providers = self._initialize_providers()
        self.primary_provider = settings.AI_PROVIDER
        self.fallback_provider = settings.AI_FALLBACK_PROVIDER
    
    def _initialize_providers(self) -> Dict[str, Any]:
        """Inicializa todos os providers disponíveis"""
        providers = {}
        
        # Gemini (Principal)
        if settings.GEMINI_API_KEY:
            providers['gemini'] = GeminiProvider(
                api_key=settings.GEMINI_API_KEY,
                model=settings.GEMINI_MODEL
            )
            print("✅ Gemini Provider inicializado")
        
        # Groq (Backup)
        if settings.GROQ_API_KEY:
            providers['groq'] = GroqProvider(
                api_key=settings.GROQ_API_KEY,
                model=settings.GROQ_MODEL
            )
            print("✅ Groq Provider inicializado")
        
        # TODO: Adicionar OpenAI e Claude no futuro
        
        if not providers:
            print("⚠️ ATENÇÃO: Nenhum provider de IA configurado!")
        
        return providers
    
    def _generate_cache_key(self, problema_id: int, solucao_texto: str) -> str:
        """
        Gera chave única para cache baseada no problema e solução
        """
        content = f"{problema_id}:{solucao_texto}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Busca análise do cache se ainda válida
        """
        if not settings.AI_ENABLE_CACHE:
            return None
        
        if cache_key not in _cache:
            return None
        
        cached = _cache[cache_key]
        cache_time = cached.get('cached_at')
        
        if not cache_time:
            return None
        
        # Verificar se cache expirou
        ttl = timedelta(hours=settings.AI_CACHE_TTL_HOURS)
        if datetime.now() - cache_time > ttl:
            del _cache[cache_key]
            return None
        
        print(f"✅ Análise encontrada no cache (key: {cache_key[:8]}...)")
        return cached['data']
    
    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]):
        """
        Salva análise no cache
        """
        if not settings.AI_ENABLE_CACHE:
            return
        
        _cache[cache_key] = {
            'data': data,
            'cached_at': datetime.now()
        }
        print(f"💾 Análise salva no cache (key: {cache_key[:8]}...)")
    
    async def analisar_com_provider(
        self, 
        provider_name: str, 
        prompt: str
    ) -> Dict[str, Any]:
        """
        Analisa usando um provider específico
        """
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' não disponível")
        
        provider = self.providers[provider_name]
        
        if not provider.is_available():
            raise ValueError(f"Provider '{provider_name}' não está configurado")
        
        return await provider.analisar(prompt)
    
    async def analisar_com_fallback(
        self, 
        prompt: str
    ) -> Dict[str, Any]:
        """
        Tenta analisar com provider principal, se falhar usa fallback
        """
        tentativas = []
        
        # Tentar provider principal
        try:
            print(f"🎯 Tentando análise com provider principal: {self.primary_provider}")
            resultado = await self.analisar_com_provider(self.primary_provider, prompt)
            resultado['used_fallback'] = False
            return resultado
        except Exception as e:
            erro_primary = str(e)
            print(f"⚠️ Provider principal falhou: {erro_primary}")
            tentativas.append({
                'provider': self.primary_provider,
                'erro': erro_primary
            })
        
        # Tentar fallback
        if self.fallback_provider and self.fallback_provider in self.providers:
            try:
                print(f"🔄 Tentando fallback: {self.fallback_provider}")
                resultado = await self.analisar_com_provider(self.fallback_provider, prompt)
                resultado['used_fallback'] = True
                resultado['fallback_reason'] = erro_primary
                return resultado
            except Exception as e:
                erro_fallback = str(e)
                print(f"❌ Fallback também falhou: {erro_fallback}")
                tentativas.append({
                    'provider': self.fallback_provider,
                    'erro': erro_fallback
                })
        
        # Todos os providers falharam
        raise Exception(f"Todos os providers falharam. Tentativas: {json.dumps(tentativas)}")
    
    def get_available_providers(self) -> Dict[str, Any]:
        """
        Lista providers disponíveis e seus status
        """
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                'available': provider.is_available(),
                'info': provider.get_info()
            }
        return status


# Instância global do serviço
_ai_service: Optional[AIAnalysisService] = None

def get_ai_service() -> AIAnalysisService:
    """
    Retorna instância global do serviço de IA (Singleton)
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIAnalysisService()
    return _ai_service


async def analisar_solucao(
    problema: Dict[str, Any],
    solucao_texto: str,
    use_cache: bool = True
) -> Dict[str, Any]:
    """
    Função principal para analisar uma solução
    
    Args:
        problema: Dict com dados do problema
        solucao_texto: Texto da solução submetida
        use_cache: Se deve usar cache (padrão: True)
    
    Returns:
        Dict com análise completa:
        {
            'pontuacao': float,
            'status_recomendado': str,
            'feedback': str,
            'pontos_fortes': List[str],
            'pontos_melhoria': List[str],
            'criterios': Dict,
            'recomendacoes_especificas': List[str],
            'tempo_analise_ms': int,
            'provider': str,
            'used_fallback': bool
        }
    """
    service = get_ai_service()
    
    # Gerar chave de cache
    cache_key = service._generate_cache_key(problema['id'], solucao_texto)
    
    # Tentar buscar do cache
    if use_cache:
        cached = service._get_from_cache(cache_key)
        if cached:
            cached['from_cache'] = True
            return cached
    
    # Gerar prompt
    prompt = get_analise_prompt(problema, solucao_texto)
    
    # Analisar com sistema de fallback
    try:
        resultado = await service.analisar_com_fallback(prompt)
        
        # Salvar no cache
        if use_cache:
            service._save_to_cache(cache_key, resultado)
        
        resultado['from_cache'] = False
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO na análise: {str(e)}")
        
        # Retornar resposta de erro estruturada
        return {
            'pontuacao': 0,
            'status_recomendado': 'revisao',
            'feedback': 'Não foi possível analisar a solução automaticamente. A empresa analisará manualmente.',
            'pontos_fortes': ['Solução aguardando análise manual'],
            'pontos_melhoria': ['Análise automática temporariamente indisponível'],
            'criterios': {
                'adequacao_problema': 0,
                'qualidade_tecnica': 0,
                'criatividade': 0,
                'clareza': 0,
                'viabilidade': 0
            },
            'recomendacoes_especificas': ['Aguardar avaliação da empresa'],
            'tempo_analise_ms': 0,
            'provider': 'none',
            'erro': str(e),
            'used_fallback': False,
            'from_cache': False
        }


def get_ai_provider() -> AIAnalysisService:
    """
    Alias para get_ai_service
    """
    return get_ai_service()


def clear_cache():
    """
    Limpa todo o cache de análises
    """
    global _cache
    _cache.clear()
    print("🗑️ Cache de análises limpo")


def get_cache_stats() -> Dict[str, Any]:
    """
    Retorna estatísticas do cache
    """
    total = len(_cache)
    validos = 0
    expirados = 0
    
    ttl = timedelta(hours=settings.AI_CACHE_TTL_HOURS)
    now = datetime.now()
    
    for cached in _cache.values():
        cache_time = cached.get('cached_at')
        if cache_time and (now - cache_time) <= ttl:
            validos += 1
        else:
            expirados += 1
    
    return {
        'total_entries': total,
        'valid_entries': validos,
        'expired_entries': expirados,
        'cache_enabled': settings.AI_ENABLE_CACHE,
        'ttl_hours': settings.AI_CACHE_TTL_HOURS
    }
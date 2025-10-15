"""
Provider para Google Gemini (PRINCIPAL - GRATUITO)
"""
import google.generativeai as genai
from typing import Dict, Any
from app.services.ai_providers.base import AIProvider
import time

class GeminiProvider(AIProvider):
    """
    Provider para Google Gemini
    Modelo: gemini-pro (gratuito, estável)
    Limites: 60 requisições/minuto gratuitas
    """
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        super().__init__(api_key, model)
        
        if api_key:
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model)
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Verifica se o Gemini está configurado"""
        return self.api_key is not None and self.client is not None
    
    async def analisar(self, prompt: str) -> Dict[str, Any]:
        """
        Analisa solução usando Gemini
        
        Args:
            prompt: Prompt formatado
            
        Returns:
            Dict com análise estruturada
        """
        if not self.is_available():
            raise ValueError("Gemini API key não configurada")
        
        inicio = time.time()
        
        try:
            print(f"🤖 [GEMINI] Iniciando análise com modelo {self.model}...")
            
            # Configurações de geração
            generation_config = {
                "temperature": 0.3,  # Mais determinístico
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            # Configurações de segurança (permitir conteúdo educacional)
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            # Gerar resposta
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Extrair texto
            response_text = response.text
            
            tempo_decorrido = (time.time() - inicio) * 1000
            print(f"✅ [GEMINI] Análise concluída em {tempo_decorrido:.0f}ms")
            
            # Parse e validação
            resultado = self.parse_response(response_text)
            resultado['tempo_analise_ms'] = int(tempo_decorrido)
            resultado['provider'] = 'gemini'
            resultado['model'] = self.model
            
            return resultado
            
        except Exception as e:
            tempo_decorrido = (time.time() - inicio) * 1000
            print(f"❌ [GEMINI] Erro após {tempo_decorrido:.0f}ms: {type(e).__name__}: {str(e)}")
            
            # Re-lançar exceção para sistema de fallback
            raise Exception(f"Gemini API Error: {str(e)}")
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provider"""
        return {
            "name": "Google Gemini",
            "model": self.model,
            "free_tier": True,
            "rate_limit": "1500 req/dia",
            "speed": "muito rápido",
            "available": self.is_available()
        }
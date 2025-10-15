"""
Provider para Groq (BACKUP - GRATUITO)
"""
from groq import Groq
from typing import Dict, Any
from app.services.ai_providers.base import AIProvider
import time

class GroqProvider(AIProvider):
    """
    Provider para Groq (Llama 3.1)
    Modelo: llama-3.1-70b-versatile
    Limites: 14,400 tokens/minuto (MUITO RÁPIDO)
    """
    
    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        super().__init__(api_key, model)
        
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Verifica se o Groq está configurado"""
        return self.api_key is not None and self.client is not None
    
    async def analisar(self, prompt: str) -> Dict[str, Any]:
        """
        Analisa solução usando Groq
        
        Args:
            prompt: Prompt formatado
            
        Returns:
            Dict com análise estruturada
        """
        if not self.is_available():
            raise ValueError("Groq API key não configurada")
        
        inicio = time.time()
        
        try:
            print(f"⚡ [GROQ] Iniciando análise com modelo {self.model}...")
            
            # Criar chat completion
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um avaliador técnico especializado que analisa soluções de estudantes. Responda APENAS com JSON válido, sem markdown."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2048,
                top_p=0.95,
                stream=False
            )
            
            # Extrair resposta
            response_text = completion.choices[0].message.content
            
            tempo_decorrido = (time.time() - inicio) * 1000
            print(f"✅ [GROQ] Análise concluída em {tempo_decorrido:.0f}ms (ULTRA-RÁPIDO!)")
            
            # Parse e validação
            resultado = self.parse_response(response_text)
            resultado['tempo_analise_ms'] = int(tempo_decorrido)
            resultado['provider'] = 'groq'
            resultado['model'] = self.model
            
            return resultado
            
        except Exception as e:
            tempo_decorrido = (time.time() - inicio) * 1000
            print(f"❌ [GROQ] Erro após {tempo_decorrido:.0f}ms: {type(e).__name__}: {str(e)}")
            
            # Re-lançar exceção para sistema de fallback
            raise Exception(f"Groq API Error: {str(e)}")
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provider"""
        return {
            "name": "Groq (Llama 3.1)",
            "model": self.model,
            "free_tier": True,
            "rate_limit": "14,400 tokens/minuto",
            "speed": "ultra-rápido",
            "available": self.is_available()
        }
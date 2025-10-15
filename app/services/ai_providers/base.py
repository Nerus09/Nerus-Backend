"""
Interface base para providers de IA
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import re

class AIProvider(ABC):
    """
    Classe abstrata para providers de IA
    Todos os providers devem implementar esta interface
    """
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def analisar(self, prompt: str) -> Dict[str, Any]:
        """
        Analisa uma solução usando o provider específico
        
        Args:
            prompt: Prompt formatado para análise
            
        Returns:
            Dict com análise estruturada
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica se o provider está disponível (tem API key configurada)
        """
        pass
    
    def clean_json_response(self, response_text: str) -> str:
        """
        Limpa a resposta da IA removendo markdown e caracteres extras
        
        Args:
            response_text: Texto bruto da resposta
            
        Returns:
            JSON limpo como string
        """
        # Remover blocos de markdown
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        # Remover espaços em branco no início e fim
        response_text = response_text.strip()
        
        # Tentar extrair JSON se houver texto antes/depois
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
        
        return response_text
    
    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida e corrige a resposta da IA
        
        Args:
            response: Dict com a resposta parseada
            
        Returns:
            Dict validado e corrigido
        """
        # Campos obrigatórios
        required_fields = {
            'pontuacao': 0,
            'status_recomendado': 'revisao',
            'feedback': 'Análise não disponível.',
            'pontos_fortes': [],
            'pontos_melhoria': [],
            'criterios': {},
            'recomendacoes_especificas': []
        }
        
        # Preencher campos faltantes
        for field, default in required_fields.items():
            if field not in response:
                response[field] = default
        
        # Validar pontuação
        try:
            response['pontuacao'] = float(response['pontuacao'])
            if response['pontuacao'] < 0:
                response['pontuacao'] = 0
            elif response['pontuacao'] > 100:
                response['pontuacao'] = 100
        except (ValueError, TypeError):
            response['pontuacao'] = 0
        
        # Validar status
        valid_statuses = ['aprovada', 'reprovada', 'revisao']
        if response['status_recomendado'] not in valid_statuses:
            response['status_recomendado'] = 'revisao'
        
        # Garantir que listas sejam realmente listas
        for field in ['pontos_fortes', 'pontos_melhoria', 'recomendacoes_especificas']:
            if not isinstance(response[field], list):
                response[field] = []
        
        # Validar critérios
        if not isinstance(response['criterios'], dict):
            response['criterios'] = {}
        
        criterios_esperados = {
            'adequacao_problema': 30,
            'qualidade_tecnica': 25,
            'criatividade': 20,
            'clareza': 15,
            'viabilidade': 10
        }
        
        for criterio, max_value in criterios_esperados.items():
            if criterio not in response['criterios']:
                response['criterios'][criterio] = 0
            else:
                try:
                    valor = float(response['criterios'][criterio])
                    response['criterios'][criterio] = max(0, min(valor, max_value))
                except (ValueError, TypeError):
                    response['criterios'][criterio] = 0
        
        return response
    
    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Faz parse e validação da resposta
        
        Args:
            response_text: Texto bruto da resposta
            
        Returns:
            Dict validado
        """
        try:
            # Limpar resposta
            cleaned = self.clean_json_response(response_text)
            
            # Tentar parse do JSON
            parsed = json.loads(cleaned)
            
            # Validar e corrigir
            validated = self.validate_response(parsed)
            
            return validated
            
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao fazer parse do JSON: {e}")
            print(f"📄 Resposta recebida: {response_text[:500]}...")
            
            # Retornar resposta padrão em caso de erro
            return {
                'pontuacao': 0,
                'status_recomendado': 'revisao',
                'feedback': 'Erro ao processar análise. Por favor, tente novamente.',
                'pontos_fortes': ['Não foi possível analisar'],
                'pontos_melhoria': ['Reenviar solução para análise'],
                'criterios': {
                    'adequacao_problema': 0,
                    'qualidade_tecnica': 0,
                    'criatividade': 0,
                    'clareza': 0,
                    'viabilidade': 0
                },
                'recomendacoes_especificas': ['Contatar suporte técnico'],
                'erro': str(e)
            }
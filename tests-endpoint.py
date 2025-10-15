"""
Script de Teste Completo - API TalentHub
Testa todos os endpoints da API v1

Uso:
    python test_api.py --base-url http://localhost:8000 --verbose

Requisitos:
    pip install requests colorama
"""

import requests
import json
import argparse
import random
import string
from datetime import date, timedelta
from typing import Dict, Optional
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

class APITester:
    def __init__(self, base_url: str, verbose: bool = False):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/v1"
        self.verbose = verbose
        
        # Armazenar tokens e IDs para usar em testes subsequentes
        self.user_token = None
        self.empresa_token = None
        self.user_id = None
        self.empresa_id = None
        self.problema_id = None
        self.solucao_id = None
        
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def generate_random_string(self, length: int = 8):
        """Gerar string aleatória para emails únicos"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def log(self, message: str, color: str = Fore.WHITE):
        """Log colorido"""
        print(f"{color}{message}{Style.RESET_ALL}")

    def log_success(self, message: str):
        self.log(f"✓ {message}", Fore.GREEN)
        self.passed += 1

    def log_error(self, message: str):
        self.log(f"✗ {message}", Fore.RED)
        self.failed += 1

    def log_skip(self, message: str):
        self.log(f"⊘ {message}", Fore.YELLOW)
        self.skipped += 1

    def log_info(self, message: str):
        self.log(f"ℹ {message}", Fore.CYAN)

    def log_section(self, title: str):
        self.log(f"\n{'='*60}\n{title}\n{'='*60}", Fore.MAGENTA)

    def make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        token: Optional[str] = None,
        params: Optional[Dict] = None,
        expected_status: int = 200
    ) -> Optional[Dict]:
        """Fazer requisição HTTP"""
        url = f"{self.api_base}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                self.log_error(f"Método HTTP inválido: {method}")
                return None
            
            if self.verbose:
                self.log_info(f"{method} {endpoint} → {response.status_code}")
                if response.text:
                    try:
                        self.log_info(f"Response: {json.dumps(response.json(), indent=2)}")
                    except:
                        self.log_info(f"Response: {response.text[:200]}")
            
            if response.status_code == expected_status:
                return response.json() if response.text else {}
            else:
                self.log_error(
                    f"{method} {endpoint} - "
                    f"Esperado: {expected_status}, Recebido: {response.status_code}"
                )
                if response.text:
                    self.log_error(f"Erro: {response.text[:200]}")
                return None
                
        except requests.exceptions.ConnectionError:
            self.log_error(f"Erro de conexão com {url}")
            return None
        except Exception as e:
            self.log_error(f"Erro ao fazer requisição: {str(e)}")
            return None

    # ==================== TESTES DE AUTENTICAÇÃO ====================

    def test_auth_endpoints(self):
        """Testar endpoints de autenticação"""
        self.log_section("TESTES DE AUTENTICAÇÃO")
        
        random_suffix = self.generate_random_string(8)
        
        # 1. Registrar usuário
        user_data = {
            "nome": f"João Teste {random_suffix}",  # 🔥 CORREÇÃO: Mudar nome_completo para nome
            "username": f"joao_teste_{random_suffix}",
            "email": f"joao.teste.{random_suffix}@test.com",
            "senha": "senha123456",
            "data_nascimento": "2000-01-15",
            "nivel_educacao": "superior",
            "palavras_chave": "python, javascript, react"
        }
        
        result = self.make_request(
            "POST", 
            "/auth/register/user", 
            data=user_data,
            expected_status=201
        )
        
        if result:
            self.log_success("Registro de usuário")
            self.user_id = result.get("user_id")
        else:
            self.log_error("Registro de usuário")
            return False
        
        # 2. Registrar empresa
        empresa_data = {
            "nome_empresa": f"Tech Solutions {random_suffix}",
            "email_corporativo": f"tech.solutions.{random_suffix}@test.com",
            "senha": "senha123456",
            "nif": f"500{random_suffix}",
            "setor_atuacao": "Tecnologia",
            "descricao": "Empresa de teste para desenvolvimento de software"
        }
        
        result = self.make_request(
            "POST",
            "/auth/register/empresa",
            data=empresa_data,
            expected_status=201
        )
        
        if result:
            self.log_success("Registro de empresa")
            self.empresa_id = result.get("empresa_id")
        else:
            self.log_error("Registro de empresa")
            # Continua mesmo com falha no registro da empresa
        
        # 3. Login usuário
        login_data = {
            "email": user_data["email"],
            "senha": user_data["senha"],
            "tipo_usuario": "user"
        }
        
        result = self.make_request("POST", "/auth/login", data=login_data)
        
        if result and "access_token" in result:
            self.log_success("Login de usuário")
            self.user_token = result["access_token"]
        else:
            self.log_error("Login de usuário")
            return False
        
        # 4. Login empresa (só tenta se o registro foi bem sucedido)
        if self.empresa_id:
            login_data_empresa = {
                "email": empresa_data["email_corporativo"],  # 🔥 CORREÇÃO: Usar email_corporativo
                "senha": empresa_data["senha"],
                "tipo_usuario": "empresa"
            }
            
            result = self.make_request("POST", "/auth/login", data=login_data_empresa)
            
            if result and "access_token" in result:
                self.log_success("Login de empresa")
                self.empresa_token = result["access_token"]
            else:
                self.log_error("Login de empresa")
        else:
            self.log_skip("Login de empresa (registro falhou)")
        
        return True

    # ==================== TESTES DE USUÁRIOS ====================

    def test_user_endpoints(self):
        """Testar endpoints de usuários"""
        self.log_section("TESTES DE USUÁRIOS")
        
        if not self.user_token:
            self.log_skip("Testes de usuários (sem token)")
            return
        
        # 1. Obter meu perfil
        result = self.make_request("GET", "/users/me", token=self.user_token)
        if result:
            self.log_success("Obter perfil do usuário")
        else:
            self.log_error("Obter perfil do usuário")
        
        # 2. Atualizar perfil
        update_data = {
            "nome": "João Silva Teste Atualizado",
            "palavras_chave": "python, javascript, react, node.js, machine learning"
        }
        
        result = self.make_request(
            "PUT", 
            "/users/me", 
            data=update_data,
            token=self.user_token
        )
        if result:
            self.log_success("Atualizar perfil")
        else:
            self.log_error("Atualizar perfil")
        
        # 3. Obter estatísticas
        result = self.make_request("GET", "/users/me/stats", token=self.user_token)
        if result:
            self.log_success("Obter estatísticas do usuário")
        else:
            self.log_error("Obter estatísticas do usuário")
        
        # 4. Listar habilidades
        result = self.make_request("GET", "/users/me/habilidades", token=self.user_token)
        if result is not None:
            self.log_success("Listar habilidades do usuário")
        else:
            self.log_error("Listar habilidades do usuário")
        
        # 5. Listar habilidades disponíveis
        result = self.make_request("GET", "/users/habilidades-disponiveis", token=self.user_token)
        if result is not None:
            self.log_success("Listar habilidades disponíveis")
        else:
            self.log_error("Listar habilidades disponíveis")
        
        # 6. Buscar usuários
        result = self.make_request(
            "GET", 
            "/users/search",
            params={"query": "teste"},
            token=self.user_token
        )
        if result is not None:
            self.log_success("Buscar usuários")
        else:
            self.log_error("Buscar usuários")
        
        # 7. Histórico de atividades
        result = self.make_request("GET", "/users/me/atividades", token=self.user_token)
        if result is not None:
            self.log_success("Histórico de atividades")
        else:
            self.log_error("Histórico de atividades")

    # ==================== TESTES DE EMPRESAS ====================

    def test_empresa_endpoints(self):
        """Testar endpoints de empresas"""
        self.log_section("TESTES DE EMPRESAS")
        
        if not self.empresa_token:
            self.log_skip("Testes de empresas (sem token)")
            return
        
        # 1. Obter perfil da empresa
        result = self.make_request("GET", "/empresas/me", token=self.empresa_token)
        if result:
            self.log_success("Obter perfil da empresa")
        else:
            self.log_error("Obter perfil da empresa")
        
        # 2. Atualizar perfil
        update_data = {
            "descricao": "Empresa de teste especializada em desenvolvimento de software e IA - ATUALIZADO"
        }
        
        result = self.make_request(
            "PUT",
            "/empresas/me",
            data=update_data,
            token=self.empresa_token
        )
        if result:
            self.log_success("Atualizar perfil da empresa")
        else:
            self.log_error("Atualizar perfil da empresa")
        
        # 3. Obter estatísticas
        result = self.make_request("GET", "/empresas/me/stats", token=self.empresa_token)
        if result:
            self.log_success("Obter estatísticas da empresa")
        else:
            self.log_error("Obter estatísticas da empresa")
        
        # 4. Listar empresas (público)
        result = self.make_request("GET", "/empresas/")
        if result is not None:
            self.log_success("Listar empresas (público)")
        else:
            self.log_error("Listar empresas (público)")
        
        # 5. Top empresas ativas
        result = self.make_request("GET", "/empresas/top/ativas")
        if result is not None:
            self.log_success("Top empresas ativas")
        else:
            self.log_error("Top empresas ativas")
        
        # 6. Listar setores
        result = self.make_request("GET", "/empresas/setores")
        if result is not None:
            self.log_success("Listar setores")
        else:
            self.log_error("Listar setores")

    # ==================== TESTES DE PROBLEMAS ====================

    def test_problema_endpoints(self):
        """Testar endpoints de problemas"""
        self.log_section("TESTES DE PROBLEMAS")
        
        if not self.empresa_token:
            self.log_skip("Testes de problemas (sem token de empresa)")
            return
        
        # 1. Criar problema
        problema_data = {
            "titulo": "Sistema de Recomendação de Produtos",
            "descricao": "Desenvolver um sistema de recomendação inteligente usando machine learning para sugerir produtos aos usuários baseado em seu histórico de compras e comportamento de navegação.",
            "contexto_empresa": "E-commerce de grande porte com milhões de produtos",
            "area": "Inteligência Artificial",
            "nivel_dificuldade": "avancado",
            "tipo": "free",
            "objetivos": "Criar sistema de ML que aumente conversão em 15%",
            "requisitos": "Python, scikit-learn, pandas, API REST",
            "recursos_fornecidos": "Dataset de transações, documentação da API",
            "prazo_dias": 30,
            "pontos_recompensa": 500,
            "oferece_certificado": True,
            "premio_descricao": "Certificado digital + possibilidade de contratação",
            "data_inicio": date.today().isoformat(),
            "data_fim": (date.today() + timedelta(days=30)).isoformat()
        }
        
        result = self.make_request(
            "POST",
            "/problemas/",
            data=problema_data,
            token=self.empresa_token,
            expected_status=201
        )
        
        if result:
            self.log_success("Criar problema")
            self.problema_id = result.get("problema_id")
        else:
            self.log_error("Criar problema")
            return
        
        # 2. Listar problemas
        result = self.make_request("GET", "/problemas/")
        if result is not None:
            self.log_success("Listar problemas")
        else:
            self.log_error("Listar problemas")
        
        # 3. Listar problemas com filtros
        result = self.make_request(
            "GET",
            "/problemas/",
            params={"area": "Inteligência Artificial", "nivel": "avancado"}
        )
        if result is not None:
            self.log_success("Listar problemas com filtros")
        else:
            self.log_error("Listar problemas com filtros")
        
        # 4. Obter detalhes do problema
        if self.problema_id and self.user_token:
            result = self.make_request(
                "GET",
                f"/problemas/{self.problema_id}",
                token=self.user_token
            )
            if result:
                self.log_success("Obter detalhes do problema")
            else:
                self.log_error("Obter detalhes do problema")
        
        # 5. Listar meus problemas (empresa)
        result = self.make_request(
            "GET",
            "/problemas/empresa/meus-problemas",
            token=self.empresa_token
        )
        if result is not None:
            self.log_success("Listar problemas da empresa")
        else:
            self.log_error("Listar problemas da empresa")

    # ==================== TESTES DE SOLUÇÕES ====================

    def test_solucao_endpoints(self):
        """Testar endpoints de soluções"""
        self.log_section("TESTES DE SOLUÇÕES")
        
        if not self.user_token or not self.problema_id:
            self.log_skip("Testes de soluções (sem token de usuário ou problema)")
            return
        
        # 1. Submeter solução
        solucao_data = {
            "problema_id": self.problema_id,
            "descricao_solucao": """
            Desenvolvi um sistema de recomendação híbrido combinando:
            
            1. Filtragem Colaborativa usando SVD (Singular Value Decomposition)
            2. Filtragem Baseada em Conteúdo com TF-IDF
            3. Sistema de ponderação adaptativo
            
            Implementação:
            - Backend em Python com FastAPI
            - Modelo ML treinado com scikit-learn
            - Cache Redis para performance
            - API REST documentada com OpenAPI
            
            Resultados nos testes:
            - Precisão: 87%
            - Recall: 82%
            - Tempo de resposta: <100ms
            - Escalabilidade testada com 1M de produtos
            
            O código está documentado, testado (cobertura 85%) e pronto para produção.
            """,
            "link_repositorio": "https://github.com/teste/recommendation-system",
            "link_demo": "https://demo.recommendation-system.com"
        }
        
        result = self.make_request(
            "POST",
            "/solucoes/",
            data=solucao_data,
            token=self.user_token,
            expected_status=201
        )
        
        if result:
            self.log_success("Submeter solução")
            self.solucao_id = result.get("solucao_id")
            
            # Exibir feedback da IA se disponível
            if "feedback" in result:
                self.log_info(f"Pontuação: {result.get('pontuacao', 'N/A')}")
                self.log_info(f"Status: {result.get('status', 'N/A')}")
        else:
            self.log_error("Submeter solução")
        
        # 2. Listar minhas soluções
        result = self.make_request(
            "GET",
            "/solucoes/minhas-solucoes",
            token=self.user_token
        )
        if result is not None:
            self.log_success("Listar minhas soluções")
        else:
            self.log_error("Listar minhas soluções")
        
        # 3. Obter detalhes da solução
        if self.solucao_id:
            result = self.make_request(
                "GET",
                f"/solucoes/{self.solucao_id}",
                token=self.user_token
            )
            if result:
                self.log_success("Obter detalhes da solução")
            else:
                self.log_error("Obter detalhes da solução")
        
        # 4. Listar soluções do problema (empresa)
        if self.empresa_token and self.problema_id:
            result = self.make_request(
                "GET",
                f"/solucoes/problema/{self.problema_id}/solucoes",
                token=self.empresa_token
            )
            if result is not None:
                self.log_success("Listar soluções do problema (empresa)")
            else:
                self.log_error("Listar soluções do problema (empresa)")

    # ==================== TESTES DE RANKING ====================

    def test_ranking_endpoints(self):
        """Testar endpoints de ranking"""
        self.log_section("TESTES DE RANKING")
        
        # 1. Ranking global
        result = self.make_request("GET", "/ranking/global")
        if result is not None:
            self.log_success("Ranking global")
        else:
            self.log_error("Ranking global")
        
        # 2. Ranking por área
        result = self.make_request("GET", "/ranking/por-area/Inteligência Artificial")
        if result is not None:
            self.log_success("Ranking por área")
        else:
            self.log_error("Ranking por área")
        
        # 3. Ranking mensal
        result = self.make_request("GET", "/ranking/mensal")
        if result is not None:
            self.log_success("Ranking mensal")
        else:
            self.log_error("Ranking mensal")
        
        # 4. Ranking semanal
        result = self.make_request("GET", "/ranking/semanal")
        if result is not None:
            self.log_success("Ranking semanal")
        else:
            self.log_error("Ranking semanal")
        
        # 5. Top performers
        result = self.make_request("GET", "/ranking/top-performers")
        if result is not None:
            self.log_success("Top performers")
        else:
            self.log_error("Top performers")
        
        # 6. Estatísticas de ranking
        result = self.make_request("GET", "/ranking/estatisticas")
        if result is not None:
            self.log_success("Estatísticas de ranking")
        else:
            self.log_error("Estatísticas de ranking")

    # ==================== TESTES DE IA ====================

    def test_ai_endpoints(self):
        """Testar endpoints de IA (teste)"""
        self.log_section("TESTES DE IA")
        
        # 1. Health check
        result = self.make_request("GET", "/ai-test/health")
        if result:
            self.log_success("Health check IA")
            self.log_info(f"Status: {result.get('status')}")
        else:
            self.log_error("Health check IA")
        
        # 2. Status dos providers
        result = self.make_request("GET", "/ai-test/providers-status")
        if result:
            self.log_success("Status dos providers IA")
            self.log_info(f"Providers disponíveis: {result.get('total_available')}")
        else:
            self.log_error("Status dos providers IA")
        
        # 3. Estatísticas do cache
        result = self.make_request("GET", "/ai-test/cache-stats")
        if result is not None:
            self.log_success("Estatísticas do cache")
        else:
            self.log_error("Estatísticas do cache")

    # ==================== EXECUTAR TODOS OS TESTES ====================

    def run_all_tests(self):
        """Executar todos os testes"""
        self.log_info(f"Iniciando testes na API: {self.base_url}")
        self.log_info(f"Modo verbose: {'Ativado' if self.verbose else 'Desativado'}\n")
        
        # Executar testes em ordem
        if not self.test_auth_endpoints():
            self.log_error("Falha nos testes de autenticação. Abortando testes subsequentes.")
            self.print_summary()
            return
        
        self.test_user_endpoints()
        self.test_empresa_endpoints()
        self.test_problema_endpoints()
        self.test_solucao_endpoints()
        self.test_ranking_endpoints()
        self.test_ai_endpoints()
        
        # Resumo final
        self.print_summary()

    def print_summary(self):
        """Imprimir resumo dos testes"""
        self.log_section("RESUMO DOS TESTES")
        
        total = self.passed + self.failed + self.skipped
        
        self.log(f"Total de testes: {total}", Fore.WHITE)
        self.log_success(f"Passou: {self.passed}")
        self.log_error(f"Falhou: {self.failed}")
        self.log_skip(f"Pulado: {self.skipped}")
        
        if self.failed == 0:
            self.log("\n🎉 Todos os testes passaram com sucesso!", Fore.GREEN)
        else:
            self.log(f"\n⚠️  {self.failed} teste(s) falharam", Fore.RED)
        
        # Taxa de sucesso
        if total > 0:
            taxa = (self.passed / total) * 100
            color = Fore.GREEN if taxa >= 90 else Fore.YELLOW if taxa >= 70 else Fore.RED
            self.log(f"\nTaxa de sucesso: {taxa:.1f}%", color)


def main():
    parser = argparse.ArgumentParser(
        description='Testar endpoints da API TalentHub'
    )
    parser.add_argument(
        '--base-url',
        default='http://localhost:8000',
        help='URL base da API (padrão: http://localhost:8000)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modo verbose (mostra detalhes das requisições)'
    )
    
    args = parser.parse_args()
    
    # Criar instância do tester e executar
    tester = APITester(args.base_url, args.verbose)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
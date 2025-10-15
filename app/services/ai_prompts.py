"""
Templates de prompts otimizados para análise de soluções
"""

def get_analise_prompt(problema: dict, solucao_texto: str) -> str:
    """
    Gera prompt otimizado para análise de solução
    
    Args:
        problema: Dict com dados do problema
        solucao_texto: Texto da solução submetida
    
    Returns:
        Prompt formatado para a IA
    """
    
    prompt = f"""Você é um avaliador técnico especializado da plataforma NERUS, responsável por avaliar soluções de estudantes angolanos para problemas reais de empresas.

## CONTEXTO DO PROBLEMA

**Título:** {problema['titulo']}

**Descrição do Problema:**
{problema['descricao']}

**Área:** {problema.get('area', 'Não especificada')}

**Nível de Dificuldade:** {problema.get('nivel_dificuldade', 'intermediario')}

**Contexto da Empresa:**
{problema.get('contexto_empresa', 'Não fornecido')}

**Objetivos Esperados:**
{problema.get('objetivos', 'Resolver o problema de forma prática e viável')}

**Requisitos Técnicos:**
{problema.get('requisitos', 'Não especificados')}

---

## SOLUÇÃO SUBMETIDA PELO ESTUDANTE

{solucao_texto}

---

## SUA TAREFA

Analise a solução submetida de forma justa, construtiva e educativa. Lembre-se que o objetivo é EDUCAR e CAPACITAR estudantes, não apenas julgar.

Avalie considerando:

1. **ADEQUAÇÃO AO PROBLEMA (30 pontos)**
   - A solução resolve o problema proposto?
   - Atende aos requisitos e objetivos?
   - É viável na prática?

2. **QUALIDADE TÉCNICA (25 pontos)**
   - Está tecnicamente sólida?
   - Usa boas práticas?
   - É bem estruturada?

3. **CRIATIVIDADE E INOVAÇÃO (20 pontos)**
   - Apresenta abordagem criativa?
   - Traz ideias inovadoras?
   - Vai além do básico?

4. **CLAREZA E APRESENTAÇÃO (15 pontos)**
   - Explicação clara e compreensível?
   - Bem organizada?
   - Fácil de entender?

5. **VIABILIDADE DE IMPLEMENTAÇÃO (10 pontos)**
   - Pode ser implementada?
   - É prática e realista?
   - Considera recursos disponíveis?

---

## INSTRUÇÕES CRÍTICAS

⚠️ **RESPONDA APENAS COM UM JSON VÁLIDO. NÃO INCLUA MARKDOWN, BACKTICKS OU QUALQUER TEXTO FORA DO JSON.**

O JSON deve ter EXATAMENTE esta estrutura:

{{
  "pontuacao": <número entre 0-100>,
  "status_recomendado": "<aprovada|reprovada|revisao>",
  "feedback": "<análise geral em 2-3 parágrafos>",
  "pontos_fortes": [
    "<ponto forte 1>",
    "<ponto forte 2>",
    "<ponto forte 3>"
  ],
  "pontos_melhoria": [
    "<melhoria 1>",
    "<melhoria 2>",
    "<melhoria 3>"
  ],
  "criterios": {{
    "adequacao_problema": <0-30>,
    "qualidade_tecnica": <0-25>,
    "criatividade": <0-20>,
    "clareza": <0-15>,
    "viabilidade": <0-10>
  }},
  "recomendacoes_especificas": [
    "<recomendação prática 1>",
    "<recomendação prática 2>"
  ]
}}

## CRITÉRIOS DE APROVAÇÃO

- **APROVADA:** Pontuação >= 60 (solução boa, viável e atende requisitos)
- **REVISÃO:** Pontuação 40-59 (tem potencial mas precisa melhorias)
- **REPROVADA:** Pontuação < 40 (não atende requisitos mínimos)

## IMPORTANTE

✅ Seja CONSTRUTIVO e EDUCATIVO no feedback
✅ Destaque pontos fortes mesmo em soluções fracas
✅ Dê recomendações PRÁTICAS e ACIONÁVEIS
✅ Considere o contexto angolano e recursos disponíveis
✅ Incentive o aprendizado contínuo
❌ NÃO seja excessivamente crítico ou desmotivador
❌ NÃO use linguagem técnica demais sem explicar

RESPONDA AGORA APENAS COM O JSON (SEM MARKDOWN):"""

    return prompt


def get_prompt_simplificado(problema_titulo: str, problema_desc: str, solucao: str) -> str:
    """
    Prompt simplificado para casos onde há pouca informação
    """
    return f"""Avalie esta solução de estudante:

PROBLEMA: {problema_titulo}
{problema_desc}

SOLUÇÃO:
{solucao}

Responda APENAS com JSON válido (sem markdown):

{{
  "pontuacao": <0-100>,
  "status_recomendado": "<aprovada|reprovada|revisao>",
  "feedback": "<análise em 2 parágrafos>",
  "pontos_fortes": ["<ponto 1>", "<ponto 2>", "<ponto 3>"],
  "pontos_melhoria": ["<melhoria 1>", "<melhoria 2>"],
  "criterios": {{
    "adequacao_problema": <0-30>,
    "qualidade_tecnica": <0-25>,
    "criatividade": <0-20>,
    "clareza": <0-15>,
    "viabilidade": <0-10>
  }},
  "recomendacoes_especificas": ["<recomendação 1>", "<recomendação 2>"]
}}

Critérios: >=60 aprovada, 40-59 revisão, <40 reprovada.
Seja construtivo e educativo."""
# 1. Decisões Técnicas do Agente

## Objetivo

Desenvolver um agente especialista capaz de interpretar relatórios genéticos estruturados e responder perguntas em linguagem natural de forma clara, segura e rastreável.

O agente não realiza diagnósticos médicos e opera exclusivamente sobre informações recuperadas do relatório por meio da arquitetura RAG (Retrieval-Augmented Generation).

---

## Modelo de Linguagem Escolhido

Modelo principal:
GPT-4.1 Mini

Modelo alternativo:
Gemini Flash

Justificativa:
O modelo foi escolhido por apresentar bom desempenho em interpretação textual, seguimento de instruções e integração com arquiteturas RAG, permitindo respostas mais consistentes e menor probabilidade de alucinação.

---

## Configuração do Modelo

| Parâmetro | Valor |
|----------|------|
| Temperatura | 0.2 |
| Top-p | 0.8 |
| Máximo de Tokens | 700 |
| Frequency Penalty | 0 |
| Presence Penalty | 0 |

---

## Estratégia de Resposta

O agente opera em dois modos:

### Modo Paciente
Explicações simplificadas, acessíveis e sem linguagem alarmista.

### Modo Técnico
Explicações mais detalhadas e técnicas para usuários avançados.

---

## Restrições

O agente:

✓ Responde apenas com base no relatório carregado  
✓ Explica termos genéticos  
✓ Exibe fontes utilizadas  

O agente NÃO:

✗ Diagnostica doenças  
✗ Prescreve tratamentos  
✗ Responde fora do escopo do relatório

# 2. Estrutura do Módulo do Agente

O módulo `agente/` foi criado para concentrar toda a lógica responsável pelo comportamento conversacional da solução Genera AI.

Enquanto as demais etapas do projeto tratam da extração, estruturação, geração de embeddings e busca semântica, este módulo define como o agente interpreta os trechos recuperados e transforma essas informações em respostas seguras, claras e rastreáveis para o usuário final.

## Organização dos Arquivos

| Arquivo | Responsabilidade |
|--------|------------------|
| `config_llm.py` | Define o modelo de linguagem e os hiperparâmetros utilizados pelo agente. |
| `prompts.py` | Armazena o system prompt, templates de resposta e prompts de fallback. |
| `guardrails.py` | Implementa regras de segurança para impedir diagnóstico, prescrição e respostas fora do escopo. |
| `agente_especialista.py` | Orquestra o fluxo principal do agente, combinando pergunta, contexto recuperado, prompts e validações. |
| `testes_agente.py` | Reúne testes com perguntas comuns, ambíguas e perguntas-limite para validar o comportamento do agente. |

## Papel do Módulo na Arquitetura RAG

O agente não acessa diretamente o relatório bruto. Ele recebe trechos previamente recuperados pela busca semântica e utiliza esses trechos como única base para formular a resposta.

Fluxo esperado:

```txt
Pergunta do usuário
↓
Busca semântica no relatório
↓
Trechos relevantes recuperados
↓
Aplicação dos guardrails
↓
Construção do prompt final
↓
Resposta do agente
↓
Exibição das fontes utilizadas

# 3. Guardrails Médicos

O agente possui uma camada de validação antes da geração da resposta. Essa camada impede que perguntas sensíveis sejam enviadas diretamente ao modelo de linguagem quando envolvem diagnóstico, prescrição, previsão médica absoluta ou temas fora do escopo do relatório.

## Categorias Bloqueadas

| Categoria | Exemplo | Comportamento esperado |
|----------|---------|------------------------|
| Diagnóstico | "Tenho câncer?" | Recusa segura e orientação para profissional de saúde |
| Prescrição | "Qual remédio devo tomar?" | Recusa indicação de medicamento ou dose |
| Risco alto | "Quanto tempo vou viver?" | Explica que genética não define prognóstico individual |
| Fora do escopo | "Qual dieta devo fazer?" | Informa que responde apenas sobre o relatório genético |
| Sem contexto | Nenhum trecho recuperado | Responde que não há informação suficiente |

## Objetivo dos Guardrails

Os guardrails reduzem riscos de alucinação, interpretações indevidas e uso inadequado do sistema em contexto de saúde.

O agente foi projetado para atuar como uma ferramenta educativa e explicativa, não como ferramenta diagnóstica.

# 4. Agente Especialista

O arquivo `agente_especialista.py` concentra a lógica principal do agente conversacional.

Ele recebe uma pergunta do usuário, valida a segurança da pergunta por meio dos guardrails, organiza os trechos recuperados pela busca semântica e constrói o prompt final que será enviado ao modelo de linguagem.

## Fluxo do Agente

```txt
Pergunta do usuário
↓
Validação dos guardrails
↓
Recebimento dos trechos recuperados pelo RAG
↓
Validação de contexto
↓
Construção do prompt final
↓
Geração da resposta
↓
Retorno com resposta + fontes

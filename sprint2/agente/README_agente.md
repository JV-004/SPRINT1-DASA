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

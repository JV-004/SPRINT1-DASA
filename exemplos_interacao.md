# Exemplos de Interação — Sistema Genera IA

Estes exemplos simulam perguntas reais de usuários e as respostas esperadas do sistema,
baseadas nos dados estruturados do arquivo `dados_estruturados.json`.
O sistema usa os dados do JSON como contexto para o LLM gerar respostas em linguagem simples.

---

## Exemplo 1 — Pergunta sobre risco específico (Diabetes)

**Perfil do usuário:** Paciente  
**Pergunta:**

> "Eu tenho risco de diabetes?"

**Dados consultados no JSON:**

```json
{
  "doenca": "Diabetes Mellitus Tipo 2",
  "risco": "Alto",
  "marcadores_geneticos": [
    "RS7903146 (TCF7L2) — T/T",
    "RS12255372 (TCF7L2) — T/G"
  ],
  "escore_poligênico_percentil": 89
}
```

**Resposta esperada do sistema:**

> Sim, Carlos. Seu perfil genético indica **risco Alto** para Diabetes Tipo 2.
>
> Dois marcadores no gene TCF7L2 — que controla como seu corpo usa insulina — apresentam variações associadas a maior risco. Seu escore poligênico está no percentil 89, ou seja, você tem predisposição genética maior que 89% da população de referência.
>
> Isso não significa que você vai desenvolver diabetes, mas que vale redobrar a atenção com:
>
> - Alimentação com baixo índice glicêmico
> - Exercícios aeróbicos regulares (pelo menos 150 min/semana)
> - Exames de glicemia e HbA1c a cada 6 meses
>
> Recomendo conversar com um endocrinologista para acompanhamento personalizado.

---

## Exemplo 2 — Pergunta sobre câncer (BRCA)

**Perfil do usuário:** Paciente  
**Pergunta:**

> "O que significa essa alteração no BRCA2 que aparece no meu relatório?"

**Dados consultados no JSON:**

```json
{
  "doenca": "Carcinoma de Mama (BRCA-relacionado)",
  "risco": "Alto",
  "marcadores_geneticos": [
    {
      "id_snp": "RS80357906",
      "gene": "BRCA2",
      "alelo": "variante patogênica c.5946delT"
    }
  ],
  "descricao_simples": "Foi encontrada uma alteração importante em um gene chamado BRCA2..."
}
```

**Resposta esperada do sistema:**

> O gene BRCA2 funciona como um "protetor" do seu DNA — ele ajuda a reparar erros que podem levar ao câncer. No seu relatório, foi identificada uma alteração nesse gene chamada **c.5946delT**, classificada como patogênica (ou seja, com impacto real na função do gene).
>
> Isso aumenta significativamente o risco de câncer de mama (entre 45% e 85% ao longo da vida) e câncer de ovário (entre 10% e 30%).
>
> **O que fazer agora:**
>
> - Procure um geneticista ou oncologista geneticista o quanto antes
> - Inicie rastreamento mamográfico anual (a partir dos 25 anos)
> - Considere também ressonância magnética de mama anual
>
> Esse resultado é importante e merece atenção especializada. Você não precisa enfrentar isso sozinho(a).

---

## Exemplo 3 — Pergunta sobre ancestralidade

**Perfil do usuário:** Paciente  
**Pergunta:**

> "De onde vêm meus ancestrais segundo o exame?"

**Dados consultados no JSON:**

```json
"ancestralidade": [
  {"regiao": "Europa Ibérica", "percentual": 42.3},
  {"regiao": "África Subsaariana", "percentual": 22.1},
  {"regiao": "Europa do Sul", "percentual": 18.7},
  {"regiao": "Ameríndio (América do Sul)", "percentual": 11.4}
]
```

**Resposta esperada do sistema:**

> Sua composição ancestral é bem diversa — típica da formação do povo brasileiro! Veja o resumo:
>
> | Origem                            | Proporção |
> | --------------------------------- | --------- |
> | Europa Ibérica (Portugal/Espanha) | 42,3%     |
> | África Subsaariana                | 22,1%     |
> | Europa do Sul (Itália/Grécia)     | 18,7%     |
> | Ameríndio (América do Sul)        | 11,4%     |
> | Outros                            | 5,5%      |
>
> Isso significa que você tem raízes predominantemente europeias ibéricas, com contribuição significativa africana e indígena sul-americana — uma mistura muito comum entre brasileiros.
>
> Importante: esses percentuais refletem padrões genéticos populacionais e não têm implicações clínicas diretas.

---

## Exemplo 4 — Pergunta de médico sobre resumo clínico

**Perfil do usuário:** Médico  
**Pergunta:**

> "Quais são as condições de alto risco identificadas neste paciente e quais as recomendações prioritárias?"

**Dados consultados no JSON:**

```json
"sumario": {"condicoes_alto_risco": 2},
"resultados": [
  {"doenca": "Diabetes Mellitus Tipo 2", "risco": "Alto", "recomendacao": "..."},
  {"doenca": "Carcinoma de Mama (BRCA-relacionado)", "risco": "Alto", "recomendacao": "..."}
]
```

**Resposta esperada do sistema:**

> **Resumo clínico — Carlos Eduardo Mendes (GEN-2024-00847)**
>
> Foram identificadas **2 condições de risco Alto**:
>
> **1. Diabetes Mellitus Tipo 2**
>
> - Marcadores: RS7903146 (TCF7L2) homozigoto T/T; RS12255372 heterozigoto T/G
> - PRS: percentil 89
> - Conduta sugerida: monitoramento semestral de glicemia e HbA1c; avaliação endocrinológica
>
> **2. Carcinoma de Mama — BRCA2 patogênico**
>
> - Variante: c.5946delT (p.Ser1982Argfs) — Classe 5 ACMG
> - Risco cumulativo de mama: 45–85%; ovário: 10–30%
> - Conduta sugerida: aconselhamento genético urgente; rastreamento mamográfico + RNM anual a partir dos 25 anos
>
> Adicionalmente, 3 condições de risco Médio foram identificadas (Hipertensão, Alzheimer tardio, Doença Celíaca). Relatório completo disponível para consulta detalhada.

---

## Exemplo 5 — Pergunta sobre condição de baixo risco

**Perfil do usuário:** Paciente  
**Pergunta:**

> "Tenho intolerância à lactose? Posso tomar leite?"

**Dados consultados no JSON:**

```json
{
  "doenca": "Intolerância à Lactose (tipo adulto)",
  "risco": "Baixo",
  "marcadores_geneticos": [
    {
      "id_snp": "RS4988235",
      "alelo": "C/T",
      "observacao": "persistência parcial da lactase"
    }
  ],
  "descricao_simples": "Você tem uma tolerância parcial à lactose..."
}
```

**Resposta esperada do sistema:**

> Boa notícia: seu risco genético para intolerância à lactose é **Baixo**.
>
> Você possui um genótipo que indica **persistência parcial da lactase** — a enzima que digere o açúcar do leite. Na prática, isso significa que você provavelmente consegue consumir leite e derivados em quantidades moderadas sem grandes desconfortos.
>
> **Dicas práticas:**
>
> - Leite e queijos frescos: consuma em porções moderadas e observe como seu corpo reage
> - Iogurte e queijos curados (parmesão, cheddar): geralmente muito bem tolerados, pois têm menos lactose
> - Não é necessário suplementar cálcio se mantiver consumo regular de laticínios
>
> Se mesmo assim sentir desconforto após consumir leite, vale mencionar ao seu médico — fatores além da genética também influenciam a tolerância individual.

---

## Exemplo 6 — Pergunta sobre visão geral do relatório

**Perfil do usuário:** Paciente  
**Pergunta:**

> "Me dá um resumo geral do meu relatório. O que devo me preocupar mais?"

**Dados consultados no JSON:**

```json
"sumario": {
  "total_condicoes_analisadas": 7,
  "condicoes_alto_risco": 2,
  "condicoes_medio_risco": 3,
  "condicoes_baixo_risco": 2
}
```

**Resposta esperada do sistema:**

> Seu relatório analisou **7 condições genéticas**. Aqui está o panorama geral:
>
> 🔴 **Atenção prioritária (Risco Alto):**
>
> - Diabetes Tipo 2 — predisposição genética elevada (percentil 89)
> - Câncer de Mama relacionado ao BRCA2 — variante patogênica identificada
>
> 🟡 **Monitoramento recomendado (Risco Médio):**
>
> - Hipertensão Arterial
> - Doença de Alzheimer (início tardio)
> - Doença Celíaca
>
> 🟢 **Sem preocupação genética específica (Risco Baixo):**
>
> - Trombofilia Hereditária — sem mutações detectadas
> - Intolerância à Lactose — tolerância parcial esperada
>
> **Minha recomendação:** Comece pelos itens de risco Alto. O resultado do BRCA2 especialmente merece consulta com um especialista o quanto antes. Para o diabetes, mudanças de estilo de vida já fazem grande diferença.
>
> Quer que eu explique alguma condição em mais detalhes?

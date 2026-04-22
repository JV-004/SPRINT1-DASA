# Processamento de Dados (PDF → Estruturado)

> Responsabilidade: Engenheiro de Dados  
> Sprint: 1 — Estruturação da Base do Projeto  
> Produto: Genera / Dasa

---

## O Problema com os Dados Não Estruturados

O relatório genético do Genera é entregue em formato PDF — um documento projetado para leitura humana, não para processamento por máquinas. Isso cria uma barreira técnica fundamental:

**O que existe no PDF:**

- Texto corrido com terminologia genômica densa
- Tabelas com dados clínicos (risco, marcadores, recomendações)
- Seções misturadas sem separação semântica clara
- Caracteres especiais (notação científica, símbolos genéticos)
- Cabeçalhos e rodapés repetidos em todas as páginas

**O que a IA precisa:**

- Dados organizados em campos nomeados
- Valores tipados (texto, número, lista, booleano)
- Relações claras entre entidades (paciente → condição → marcador → recomendação)
- Formato padronizado e previsível (JSON)

Sem essa transformação, a IA não consegue responder perguntas com precisão — ela "vê" um bloco de texto sem contexto, não um conjunto de dados estruturados.

---

## Upload do PDF

O fluxo começa com o envio do arquivo pelo usuário:

```
Usuário → Interface Web/App → Upload do PDF → Backend (API REST)
```

**Especificações do upload:**

- Formato aceito: `.pdf`
- Tamanho máximo: 50 MB
- Validação: verificação de MIME type (`application/pdf`) antes do processamento
- Armazenamento temporário: o arquivo é processado em memória e descartado após a extração — nenhum PDF é persistido no servidor (privacidade)
- Autenticação: o upload exige token de sessão autenticado do paciente

---

## Técnica de Extração Escolhida

### Ferramenta principal: `pdfplumber`

### Ferramenta complementar: `PyMuPDF (fitz)`

O relatório Genera é um **PDF nativo** (texto selecionável, gerado digitalmente pelo sistema do laboratório). Portanto, OCR não é necessário no fluxo padrão.

**Por que pdfplumber:**

- Extração de tabelas como estruturas de dados nativas (listas de listas)
- Detecção automática de bordas e células de tabela
- Integração direta com pandas para transformação dos dados
- Amplamente usado em projetos de ciência de dados em saúde

**Por que PyMuPDF como complemento:**

- Extração de metadados do documento (versão, data de criação)
- Extração de texto de seções sem tabela (parágrafos de descrição técnica)
- Melhor performance em PDFs com layout complexo

**Fallback para PDFs escaneados:**  
Se `pdfplumber` retornar menos de 100 caracteres por página, o sistema ativa automaticamente o pipeline OCR:

```
pdf2image → imagens por página → Tesseract OCR (lang=por) → texto bruto
```

Para documentação completa da justificativa técnica, ver [`extracao_tecnica.md`](./extracao_tecnica.md).

---

## Limpeza dos Dados Extraídos

O texto bruto extraído passa por um pipeline de limpeza antes da estruturação:

| Etapa                 | Problema                                  | Solução                                     |
| --------------------- | ----------------------------------------- | ------------------------------------------- |
| Remoção de cabeçalhos | "DASA \| GENERA" repetido em cada página  | Regex de detecção e remoção                 |
| Remoção de rodapés    | "Página X de Y", dados do laboratório     | `re.sub(r'Página \d+ de \d+', '', texto)`   |
| Quebras de linha      | `\n\n\n` excessivos                       | Normalização para separador único           |
| Espaços duplos        | Tabulações e espaços irregulares          | `re.sub(r'\s+', ' ', texto)`                |
| Caracteres especiais  | `ε`, `μ`, `≥` corrompidos                 | Forçar UTF-8; mapeamento de substituição    |
| Marcadores genéticos  | `RS7903146 \| RS12255372` em célula única | Split por `\|` e strip                      |
| Percentuais decimais  | `42,3%` (padrão BR)                       | Substituir `,` por `.` em contexto numérico |

---

## Estruturação dos Dados (JSON)

Após a limpeza, os dados são mapeados para um schema JSON padronizado.

**Campos principais:**

```json
{
  "paciente": { "nome", "data_nascimento", "id_relatorio", "data_exame" },
  "sumario": { "total_condicoes_analisadas", "condicoes_alto_risco", ... },
  "resultados": [
    {
      "id", "doenca", "categoria", "risco",
      "marcadores_geneticos": [{ "id_snp", "gene", "alelo", "observacao" }],
      "escore_poligênico_percentil",
      "descricao_tecnica",
      "descricao_simples",
      "recomendacao",
      "fontes": [...]
    }
  ],
  "ancestralidade": [{ "regiao", "percentual", "intervalo_confianca_95" }],
  "metadata": { "versao_relatorio", "laboratorio", "responsavel_tecnico", ... }
}
```

O campo `descricao_simples` é gerado pelo LLM a partir da `descricao_tecnica` — é o coração da proposta de valor do sistema.

Para o JSON completo com todos os dados do relatório simulado, ver [`dados_estruturados.json`](./dados_estruturados.json).

---

## Pipeline de Dados — Diagrama

```
┌──────────────────────────────────────────────────────────────────┐
│  1. PDF                                                          │
│  Upload pelo usuário via interface                               │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  2. EXTRAÇÃO                                                     │
│  pdfplumber → tabelas como listas                                │
│  PyMuPDF   → texto de parágrafos e metadados                     │
│  [fallback] Tesseract OCR → se PDF escaneado                     │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  3. LIMPEZA                                                      │
│  Remoção de cabeçalhos/rodapés repetidos                         │
│  Normalização de espaços, quebras de linha, encoding             │
│  Separação de marcadores genéticos                               │
│  Normalização de percentuais (vírgula → ponto)                   │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  4. ESTRUTURAÇÃO                                                 │
│  Identificação de seções por regex (subtítulos numerados)        │
│  Mapeamento campo a campo para schema JSON                       │
│  Validação de tipos e valores obrigatórios                       │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  5. JSON                                                         │
│  dados_estruturados.json — schema padronizado e validado         │
│  Pronto para consumo pelo pipeline de IA                         │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  6. IA                                                           │
│  JSON → embeddings → RAG → LLM → resposta em linguagem simples   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Mapeamento das Seções do PDF

| Seção                          | Conteúdo                                         | Tipo de Dado         | Complexidade |
| ------------------------------ | ------------------------------------------------ | -------------------- | ------------ |
| Cabeçalho                      | Dados do paciente, ID, datas                     | Tabela 4 colunas     | Média        |
| Sumário Executivo              | Contagens por nível de risco                     | Tabela + texto       | Baixa        |
| Resultados Genéticos (2.1–2.7) | Condições, marcadores, descrições, recomendações | Tabela + texto misto | Alta         |
| Ancestralidade                 | Percentuais por região biogeográfica             | Tabela 3 colunas     | Baixa        |
| Metodologia                    | Pipeline laboratorial e parâmetros               | Tabela técnica       | Média        |
| Rodapé                         | Assinatura, laboratório, versão                  | Texto simples        | Baixa        |

Para mapeamento detalhado de cada seção, ver [`mapeamento_secoes.md`](./mapeamento_secoes.md).

---

## Dado Bruto vs. Dado Estruturado

### Texto bruto extraído do PDF (seção 2.1):

```
2.1 Diabetes Mellitus Tipo 2
Nível de Risco  Categoria  Marcadores Principais
ALTO  Metabolismo e Endocrinologia  RS7903146 (TCF7L2) — alelo T/T | RS12255372 (TCF7L2) — alelo T/G | RS1801282 (PPARG) — alelo C/G
Descrição Técnica: A análise identificou homozigose para o alelo de risco T no polimorfismo
RS7903146 do gene TCF7L2 (Transcription Factor 7-Like 2), variante com odds ratio de 1,37
por alelo de risco em populações europeias (OR combinado: 1,88)...
Recomendação Clínica: Monitoramento semestral de glicemia de jejum e HbA1c...
```

### Dado estruturado (JSON resultante):

```json
{
  "id": "2.1",
  "doenca": "Diabetes Mellitus Tipo 2",
  "categoria": "Metabolismo e Endocrinologia",
  "risco": "Alto",
  "marcadores_geneticos": [
    {
      "id_snp": "RS7903146",
      "gene": "TCF7L2",
      "alelo": "T/T",
      "observacao": "homozigoto para alelo de risco"
    },
    {
      "id_snp": "RS12255372",
      "gene": "TCF7L2",
      "alelo": "T/G",
      "observacao": "heterozigoto"
    },
    {
      "id_snp": "RS1801282",
      "gene": "PPARG",
      "alelo": "C/G",
      "observacao": "Pro12Ala heterozigoto"
    }
  ],
  "escore_poligênico_percentil": 89,
  "descricao_tecnica": "Homozigose para o alelo de risco T no polimorfismo RS7903146...",
  "descricao_simples": "Seu DNA indica uma chance maior de desenvolver diabetes tipo 2...",
  "recomendacao": "Monitoramento semestral de glicemia de jejum e HbA1c..."
}
```

A transformação de texto bruto para JSON estruturado é o que permite à IA responder perguntas com precisão, contexto e rastreabilidade.

---

## Arquivos Gerados

| Arquivo                                                            | Descrição                                            |
| ------------------------------------------------------------------ | ---------------------------------------------------- |
| [`relatorio_genera_simulado.pdf`](./relatorio_genera_simulado.pdf) | PDF fictício e realista do relatório genético        |
| [`mapeamento_secoes.md`](./mapeamento_secoes.md)                   | Documentação detalhada das seções do PDF             |
| [`extracao_tecnica.md`](./extracao_tecnica.md)                     | Justificativa técnica da extração e limpeza          |
| [`dados_estruturados.json`](./dados_estruturados.json)             | JSON completo com todos os dados do relatório        |
| [`exemplos_interacao.md`](./exemplos_interacao.md)                 | 6 exemplos de pergunta e resposta baseados nos dados |

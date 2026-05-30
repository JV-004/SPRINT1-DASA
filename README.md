# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="docs/images/logo-fiap (2).png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>
---

# Projeto Dasa Genera - RAG e Agentes de IA
### Transformando relatórios genéticos em uma experiência inteligente e interativa

---

## EQUIPE FIAP 
## 👨‍🎓 Integrantes: 

| Nome | RM | Contribuição |
|---|---:|---|
| Tayná Esteves | RM562491 | Product Owner / Negócio |
| João | RM565999 | Engenheiro de Dados (Pipeline e Estruturação) |
| Carlos Eduardo | RM566487 | Especialista em IA (Agentes e Prompts) |
| Endrew Alves | RM563646 | Arquiteto + Front-end (Interface Streamlit e Integração) |

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/john-paul-lima/">JOHN PAUL LIMA</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">ANDRÉ GODOI CHIOVATO</a>


## 1. Problema

Os relatórios genéticos do produto Genera, da Dasa, concentram informações extremamente valiosas sobre saúde, como predisposição a doenças e características genéticas.
No entanto, esses dados são entregues em formato PDF, com grande volume de conteúdo e linguagem altamente técnica. Isso gera uma barreira crítica: o usuário possui acesso à informação, mas não consegue compreendê-la plenamente — e, principalmente, não consegue transformá-la em decisões práticas sobre sua saúde. O resultado é um desalinhamento entre o potencial do dado gerado e o valor percebido pelo usuário.

---

## 2. A Solução: Genera AI

A solução consiste na criação de uma interface de chat interativa baseada na arquitetura **RAG (Retrieval-Augmented Generation)** utilizando **LLMs (GPT-4 / GPT-4o)** para transformar relatórios genéticos estruturados em uma experiência conversacional acessível.

O sistema é responsável por:
- Processar o relatório estruturado em JSON e criar *embeddings*.
- Indexar as informações em um banco de dados vetorial (**ChromaDB**).
- Interpretar os resultados com IA e buscar os trechos mais relevantes para a pergunta do usuário.
- Traduzir os conteúdos técnicos para linguagem acessível (modo paciente) ou detalhada (modo técnico).
- Proteger as respostas através de rigorosos **Guardrails** (nunca prescrever medicamentos ou dar diagnósticos fechados).

---

## 3. 🚀 Como Executar o Projeto

Este projeto foi construído utilizando **Python**, **Streamlit**, **ChromaDB** e a **API da OpenAI**. 
Siga os passos abaixo para executar a interface localmente:

### Pré-requisitos
- Python 3.10 ou superior.
- Chave de API da OpenAI (`OPENAI_API_KEY`).

### Passos para instalação

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/JV-004/SPRINT1-DASA.git
   cd SPRINT1-DASA
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r sprint2/interface/requirements_interface.txt
   ```

4. **Configuração de Variáveis de Ambiente:**
   Crie um arquivo `.env` dentro da pasta `sprint2/interface/` ou adicione sua chave de API diretamente na interface do app quando rodar.
   ```env
   OPENAI_API_KEY=sk-sua-chave-aqui
   ```

5. **Inicie o servidor Streamlit:**
   A partir da raiz do projeto, execute o seguinte comando:
   ```bash
   streamlit run sprint2/interface/app.py
   ```

6. Acesse a aplicação no seu navegador: `http://localhost:8501`.

Na interface, você poderá clicar no botão **"▶ Usar relatório de demonstração"** para indexar o arquivo `dados_estruturados.json` contido no repositório e iniciar o chat com a IA.

---

## 4. Arquitetura Técnica

A arquitetura foi dividida entre os integrantes da equipe durante a **Sprint 2** e atua no seguinte fluxo:

1. **Upload / Carga do Relatório (Pipeline):** Processamento do arquivo JSON do relatório genético utilizando um script pipeline que gera os embeddings com o modelo `sentence-transformers` local.
2. **Indexação Vetorial (RAG):** Os embeddings gerados são indexados e salvos localmente utilizando **ChromaDB**. Quando o usuário faz uma pergunta, a busca vetorial retorna os `top_k` (3) trechos mais relevantes do JSON.
3. **Agente Especialista:** O contexto encontrado no ChromaDB é passado junto à pergunta do usuário e instruções de sistema (Prompts e Guardrails) para a API da **OpenAI**.
4. **Interface Streamlit:** Interface gráfica onde o usuário interage, seleciona seu modo de conversa (técnico ou paciente) e lê a resposta contextualizada, verificando também o nível de similaridade e as fontes do seu próprio relatório que foram utilizadas para construir aquela resposta.

### 🛡️ Guardrails (Segurança)

Por se tratar de dados de saúde, foram integrados *guardrails* rígidos na camada do modelo especialista:
- **Sem diagnóstico ou receita:** A IA é proibida de sugerir medicamentos ou declarar o diagnóstico final.
- **Fora de escopo:** Perguntas que fogem dos dados contidos no exame genético não são respondidas para evitar "alucinações".
- **Transparência:** O usuário vê de forma clara e visível de onde (qual parte do exame) a IA extraiu a informação para a resposta (na forma de cards de fontes).

---

## 5. Estrutura do Repositório (Sprint 2)

```text
📦 SPRINT1-DASA
 ┣ 📂 docs                   # Imagens e documentação
 ┣ 📂 sprint2
 ┃ ┣ 📂 agente               # Lógica de prompts, guardrails e chamadas ao LLM
 ┃ ┣ 📂 embeddings           # Funções de geração de representação vetorial
 ┃ ┣ 📂 interface            # App em Streamlit (app.py) e conectores
 ┃ ┣ 📂 pipeline             # Orquestrador de indexação do JSON para a Base Vetorial
 ┃ ┣ 📂 testes               # Scripts de validação de busca
 ┃ ┗ 📂 vetorial             # Manipulação do banco vetorial (ChromaDB)
 ┣ 📜 README.md              # Documentação principal do projeto
 ┗ 📜 dados_estruturados.json # Exemplo de payload simulando os dados de um relatório Genera
```

---

## 6. Conclusão

Esta entrega demonstra a viabilidade técnica de empoderar pacientes da Dasa (Genera) através da inteligência artificial generativa. A união da segurança do **Retrieval-Augmented Generation (RAG)** com a capacidade interpretativa e empática dos LLMs modernos garante respostas confiáveis, personalizadas, didáticas e restritas unicamente aos resultados médicos verídicos do paciente.

> 📹 **Vídeo de apresentação original (Sprint 1):** https://youtu.be/0x63S_5DD_8?si=tAdz-H4V1V-Ay5te *

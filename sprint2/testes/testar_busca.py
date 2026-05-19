"""
Teste de Busca Semântica — Sprint 2 / Genera / Dasa
Faz perguntas em linguagem natural e recupera os chunks mais relevantes.

Uso:
    python sprint2/testes/testar_busca.py
"""

import sys
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

RAIZ = Path(__file__).resolve().parents[2]
BASE_VETORIAL = RAIZ / "sprint2" / "vetorial" / "base_vetorial"
COLECAO_NOME = "genera_relatorio"
MODELO_NOME = "all-MiniLM-L6-v2"
TOP_K = 3

PERGUNTAS_TESTE = [
    "Eu tenho risco de diabetes?",
    "Quais são minhas condições de risco alto?",
    "O que devo fazer para prevenir doenças?",
    "Qual é minha ancestralidade?",
    "Existe algum problema genético relacionado ao câncer?",
]


def buscar(pergunta: str, colecao, modelo: SentenceTransformer, top_k: int = TOP_K) -> list[dict]:
    embedding_pergunta = modelo.encode(pergunta).tolist()
    resultados = colecao.query(
        query_embeddings=[embedding_pergunta],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    chunks_encontrados = []
    for i in range(len(resultados["documents"][0])):
        chunks_encontrados.append({
            "conteudo":    resultados["documents"][0][i],
            "secao":       resultados["metadatas"][0][i].get("secao", ""),
            "fonte":       resultados["metadatas"][0][i].get("fonte", ""),
            "similaridade": round(1 - resultados["distances"][0][i], 4),
        })
    return chunks_encontrados


def imprimir_resultado(pergunta: str, chunks: list[dict]):
    print(f"\n{'─' * 60}")
    print(f"PERGUNTA: {pergunta}")
    print(f"{'─' * 60}")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n  [{i}] Similaridade: {chunk['similaridade']:.4f}")
        print(f"      Seção:  {chunk['secao']}")
        print(f"      Fonte:  {chunk['fonte']}")
        print(
            f"      Trecho: {chunk['conteudo'][:220]}{'...' if len(chunk['conteudo']) > 220 else ''}")


def main():
    print("=" * 60)
    print("TESTE DE BUSCA SEMÂNTICA — Sprint 2 / Genera")
    print("=" * 60)

    if not BASE_VETORIAL.exists():
        print(f"\n[ERRO] Base vetorial não encontrada em: {BASE_VETORIAL}")
        print("       Execute primeiro: python sprint2/pipeline/pipeline_completo.py")
        sys.exit(1)

    print(f"\n[1/2] Conectando à base vetorial: {BASE_VETORIAL}")
    cliente = chromadb.PersistentClient(path=str(BASE_VETORIAL))
    colecao = cliente.get_collection(COLECAO_NOME)
    print(f"      {colecao.count()} documentos indexados.")

    print(f"[2/2] Carregando modelo: {MODELO_NOME}")
    modelo = SentenceTransformer(MODELO_NOME)

    print(f"\n{'=' * 60}")
    print(f"EXECUTANDO {len(PERGUNTAS_TESTE)} PERGUNTAS DE TESTE")
    print(f"{'=' * 60}")

    for pergunta in PERGUNTAS_TESTE:
        chunks = buscar(pergunta, colecao, modelo)
        imprimir_resultado(pergunta, chunks)

    print(f"\n{'=' * 60}")
    print("BUSCA CONCLUÍDA — Sistema funcionando corretamente.")
    print("=" * 60)


if __name__ == "__main__":
    main()

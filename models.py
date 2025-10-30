# models.py
from pydantic import BaseModel
from typing import Dict, List
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Caminho para o arquivo JSON (banco de dados local)
CAMINHO_ARQUIVO = Path("data/dados_operacao.json")

# Lista de locais fictícios (baseados em regiões reais)
LOCAIS = [
    "Complexo do Alemão",
    "Penha",
    "Morro do Adeus",
    "Morro da Baiana",
    "Vila Cruzeiro",
    "Morro do Alemão - Rua 2",
    "Morro do Alemão - Rua 4",
    "Avenida Itaoca",
]

# Tipos de eventos
TIPOS_EVENTO = [
    "Operação Policial",
    "Confronto",
    "Prisões",
    "Apreensão de Armas",
    "Denúncia de Abuso",
    "Resgate de Feridos",
]

# Fontes de notícias simuladas
FONTES = [
    "Agência Brasil",
    "G1",
    "CNN Brasil",
    "Jornal O Globo",
    "Folha de S.Paulo",
    "Extra RJ",
]

# Modelo de dados para representar cada ocorrência
class Ocorrencia(BaseModel):
    id: int
    data: str
    local: str
    tipo_evento: str
    vitimas_reportadas: int
    policiais_envovidos: bool
    unidade_responsavel: str
    descricao: str
    fonte: str

# Função para gerar uma lista com 1000 ocorrências sintéticas
def gerar_dados(qtd: int = 1000) -> List[Ocorrencia]:
    dados = []
    for i in range(1, qtd + 1):
        data_base = datetime(2025, 10, 28, 6, 0, 0)
        data_aleatoria = data_base + timedelta(
            days=random.randint(-2, 2),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        vitimas = random.choice([0, 1, 2, 3, 4, random.randint(5, 15)])
        policiais = random.choice([True, True, True, False])
        unidade = random.choice(["PMERJ", "BOPE", "CORE", "Polícia Civil", "Desconhecida"])
        descricao = random.choice([
            "Moradores relataram intensos disparos durante a madrugada.",
            "Equipes do BOPE atuaram na região com apoio aéreo.",
            "Denúncias apontam prisões e revistas em várias residências.",
            "Relatos de feridos sendo levados por vizinhos até o hospital local.",
            "Polícia afirma ter apreendido armas e drogas.",
            "Trânsito interditado em pontos principais da Penha e do Alemão."
        ])

        dados.append(
            Ocorrencia(
                id=i,
                data=data_aleatoria.isoformat(),
                local=random.choice(LOCAIS),
                tipo_evento=random.choice(TIPOS_EVENTO),
                vitimas_reportadas=vitimas,
                policiais_envovidos=policiais,
                unidade_responsavel=unidade,
                descricao=descricao,
                fonte=random.choice(FONTES),
            )
        )
    return dados

# Função para salvar os dados no arquivo JSON
def salvar_dados_json(dados: List[Ocorrencia]):
    CAMINHO_ARQUIVO.parent.mkdir(exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump([d.dict() for d in dados], arquivo, ensure_ascii=False, indent=2)

# Função para carregar os dados do arquivo
def carregar_dados_json() -> List[Dict]:
    if not CAMINHO_ARQUIVO.exists():
        salvar_dados_json(gerar_dados())
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

# Criamos a base de dados em memória
BASE_DADOS = carregar_dados_json()

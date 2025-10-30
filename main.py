# main.py
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from models import BASE_DADOS, Ocorrencia

# Criando a aplicação FastAPI
app = FastAPI(
    title="API - Ocorrências da Operação no Rio de Janeiro",
    description="API criada para praticar rotas, filtros e buscas usando FastAPI com dados sintéticos.",
    version="1.0.0"
)

# Rota inicial
@app.get("/")
async def inicio():
    return {"mensagem": "Bem-vindo à API da Operação no Rio de Janeiro - Dados Sintéticos"}



#Vamos criar uma rota aonde vamos buscar apenas pelo id e vai me dar todas as informações daquela ocorrência
@app.get("/ocorrencias/{ocorrencia_id}", response_model=Ocorrencia)
async def obter_ocorrencia(ocorrencia_id: int):
    for ocorrencia in BASE_DADOS:
        if ocorrencia["id"] == ocorrencia_id:
            return ocorrencia
    raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
  

#Aqui vamos criar uma rota para contar o numero de vitimas reportadas em todas as ocorrências e as unidades responsáveis pelas operações 
@app.get("/estatisticas/vitimas_reportadas")
async def contar_vitimas_reportadas():
    total_vitimas = sum(ocorrencia["vitimas_reportadas"] for ocorrencia in BASE_DADOS)
    unidades_responsaveis = {}
    for ocorrencia in BASE_DADOS:
        unidade = ocorrencia["unidade_responsavel"]
        if unidade in unidades_responsaveis:
            unidades_responsaveis[unidade] += 1
        else:
            unidades_responsaveis[unidade] = 1
    return {
        "total_vitimas_reportadas": total_vitimas,
        "unidades_responsaveis": unidades_responsaveis
    }


#uvicorn main:app --reload
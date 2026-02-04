from fastapi import APIRouter, HTTPException, Query
from models import EstatisticasResponse, PaginacaoResponse
from db.db import execute_query


router = APIRouter(prefix="/api", tags=["Api"])

@router.get("/operadoras", response_model=PaginacaoResponse)
def listar_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
):
    
    offset = (page - 1) * limit
    
    if search:
        search_term = search.strip()
        search_clean = ''.join(filter(str.isalnum, search_term))
        
        count_query = """
            SELECT COUNT(*) as total FROM dados_operadoras 
            WHERE CNPJ LIKE %s OR UPPER(Razao_Social) LIKE UPPER(%s)
        """
        total_result = execute_query(count_query, (f"%{search_clean}%", f"%{search_term}%"), fetch_one=True)
        
        data_query = """
            SELECT * FROM dados_operadoras 
            WHERE CNPJ LIKE %s OR UPPER(Razao_Social) LIKE UPPER(%s)
            ORDER BY Razao_Social
            LIMIT %s OFFSET %s
        """
        data = execute_query(data_query, (f"%{search_clean}%", f"%{search_term}%", limit, offset))
    else:
        count_query = "SELECT COUNT(*) as total FROM dados_operadoras"
        total_result = execute_query(count_query, fetch_one=True)
        
        data_query = """
            SELECT * FROM dados_operadoras 
            ORDER BY Razao_Social
            LIMIT %s OFFSET %s
        """
        data = execute_query(data_query, (limit, offset))
    
    if total_result:
        total = total_result.get('total', 0)
    else:
        total = 0
    total_pages = (total + limit - 1) // limit
    
    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }


@router.get("/operadoras/{cnpj}")
def obter_operadora(cnpj: str):
    query = "SELECT * FROM dados_operadoras WHERE CNPJ = %s"
    resultado = execute_query(query, (cnpj,), fetch_one=True)
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    
    return resultado


@router.get("/operadoras/{cnpj}/despesas")
def obter_despesas_operadora(
    cnpj: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    offset = (page - 1) * limit
    
    
    operadora_query = "SELECT REGISTRO_OPERADORA FROM dados_operadoras WHERE CNPJ = %s"
    operadora = execute_query(operadora_query, (cnpj,), fetch_one=True)
    
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    
    reg_ans = operadora.get('registro_operadora')
    
    count_query = """
        SELECT COUNT(*) as total 
        FROM despesas_agregadas 
        WHERE REGISTRO_ANS = %s
    """
    total_result = execute_query(count_query, (reg_ans,), fetch_one=True)
    
    
    despesas_query = """
        SELECT Trimestre, Ano, Total_Despesas, Media_Trimestral
        FROM despesas_agregadas 
        WHERE REGISTRO_ANS = %s
        ORDER BY Ano DESC, Trimestre DESC
        LIMIT %s OFFSET %s
    """
    despesas = execute_query(despesas_query, (reg_ans, limit, offset))
    
    if total_result:
        total = total_result.get('total', 0)
    else:
        total = 0
    total_pages = (total + limit - 1) // limit
    
    return {
        "cnpj": cnpj,
        "registro_ans": reg_ans,
        "data": despesas,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }


@router.get("/estatisticas", response_model=EstatisticasResponse)
def obter_estatisticas():
    stats_query = """
        SELECT 
            COALESCE(SUM(Total_Despesas), 0) as total_despesas,
            COALESCE(AVG(Total_Despesas), 0) as media_despesas,
            COUNT(DISTINCT REGISTRO_ANS) as total_operadoras
        FROM despesas_agregadas
    """
    stats = execute_query(stats_query, fetch_one=True)
    
    top5_query = """
        SELECT 
            da.Razao_Social,
            da.CNPJ,
            da.UF,
            SUM(da.Total_Despesas) as total_despesas
        FROM despesas_agregadas da
        GROUP BY da.Razao_Social, da.CNPJ, da.UF
        ORDER BY total_despesas DESC
        LIMIT 5
    """
    top5 = execute_query(top5_query)
    
    return {
        "total_despesas": float(stats.get('total_despesas', 0)),
        "media_despesas": float(stats.get('media_despesas', 0)),
        "total_operadoras": stats.get('total_operadoras', 0),
        "top_5_operadoras": top5
    }


"""
Estoque Engenho - Rotas de Movimentações
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Movimentacao, Produto, TipoMovimento
from app.schemas import (
    MovimentacaoCreate, MovimentacaoResponse,
    MovimentacaoComProduto
)

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.get("/", response_model=List[MovimentacaoComProduto])
def listar_movimentacoes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    produto_id: Optional[int] = None,
    tipo_movimento: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Lista movimentações com filtros e paginação"""
    query = db.query(Movimentacao)
    
    # Filtros
    if produto_id:
        query = query.filter(Movimentacao.produto_id == produto_id)
    
    if tipo_movimento:
        query = query.filter(Movimentacao.tipo_movimento == tipo_movimento)
    
    if data_inicio:
        query = query.filter(Movimentacao.data_movimento >= data_inicio)
    
    if data_fim:
        query = query.filter(Movimentacao.data_movimento <= data_fim)
    
    # Ordenação e paginação
    movimentacoes = query.order_by(
        desc(Movimentacao.data_movimento)
    ).offset(skip).limit(limit).all()
    
    return movimentacoes


@router.get("/recentes", response_model=List[MovimentacaoComProduto])
def listar_movimentacoes_recentes(
    horas: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db)
):
    """Lista movimentações das últimas N horas"""
    data_limite = datetime.now() - timedelta(hours=horas)
    
    movimentacoes = db.query(Movimentacao).filter(
        Movimentacao.data_movimento >= data_limite
    ).order_by(desc(Movimentacao.data_movimento)).all()
    
    return movimentacoes


@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def obter_movimentacao(movimentacao_id: int, db: Session = Depends(get_db)):
    """Obtém uma movimentação específica"""
    movimentacao = db.query(Movimentacao).filter(
        Movimentacao.id == movimentacao_id
    ).first()
    
    if not movimentacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimentação não encontrada"
        )
    
    return movimentacao


@router.post("/entrada", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def dar_entrada(movimentacao_data: MovimentacaoCreate, db: Session = Depends(get_db)):
    """Registra entrada de estoque"""
    return _processar_movimentacao(
        movimentacao_data,
        TipoMovimento.ENTRADA,
        db
    )


@router.post("/saida", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def dar_saida(movimentacao_data: MovimentacaoCreate, db: Session = Depends(get_db)):
    """Registra saída de estoque"""
    return _processar_movimentacao(
        movimentacao_data,
        TipoMovimento.SAIDA,
        db
    )


@router.post("/ajuste", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def ajustar_estoque(movimentacao_data: MovimentacaoCreate, db: Session = Depends(get_db)):
    """Registra ajuste de estoque"""
    return _processar_movimentacao(
        movimentacao_data,
        TipoMovimento.AJUSTE,
        db
    )


def _processar_movimentacao(
    movimentacao_data: MovimentacaoCreate,
    tipo_movimento: TipoMovimento,
    db: Session
) -> Movimentacao:
    """
    Processa uma movimentação de estoque
    """
    # Busca produto pelo código de barras
    produto = db.query(Produto).filter(
        Produto.codigo_barras == movimentacao_data.codigo_barras
    ).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com código {movimentacao_data.codigo_barras} não encontrado"
        )
    
    if not produto.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto está inativo"
        )
    
    # Calcula novo estoque
    estoque_anterior = produto.estoque_atual
    
    if tipo_movimento == TipoMovimento.ENTRADA:
        novo_estoque = estoque_anterior + movimentacao_data.quantidade
    elif tipo_movimento == TipoMovimento.SAIDA:
        novo_estoque = estoque_anterior - movimentacao_data.quantidade
        if novo_estoque < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente. Atual: {estoque_anterior}, Solicitado: {movimentacao_data.quantidade}"
            )
    else:  # AJUSTE
        # Para ajuste, a quantidade é o valor absoluto desejado
        novo_estoque = movimentacao_data.quantidade
    
    # Cria movimentação
    movimentacao = Movimentacao(
        produto_id=produto.id,
        tipo_movimento=tipo_movimento,
        quantidade=movimentacao_data.quantidade,
        estoque_anterior=estoque_anterior,
        estoque_atual=novo_estoque,
        observacao=movimentacao_data.observacao,
        usuario=movimentacao_data.usuario or "App"
    )
    
    # Atualiza estoque do produto
    produto.estoque_atual = novo_estoque
    
    db.add(movimentacao)
    db.commit()
    db.refresh(movimentacao)
    
    return movimentacao


@router.get("/produto/{produto_id}/historico", response_model=List[MovimentacaoResponse])
def listar_historico_produto(
    produto_id: int,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lista histórico de movimentações de um produto específico"""
    
    # Verifica se produto existe
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    movimentacoes = db.query(Movimentacao).filter(
        Movimentacao.produto_id == produto_id
    ).order_by(desc(Movimentacao.data_movimento)).limit(limit).all()
    
    return movimentacoes

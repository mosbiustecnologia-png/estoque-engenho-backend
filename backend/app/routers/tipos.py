"""
Estoque Engenho - Rotas de Tipos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Tipo
from app.schemas import TipoCreate, TipoUpdate, TipoResponse

router = APIRouter(prefix="/tipos", tags=["Tipos"])


@router.get("/", response_model=List[TipoResponse])
def listar_tipos(
    ativo: bool = None,
    db: Session = Depends(get_db)
):
    """Lista todos os tipos de produtos"""
    query = db.query(Tipo)
    
    if ativo is not None:
        query = query.filter(Tipo.ativo == ativo)
    
    return query.all()


@router.get("/{tipo_id}", response_model=TipoResponse)
def obter_tipo(tipo_id: int, db: Session = Depends(get_db)):
    """Obtém um tipo específico"""
    tipo = db.query(Tipo).filter(Tipo.id == tipo_id).first()
    
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo não encontrado"
        )
    
    return tipo


@router.post("/", response_model=TipoResponse, status_code=status.HTTP_201_CREATED)
def criar_tipo(tipo_data: TipoCreate, db: Session = Depends(get_db)):
    """Cria um novo tipo de produto"""
    
    # Verifica se o código já existe
    tipo_existente = db.query(Tipo).filter(Tipo.codigo == tipo_data.codigo).first()
    if tipo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Código {tipo_data.codigo} já está em uso"
        )
    
    novo_tipo = Tipo(**tipo_data.model_dump())
    db.add(novo_tipo)
    db.commit()
    db.refresh(novo_tipo)
    
    return novo_tipo


@router.put("/{tipo_id}", response_model=TipoResponse)
def atualizar_tipo(
    tipo_id: int,
    tipo_data: TipoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um tipo de produto"""
    tipo = db.query(Tipo).filter(Tipo.id == tipo_id).first()
    
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo não encontrado"
        )
    
    # Verifica se o novo código já existe (se foi alterado)
    if tipo_data.codigo and tipo_data.codigo != tipo.codigo:
        tipo_existente = db.query(Tipo).filter(Tipo.codigo == tipo_data.codigo).first()
        if tipo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código {tipo_data.codigo} já está em uso"
            )
    
    # Atualiza apenas os campos fornecidos
    update_data = tipo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tipo, field, value)
    
    db.commit()
    db.refresh(tipo)
    
    return tipo


@router.delete("/{tipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    """Desativa um tipo (soft delete)"""
    tipo = db.query(Tipo).filter(Tipo.id == tipo_id).first()
    
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo não encontrado"
        )
    
    tipo.ativo = False
    db.commit()
    
    return None

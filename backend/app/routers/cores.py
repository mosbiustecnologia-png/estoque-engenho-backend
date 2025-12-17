"""
Estoque Engenho - Rotas de Cores
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Cor
from app.schemas import CorCreate, CorUpdate, CorResponse

router = APIRouter(prefix="/cores", tags=["Cores"])


@router.get("/", response_model=List[CorResponse])
def listar_cores(
    ativo: bool = None,
    db: Session = Depends(get_db)
):
    """Lista todas as cores"""
    query = db.query(Cor)
    
    if ativo is not None:
        query = query.filter(Cor.ativo == ativo)
    
    return query.all()


@router.get("/{cor_id}", response_model=CorResponse)
def obter_cor(cor_id: int, db: Session = Depends(get_db)):
    """Obtém uma cor específica"""
    cor = db.query(Cor).filter(Cor.id == cor_id).first()
    
    if not cor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cor não encontrada"
        )
    
    return cor


@router.post("/", response_model=CorResponse, status_code=status.HTTP_201_CREATED)
def criar_cor(cor_data: CorCreate, db: Session = Depends(get_db)):
    """Cria uma nova cor"""
    
    # Verifica se o código já existe
    cor_existente = db.query(Cor).filter(Cor.codigo == cor_data.codigo).first()
    if cor_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Código {cor_data.codigo} já está em uso"
        )
    
    nova_cor = Cor(**cor_data.model_dump())
    db.add(nova_cor)
    db.commit()
    db.refresh(nova_cor)
    
    return nova_cor


@router.put("/{cor_id}", response_model=CorResponse)
def atualizar_cor(
    cor_id: int,
    cor_data: CorUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma cor"""
    cor = db.query(Cor).filter(Cor.id == cor_id).first()
    
    if not cor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cor não encontrada"
        )
    
    # Verifica se o novo código já existe (se foi alterado)
    if cor_data.codigo and cor_data.codigo != cor.codigo:
        cor_existente = db.query(Cor).filter(Cor.codigo == cor_data.codigo).first()
        if cor_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código {cor_data.codigo} já está em uso"
            )
    
    # Atualiza apenas os campos fornecidos
    update_data = cor_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cor, field, value)
    
    db.commit()
    db.refresh(cor)
    
    return cor


@router.delete("/{cor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cor(cor_id: int, db: Session = Depends(get_db)):
    """Desativa uma cor (soft delete)"""
    cor = db.query(Cor).filter(Cor.id == cor_id).first()
    
    if not cor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cor não encontrada"
        )
    
    cor.ativo = False
    db.commit()
    
    return None

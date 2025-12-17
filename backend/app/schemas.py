"""
Estoque Engenho - Schemas Pydantic
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ============= CORES =============

class CorBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=50)
    codigo: str = Field(..., min_length=2, max_length=2)


class CorCreate(CorBase):
    pass


class CorUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=50)
    codigo: Optional[str] = Field(None, min_length=2, max_length=2)
    ativo: Optional[bool] = None


class CorResponse(CorBase):
    id: int
    ativo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= TIPOS =============

class TipoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    codigo: str = Field(..., min_length=2, max_length=2)
    descricao: Optional[str] = None


class TipoCreate(TipoBase):
    pass


class TipoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    codigo: Optional[str] = Field(None, min_length=2, max_length=2)
    descricao: Optional[str] = None
    ativo: Optional[bool] = None


class TipoResponse(TipoBase):
    id: int
    ativo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= PRODUTOS =============

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=200)
    tipo_id: int = Field(..., gt=0)
    cor_id: int = Field(..., gt=0)
    estoque_minimo: int = Field(default=5, ge=0)
    preco_custo: Optional[Decimal] = Field(None, ge=0)
    preco_venda: Optional[Decimal] = Field(None, ge=0)
    observacoes: Optional[str] = None


class ProdutoCreate(ProdutoBase):
    estoque_inicial: int = Field(default=0, ge=0)
    
    @validator('preco_venda')
    def validar_preco_venda(cls, v, values):
        if v is not None and 'preco_custo' in values and values['preco_custo'] is not None:
            if v < values['preco_custo']:
                raise ValueError('Preço de venda não pode ser menor que o preço de custo')
        return v


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    tipo_id: Optional[int] = Field(None, gt=0)
    cor_id: Optional[int] = Field(None, gt=0)
    estoque_minimo: Optional[int] = Field(None, ge=0)
    preco_custo: Optional[Decimal] = Field(None, ge=0)
    preco_venda: Optional[Decimal] = Field(None, ge=0)
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None


class ProdutoResponse(ProdutoBase):
    id: int
    codigo_produto: str
    codigo_barras: str
    estoque_atual: int
    ativo: bool
    created_at: datetime
    tipo: TipoResponse
    cor: CorResponse
    
    class Config:
        from_attributes = True


class ProdutoListResponse(BaseModel):
    id: int
    nome: str
    codigo_barras: str
    estoque_atual: int
    tipo_nome: str
    cor_nome: str
    preco_venda: Optional[Decimal]
    ativo: bool


# ============= MOVIMENTAÇÕES =============

class MovimentacaoBase(BaseModel):
    tipo_movimento: str = Field(..., pattern="^(ENTRADA|SAIDA|AJUSTE)$")
    quantidade: int = Field(..., gt=0)
    observacao: Optional[str] = Field(None, max_length=255)
    usuario: Optional[str] = Field(None, max_length=100)


class MovimentacaoCreate(MovimentacaoBase):
    codigo_barras: str = Field(..., min_length=1)


class MovimentacaoResponse(BaseModel):
    id: int
    produto_id: int
    tipo_movimento: str
    quantidade: int
    estoque_anterior: int
    estoque_atual: int
    observacao: Optional[str]
    usuario: Optional[str]
    data_movimento: datetime
    
    class Config:
        from_attributes = True


class MovimentacaoComProduto(MovimentacaoResponse):
    produto: ProdutoResponse


# ============= RELATÓRIOS =============

class RelatorioEstoque(BaseModel):
    """Relatório de estoque atual"""
    total_produtos: int
    total_itens: int
    produtos_abaixo_minimo: int
    produtos_zerados: int


class ProdutoBaixoEstoque(BaseModel):
    """Produto com estoque baixo"""
    id: int
    nome: str
    codigo_barras: str
    estoque_atual: int
    estoque_minimo: int
    tipo_nome: str
    cor_nome: str


# ============= BARCODE =============

class BarcodeResponse(BaseModel):
    """Resposta com imagem do código de barras"""
    codigo_barras: str
    formato: str
    image_base64: str

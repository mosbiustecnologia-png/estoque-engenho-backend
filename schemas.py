"""
Schemas Pydantic para validação de dados - Estoque Engenho
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ====== SCHEMAS PARA COR ======
class CorBase(BaseModel):
    codigo: str = Field(..., max_length=10, description="Código da cor")
    nome: str = Field(..., max_length=100, description="Nome da cor")

class CorCreate(CorBase):
    pass

class CorUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=10)
    nome: Optional[str] = Field(None, max_length=100)

class Cor(CorBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ====== SCHEMAS PARA TIPO ======
class TipoBase(BaseModel):
    codigo: str = Field(..., max_length=10, description="Código do tipo")
    nome: str = Field(..., max_length=100, description="Nome do tipo")

class TipoCreate(TipoBase):
    pass

class TipoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=10)
    nome: Optional[str] = Field(None, max_length=100)

class Tipo(TipoBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ====== SCHEMAS PARA PRODUTO ======
class ProdutoBase(BaseModel):
    codigo_barras: str = Field(..., max_length=100, description="Código de barras")
    nome: str = Field(..., max_length=200, description="Nome do produto")
    descricao: Optional[str] = Field(None, description="Descrição do produto")
    preco_compra: float = Field(0.0, ge=0, description="Preço de compra")
    preco_venda: float = Field(0.0, ge=0, description="Preço de venda")
    estoque_minimo: int = Field(0, ge=0, description="Estoque mínimo")
    estoque_atual: int = Field(0, ge=0, description="Estoque atual")
    cor_id: Optional[int] = Field(None, description="ID da cor")
    tipo_id: Optional[int] = Field(None, description="ID do tipo")

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    codigo_barras: Optional[str] = Field(None, max_length=100)
    nome: Optional[str] = Field(None, max_length=200)
    descricao: Optional[str] = None
    preco_compra: Optional[float] = Field(None, ge=0)
    preco_venda: Optional[float] = Field(None, ge=0)
    estoque_minimo: Optional[int] = Field(None, ge=0)
    estoque_atual: Optional[int] = Field(None, ge=0)
    cor_id: Optional[int] = None
    tipo_id: Optional[int] = None
    ativo: Optional[bool] = None

class Produto(ProdutoBase):
    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
    cor: Optional[Cor] = None
    tipo: Optional[Tipo] = None
    
    class Config:
        from_attributes = True

# ====== SCHEMAS PARA MOVIMENTAÇÃO ======
class MovimentacaoBase(BaseModel):
    produto_id: int = Field(..., description="ID do produto")
    tipo_movimentacao: str = Field(..., description="Tipo: entrada, saida, ajuste")
    quantidade: int = Field(..., description="Quantidade movimentada")
    motivo: Optional[str] = Field(None, max_length=200, description="Motivo da movimentação")
    observacao: Optional[str] = Field(None, description="Observações")

class MovimentacaoCreate(MovimentacaoBase):
    pass

class Movimentacao(MovimentacaoBase):
    id: int
    quantidade_anterior: int
    quantidade_atual: int
    created_at: datetime
    produto: Optional[Produto] = None
    
    class Config:
        from_attributes = True

# ====== SCHEMAS PARA USUÁRIO ======
class UsuarioBase(BaseModel):
    email: str = Field(..., max_length=255, description="Email do usuário")
    nome: str = Field(..., max_length=200, description="Nome do usuário")

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, description="Senha do usuário")

class UsuarioUpdate(BaseModel):
    email: Optional[str] = Field(None, max_length=255)
    nome: Optional[str] = Field(None, max_length=200)
    senha: Optional[str] = Field(None, min_length=6)
    ativo: Optional[bool] = None

class Usuario(UsuarioBase):
    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ====== SCHEMAS DE RESPOSTA ======
class Message(BaseModel):
    message: str

class ErrorMessage(BaseModel):
    error: str
    detail: Optional[str] = None

# ====== SCHEMAS PARA RELATÓRIOS ======
class RelatorioEstoque(BaseModel):
    produto_id: int
    codigo_barras: str
    nome: str
    estoque_atual: int
    estoque_minimo: int
    status: str  # "normal", "baixo", "zerado"
    
class RelatorioProduto(BaseModel):
    total_produtos: int
    produtos_ativos: int
    produtos_inativos: int
    estoque_baixo: int
    estoque_zerado: int

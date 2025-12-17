"""
Estoque Engenho - Models do Banco de Dados
"""
from sqlalchemy import (
    Column, Integer, String, Boolean, DECIMAL, Text, 
    DateTime, ForeignKey, Enum, TIMESTAMP
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class TipoMovimento(str, enum.Enum):
    """Tipos de movimentação de estoque"""
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    AJUSTE = "AJUSTE"


class Cor(Base):
    """Model para cores dos produtos"""
    __tablename__ = "cores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    codigo = Column(String(2), nullable=False, unique=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="cor")


class Tipo(Base):
    """Model para tipos/categorias de produtos"""
    __tablename__ = "tipos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codigo = Column(String(2), nullable=False, unique=True)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="tipo")


class Produto(Base):
    """Model para produtos"""
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_produto = Column(String(4), nullable=False, unique=True)
    nome = Column(String(200), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos.id"), nullable=False)
    cor_id = Column(Integer, ForeignKey("cores.id"), nullable=False)
    codigo_barras = Column(String(20), nullable=False, unique=True)
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=5)
    preco_custo = Column(DECIMAL(10, 2))
    preco_venda = Column(DECIMAL(10, 2))
    observacoes = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tipo = relationship("Tipo", back_populates="produtos")
    cor = relationship("Cor", back_populates="produtos")
    movimentacoes = relationship("Movimentacao", back_populates="produto")


class Movimentacao(Base):
    """Model para movimentações de estoque"""
    __tablename__ = "movimentacoes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo_movimento = Column(Enum(TipoMovimento), nullable=False)
    quantidade = Column(Integer, nullable=False)
    estoque_anterior = Column(Integer, nullable=False)
    estoque_atual = Column(Integer, nullable=False)
    observacao = Column(String(255))
    usuario = Column(String(100))
    data_movimento = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="movimentacoes")

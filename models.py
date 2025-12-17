"""
Modelos do banco de dados - Estoque Engenho
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Cor(Base):
    __tablename__ = "cores"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, index=True, nullable=False)
    nome = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com produtos
    produtos = relationship("Produto", back_populates="cor")

class Tipo(Base):
    __tablename__ = "tipos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, index=True, nullable=False)
    nome = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com produtos
    produtos = relationship("Produto", back_populates="tipo")

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String(100), unique=True, index=True, nullable=False)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    preco_compra = Column(Float, nullable=False, default=0.0)
    preco_venda = Column(Float, nullable=False, default=0.0)
    estoque_minimo = Column(Integer, default=0)
    estoque_atual = Column(Integer, default=0)
    
    # Chaves estrangeiras
    cor_id = Column(Integer, ForeignKey("cores.id"), nullable=True)
    tipo_id = Column(Integer, ForeignKey("tipos.id"), nullable=True)
    
    # Campos de controle
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cor = relationship("Cor", back_populates="produtos")
    tipo = relationship("Tipo", back_populates="produtos")
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")

class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo_movimentacao = Column(String(20), nullable=False)  # 'entrada', 'saida', 'ajuste'
    quantidade = Column(Integer, nullable=False)
    quantidade_anterior = Column(Integer, nullable=False)
    quantidade_atual = Column(Integer, nullable=False)
    motivo = Column(String(200), nullable=True)
    observacao = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    produto = relationship("Produto", back_populates="movimentacoes")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(200), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
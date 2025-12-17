"""
Configuração do Banco de Dados - Debug detalhado
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Debug - vamos ver o que está chegando
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/estoque_engenho")

print(f"🔍 DEBUG - DATABASE_URL original: {DATABASE_URL}")
print(f"🔍 DEBUG - Tipo da DATABASE_URL: {type(DATABASE_URL)}")

# Se a URL contém caracteres especiais ou problemas, vamos limpar
if DATABASE_URL and DATABASE_URL != "mysql+pymysql://user:password@localhost:3306/estoque_engenho":
    # Railway às vezes adiciona espaços ou caracteres extras
    DATABASE_URL = DATABASE_URL.strip()
    
    # Se for Railway e não tiver o driver correto
    if "mysql://" in DATABASE_URL and "mysql+pymysql://" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")
        print(f"🔧 CORREÇÃO - URL corrigida: {DATABASE_URL}")
    
    print(f"✅ DATABASE_URL final: {DATABASE_URL}")
else:
    print("⚠️  Usando DATABASE_URL padrão (desenvolvimento)")

# Criar engine com tratamento de erro
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=True  # Vamos ver as queries SQL
    )
    print("✅ Engine criado com sucesso!")
except Exception as e:
    print(f"❌ ERRO ao criar engine: {e}")
    print(f"❌ DATABASE_URL problemática: {DATABASE_URL}")
    # Fallback para desenvolvimento local
    engine = create_engine(
        "mysql+pymysql://root:@localhost:3306/estoque_engenho",
        pool_pre_ping=True,
        pool_recycle=300,
        echo=True
    )

# Criar session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()

def test_connection():
    """Testar conexão com banco"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Conexão com banco estabelecida! Resultado: {row}")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        print(f"❌ URL usada: {DATABASE_URL}")
        return False

def init_db():
    """Inicializar banco com dados padrão"""
    try:
        from models import Cor, Tipo
        
        # Testar conexão primeiro
        if not test_connection():
            print("❌ Não foi possível conectar ao banco, pulando inicialização")
            return
        
        print("🔄 Inicializando dados padrão...")
        db = SessionLocal()
        
        # Cores padrão
        cores_padrao = [
            {"nome": "Preto", "codigo": "01"},
            {"nome": "Branco", "codigo": "02"},
            {"nome": "Azul", "codigo": "03"},
            {"nome": "Vermelho", "codigo": "04"},
            {"nome": "Verde", "codigo": "05"},
        ]
        
        # Inserir cores se não existirem
        for cor_data in cores_padrao:
            cor_existente = db.query(Cor).filter(Cor.codigo == cor_data["codigo"]).first()
            if not cor_existente:
                cor = Cor(**cor_data)
                db.add(cor)
                print(f"➕ Adicionando cor: {cor_data['nome']}")
        
        # Tipos padrão
        tipos_padrao = [
            {"nome": "Blusa", "codigo": "01"},
            {"nome": "Calça", "codigo": "02"},
            {"nome": "Vestido", "codigo": "03"},
        ]
        
        # Inserir tipos se não existirem
        for tipo_data in tipos_padrao:
            tipo_existente = db.query(Tipo).filter(Tipo.codigo == tipo_data["codigo"]).first()
            if not tipo_existente:
                tipo = Tipo(**tipo_data)
                db.add(tipo)
                print(f"➕ Adicionando tipo: {tipo_data['nome']}")
        
        db.commit()
        print("✅ Dados padrão inicializados!")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar dados: {e}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

# Debug na inicialização
print("🚀 Iniciando configuração do banco...")
if __name__ == "__main__":
    test_connection()
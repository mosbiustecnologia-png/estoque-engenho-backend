"""
Configuração do Banco de Dados - Produção
Suporte para MySQL local e Railway
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Configurações do banco
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://user:password@localhost:3306/estoque_engenho"
)

# Se for Railway, a URL já vem formatada
if "railway" in DATABASE_URL or "mysql://" in DATABASE_URL:
    # Railway às vezes usa mysql:// em vez de mysql+pymysql://
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")

# Criar engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexão antes de usar
    pool_recycle=300,    # Reconectar a cada 5 minutos
    echo=False           # Log SQL queries (desabilitado em produção)
)

# Criar session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()

def test_connection():
    """Testar conexão com banco"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco estabelecida!")
            return True
    except OperationalError as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        return False

def init_db():
    """Inicializar banco com dados padrão"""
    from models import Cor, Tipo
    
    try:
        # Verificar se dados já existem
        db = SessionLocal()
        
        # Cores padrão
        cores_padrao = [
            {"nome": "Preto", "codigo": "01"},
            {"nome": "Branco", "codigo": "02"},
            {"nome": "Azul", "codigo": "03"},
            {"nome": "Vermelho", "codigo": "04"},
            {"nome": "Verde", "codigo": "05"},
            {"nome": "Amarelo", "codigo": "06"},
            {"nome": "Rosa", "codigo": "07"},
            {"nome": "Roxo", "codigo": "08"},
            {"nome": "Cinza", "codigo": "09"},
            {"nome": "Marrom", "codigo": "10"}
        ]
        
        # Inserir cores se não existirem
        for cor_data in cores_padrao:
            cor_existente = db.query(Cor).filter(Cor.codigo == cor_data["codigo"]).first()
            if not cor_existente:
                cor = Cor(**cor_data)
                db.add(cor)
        
        # Tipos padrão
        tipos_padrao = [
            {"nome": "Blusa", "codigo": "01"},
            {"nome": "Calça", "codigo": "02"},
            {"nome": "Vestido", "codigo": "03"},
            {"nome": "Saia", "codigo": "04"},
            {"nome": "Shorts", "codigo": "05"},
            {"nome": "Casaco", "codigo": "06"},
            {"nome": "Cropped", "codigo": "07"},
            {"nome": "Conjunto", "codigo": "08"},
            {"nome": "Acessório", "codigo": "09"},
            {"nome": "Lingerie", "codigo": "10"}
        ]
        
        # Inserir tipos se não existirem
        for tipo_data in tipos_padrao:
            tipo_existente = db.query(Tipo).filter(Tipo.codigo == tipo_data["codigo"]).first()
            if not tipo_existente:
                tipo = Tipo(**tipo_data)
                db.add(tipo)
        
        db.commit()
        print("✅ Dados padrão inicializados!")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar dados: {e}")
        db.rollback()
    finally:
        db.close()

# Teste de conexão na inicialização
if __name__ == "__main__":
    test_connection()
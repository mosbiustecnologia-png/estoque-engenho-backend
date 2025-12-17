"""
Estoque Engenho - API Principal
Sistema de controle de estoque com códigos de barras
"""
import os
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

# Importar módulos locais
from database import SessionLocal, engine, init_db
from models import Base
from schemas import *
#from crud import *
from utils.barcode_generator import gerar_codigo_barras, gerar_etiqueta_pdf
from utils.qr_generator import gerar_qr_code

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

# Inicializar dados padrão
init_db()

# Criar app FastAPI
app = FastAPI(
    title="Estoque Engenho API",
    description="Sistema de controle de estoque com códigos de barras",
    version="1.0.0"
)

# Configurar CORS para permitir acesso do app mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretório para arquivos estáticos
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependência para sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================================
# ENDPOINTS DE SAÚDE E INFO
# ================================

@app.get("/")
async def root():
    return {"message": "Estoque Engenho API - Funcionando! 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "estoque-engenho"}

# ================================
# ENDPOINTS DE PRODUTOS
# ================================

@app.post("/produtos/", response_model=ProdutoResponse)
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Criar novo produto com código de barras automático"""
    return criar_produto_db(db, produto)

@app.get("/produtos/", response_model=List[ProdutoResponse])
async def listar_produtos(
    skip: int = 0, 
    limit: int = 100, 
    busca: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar todos os produtos com filtro opcional"""
    if busca:
        return buscar_produtos_db(db, busca)
    return listar_produtos_db(db, skip=skip, limit=limit)

@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Obter produto por ID"""
    produto = obter_produto_db(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.get("/produtos/codigo/{codigo_barras}", response_model=ProdutoResponse)
async def obter_produto_por_codigo(codigo_barras: str, db: Session = Depends(get_db)):
    """Obter produto por código de barras"""
    produto = obter_produto_por_codigo_db(db, codigo_barras)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/produtos/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(
    produto_id: int, 
    produto: ProdutoUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar produto"""
    produto_atualizado = atualizar_produto_db(db, produto_id, produto)
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto_atualizado

@app.delete("/produtos/{produto_id}")
async def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Deletar produto"""
    if not deletar_produto_db(db, produto_id):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}

# ================================
# ENDPOINTS DE MOVIMENTAÇÕES
# ================================

@app.post("/movimentacoes/", response_model=MovimentacaoResponse)
async def criar_movimentacao(
    movimentacao: MovimentacaoCreate, 
    db: Session = Depends(get_db)
):
    """Criar nova movimentação (entrada/saída)"""
    return criar_movimentacao_db(db, movimentacao)

@app.post("/movimentacoes/entrada/")
async def entrada_estoque(
    entrada: EntradaEstoque,
    db: Session = Depends(get_db)
):
    """Dar entrada no estoque via código de barras"""
    produto = obter_produto_por_codigo_db(db, entrada.codigo_barras)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    movimentacao = MovimentacaoCreate(
        produto_id=produto.id,
        tipo_movimento="entrada",
        quantidade=entrada.quantidade,
        observacao=entrada.observacao or f"Entrada via scanner - {entrada.quantidade} unidades"
    )
    
    return criar_movimentacao_db(db, movimentacao)

@app.post("/movimentacoes/saida/")
async def saida_estoque(
    saida: SaidaEstoque,
    db: Session = Depends(get_db)
):
    """Dar saída do estoque via código de barras"""
    produto = obter_produto_por_codigo_db(db, saida.codigo_barras)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if produto.estoque_atual < saida.quantidade:
        raise HTTPException(
            status_code=400, 
            detail=f"Estoque insuficiente. Disponível: {produto.estoque_atual}"
        )
    
    movimentacao = MovimentacaoCreate(
        produto_id=produto.id,
        tipo_movimento="saida",
        quantidade=saida.quantidade,
        observacao=saida.observacao or f"Saída via scanner - {saida.quantidade} unidades"
    )
    
    return criar_movimentacao_db(db, movimentacao)

@app.get("/movimentacoes/", response_model=List[MovimentacaoResponse])
async def listar_movimentacoes(
    skip: int = 0, 
    limit: int = 100,
    produto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar movimentações com filtro opcional por produto"""
    return listar_movimentacoes_db(db, skip=skip, limit=limit, produto_id=produto_id)

# ================================
# ENDPOINTS DE CÓDIGOS DE BARRAS
# ================================

@app.get("/produtos/{produto_id}/codigo-barras")
async def gerar_codigo_barras_produto(produto_id: int, db: Session = Depends(get_db)):
    """Gerar imagem do código de barras do produto"""
    produto = obter_produto_db(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Gerar código de barras
    imagem_path = gerar_codigo_barras(produto.codigo_barras)
    return FileResponse(imagem_path, media_type="image/png")

@app.get("/produtos/{produto_id}/etiqueta")
async def gerar_etiqueta_produto(produto_id: int, db: Session = Depends(get_db)):
    """Gerar etiqueta PDF para impressão"""
    produto = obter_produto_db(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Gerar etiqueta PDF
    pdf_path = gerar_etiqueta_pdf(produto)
    return FileResponse(
        pdf_path, 
        media_type="application/pdf",
        filename=f"etiqueta_{produto.codigo_barras}.pdf"
    )

@app.get("/produtos/{produto_id}/qr-code")
async def gerar_qr_code_produto(produto_id: int, db: Session = Depends(get_db)):
    """Gerar QR Code do produto"""
    produto = obter_produto_db(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Gerar QR Code
    imagem_path = gerar_qr_code(produto.codigo_barras)
    return FileResponse(imagem_path, media_type="image/png")

# ================================
# ENDPOINTS DE RELATÓRIOS
# ================================

@app.get("/relatorios/estoque-baixo")
async def produtos_estoque_baixo(limite: int = 5, db: Session = Depends(get_db)):
    """Listar produtos com estoque baixo"""
    return produtos_estoque_baixo_db(db, limite)

@app.get("/relatorios/dashboard")
async def dashboard(db: Session = Depends(get_db)):
    """Dashboard com resumo do estoque"""
    return obter_dashboard_db(db)

# ================================
# ENDPOINTS AUXILIARES
# ================================

@app.get("/cores/", response_model=List[CorResponse])
async def listar_cores(db: Session = Depends(get_db)):
    """Listar todas as cores disponíveis"""
    return listar_cores_db(db)

@app.get("/tipos/", response_model=List[TipoResponse])
async def listar_tipos(db: Session = Depends(get_db)):
    """Listar todos os tipos disponíveis"""
    return listar_tipos_db(db)

# ================================
# CONFIGURAÇÃO PARA PRODUÇÃO
# ================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=False
    )
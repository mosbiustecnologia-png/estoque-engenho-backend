"""
Estoque Engenho - Rotas de Produtos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional
from app.database import get_db
from app.models import Produto, Tipo, Cor, Movimentacao, TipoMovimento
from app.schemas import (
    ProdutoCreate, ProdutoUpdate, ProdutoResponse,
    ProdutoListResponse, BarcodeResponse
)
from app.services.barcode_service import barcode_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: Optional[bool] = None,
    tipo_id: Optional[int] = None,
    cor_id: Optional[int] = None,
    busca: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista produtos com filtros e paginação"""
    query = db.query(Produto)
    
    # Filtros
    if ativo is not None:
        query = query.filter(Produto.ativo == ativo)
    
    if tipo_id:
        query = query.filter(Produto.tipo_id == tipo_id)
    
    if cor_id:
        query = query.filter(Produto.cor_id == cor_id)
    
    if busca:
        query = query.filter(
            or_(
                Produto.nome.ilike(f"%{busca}%"),
                Produto.codigo_barras.ilike(f"%{busca}%")
            )
        )
    
    # Ordenação e paginação
    produtos = query.order_by(desc(Produto.created_at)).offset(skip).limit(limit).all()
    
    return produtos


@router.get("/baixo-estoque", response_model=List[ProdutoResponse])
def listar_produtos_baixo_estoque(db: Session = Depends(get_db)):
    """Lista produtos com estoque abaixo do mínimo"""
    produtos = db.query(Produto).filter(
        Produto.estoque_atual <= Produto.estoque_minimo,
        Produto.ativo == True
    ).all()
    
    return produtos


@router.get("/codigo-barras/{codigo_barras}", response_model=ProdutoResponse)
def buscar_por_codigo_barras(codigo_barras: str, db: Session = Depends(get_db)):
    """Busca produto pelo código de barras"""
    produto = db.query(Produto).filter(
        Produto.codigo_barras == codigo_barras
    ).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    return produto


@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Obtém um produto específico"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    return produto


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto_data: ProdutoCreate, db: Session = Depends(get_db)):
    """Cria um novo produto e gera código de barras automaticamente"""
    
    # Valida se tipo existe
    tipo = db.query(Tipo).filter(Tipo.id == produto_data.tipo_id).first()
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo não encontrado"
        )
    
    # Valida se cor existe
    cor = db.query(Cor).filter(Cor.id == produto_data.cor_id).first()
    if not cor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cor não encontrada"
        )
    
    # Gera próximo código de produto
    ultimo_produto = db.query(Produto).order_by(desc(Produto.id)).first()
    if ultimo_produto:
        codigo_produto = barcode_service.gerar_proximo_codigo_produto(
            ultimo_produto.codigo_produto
        )
    else:
        codigo_produto = "0001"
    
    # Gera código de barras
    codigo_barras = barcode_service.gerar_codigo_barras(
        codigo_produto,
        tipo.codigo,
        cor.codigo
    )
    
    # Verifica se código de barras já existe (não deveria, mas precaução)
    if db.query(Produto).filter(Produto.codigo_barras == codigo_barras).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de barras já existe"
        )
    
    # Cria produto
    produto_dict = produto_data.model_dump(exclude={'estoque_inicial'})
    novo_produto = Produto(
        **produto_dict,
        codigo_produto=codigo_produto,
        codigo_barras=codigo_barras,
        estoque_atual=produto_data.estoque_inicial
    )
    
    db.add(novo_produto)
    db.flush()  # Para obter o ID antes do commit
    
    # Registra movimentação inicial se houver estoque
    if produto_data.estoque_inicial > 0:
        movimentacao = Movimentacao(
            produto_id=novo_produto.id,
            tipo_movimento=TipoMovimento.ENTRADA,
            quantidade=produto_data.estoque_inicial,
            estoque_anterior=0,
            estoque_atual=produto_data.estoque_inicial,
            observacao="Estoque inicial",
            usuario="Sistema"
        )
        db.add(movimentacao)
    
    db.commit()
    db.refresh(novo_produto)
    
    return novo_produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um produto"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    # Valida tipo se foi alterado
    if produto_data.tipo_id:
        tipo = db.query(Tipo).filter(Tipo.id == produto_data.tipo_id).first()
        if not tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo não encontrado"
            )
    
    # Valida cor se foi alterada
    if produto_data.cor_id:
        cor = db.query(Cor).filter(Cor.id == produto_data.cor_id).first()
        if not cor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cor não encontrada"
            )
    
    # Atualiza apenas os campos fornecidos
    update_data = produto_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(produto, field, value)
    
    db.commit()
    db.refresh(produto)
    
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Desativa um produto (soft delete)"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    produto.ativo = False
    db.commit()
    
    return None

@router.get("/{produto_id}/etiqueta")
def gerar_etiqueta(produto_id: int, db: Session = Depends(get_db)):
    """Gera etiqueta completa do produto para impressão - RETORNA IMAGEM"""
    from fastapi.responses import Response
    import base64
    
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    image_base64 = barcode_service.gerar_etiqueta_produto(
        codigo_barras=produto.codigo_barras,
        nome_produto=produto.nome,
        tipo_nome=produto.tipo.nome,
        cor_nome=produto.cor.nome,
        preco=float(produto.preco_venda) if produto.preco_venda else None
    )
    
    # Decodifica base64 e retorna como imagem PNG
    image_bytes = base64.b64decode(image_base64)
    
    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=etiqueta_{produto_id}.png"
        }
    )

@router.post("/etiquetas-pdf")
def gerar_pdf_etiquetas(
    produto_ids: list[int],
    db: Session = Depends(get_db)
):
    """Gera PDF com múltiplas etiquetas"""
    from fastapi.responses import Response
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from io import BytesIO
    import base64
    
    # Busca produtos
    produtos = db.query(Produto).filter(Produto.id.in_(produto_ids)).all()
    
    if not produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum produto encontrado"
        )
    
    # Cria PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Configuração: 2 etiquetas por linha, 4 por página
    etiqueta_width = (width - 60) / 2
    etiqueta_height = 150
    
    x_start = 30
    y_start = height - 180
    
    x = x_start
    y = y_start
    count = 0
    
    for produto in produtos:
        # Gera etiqueta
        image_base64 = barcode_service.gerar_etiqueta_produto(
            codigo_barras=produto.codigo_barras,
            nome_produto=produto.nome,
            tipo_nome=produto.tipo.nome,
            cor_nome=produto.cor.nome,
            preco=float(produto.preco_venda) if produto.preco_venda else None
        )
        
        # Decodifica imagem
        image_data = base64.b64decode(image_base64)
        img = ImageReader(BytesIO(image_data))
        
        # Adiciona ao PDF
        c.drawImage(img, x, y, width=etiqueta_width, height=etiqueta_height)
        
        # Próxima posição
        count += 1
        if count % 2 == 0:  # A cada 2 etiquetas, desce
            x = x_start
            y -= etiqueta_height + 20
        else:  # Vai para a direita
            x += etiqueta_width + 30
        
        # Nova página a cada 4 etiquetas
        if count % 4 == 0:
            c.showPage()
            x = x_start
            y = y_start
    
    c.save()
    
    # Retorna PDF
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=etiquetas_{len(produtos)}_produtos.pdf"
        }
    )

@router.get("/{produto_id}/barcode", response_model=BarcodeResponse)
def gerar_codigo_barras_imagem(
    produto_id: int,
    formato: str = Query("code128", regex="^(code128|qrcode)$"),
    db: Session = Depends(get_db)
):
    """Gera imagem do código de barras do produto"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    if formato == "qrcode":
        image_base64 = barcode_service.gerar_imagem_qrcode(produto.codigo_barras)
    else:
        image_base64 = barcode_service.gerar_imagem_code128(produto.codigo_barras)
    
    return BarcodeResponse(
        codigo_barras=produto.codigo_barras,
        formato=formato,
        image_base64=image_base64
    )


@router.get("/{produto_id}/etiqueta")
def gerar_etiqueta(produto_id: int, db: Session = Depends(get_db)):
    """Gera etiqueta completa do produto para impressão"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    image_base64 = barcode_service.gerar_etiqueta_produto(
        codigo_barras=produto.codigo_barras,
        nome_produto=produto.nome,
        tipo_nome=produto.tipo.nome,
        cor_nome=produto.cor.nome,
        preco=float(produto.preco_venda) if produto.preco_venda else None
    )
    
    return {
        "produto_id": produto.id,
        "nome": produto.nome,
        "codigo_barras": produto.codigo_barras,
        "etiqueta_base64": image_base64
    }

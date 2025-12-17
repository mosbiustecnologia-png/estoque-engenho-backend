"""
Estoque Engenho - Serviço de Código de Barras
"""
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont


class BarcodeService:
    """Serviço para gerar códigos de barras"""
    
    @staticmethod
    def gerar_codigo_barras(
        codigo_produto: str, 
        tipo_codigo: str, 
        cor_codigo: str
    ) -> str:
        """
        Gera código de barras no formato: PPPPTTCC
        
        Args:
            codigo_produto: Código do produto (4 dígitos)
            tipo_codigo: Código do tipo (2 dígitos)
            cor_codigo: Código da cor (2 dígitos)
            
        Returns:
            Código de barras gerado (8 dígitos)
        """
        return f"{codigo_produto}{tipo_codigo}{cor_codigo}"
    
    @staticmethod
    def gerar_proximo_codigo_produto(ultimo_codigo: str = "0000") -> str:
        """
        Gera o próximo código de produto sequencial
        
        Args:
            ultimo_codigo: Último código utilizado
            
        Returns:
            Próximo código (4 dígitos)
        """
        numero = int(ultimo_codigo) + 1
        return f"{numero:04d}"
    
    @staticmethod
    def gerar_imagem_code128(codigo: str, with_text: bool = True) -> str:
        """
        Gera imagem do código de barras Code128
        
        Args:
            codigo: Código a ser convertido em barcode
            with_text: Se deve mostrar o texto abaixo do código
            
        Returns:
            Imagem em base64
        """
        # Cria o código de barras
        CODE128 = barcode.get_barcode_class('code128')
        code_instance = CODE128(codigo, writer=ImageWriter())
        
        # Gera a imagem em memória
        buffer = BytesIO()
        code_instance.write(
            buffer,
            options={
                'write_text': with_text,
                'text_distance': 5,
                'module_height': 15,
                'module_width': 0.3,
                'font_size': 10,
                'quiet_zone': 6.5
            }
        )
        
        # Converte para base64
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return image_base64
    
    @staticmethod
    def gerar_imagem_qrcode(codigo: str, size: int = 200) -> str:
        """
        Gera imagem QR Code
        
        Args:
            codigo: Código a ser convertido em QR Code
            size: Tamanho da imagem em pixels
            
        Returns:
            Imagem em base64
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(codigo)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))
        
        # Converte para base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return image_base64
    
    @staticmethod
    def gerar_etiqueta_produto(
        codigo_barras: str,
        nome_produto: str,
        tipo_nome: str,
        cor_nome: str,
        preco: float = None
    ) -> str:
        """
        Gera etiqueta completa com código de barras e informações do produto
        
        Args:
            codigo_barras: Código de barras
            nome_produto: Nome do produto
            tipo_nome: Nome do tipo/categoria
            cor_nome: Nome da cor
            preco: Preço (opcional)
            
        Returns:
            Imagem da etiqueta em base64
        """
        # Cria imagem base
        width, height = 400, 250
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            # Tenta carregar fonte do sistema
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            font_info = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            font_price = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            # Fallback para fonte padrão
            font_title = ImageFont.load_default()
            font_info = ImageFont.load_default()
            font_price = ImageFont.load_default()
        
        # Adiciona nome do produto
        y_position = 10
        draw.text((10, y_position), nome_produto[:30], fill='black', font=font_title)
        
        # Adiciona tipo e cor
        y_position += 25
        draw.text((10, y_position), f"{tipo_nome} - {cor_nome}", fill='black', font=font_info)
        
        # Adiciona preço se fornecido
        if preco:
            y_position += 25
            draw.text((10, y_position), f"R$ {preco:.2f}", fill='black', font=font_price)
        
        # Gera código de barras
        CODE128 = barcode.get_barcode_class('code128')
        code_instance = CODE128(codigo_barras, writer=ImageWriter())
        
        barcode_buffer = BytesIO()
        code_instance.write(
            barcode_buffer,
            options={
                'write_text': True,
                'text_distance': 3,
                'module_height': 10,
                'module_width': 0.25,
                'font_size': 8,
                'quiet_zone': 3
            }
        )
        
        # Adiciona código de barras na etiqueta
        barcode_buffer.seek(0)
        barcode_img = Image.open(barcode_buffer)
        barcode_img = barcode_img.resize((350, 100))
        
        img.paste(barcode_img, (25, 120))
        
        # Converte para base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return image_base64


# Instância global do serviço
barcode_service = BarcodeService()

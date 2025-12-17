-- Estoque Engenho - Schema do Banco de Dados
-- Database: estoque_engenho

CREATE DATABASE IF NOT EXISTS estoque_engenho;
USE estoque_engenho;

-- Tabela de Cores
CREATE TABLE cores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    codigo CHAR(2) NOT NULL UNIQUE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Tipos/Categorias
CREATE TABLE tipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo CHAR(2) NOT NULL UNIQUE,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_produto CHAR(4) NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    tipo_id INT NOT NULL,
    cor_id INT NOT NULL,
    codigo_barras VARCHAR(20) NOT NULL UNIQUE,
    estoque_atual INT DEFAULT 0,
    estoque_minimo INT DEFAULT 5,
    preco_custo DECIMAL(10, 2),
    preco_venda DECIMAL(10, 2),
    observacoes TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_id) REFERENCES tipos(id),
    FOREIGN KEY (cor_id) REFERENCES cores(id),
    INDEX idx_codigo_barras (codigo_barras),
    INDEX idx_estoque (estoque_atual)
);

-- Tabela de Movimentações
CREATE TABLE movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    tipo_movimento ENUM('ENTRADA', 'SAIDA', 'AJUSTE') NOT NULL,
    quantidade INT NOT NULL,
    estoque_anterior INT NOT NULL,
    estoque_atual INT NOT NULL,
    observacao VARCHAR(255),
    usuario VARCHAR(100),
    data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    INDEX idx_produto (produto_id),
    INDEX idx_data (data_movimento),
    INDEX idx_tipo (tipo_movimento)
);

-- Inserir cores padrão
INSERT INTO cores (nome, codigo) VALUES
('Preto', '01'),
('Branco', '02'),
('Vermelho', '03'),
('Azul', '04'),
('Verde', '05'),
('Amarelo', '06'),
('Rosa', '07'),
('Roxo', '08'),
('Laranja', '09'),
('Marrom', '10'),
('Cinza', '11'),
('Bege', '12'),
('Nude', '13'),
('Estampado', '99');

-- Inserir tipos padrão (exemplo para loja de roupas)
INSERT INTO tipos (nome, codigo, descricao) VALUES
('Blusa', '01', 'Blusas e camisetas'),
('Calça', '02', 'Calças e leggings'),
('Vestido', '03', 'Vestidos'),
('Saia', '04', 'Saias'),
('Short', '05', 'Shorts'),
('Conjunto', '06', 'Conjuntos'),
('Casaco', '07', 'Casacos e jaquetas'),
('Macacão', '08', 'Macacões'),
('Cropped', '09', 'Croppeds'),
('Body', '10', 'Bodies');

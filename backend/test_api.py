#!/usr/bin/env python3
"""
Estoque Engenho - Script de Teste
Testa os principais endpoints da API
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_health():
    print_section("1. Testando Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_create_produto():
    print_section("2. Criando Produto")
    
    produto = {
        "nome": "Blusa Manga Longa Preta",
        "tipo_id": 1,  # Blusa
        "cor_id": 1,   # Preto
        "estoque_inicial": 20,
        "estoque_minimo": 5,
        "preco_custo": 25.00,
        "preco_venda": 59.90,
        "observacoes": "Produto teste"
    }
    
    response = requests.post(f"{BASE_URL}/produtos", json=produto)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Produto criado com sucesso!")
        print(f"   ID: {data['id']}")
        print(f"   Nome: {data['nome']}")
        print(f"   Código de Barras: {data['codigo_barras']}")
        print(f"   Estoque: {data['estoque_atual']}")
        return data
    else:
        print(f"❌ Erro: {response.text}")
        return None


def test_list_produtos():
    print_section("3. Listando Produtos")
    response = requests.get(f"{BASE_URL}/produtos")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        produtos = response.json()
        print(f"Total de produtos: {len(produtos)}")
        for p in produtos[:3]:  # Mostra os 3 primeiros
            print(f"  - {p['nome']} | Código: {p['codigo_barras']} | Estoque: {p['estoque_atual']}")


def test_buscar_por_codigo(codigo_barras):
    print_section("4. Buscando Produto por Código de Barras")
    response = requests.get(f"{BASE_URL}/produtos/codigo-barras/{codigo_barras}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        produto = response.json()
        print(f"✅ Produto encontrado:")
        print(f"   Nome: {produto['nome']}")
        print(f"   Tipo: {produto['tipo']['nome']}")
        print(f"   Cor: {produto['cor']['nome']}")
        print(f"   Estoque: {produto['estoque_atual']}")


def test_entrada_estoque(codigo_barras):
    print_section("5. Dando Entrada no Estoque")
    
    movimentacao = {
        "codigo_barras": codigo_barras,
        "tipo_movimento": "ENTRADA",
        "quantidade": 15,
        "observacao": "Chegou do fornecedor",
        "usuario": "Teste Script"
    }
    
    response = requests.post(f"{BASE_URL}/movimentacoes/entrada", json=movimentacao)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Entrada registrada!")
        print(f"   Quantidade: {data['quantidade']}")
        print(f"   Estoque Anterior: {data['estoque_anterior']}")
        print(f"   Estoque Atual: {data['estoque_atual']}")


def test_saida_estoque(codigo_barras):
    print_section("6. Dando Saída no Estoque")
    
    movimentacao = {
        "codigo_barras": codigo_barras,
        "tipo_movimento": "SAIDA",
        "quantidade": 5,
        "observacao": "Venda realizada",
        "usuario": "Teste Script"
    }
    
    response = requests.post(f"{BASE_URL}/movimentacoes/saida", json=movimentacao)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Saída registrada!")
        print(f"   Quantidade: {data['quantidade']}")
        print(f"   Estoque Anterior: {data['estoque_anterior']}")
        print(f"   Estoque Atual: {data['estoque_atual']}")


def test_listar_cores():
    print_section("7. Listando Cores Disponíveis")
    response = requests.get(f"{BASE_URL}/cores")
    
    if response.status_code == 200:
        cores = response.json()
        print(f"Total de cores: {len(cores)}")
        for cor in cores[:5]:
            print(f"  {cor['codigo']} - {cor['nome']}")


def test_listar_tipos():
    print_section("8. Listando Tipos Disponíveis")
    response = requests.get(f"{BASE_URL}/tipos")
    
    if response.status_code == 200:
        tipos = response.json()
        print(f"Total de tipos: {len(tipos)}")
        for tipo in tipos[:5]:
            print(f"  {tipo['codigo']} - {tipo['nome']}")


def main():
    print("\n🏭 ESTOQUE ENGENHO - TESTE DA API")
    print("=" * 60)
    
    try:
        # 1. Health Check
        test_health()
        sleep(1)
        
        # 2. Listar cores e tipos disponíveis
        test_listar_cores()
        sleep(1)
        test_listar_tipos()
        sleep(1)
        
        # 3. Criar produto
        produto = test_create_produto()
        if not produto:
            print("\n❌ Não foi possível criar produto. Verifique se a API está rodando.")
            return
        
        codigo_barras = produto['codigo_barras']
        sleep(1)
        
        # 4. Listar produtos
        test_list_produtos()
        sleep(1)
        
        # 5. Buscar por código
        test_buscar_por_codigo(codigo_barras)
        sleep(1)
        
        # 6. Entrada de estoque
        test_entrada_estoque(codigo_barras)
        sleep(1)
        
        # 7. Saída de estoque
        test_saida_estoque(codigo_barras)
        
        print_section("✅ Testes Concluídos!")
        print(f"Acesse a documentação completa em: {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        print("\nPara iniciar a API:")
        print("  docker-compose up -d")
        print("  ou")
        print("  python main.py")


if __name__ == "__main__":
    main()

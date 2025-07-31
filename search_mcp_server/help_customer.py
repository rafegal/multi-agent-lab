import requests

from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Product-Tools")


@mcp.tool()
def search_products_by_terms(terms: str):
    """
    Retorna uma lista de produtos disponíveis com base nos termos de pesquisa fornecidos.
    Irá retornar os produtos mais relevantes encontrados no MeiliSearch.
    Deve-se usar termos apropriados para melhor acurácia, dentro do Meilisearch temos o nome do produto,
    a categoria e a descrição, então quando melhor os termos forem ajustados, melhor acurácia a busca terá.
    """
    
    headers = {
        "Authorization": f"Bearer <password>",
        "Content-Type": "application/json"
    }
    with open("log/search_product_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: Searching for products with terms: {terms}\n")
    response = requests.post(f"http://127.0.0.1:7700/indexes/products/search", headers=headers, json={"q": terms, "limit": 10})
    return response.json()

@mcp.tool()
def get_payment_plans_available():
    """
    Retorna os planos de pagamento disponíveis.
    Irá retornar um dicionário com uma lista de planos, onde é possível ver:
       - nome do plano
       - porcentagem de juros
       - meses de parcelamento
    """
    with open("log/payment_plans_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: Searching for payment plans\n")
    payment_terms = {
        "plans": [
            {"name": "Parcelamento 3x", "fees": "0%", "months": 3},
            {"name": "Parcelamento 6x", "fees": "3%", "months": 6},
            {"name": "Parcelamento 9x", "fees": "5%", "months": 9},
            {"name": "Parcelamento 12x", "fees": "7%", "months": 12},
        ]
    }
    return payment_terms

if __name__ == "__main__":
    mcp.run()

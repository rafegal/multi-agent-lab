# Multi-Agent Lab 🤖

## 📚 Propósito Educacional

Este projeto foi desenvolvido exclusivamente para **fins educacionais e demonstrativos**, com o objetivo de ilustrar os conceitos fundamentais de sistemas multi-agentes usando o Google ADK (Agent Development Kit). 

**⚠️ IMPORTANTE**: Este NÃO é um exemplo para produção! É um laboratório didático para entender:
- Como implementar arquiteturas hierárquicas de agentes
- Integração entre agentes especializados
- Uso do protocolo MCP (Model Context Protocol)
- Execução de ferramentas (tools) por agentes de IA
- Coordenação entre múltiplos modelos de linguagem

## 🏗️ Arquitetura do Sistema

### Visão Geral
O sistema simula um e-commerce com consultoria de saúde, onde diferentes agentes especializados trabalham em conjunto para atender o cliente.

```
Root Agent (Coordenador Principal)
├── Shop Mate (Especialista em Produtos)
│   └── Help Customer (Interface MCP)
├── Seller Agent (Especialista em Vendas)
│   ├── Create Order (Criação de Pedidos)
│   ├── Billing (Faturamento)
│   └── Manage Stock (Gestão de Estoque)
└── Health Mate (Consultor de Saúde)
    ├── Nutra Specialist (Especialista em Nutrição/Pele)
    └── Workout Specialist (Especialista em Exercícios)
```

## 🧩 Componentes Implementados

### 1. **Vitra AI** (Sistema Principal)
- **Root Agent**: Coordenador principal que delega tarefas aos sub-agentes
- **Prompts especializados**: Instruções específicas para cada agente
- **Modelos variados**: Gemini, Claude, e Llama via LiteLLM

### 2. **Search MCP Server** (Servidor de Ferramentas)
- **Busca de produtos**: Interface com sistema de busca (MeiliSearch)
- **Planos de pagamento**: Simulação de opções de financiamento
- **Logging**: Registro de todas as operações para auditoria

### 3. **Sub-Agentes Especializados**

#### Shop Mate
- **Função**: Recomendação e busca de produtos
- **Ferramentas**: Acesso ao MCP server para consultas
- **Modelo**: Claude 3.5 Sonnet

#### Seller Agent
- **Função**: Processamento completo de pedidos
- **Sub-agentes**:
  - **Create Order**: Criação e gestão de pedidos
  - **Billing**: Geração de faturas
  - **Manage Stock**: Controle de estoque
- **Ferramentas**: Funções customizadas de e-commerce

#### Health Mate
- **Função**: Consultoria de saúde e bem-estar
- **Sub-agentes**:
  - **Nutra Specialist**: Cuidados com a pele e nutrição
  - **Workout Specialist**: Dicas de exercícios e treinos
- **Modelos**: Gemini 2.5 Flash e Llama 3.1 8B

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.13+
- UV (gerenciador de pacotes Python)
- MeiliSearch rodando na porta 7700 (opcional - veja alternativas abaixo)

### 1. Instalação das Dependências

```bash
# Clone o repositório
git clone <seu-repositorio>
cd multi_agent_lab

# Instalar dependências do sistema principal
cd vitra_ai
uv sync

# Instalar dependências do servidor MCP
cd ../search_mcp_server
uv sync
```

### 2. Configuração dos Modelos

Certifique-se de ter as chaves de API configuradas:
```bash
# Para Claude (Anthropic)
export ANTHROPIC_API_KEY="sua_chave_aqui"

# Para Gemini (Google)
export GOOGLE_API_KEY="sua_chave_aqui"

# Para Ollama (local)
# Instale o Ollama e baixe o modelo llama3.1:8b
ollama pull llama3.1:8b
```

### 3. Executando o Sistema

#### Opção 1: Com MeiliSearch (Completo)
```bash
# Terminal 1: Iniciar MeiliSearch
docker run -it --rm -p 7700:7700 getmeili/meilisearch:v1.5

# Terminal 2: Executar o servidor MCP
cd search_mcp_server
uv run help_customer.py

# Terminal 3: Executar o sistema principal
cd vitra_ai
uv run agent.py
```

#### Opção 2: Sem MeiliSearch (Simulado)
```bash
# Apenas o sistema principal (com dados mockados)
cd vitra_ai
uv run agent.py
```

### 4. Testando com ADK Web Interface

Para testar o sistema usando a interface web do ADK:

```bash
# 1. Primeiro, instale as dependências
cd vitra_ai
uv sync

# 2. Ative o ambiente virtual
source .venv/bin/activate

# 3. Volte para a pasta raiz do projeto
cd ..

# 4. Execute o ADK web (deve ser executado um nível acima da pasta do projeto)
adk web
```

**Importante**: O comando `adk web` deve sempre ser executado em uma pasta que seja pai da pasta do projeto, não dentro da pasta do projeto em si.

## 🔧 Personalizando o Servidor MCP

### Alternativas ao MeiliSearch

O arquivo `search_mcp_server/help_customer.py` pode ser facilmente modificado para usar outras fontes de dados:

#### 1. **Arquivo JSON Local**
```python
import json

@mcp.tool()
def search_products_by_terms(terms: str):
    with open("products.json", "r") as f:
        products = json.load(f)
    # Implementar busca simples por termo
    results = [p for p in products if terms.lower() in p['name'].lower()]
    return {"hits": results}
```

#### 2. **API REST Externa**
```python
@mcp.tool()
def search_products_by_terms(terms: str):
    # Exemplo com uma API de produtos
    response = requests.get(f"https://api.mercadolibre.com/sites/MLB/search?q={terms}")
    return response.json()
```

#### 3. **Banco de Dados SQLite**
```python
import sqlite3

@mcp.tool()
def search_products_by_terms(terms: str):
    conn = sqlite3.connect("products.db")
    cursor = conn.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{terms}%",))
    results = cursor.fetchall()
    conn.close()
    return {"hits": results}
```

#### 4. **Elasticsearch**
```python
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@mcp.tool()
def search_products_by_terms(terms: str):
    response = es.search(
        index="products",
        body={"query": {"match": {"name": terms}}}
    )
    return response
```

## 📁 Estrutura do Projeto

```
multi_agent_lab/
├── vitra_ai/                    # Sistema principal de agentes
│   ├── agent.py                 # Configuração do agente raiz
│   ├── prompt.py                # Prompts e instruções
│   ├── sub_agents/              # Agentes especializados
│   │   ├── shop_mate/           # Especialista em produtos
│   │   ├── seller/              # Especialista em vendas
│   │   └── health_mate/         # Consultor de saúde
│   ├── vitra_doc/               # Logs do sistema
│   └── pyproject.toml           # Dependências
├── search_mcp_server/           # Servidor de ferramentas MCP
│   ├── help_customer.py         # Implementação das tools
│   ├── log/                     # Logs das operações
│   └── pyproject.toml           # Dependências
└── README.md                    # Este arquivo
```

## 🎯 Conceitos Demonstrados

### 1. **Hierarquia de Agentes**
- Como organizar agentes em uma estrutura hierárquica
- Delegação de tarefas entre agentes especializados
- Coordenação de múltiplos sub-sistemas

### 2. **Protocolo MCP**
- Implementação de ferramentas externas
- Comunicação entre agentes e serviços
- Logging e auditoria de operações

### 3. **Integração Multi-Modelo**
- Uso simultâneo de diferentes LLMs
- Especialização por tipo de tarefa
- Configuração de parâmetros por agente

### 4. **Ferramentas Customizadas**
- Criação de tools específicas do domínio
- Persistência de dados em arquivos
- Simulação de sistemas externos

## 🧪 Experimentação e Aprendizado

### Sugestões de Modificações

1. **Adicionar novos agentes**: Crie um agente de atendimento ao cliente
2. **Implementar novas ferramentas**: Adicione integração com APIs reais
3. **Experimentar modelos**: Teste outros LLMs ou ajuste parâmetros
4. **Melhorar logging**: Implemente logging estruturado com JSON
5. **Adicionar validação**: Implemente validação de dados entre agentes

### Pontos de Atenção

- **Hardcoded paths**: Os caminhos estão fixos, adapte para seu ambiente
- **Autenticação**: Tokens estão expostos para fins didáticos
- **Error handling**: Implementação mínima, adequada apenas para demonstração
- **Performance**: Não otimizado para produção

## 📖 Recursos Adicionais

- [Google ADK Documentation](https://developers.google.com/agent-development-kit)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [LiteLLM Documentation](https://docs.litellm.ai/)

## 🤝 Contribuições

Este é um projeto educacional! Sinta-se à vontade para:
- Fazer fork e experimentar
- Sugerir melhorias didáticas
- Adicionar exemplos de uso
- Reportar bugs ou inconsistências

---

**Lembre-se**: Este projeto é uma ferramenta de aprendizado. Use-o para entender os conceitos, experimente modificações e adapte para suas necessidades educacionais! 🚀
# Buscador e Tradutor de Artigos do PubMed

Este projeto consiste em um script Python que automatiza a busca por artigos científicos recentes e relevantes na plataforma PubMed, seleciona aleatoriamente um número definido de artigos, traduz seus títulos, resumos e palavras-chave para o português brasileiro usando a API do Google Gemini e, por fim, compila todas as informações em um relatório PDF.

## Visão Geral

O objetivo principal é incentivar a literatura científica para pesquisadores, estudantes e profissionais que precisam se manter atualizados. Em vez de navegar manualmente pelo PubMed e traduzir textos, este script entrega um relatório conciso e traduzido de alguns artigos que podem ser interessantes para a prática clínica diária ou estudo.

## Funcionalidades

-   **Busca Personalizada:** Pesquisa artigos no PubMed com base em termos específicos (`dog`, `cat`, `feline`, `canine`) e filtros avançados (``apenas artigos de revisão sistemática, meta-análises e ensaios clínicos dos últimos 5 anos``).
-   **Seleção Aleatória:** Busca os 100 artigos mais recentes que correspondem aos critérios e seleciona 5 de forma aleatória para análise.
-   **Extração de Dados:** Coleta informações essenciais dos artigos selecionados, como Título, Resumo, Palavras-chave e o link direto para o artigo (URL).
-   **Tradução Automática:** Utiliza a poderosa API do Google Gemini para traduzir o conteúdo textual para o Português do Brasil.
-   **Geração de Relatório:** Cria um arquivo `relatorio_artigos.pdf` formatado e de fácil leitura, contendo os dados originais e traduzidos de cada artigo.

## Tecnologias Utilizadas

-   **Python 3**
-   **APIs:**
    -   NCBI E-utils (PubMed)
    -   Google Gemini API
        
-   **Bibliotecas Python:**
    -   `requests`: Para realizar as chamadas às APIs.
    -   `google-generativeai`: Para interagir com o modelo Gemini.
    -   `reportlab`: Para a criação do documento PDF.
    -   `python-dotenv`: Para gerenciar as chaves de API de forma segura.
        

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Pré-requisitos

-   Python 3.7 ou superior instalado.
-   Uma chave de API do Google Gemini. Você pode obter uma no [Google AI Studio](https://aistudio.google.com/app/apikey?authuser=1).

### 2. Clonar o Repositório

```
git clone https://github.com/rdcar/med-vet-updater.git
cd med-vet-updater
```
### 3. Criar um Ambiente Virtual (Recomendado)   
Bash
```
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
### 4. Instalar as Dependências
```
pip install -r requirements.txt

```

### 5. Configurar a Chave de API
Crie um arquivo chamado `.env` na raiz do projeto. Este arquivo guardará sua chave de API de forma segura.

**ATENÇÃO:** Nunca envie este arquivo para um repositório público. Adicione `.env` ao seu arquivo `.gitignore`.
Adicione sua chave de API ao arquivo `.env` da seguinte forma:

**.env**

```
GOOGLE_API_KEY="SUA_CHAVE_DE_API_DO_GEMINI_AQUI"

```
## Como Usar

Com o ambiente configurado, basta executar o script principal a partir do seu terminal:

Bash

```
python renatorio_artigos.py

```
O script exibirá o progresso no terminal, desde a busca dos artigos até a finalização do PDF. Ao final do processo, um arquivo chamado `relatorio_artigos.pdf` será gerado na mesma pasta.

### Personalizando a Busca

Se desejar alterar os critérios de busca, modifique a variável `search_terms` no início do script. Você pode alterar as palavras-chave, os tipos de estudo e o filtro de data conforme a sintaxe de busca do PubMed.

```
# Exemplo de personalização
search_terms = f"(anesthesia OR pain) AND (dog OR canine) AND (randomizedcontrolledtrial[Filter]) AND (y_1[Filter]))"

```

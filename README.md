-----

#🩺Pesquisa e Tradução de Artigos no PubMed

-----

Este script Python automatiza a busca, análise e tradução de artigos científicos do **PubMed** e **Google Gemini**. Ele encontra os artigos mais citados sobre tópicos específicos, traduz seus resumos para o português e salva os resultados em um arquivo PDF. É uma ferramenta útil para pesquisadores ou estudantes que precisam fazer uma revisão bibliográfica rápida em sua área de interesse.

-----

## Como Funciona o Script ⚙️

O script executa um processo de cinco etapas para entregar os resultados:

1.  **Busca no PubMed:** O script usa a API do PubMed (**E-Utils**) para buscar IDs de artigos sobre "cães" e "gatos". A busca é filtrada para incluir apenas revisões sistemáticas, meta-análises e ensaios clínicos randomizados publicados nos últimos **cinco anos**.
2.  **Contagem de Citações:** Com os IDs em mãos, o script conta quantas vezes cada artigo foi citado usando a mesma API, ordenando-os do mais para o menos citado.
3.  **Seleção e Extração de Detalhes:** De forma inteligente, o script seleciona **cinco artigos aleatórios** dentre os **20 mais citados** para evitar viés. Em seguida, ele extrai o título, o resumo, as palavras-chave e o link para a página do PubMed de cada um.
4.  **Tradução com a API do Gemini:** A ferramenta traduz todo o conteúdo extraído (título, resumo e palavras-chave) para o português, usando o modelo **'gemini-2.5-flash'** da API do Google Gemini.
5.  **Geração do PDF:** Por fim, um arquivo PDF chamado **relatorio\_artigos.pdf** é criado. Ele contém todos os artigos selecionados, com seus títulos, IDs, números de citações, URLs e as traduções feitas pelo Gemini.

-----

## Como Usar o Script 🚀

Para usar o script, siga estes passos simples:

1.  **Instale as dependências:** Você precisa ter o Python instalado. Execute o seguinte comando para instalar as bibliotecas necessárias:
    ```bash
    pip install requests python-dotenv google-generativeai reportlab
    ```
2.  **Configure a API:** O script requer uma chave de API do Google Gemini.
      * Crie uma conta na plataforma **Google AI Studio** para obter sua chave.
      * Crie um arquivo chamado **.env** na mesma pasta do script.
      * Dentro do arquivo `.env`, adicione sua chave de API desta forma:
        ```env
        GOOGLE_API_KEY="SUA_CHAVE_AQUI"
        ```
3.  **Execute o script:** Com as dependências instaladas e o arquivo `.env` configurado, basta executar o script no seu terminal:
    ```bash
    python nome_do_seu_script.py
    ```
    Após a execução, um arquivo chamado **relatorio\_artigos.pdf** será gerado na mesma pasta do script, contendo os resultados.

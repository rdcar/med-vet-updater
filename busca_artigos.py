import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import google.generativeai as genai

# ----------------- ETAPA 1: BUSCA NO PUBMED -----------------

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Termos de busca no PubMed
search_terms = f"(dog OR cat OR canine OR feline) AND (clinicaltrial[Filter] OR meta-analysis[Filter] OR randomizedcontrolledtrial[Filter] OR systematicreview[Filter]) AND (y_5[Filter]))"

# API do PubMed - Endpoint para busca de IDs (e-search)
search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    'db': 'pubmed',
    'term': search_terms,
    'retmax': 100,  # Buscar até 100 artigos
    'retmode': 'json'
}

print("Buscando IDs de artigos no PubMed...")
response = requests.get(search_url, params=params)
data = response.json()

# Extrair os IDs dos artigos
article_ids = data['esearchresult']['idlist']
print(f"IDs encontrados: {len(article_ids)} artigos")

if not article_ids:
    raise ValueError("Nenhum artigo encontrado com os critérios de busca.")

# ----------------- ETAPA 2: SELEÇÃO ALEATÓRIA DE ARTIGOS -----------------

print("\nSelecionando 5 artigos aleatoriamente...")
# Selecionar aleatoriamente 5 artigos da lista total de IDs encontrados
selected_pmids = random.sample(article_ids, min(5, len(article_ids)))

print(f"Artigos escolhidos aleatoriamente: {selected_pmids}")

# ----------------- ETAPA 3: PEGAR DETALHES DOS ARTIGOS -----------------

fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
params_fetch = {
    'db': 'pubmed',
    'id': ",".join(selected_pmids),
    'retmode': 'xml',
}

print("\nObtendo detalhes completos dos artigos selecionados...")
response_fetch = requests.get(fetch_url, params=params_fetch)
root = ET.fromstring(response_fetch.content)

articles_data = []
for article in root.findall('.//PubmedArticle'):
    title = article.find('.//ArticleTitle').text
    abstract_element = article.find('.//AbstractText')
    abstract = abstract_element.text if abstract_element is not None else "Resumo não disponível."
    pmid = article.find('.//PMID').text
    article_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    # Extrair palavras-chave (se houver)
    keywords = []
    for kwd in article.findall('.//Keyword'):
        if kwd.text:
            keywords.append(kwd.text)

    articles_data.append({
        'title': title,
        'abstract': abstract,
        'keywords': keywords,
        'url': article_url,
        'pmid': pmid,
    })

print("Detalhes dos artigos extraídos com sucesso.")

# ----------------- ETAPA 4: TRADUÇÃO COM GEMINI -----------------

# Configurar a chave da API do Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A chave de API GOOGLE_API_KEY não foi encontrada. Verifique seu arquivo .env.")

genai.configure(api_key=GOOGLE_API_KEY)

# Inicializar o modelo
model = genai.GenerativeModel('gemini-1.5-flash')


def process_article_with_gemini(article_data):
    """
    Tradução do título, resumo e palavras-chave para português brasileiro.
    """
    title = article_data['title']
    abstract = article_data['abstract']
    keywords = article_data['keywords']

    full_text = f"Título: {title}\n\nResumo: {abstract}\n\nPalavras-chave: {', '.join(keywords) if keywords else 'Nenhuma encontrada'}"

    prompt = f"""
    Traduza para o português brasileiro o título, o resumo e as palavras-chave a seguir.

    {full_text}

    Formato da resposta:

    **Título (pt):** [tradução aqui]
    **Resumo (pt):** [tradução aqui]
    **Palavras-chave (pt):** [tradução aqui]
    """

    try:
        response = model.generate_content(prompt)

        # Obter resposta
        if hasattr(response, "text"):
            processed_response = response.text.strip()
        else:
            processed_response = response.candidates[0].content.parts[0].text.strip()

        return {
            'translation_pt': processed_response
        }

    except Exception as e:
        print(f"Erro ao processar o artigo com a API do Gemini: {e}")
        return {
            'translation_pt': "N/A"
        }


print("\nTraduzindo artigos selecionados com a API do Google Gemini...")
processed_articles = []
for article in articles_data:
    gemini_output = process_article_with_gemini(article)
    article.update(gemini_output)
    processed_articles.append(article)

print("Traduções concluídas.")

# ----------------- ETAPA 5: GERAR PDF -----------------

def create_pdf(filename, articles_data):
    """
    Cria um arquivo PDF com os artigos traduzidos.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Título do documento
    elements.append(Paragraph("Artigos Científicos", styles['Heading1']))
    elements.append(Spacer(1, 0.2 * inch))

    for article in articles_data:
        elements.append(Paragraph(f"<b>Título Original:</b> {article['title']}", styles['Heading2']))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"<b>PMID:</b> {article['pmid']}", styles['BodyText']))
        elements.append(Paragraph(f"<b>URL:</b> <a href='{article['url']}'>{article['url']}</a>", styles['BodyText']))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"<b>Tradução:</b><br/>{article['translation_pt']}", styles['BodyText']))

        elements.append(Spacer(1, 0.5 * inch))

    doc.build(elements)
    print(f"\nPDF gerado com sucesso! Verifique o arquivo '{filename}' na sua pasta de projeto.")


# Gerar o PDF final
create_pdf("relatorio_artigos.pdf", processed_articles)
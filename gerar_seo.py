# Gera os arquivos que buscadores e agentes de IA leem:
#   robots.txt   — quem pode rastrear e onde fica o mapa
#   sitemap.xml  — todas as URLs nos dois idiomas, com alternates
#   llms.txt     — resumo do site em texto puro, para modelos de linguagem
#   404.html     — pagina de erro que devolve a pessoa ao site
#
# Rode depois de acrescentar projeto ou idioma: python gerar_seo.py

import io, os, datetime

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://kralluz.github.io'
HOJE = datetime.date.today().isoformat()

PAGINAS = [
    ('', 'en/', '1.0', 'monthly'),
]

PROJETOS = [
    ('saude-brasil-360.html',        'Saúde Brasil 360'),
    ('atende-facil.html',            'Atende Fácil'),
    ('alcance.html',                 'Alcance'),
    ('distribuicao-financeira.html', 'Distribuição Financeira'),
    ('eventa-pro.html',              'Eventa Pro'),
    ('crm-getmoto.html',             'CRM GetMoto'),
]


# --------------------------------------------------------------- robots.txt
ROBOTS = f"""# Portfolio de Carlos Henrique — conteudo publico, rastreio liberado.

User-agent: *
Allow: /

# Agentes de IA e buscadores generativos sao bem-vindos: o conteudo aqui
# descreve sistemas reais em producao e existe para ser encontrado.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: cohere-ai
Allow: /

# arquivos de trabalho, nao de leitura
Disallow: /og/

Sitemap: {BASE}/sitemap.xml
"""


# -------------------------------------------------------------- sitemap.xml
def sitemap():
    urls = []

    def entrada(caminho_pt, caminho_en, prioridade, freq):
        for atual, outro, lang in ((caminho_pt, caminho_en, 'pt-BR'),
                                   (caminho_en, caminho_pt, 'en')):
            alt = (f'    <xhtml:link rel="alternate" hreflang="pt-BR" href="{BASE}/{caminho_pt}"/>\n'
                   f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/{caminho_en}"/>\n'
                   f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/{caminho_pt}"/>')
            urls.append(
                f'  <url>\n'
                f'    <loc>{BASE}/{atual}</loc>\n'
                f'{alt}\n'
                f'    <lastmod>{HOJE}</lastmod>\n'
                f'    <changefreq>{freq}</changefreq>\n'
                f'    <priority>{prioridade}</priority>\n'
                f'  </url>')

    entrada('', 'en/', '1.0', 'monthly')
    for arq, _ in PROJETOS:
        entrada(f'projetos/{arq}', f'en/projects/{arq}', '0.8', 'monthly')

    corpo = '\n'.join(urls)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            f'        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f'{corpo}\n'
            f'</urlset>\n')


# ----------------------------------------------------------------- llms.txt
LLMS = f"""# Carlos Henrique — Desenvolvedor Full Stack

> Desenvolvedor full stack e arquiteto de sistemas, no Brasil, disponivel para
> trabalho remoto. Constroi e mantem seis produtos em producao: paineis de
> indicadores de saude publica usados por prefeituras, plataforma de atendimento
> ao cidadao vendida a municipios, sistemas de gestao financeira e um aplicativo
> Android publicado na Google Play. TypeScript de ponta a ponta.

Site: {BASE}
Versao em ingles: {BASE}/en/
GitHub: https://github.com/kralluz
LinkedIn: https://www.linkedin.com/in/carlosklz/

## Quem e

- Nome: Carlos Henrique (kralluz)
- Funcao: Desenvolvedor Full Stack e arquiteto de sistemas
- Idiomas: portugues (nativo), ingles
- Formacao: Kenzie Academy Brasil (Full Stack, 2023); bacharelado em Sistemas de
  Informacao pelo Instituto Federal Goiano
- Atua em todas as camadas: modelagem de banco, API, frontend, mobile e deploy

## Stack principal

TypeScript, JavaScript, React, React Native, Expo, Next.js, Vite, Ant Design,
TailwindCSS, TanStack Query, Zustand, Node.js, NestJS, Express, Prisma,
PostgreSQL, Docker, Vitest, Jest, Swagger/OpenAPI, OpenTelemetry, MinIO.

## Projetos em producao

- [Saude Brasil 360]({BASE}/projetos/saude-brasil-360.html): sistema de gestao
  para secretarias municipais de saude. Calcula os indicadores da Atencao
  Primaria de que depende o repasse federal, a partir da base de e-SUS/PEC de
  cada prefeitura, e emite os documentos oficiais de faturamento do SUS.
  358 mil linhas, 598 endpoints, 92 tabelas, mais de 30 modulos.
  Multi-tenant com uma conexao de banco por municipio.

- [Atende Facil]({BASE}/projetos/atende-facil.html): plataforma de atendimento
  ao cidadao para prefeituras. Reune varios numeros de WhatsApp num painel,
  chamado formal com protocolo e prazo, quadro Kanban e um robo de atendimento
  montado em editor visual. 103 mil linhas, 293 endpoints, 66 tabelas, 25
  modulos. Isolamento entre organizacoes garantido no banco por extensao do
  Prisma e indices unicos parciais.

- [Alcance]({BASE}/projetos/alcance.html): gestao de contratos e comissionamento
  para administradora de beneficios. Importa o faturamento de cada fornecedor
  lendo Excel, CSV, PDF ou foto com OCR, aprende o layout por fornecedor e casa
  cada linha com o contrato certo. 43,8 mil linhas, 91 endpoints, 26 tabelas.

- [Distribuicao Financeira]({BASE}/projetos/distribuicao-financeira.html):
  aplicativo Android de organizacao financeira pessoal, publicado na Google Play.
  Divide a renda do mes por categoria, controla dividas e fecha cada mes num
  snapshot imutavel. Offline-first com padrao outbox e escrita idempotente.
  51,7 mil linhas, 73 endpoints, 25 tabelas, 24 telas.
  Loja: https://play.google.com/store/apps/details?id=com.distribuicao_financeira.app

- [Eventa Pro]({BASE}/projetos/eventa-pro.html): plataforma de inscricao em
  corridas de rua. Lotes de preco por data, cupons, pagamento por PIX ou cartao,
  ingresso com QR code para check-in, resultados e certificado em PDF, e controle
  de repasse ao organizador. 47 mil linhas, 143 endpoints, 19 tabelas, 71 telas.

- [CRM GetMoto]({BASE}/projetos/crm-getmoto.html): gestao de oficina de motos em
  operacao no Reino Unido. Ordem de servico, estoque, compras, despesas e folha
  de pagamento convergindo para um livro-caixa unico. 50 mil linhas, 96
  endpoints, 18 tabelas, 39 telas, interface em tres idiomas.

## Como trabalha

Quatro decisoes que se repetem em projetos independentes:

1. Dinheiro nunca e numero quebrado. Valor monetario e inteiro (centavos, pence
   em BigInt) e percentual e ponto-base, do schema ate a tela.
2. O passado nao se reescreve. O resultado do periodo e congelado num snapshot
   imutavel, e cancelar cria lancamento reverso em vez de apagar o original.
3. O servidor nao confia no cliente. Totais sao recalculados no servidor na
   gravacao, e o escopo de acesso vem do usuario autenticado, nunca da requisicao.
4. A regra que nao pode falhar mora no banco. Sob concorrencia real a garantia e
   transacao, indice unico parcial e trigger — nao checagem na aplicacao.

## Contato

Para propostas de projeto ou vaga, o caminho mais rapido e o LinkedIn:
https://www.linkedin.com/in/carlosklz/
"""


# ----------------------------------------------------------------- 404.html
PAGINA_404 = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página não encontrada — Carlos Henrique</title>
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/assets/perfil.jpg">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<style>
  .erro {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 24px;
  }
  .erro-cod {
    font-family: var(--fonte-mono);
    font-size: clamp(64px, 18vw, 128px);
    font-weight: 500;
    line-height: 1;
    color: var(--destaque);
    letter-spacing: -.04em;
    margin: 0 0 18px;
  }
  .erro h1 { font-size: clamp(22px, 5vw, 30px); margin: 0 0 12px; }
  .erro p  { color: var(--texto-fraco); max-width: 460px; margin: 0 0 30px; }
  .erro .hero-acoes { justify-content: center; }
</style>
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-seta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M5 12h14M13 6l6 6-6 6"/>
  </symbol>
</svg>

<div class="container erro">
  <p class="erro-cod">404</p>
  <h1>Esta página não existe</h1>
  <p>
    O endereço pode ter mudado ou o link veio quebrado.
    Os seis projetos continuam onde estavam.
  </p>
  <div class="hero-acoes">
    <a class="btn btn-primario" href="/">
      Ir para o início
      <svg class="ico"><use href="#i-seta"/></svg>
    </a>
    <a class="btn" href="/#projetos">Ver projetos</a>
    <a class="btn" href="/en/">English</a>
  </div>
</div>

</body>
</html>
"""


def gravar(nome, conteudo):
    caminho = os.path.join(RAIZ, nome)
    with io.open(caminho, 'w', encoding='utf-8', newline='\n') as f:
        f.write(conteudo)
    print(f'  {nome:16} {len(conteudo):>7} bytes')


if __name__ == '__main__':
    gravar('robots.txt', ROBOTS)
    gravar('sitemap.xml', sitemap())
    gravar('llms.txt', LLMS)
    gravar('404.html', PAGINA_404)
    print(f'\n{2 + len(PROJETOS) * 2} URLs no sitemap')

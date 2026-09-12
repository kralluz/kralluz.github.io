# Molde e motor de geracao das paginas de projeto, nos dois idiomas.
# O conteudo fica em gerar_paginas.py (pt) e conteudo_en.py (en);
# aqui mora so o HTML e a montagem.

import os, io, re, json, html as _html

SITE = {
    'url':      'https://kralluz.github.io',
    'autor':    'Carlos Henrique',
    'cargo_pt': 'Desenvolvedor Full Stack',
    'cargo_en': 'Full Stack Developer',
    'github':   'https://github.com/kralluz',
    'linkedin': 'https://www.linkedin.com/in/carlosklz/',
    'og':       'assets/og.png',
}

# textos de interface por idioma
IDIOMAS = {
    'pt': {
        'lang':        'pt-BR',
        'dir_paginas': 'projetos',
        'raiz':        '../',           # caminho ate a raiz do site
        'home':        '../index.html',
        'voltar':      'Todos os projetos',
        'contato':     'Contato',
        'papel':       'Papel',
        'periodo':     'Período',
        'situacao':    'Situação',
        'problema':    'O problema',
        'solucao':     'O que foi construído',
        'modulos':     'Módulos',
        'arquitetura': 'Arquitetura',
        'integracoes': 'Integrações',
        'integracoes_sub': 'Sistemas externos com que o produto conversa.',
        'desafios':    'Desafios técnicos',
        'telas':       'Telas',
        'telas_sub':   'Prints do sistema em funcionamento.',
        'rodape':      'Carlos Henrique · Desenvolvedor Full Stack',
        'sufixo_titulo': 'Carlos Henrique',
        'outro_idioma_url': '../en/projects/{arquivo}',
        'outro_idioma_rot': 'EN',
        'outro_idioma_titulo': 'Read in English',
    },
    'en': {
        'lang':        'en',
        'dir_paginas': 'en/projects',
        'raiz':        '../../',
        'home':        '../index.html',
        'voltar':      'All projects',
        'contato':     'Contact',
        'papel':       'Role',
        'periodo':     'Period',
        'situacao':    'Status',
        'problema':    'The problem',
        'solucao':     'What was built',
        'modulos':     'Modules',
        'arquitetura': 'Architecture',
        'integracoes': 'Integrations',
        'integracoes_sub': 'External systems the product talks to.',
        'desafios':    'Technical challenges',
        'telas':       'Screens',
        'telas_sub':   'Screenshots of the system in use.',
        'rodape':      'Carlos Henrique · Full Stack Developer',
        'sufixo_titulo': 'Carlos Henrique',
        'outro_idioma_url': '../../projetos/{arquivo}',
        'outro_idioma_rot': 'PT',
        'outro_idioma_titulo': 'Ler em português',
    },
}


MODELO = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js');</script>
<!-- a classe .js habilita a animacao de entrada; sem ela o conteudo
     aparece direto, entao uma falha de script nunca deixa a pagina vazia -->
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<link rel="canonical" href="{canonico}">
<link rel="alternate" hreflang="pt-BR" href="{alt_pt}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_pt}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="Carlos Henrique">

<!-- compartilhamento: WhatsApp, LinkedIn, Slack, Telegram, X -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Carlos Henrique">
<meta property="og:locale" content="{og_locale}">
<meta property="og:title" content="{og_titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{canonico}">
<meta property="og:image" content="{og_imagem}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_titulo}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{og_imagem}">

<link rel="icon" href="{raiz}assets/perfil.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{raiz}style.css">
<link rel="stylesheet" href="{raiz}projetos/projeto.css">

<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-seta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M5 12h14M13 6l6 6-6 6"/>
  </symbol>
  <symbol id="f-br" viewBox="0 0 30 20">
    <rect width="30" height="20" fill="#009b3a"/>
    <path d="M15 2.6 27.4 10 15 17.4 2.6 10Z" fill="#fedf00"/>
    <circle cx="15" cy="10" r="4.4" fill="#002776"/>
    <path d="M10.9 11.4a5.2 5.2 0 0 1 8.2 0" fill="none" stroke="#fff" stroke-width="1.3"/>
  </symbol>
  <symbol id="f-en" viewBox="0 0 30 20">
    <rect width="30" height="20" fill="#012169"/>
    <path d="M0 0 30 20M30 0 0 20" stroke="#fff" stroke-width="4.4"/>
    <path d="M0 0 30 20M30 0 0 20" stroke="#c8102e" stroke-width="2.2"/>
    <path d="M15 0v20M0 10h30" stroke="#fff" stroke-width="6.6"/>
    <path d="M15 0v20M0 10h30" stroke="#c8102e" stroke-width="3.8"/>
  </symbol>
</svg>

<div class="topo-fixo">
  <div class="container">
    <a class="voltar" href="{home}#projetos">
      <svg class="ico"><use href="#i-seta"/></svg>
      {rot_voltar}
    </a>
    <span class="topo-acoes">
      <a class="troca-idioma" href="{outro_idioma}" hreflang="{outro_lang}" title="{rot_titulo_idioma}" aria-label="{rot_titulo_idioma}">
        <svg class="bandeira" viewBox="0 0 30 20" aria-hidden="true"><use href="#f-{bandeira}"/></svg>{rot_outro_idioma}</a>
      <a class="btn" href="{home}#contato">{rot_contato}</a>
    </span>
  </div>
</div>

<header class="projeto-hero">
  <div class="container">
    <span class="etiqueta">{etiqueta}</span>
    <h1 class="revelar">{nome}</h1>
    <p class="projeto-resumo revelar" data-atraso="80">{resumo}</p>
{loja_html}    <ul class="stack revelar" data-atraso="140">{stack_html}</ul>

    <div class="fatos revelar" data-atraso="200">
      <div class="fato"><span>{rot_papel}</span><strong>{papel}</strong></div>
      <div class="fato"><span>{rot_periodo}</span><strong>{periodo}</strong></div>
      <div class="fato"><span>{rot_situacao}</span><strong>{situacao}</strong></div>
    </div>
  </div>
</header>

<main class="conteudo">
  <div class="container">
{numeros_html}
    <h2 class="revelar">{rot_problema}</h2>
    <div class="destaque revelar" data-atraso="60">
      <p>{problema}</p>
    </div>

    <h2 class="revelar">{rot_solucao}</h2>
    <ul class="entregas revelar" data-atraso="60">{solucao_html}
    </ul>
{modulos_html}{arquitetura_html}{integracoes_html}
    <h2 class="revelar">{rot_desafios}</h2>
{desafios_html}

    <h2 class="revelar">{rot_telas}</h2>
    <p class="revelar">{rot_telas_sub}</p>
    <div class="galeria">{galeria_html}
    </div>

    <div class="nav-projetos">
      <a class="btn" href="{home}#projetos">
        <svg class="ico" style="transform:rotate(180deg)"><use href="#i-seta"/></svg>
        {rot_voltar}
      </a>
      <a class="btn btn-primario" href="{proximo_arquivo}">
        {proximo_nome}
        <svg class="ico"><use href="#i-seta"/></svg>
      </a>
    </div>

  </div>
</main>

<footer>
  <div class="container">
    <p>{rodape}</p>
  </div>
</footer>

<script src="{raiz}script.js"></script>
</body>
</html>
"""


def limpa(txt):
    """tira as tags do texto para usar em atributo meta"""
    for t in ('<strong>', '</strong>', '<code>', '</code>'):
        txt = txt.replace(t, '')
    return txt.replace('"', '&quot;')


def atributos_contador(valor):
    """Separa o numero do que vem depois dele para o contador do JS.

    "103 mil" -> conta 103, sufixo " mil"
    "43,8 mil" -> conta 43,8 com uma casa decimal
    "30+"      -> conta 30, sufixo "+"
    Se nao comecar com digito, devolve vazio e o texto fica estatico.
    """
    m = re.match(r'^(\d+(?:[.,]\d+)?)(.*)$', valor.strip())
    if not m:
        return ''
    numero, resto = m.group(1), m.group(2)
    decimais = 0
    if ',' in numero or '.' in numero:
        decimais = len(re.split(r'[.,]', numero)[1])
    attr = f' data-contar="{numero.replace(",", ".")}"'
    if decimais:
        attr += f' data-decimais="{decimais}"'
    if resto:
        attr += f' data-sufixo="{resto}"'
    return attr


def mescla(base, traducao):
    """campo traduzido vence; o que nao foi traduzido vem do portugues"""
    if not traducao:
        return dict(base)
    junto = dict(base)
    junto.update(traducao)
    return junto


def url_pagina(idioma, arquivo):
    return f"{SITE['url']}/{IDIOMAS[idioma]['dir_paginas']}/{arquivo}"


def estruturado(p, idioma, canonico):
    """JSON-LD: descreve o projeto como software para buscadores e agentes."""
    dados = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": p['nome'],
        "description": limpa(p['resumo']).replace('&quot;', '"'),
        "url": canonico,
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "inLanguage": IDIOMAS[idioma]['lang'],
        "author": {
            "@type": "Person",
            "name": SITE['autor'],
            "url": SITE['url'],
            "jobTitle": SITE['cargo_en'] if idioma == 'en' else SITE['cargo_pt'],
            "sameAs": [SITE['github'], SITE['linkedin']],
        },
    }
    if p.get('stack'):
        dados["softwareRequirements"] = ', '.join(p['stack'])
    if p.get('loja'):
        dados["downloadUrl"] = p['loja']['url'].replace('&amp;', '&')
        dados["offers"] = {"@type": "Offer", "category": "subscription"}
    return json.dumps(dados, ensure_ascii=False, indent=2)


def gerar_pagina(p, prox, idioma, raiz_fs):
    cfg = IDIOMAS[idioma]
    arquivo = p['arquivo']
    canonico = url_pagina(idioma, arquivo)
    descricao = limpa(p['resumo'])

    stack_html = ''.join(f'<li>{t}</li>' for t in p['stack'])
    solucao_html = ''.join(f'\n      <li>{item}</li>' for item in p['solucao'])

    loja_html = ''
    if p.get('loja'):
        loja = p['loja']
        loja_html = f'''
    <a class="loja revelar" data-atraso="110" href="{loja['url']}" target="_blank" rel="noopener">
      <svg class="loja-ico" viewBox="0 0 512 512" aria-hidden="true">
        <path fill="#00d0ff" d="M47 19a24 24 0 0 0-13 21v432a24 24 0 0 0 13 21l236-237z"/>
        <path fill="#00f076" d="M47 19a24 24 0 0 1 25 1l269 154-58 58z"/>
        <path fill="#fd0" d="M341 174l70 40c22 13 22 43 0 56l-70 40-58-58z"/>
        <path fill="#f53" d="M72 492a24 24 0 0 1-25 1l236-237 58 58z"/>
      </svg>
      <span class="loja-txt">
        <small>{loja['selo']}</small>
        <strong>{loja['nome']}</strong>
      </span>
      <svg class="ico loja-seta"><use href="#i-seta"/></svg>
    </a>
'''

    numeros_html = ''
    if p.get('numeros'):
        cartoes = ''.join(f'''
        <div class="num-cartao">
          <strong{atributos_contador(v)}>{v}</strong>
          <span>{rot}</span>
        </div>''' for v, rot in p['numeros'])
        numeros_html = f'''
    <div class="numeros-projeto revelar">{cartoes}
    </div>

'''

    modulos_html = ''
    if p.get('modulos'):
        grupos = ''.join(f'''
      <div class="grupo-modulo revelar">
        <h3>{grupo}</h3>
        <ul>{''.join(f"<li>{m}</li>" for m in itens)}</ul>
      </div>''' for grupo, itens in p['modulos'])
        modulos_html = f'''
    <h2 class="revelar">{cfg['modulos']}</h2>
    <p class="revelar">{p.get('modulos_intro', '')}</p>
    <div class="modulos">{grupos}
    </div>
'''

    arquitetura_html = ''
    if p.get('arquitetura'):
        itens = ''.join(f'\n      <li>{a}</li>' for a in p['arquitetura'])
        arquitetura_html = f'''
    <h2 class="revelar">{cfg['arquitetura']}</h2>
    <ul class="entregas revelar">{itens}
    </ul>
'''

    integracoes_html = ''
    if p.get('integracoes'):
        chips = ''.join(f'<li>{i}</li>' for i in p['integracoes'])
        integracoes_html = f'''
    <h2 class="revelar">{cfg['integracoes']}</h2>
    <p class="revelar">{cfg['integracoes_sub']}</p>
    <ul class="stack revelar">{chips}</ul>
'''

    if isinstance(p['desafio'], str):
        desafios_html = f'    <p class="revelar">{p["desafio"]}</p>'
    else:
        desafios_html = ''.join(f'''
    <div class="desafio revelar">
      <h3>{titulo}</h3>
      <p>{texto}</p>
    </div>''' for titulo, texto in p['desafio'])

    figuras = []
    for item in p['prints']:
        if isinstance(item, tuple):
            arq, legenda = item
            figuras.append(f'''
      <figure>
        <a href="{cfg['raiz']}assets/prints/{arq}" target="_blank" rel="noopener">
          <img src="{cfg['raiz']}assets/prints/{arq}" alt="{legenda}" loading="lazy">
        </a>
        <figcaption>{legenda}</figcaption>
      </figure>''')
        else:
            figuras.append(f'''
      <figure>
        <div class="vaga-print">{item}</div>
        <figcaption>{item}</figcaption>
      </figure>''')

    outro = 'en' if idioma == 'pt' else 'pt'

    html = MODELO.format(
        lang=cfg['lang'],
        raiz=cfg['raiz'],
        home=cfg['home'],
        titulo=f"{p['nome']} — {cfg['sufixo_titulo']}",
        og_titulo=f"{p['nome']} — {cfg['sufixo_titulo']}",
        descricao=descricao,
        canonico=canonico,
        alt_pt=url_pagina('pt', arquivo),
        alt_en=url_pagina('en', arquivo),
        og_locale='pt_BR' if idioma == 'pt' else 'en_US',
        og_imagem=f"{SITE['url']}/{SITE['og']}",
        jsonld=estruturado(p, idioma, canonico),
        outro_idioma=cfg['outro_idioma_url'].format(arquivo=arquivo),
        outro_lang=IDIOMAS[outro]['lang'],
        rot_outro_idioma=cfg['outro_idioma_rot'],
        rot_titulo_idioma=cfg['outro_idioma_titulo'],
        bandeira='en' if idioma == 'pt' else 'br',
        rot_voltar=cfg['voltar'],
        rot_contato=cfg['contato'],
        rot_papel=cfg['papel'],
        rot_periodo=cfg['periodo'],
        rot_situacao=cfg['situacao'],
        rot_problema=cfg['problema'],
        rot_solucao=cfg['solucao'],
        rot_desafios=cfg['desafios'],
        rot_telas=cfg['telas'],
        rot_telas_sub=cfg['telas_sub'],
        rodape=cfg['rodape'],
        nome=p['nome'],
        etiqueta=p['etiqueta'],
        resumo=p['resumo'],
        papel=p['papel'],
        periodo=p['periodo'],
        situacao=p['situacao'],
        stack_html=stack_html,
        problema=p['problema'],
        solucao_html=solucao_html,
        desafios_html=desafios_html,
        numeros_html=numeros_html,
        loja_html=loja_html,
        modulos_html=modulos_html,
        arquitetura_html=arquitetura_html,
        integracoes_html=integracoes_html,
        galeria_html=''.join(figuras),
        proximo_arquivo=prox['arquivo'],
        proximo_nome=prox['nome'],
    )

    pasta = os.path.join(raiz_fs, *cfg['dir_paginas'].split('/'))
    os.makedirs(pasta, exist_ok=True)
    with io.open(os.path.join(pasta, arquivo), 'w', encoding='utf-8') as f:
        f.write(html)
    return f"{cfg['dir_paginas']}/{arquivo}"

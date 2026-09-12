# Gera en/index.html a partir de index.html.
# A home em portugues continua sendo a fonte: aqui so trocamos os caminhos e
# os textos. Se sobrar frase sem traducao, o script avisa no fim.
#
# Rode depois de mexer em index.html: python gerar_home_en.py

import io, os, re

RAIZ = os.path.dirname(os.path.abspath(__file__))


# o seletor de idioma troca de destino e de bandeira
TROCA_PT = ('<a class="troca-idioma" href="en/" hreflang="en" title="Read in English" aria-label="Read in English"><svg class="bandeira" viewBox="0 0 30 20" aria-hidden="true"><use href="#f-en"/></svg>EN</a>')
TROCA_EN = ('<a class="troca-idioma" href="../" hreflang="pt-BR" title="Ler em português" aria-label="Ler em português"><svg class="bandeira" viewBox="0 0 30 20" aria-hidden="true"><use href="#f-br"/></svg>PT</a>')

# ---------------------------------------------------------------- caminhos
CAMINHOS = [
    ('href="assets/',  'href="../assets/'),
    ('src="assets/',   'src="../assets/'),
    ('href="style.css"', 'href="../style.css"'),
    ('src="script.js"',  'src="../script.js"'),
    ('href="projetos/', 'href="projects/'),
    (TROCA_PT, TROCA_EN),
]

# ---------------------------------------------------------------- textos
DESC_EN = ("Full stack developer and systems architect. Public-health indicator dashboards, "
           "citizen-service platforms for city halls and management systems in production.")

TEXTOS = [
    # ---- cabecalho / meta ----
    ('<html lang="pt-BR">', '<html lang="en">'),
    ('<title>Carlos Henrique — Desenvolvedor Full Stack</title>',
     '<title>Carlos Henrique — Full Stack Developer</title>'),
    ('Desenvolvedor Full Stack e arquiteto de sistemas. Painéis de saúde pública, '
     'plataformas de atendimento ao cidadão e sistemas de gestão em produção.', DESC_EN),
    ('<link rel="canonical" href="https://kralluz.github.io/">',
     '<link rel="canonical" href="https://kralluz.github.io/en/">'),
    ('<meta property="og:locale" content="pt_BR">\n'
     '<meta property="og:locale:alternate" content="en_US">',
     '<meta property="og:locale" content="en_US">\n'
     '<meta property="og:locale:alternate" content="pt_BR">'),
    ('<meta property="og:url" content="https://kralluz.github.io/">',
     '<meta property="og:url" content="https://kralluz.github.io/en/">'),
    ('content="Carlos Henrique — Desenvolvedor Full Stack"',
     'content="Carlos Henrique — Full Stack Developer"'),
    ('<meta name="keywords" content="desenvolvedor full stack, TypeScript, React, NestJS, '
     'Prisma, PostgreSQL, React Native, govtech, saúde pública, e-SUS, multi-tenant, Brasil">',
     '<meta name="keywords" content="full stack developer, TypeScript, React, NestJS, Prisma, '
     'PostgreSQL, React Native, govtech, public health software, multi-tenant, Brazil, remote">'),

    # ---- navegacao ----
    ('<li><a href="#sobre">Sobre</a></li>',   '<li><a href="#sobre">About</a></li>'),
    ('<li><a href="#projetos">Projetos</a></li>', '<li><a href="#projetos">Projects</a></li>'),
    ('<li><a href="#metodo">Método</a></li>', '<li><a href="#metodo">Method</a></li>'),
    ('<li><a href="#contato">Contato</a></li>', '<li><a href="#contato">Contact</a></li>'),

    # ---- hero ----
    ('<p class="hero-sup">Disponível para projetos remotos</p>',
     '<p class="hero-sup">Available for remote work</p>'),
    ('<p class="hero-cargo">Desenvolvedor Full Stack · Arquiteto de sistemas</p>',
     '<p class="hero-cargo">Full Stack Developer · Systems architect</p>'),
    ('Do banco ao layout. Transformo ruído em número, e número em decisão.',
     'From the database to the layout. I turn noise into numbers, and numbers into decisions.'),
    ('Ver projetos', 'See projects'),
    ('title="Disponível para projetos"', 'title="Available for work"'),

    # ---- faixa de numeros ----
    ('<span>commits</span>', '<span>commits</span>'),
    ('<span>contribuições no último ano</span>', '<span>contributions in the last year</span>'),
    ('<span>dos repositórios em TypeScript</span>', '<span>of repositories in TypeScript</span>'),
    ('<span>produtos em produção</span>', '<span>products in production</span>'),

    # ---- sobre ----
    ('<span class="num-secao">01</span>Sobre', '<span class="num-secao">01</span>About'),
    ('Construo produtos que rodam em produção e são usados todos os dias — painéis de\n'
     '            indicadores de saúde pública em dezenas de municípios, plataformas de atendimento\n'
     '            ao cidadão vendidas a prefeituras, sistemas de gestão financeira e de contratos.',
     'I build products that run in production and get used every day — public-health indicator\n'
     '            dashboards across dozens of municipalities, citizen-service platforms sold to city\n'
     '            halls, and financial and contract management systems.'),
    ('Atuo em todas as camadas: modelagem de banco, API, frontend, mobile e deploy.\n'
     '            O que me interessa não é a tela bonita isolada, é o caminho inteiro — do dado bruto\n'
     '            que chega de um sistema de governo até a decisão que alguém toma olhando um número.',
     'I work across every layer: database modelling, API, frontend, mobile and deployment.\n'
     '            What interests me is not the pretty screen on its own, it is the whole path — from\n'
     '            the raw record arriving out of a government system to the decision someone makes\n'
     '            looking at a number.'),
    ('<li>Formação Full Stack pela <strong>Kenzie Academy Brasil</strong> (2023)</li>',
     '<li>Full Stack programme at <strong>Kenzie Academy Brasil</strong> (2023)</li>'),
    ('<li>Bacharelado em <strong>Sistemas de Informação</strong> — IF Goiano, Campus Ceres</li>',
     '<li>BSc in <strong>Information Systems</strong> — Instituto Federal Goiano</li>'),
    ('<li>Integração com <strong>PEC / e-SUS / SISAB</strong></li>',
     '<li>Integration with <strong>Brazilian public-health systems</strong></li>'),
    ('<li>Sistemas de uso institucional em saúde e administração pública</li>',
     '<li>Institutional systems for healthcare and public administration</li>'),
    ('<li>TypeScript de ponta a ponta</li>', '<li>TypeScript end to end</li>'),

    # ---- projetos ----
    ('<span class="num-secao">02</span>Projetos', '<span class="num-secao">02</span>Projects'),
    ('Produtos em produção. A maior parte vive em repositórios privados de clientes.',
     'Products in production. Most of them live in private client repositories.'),
    ('<strong>O problema:</strong>', '<strong>The problem:</strong>'),
    ('<span class="projeto-link">Ver detalhes', '<span class="projeto-link">See details'),
    ('<span class="selo-loja">Na Play Store</span>', '<span class="selo-loja">On Google Play</span>'),

    ('<span class="etiqueta">saúde pública</span>', '<span class="etiqueta">public health</span>'),
    ('o repasse federal da Atenção Primária depende de\n'
     '            indicadores que o município precisa calcular e comprovar — e o dado chegava tarde\n'
     '            demais, agregado demais.',
     'federal primary-care funding depends on indicators each\n'
     '            municipality must calculate and prove — and the data arrived too late, too\n'
     '            aggregated.'),
    ('Calcula os indicadores oficiais do Ministério da Saúde a partir das bases de e-SUS/PEC\n'
     '            de cada prefeitura, gera as listas nominais para busca ativa e emite BPA e RAAS para\n'
     '            o faturamento do SUS.',
     'Computes the Ministry of Health\'s official indicators from each city hall\'s\n'
     '            electronic health record, produces named patient lists for outreach and issues the\n'
     '            official public-health billing documents.'),
    ('598 endpoints · 92 tabelas · 30+ módulos', '598 endpoints · 92 tables · 30+ modules'),

    ('<span class="etiqueta">atendimento público</span>',
     '<span class="etiqueta">citizen services</span>'),
    ('o cidadão manda mensagem no WhatsApp da prefeitura e a\n'
     '            solicitação morre na conversa — sem protocolo, sem prazo, sem responsável.',
     'a citizen messages the city hall\'s WhatsApp and the request\n'
     '            dies inside the conversation — no protocol, no deadline, no owner.'),
    ('Reúne num painel só os vários números de WhatsApp da organização, o chamado formal com\n'
     '            protocolo, um robô montado em tela e o portal onde o cidadão acompanha sem login.\n'
     '            Multi-organização desde a raiz, com isolamento garantido no banco.',
     'Brings the organisation\'s several WhatsApp numbers, the formal ticket with protocol, a\n'
     '            bot built on screen and the portal where citizens track requests without signing in\n'
     '            into one panel. Multi-organisation from the ground up, isolated at the database level.'),
    ('293 endpoints · 66 tabelas · 25 módulos', '293 endpoints · 66 tables · 25 modules'),

    ('<span class="etiqueta">gestão comercial</span>',
     '<span class="etiqueta">commercial management</span>'),
    ('cada fornecedor manda o faturamento num layout diferente —\n'
     '            Excel, PDF, às vezes uma foto da tela — e alguém redigita tudo à mão.',
     'every supplier sends billing in a different layout — Excel,\n'
     '            PDF, sometimes a photo of a screen — and someone retypes all of it by hand.'),
    ('Importação que lê o arquivo com OCR, aprende o layout de cada fornecedor e casa cada\n'
     '            linha com o contrato certo. Divide a comissão entre vários representantes com centavos\n'
     '            que fecham, e vigia a carteira sozinha por e-mail.',
     'An import that reads the file with OCR, learns each supplier\'s layout and matches every\n'
     '            row to the right contract. Splits commission across several reps with cents that add\n'
     '            up, and watches the portfolio on its own by email.'),
    ('91 endpoints · 26 tabelas · 15 módulos', '91 endpoints · 26 tables · 15 modules'),

    ('quem tenta organizar as contas em planilha desiste na\n'
     '            terceira semana — e a conta é lançada no ônibus, sem sinal.',
     'people who budget in a spreadsheet quit in the third week —\n'
     '            and the expense gets entered on the bus, with no signal.'),
    ('App que divide a renda do mês entre categorias definidas pelo usuário, acompanha\n'
     '            dívidas e fecha cada mês num retrato que não muda depois. Funciona offline e sincroniza\n'
     '            quando a conexão volta, sem duplicar lançamento.',
     'An app that splits the month\'s income across user-defined categories, tracks debts and\n'
     '            closes each month into a snapshot that never changes. Works offline and syncs when the\n'
     '            connection returns, without duplicating entries.'),
    ('73 endpoints · 25 tabelas · 24 telas', '73 endpoints · 25 tables · 24 screens'),

    ('<span class="etiqueta">eventos</span>', '<span class="etiqueta">events</span>'),
    ('organizador de corrida controla inscrição por formulário e\n'
     '            recebe Pix na mão — sem ingresso, sem controle de vaga, e conferindo nome em papel\n'
     '            impresso na largada.',
     'race organisers run sign-ups through a form and take payment\n'
     '            by hand — no ticket, no seat control, checking names on printed paper at the start\n'
     '            line.'),
    ('Lotes de preço por data, cupom, pagamento por PIX ou cartão e ingresso com QR code\n'
     '            para o check-in. Depois da prova, resultado e certificado. A vaga é reservada dentro\n'
     '            de uma transação, então duas pessoas nunca levam a última.',
     'Date-based price tiers, coupons, payment by instant transfer or card, and a QR-code\n'
     '            ticket for check-in. After the race, results and certificate. The seat is held inside\n'
     '            a transaction, so two people never take the last one.'),
    ('143 endpoints · 19 tabelas · 71 telas', '143 endpoints · 19 tables · 71 screens'),

    ('<span class="etiqueta">gestão</span>', '<span class="etiqueta">management</span>'),
    ('ordem de serviço, estoque e folha em lugares separados, e\n'
     '            nenhum deles conversando com o caixa — ninguém sabia o que o mês fechou de verdade.',
     'work orders, stock and payroll in separate places, none of\n'
     '            them talking to the cash book — nobody knew what the month actually closed at.'),
    ('Gestão de oficina de motos em operação no Reino Unido. A OS soma peça e mão de obra,\n'
     '            baixa o estoque e lança o caixa na mesma transação; a folha calcula hora extra e vale\n'
     '            em pence inteiros, sem arredondamento.',
     'Motorcycle workshop management running in the United Kingdom. The work order adds parts\n'
     '            and labour, deducts stock and posts to the cash book in the same transaction; payroll\n'
     '            computes overtime and advances in whole pence, with no rounding.'),
    ('96 endpoints · 18 tabelas · 19 módulos', '96 endpoints · 18 tables · 19 modules'),

    # ---- metodo ----
    ('<span class="num-secao">03</span>Como eu trabalho',
     '<span class="num-secao">03</span>How I work'),
    ('Quatro decisões que nenhum cliente pediu e que eu repeti em projetos que não se conhecem.',
     'Four decisions no client asked for, repeated across projects that never met each other.'),
    ('<h3>Dinheiro nunca é número quebrado</h3>', '<h3>Money is never a fractional number</h3>'),
    ('Ponto flutuante erra centavo, e centavo errado em folha de pagamento é problema\n'
     '            trabalhista. Guardo valor como <strong>inteiro</strong> e percentual como\n'
     '            <strong>ponto-base</strong>, do banco até a tela.',
     'Floating point loses cents, and a wrong cent in payroll is a labour dispute. I store\n'
     '            amounts as <strong>integers</strong> and percentages as <strong>basis\n'
     '            points</strong>, from the database to the screen.'),
    ('Centavos no Distribuição Financeira e no Eventa Pro · pence em BigInt no GetMoto ·\n'
     '            ponto-base no Alcance',
     'Cents in Distribuição Financeira and Eventa Pro · pence as BigInt in GetMoto ·\n'
     '            basis points in Alcance'),
    ('<h3>O passado não se reescreve</h3>', '<h3>The past does not get rewritten</h3>'),
    ('Mudar uma regra hoje não pode alterar o que já fechou. O resultado do período é\n'
     '            <strong>congelado num retrato imutável</strong>, e cancelar cria um lançamento\n'
     '            contrário em vez de apagar o original.',
     'Changing a rule today cannot alter what already closed. The period result is\n'
     '            <strong>frozen into an immutable snapshot</strong>, and cancelling posts an opposite\n'
     '            entry instead of deleting the original.'),
    ('Snapshot por competência no Saúde Brasil 360 e no Distribuição Financeira ·\n'
     '            estorno por lançamento reverso no GetMoto · taxa congelada no Eventa Pro',
     'Per-period snapshots in Saúde Brasil 360 and Distribuição Financeira · reversal entries\n'
     '            in GetMoto · fee frozen at payment time in Eventa Pro'),
    ('<h3>O servidor não confia no cliente</h3>', '<h3>The server does not trust the client</h3>'),
    ('Valor que chega de fora é entrada, não verdade. Totais são\n'
     '            <strong>recalculados no servidor</strong> na hora de gravar, e o escopo de quem pode\n'
     '            ver o quê é resolvido pelo usuário autenticado — nunca por um parâmetro da requisição.',
     'A value arriving from outside is input, not truth. Totals are\n'
     '            <strong>recomputed on the server</strong> at write time, and who can see what is\n'
     '            resolved from the authenticated user — never from a request parameter.'),
    ('Recálculo na confirmação de importação no Alcance · escopo de tenant em middleware no\n'
     '            Atende Fácil · preço refeito no checkout do Eventa Pro',
     'Recalculation on import confirmation in Alcance · tenant scope in middleware in Atende\n'
     '            Fácil · price rebuilt at checkout in Eventa Pro'),
    ('<h3>A regra que não pode falhar mora no banco</h3>',
     '<h3>The rule that cannot fail lives in the database</h3>'),
    ('Sob concorrência real, checagem na aplicação perde. Uma vaga, um chamado aberto por\n'
     '            conversa, uma execução viva de robô: garantia de verdade é\n'
     '            <strong>transação, índice único parcial e trigger</strong>.',
     'Under real concurrency, an application-level check loses. One seat, one open ticket per\n'
     '            conversation, one live bot execution: the real guarantee is a\n'
     '            <strong>transaction, a partial unique index and a trigger</strong>.'),
    ('Índices parciais escritos à mão no Atende Fácil · reserva de vaga em transação no\n'
     '            Eventa Pro · histórico append-only por trigger',
     'Hand-written partial indexes in Atende Fácil · seat hold inside a transaction in Eventa\n'
     '            Pro · append-only history through a trigger'),

    # ---- stack ----
    ('<h3>Linguagem</h3>', '<h3>Language</h3>'),
    ('<h3>Dados</h3>', '<h3>Data</h3>'),
    ('<h3>Testes &amp; Infra</h3>', '<h3>Testing &amp; Infra</h3>'),
    ('O que realmente uso no dia a dia, não uma lista de tudo que já vi.',
     'What I actually use day to day, not a list of everything I have seen.'),

    # ---- contato ----
    ('<span class="num-secao">05</span>Vamos conversar',
     '<span class="num-secao">05</span>Let us talk'),
    ('Disponível para projetos e oportunidades. Respondo rápido.',
     'Available for projects and opportunities. I reply quickly.'),
    ('<p>Carlos Henrique · Desenvolvedor Full Stack</p>',
     '<p>Carlos Henrique · Full Stack Developer</p>'),
]

# palavras que sobrando indicam traducao esquecida
SUSPEITAS = ['ção', 'ções', 'não ', 'uma ', ' que ', ' para ', ' com ', 'ário', 'Módulos']


def gerar():
    origem = io.open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
    s = origem

    for de, para in TEXTOS:
        if de not in s:
            print(f'  ! nao encontrei: {de[:70]}...')
            continue
        s = s.replace(de, para)

    for de, para in CAMINHOS:
        s = s.replace(de, para)

    # o JSON-LD da home tem versao propria em ingles
    ini = s.index('<script type="application/ld+json">')
    fim = s.index('</script>', ini) + len('</script>')
    s = s[:ini] + JSONLD_EN + s[fim:]

    destino = os.path.join(RAIZ, 'en')
    os.makedirs(destino, exist_ok=True)
    with io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(s)

    # relatorio de sobras: linhas de texto visivel ainda em portugues
    sobras = []
    for linha in s.split('\n'):
        t = re.sub(r'<[^>]+>', '', linha).strip()
        if not t or t.startswith(('http', '{', '"', '}')):
            continue
        if any(p in t for p in SUSPEITAS):
            sobras.append(t[:90])

    print('en/index.html gerado')
    if sobras:
        print(f'\n{len(sobras)} trecho(s) possivelmente sem traducao:')
        for t in sobras[:15]:
            print('   ', t)
    else:
        print('nenhum trecho suspeito em portugues')


JSONLD_EN = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://kralluz.github.io/#carlos",
      "name": "Carlos Henrique",
      "alternateName": "kralluz",
      "jobTitle": "Full Stack Developer",
      "description": "Full stack developer and systems architect. Builds public-health indicator dashboards, citizen-service platforms for city halls and financial management systems in production.",
      "url": "https://kralluz.github.io/en/",
      "image": "https://kralluz.github.io/assets/perfil.jpg",
      "sameAs": [
        "https://github.com/kralluz",
        "https://www.linkedin.com/in/carlosklz/",
        "https://www.instagram.com/klz.carlos/"
      ],
      "knowsLanguage": ["pt-BR", "en"],
      "knowsAbout": [
        "TypeScript", "React", "React Native", "Node.js", "NestJS", "Express",
        "Prisma", "PostgreSQL", "Expo", "Docker", "multi-tenant architecture",
        "financial systems", "digital public health", "govtech"
      ],
      "alumniOf": [
        { "@type": "EducationalOrganization", "name": "Kenzie Academy Brasil" },
        { "@type": "EducationalOrganization", "name": "Instituto Federal Goiano" }
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://kralluz.github.io/en/#site",
      "url": "https://kralluz.github.io/en/",
      "name": "Carlos Henrique — Portfolio",
      "description": "Full stack developer and systems architect. Public-health indicator dashboards, citizen-service platforms for city halls and management systems in production.",
      "inLanguage": "en",
      "author": { "@id": "https://kralluz.github.io/#carlos" }
    },
    {
      "@type": "ProfilePage",
      "@id": "https://kralluz.github.io/en/#pagina",
      "url": "https://kralluz.github.io/en/",
      "name": "Carlos Henrique — Full Stack Developer",
      "inLanguage": "en",
      "isPartOf": { "@id": "https://kralluz.github.io/en/#site" },
      "about": { "@id": "https://kralluz.github.io/#carlos" },
      "hasPart": [
        {
          "@type": "SoftwareApplication",
          "name": "Saude Brasil 360",
          "url": "https://kralluz.github.io/en/projects/saude-brasil-360.html",
          "description": "Calculates and proves the primary-care indicators required by the Brazilian Ministry of Health from each city hall's electronic health record.",
          "applicationCategory": "BusinessApplication",
          "operatingSystem": "Web",
          "author": { "@id": "https://kralluz.github.io/#carlos" }
        },
        {
          "@type": "SoftwareApplication",
          "name": "Atende Facil",
          "url": "https://kralluz.github.io/en/projects/atende-facil.html",
          "description": "Citizen-service platform for city halls: multi-channel WhatsApp, tickets with protocol, Kanban board and a visual service bot.",
          "applicationCategory": "BusinessApplication",
          "operatingSystem": "Web",
          "author": { "@id": "https://kralluz.github.io/#carlos" }
        },
        {
          "@type": "SoftwareApplication",
          "name": "Alcance",
          "url": "https://kralluz.github.io/en/projects/alcance.html",
          "description": "Contract and commission management for a benefits broker, with OCR-based billing import.",
          "applicationCategory": "BusinessApplication",
          "operatingSystem": "Web",
          "author": { "@id": "https://kralluz.github.io/#carlos" }
        },
        {
          "@type": "SoftwareApplication",
          "name": "Distribuicao Financeira",
          "url": "https://kralluz.github.io/en/projects/distribuicao-financeira.html",
          "description": "Offline-first Android personal budgeting app, published on Google Play.",
          "applicationCategory": "FinanceApplication",
          "operatingSystem": "Android",
          "author": { "@id": "https://kralluz.github.io/#carlos" }
        },
        {
          "@type": "SoftwareApplication",
          "name": "Eventa Pro",
          "url": "https://kralluz.github.io/en/projects/eventa-pro.html",
          "description": "Running-event sign-up platform with price tiers, payment, QR-code tickets and organiser payouts.",
          "applicationCategory": "BusinessApplication",
          "operatingSystem": "Web",
          "author": { "@id": "https://kralluz.github.io/#carlos" }
        },
        {
          "@type": "SoftwareApplication",
          "name": "CRM GetMoto",
          "url": "https://kralluz.github.io/en/projects/crm-getmoto.html",
          "description": "Motorcycle workshop management in the United Kingdom: work orders, stock, cash book and payroll.",
          "applicationCategory": "BusinessApplication",
          "operatingSystem": "Web",
          "author": { "@id": "https://kralluz.github.io/#carlos" }
        }
      ]
    }
  ]
}
</script>'''


if __name__ == '__main__':
    gerar()

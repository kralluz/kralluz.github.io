# Baixa os logos das tecnologias do Devicon (logos originais coloridos) e gera:
#   - assets/tec/*.svg  : um arquivo por tecnologia
#   - icones_stack.txt  : o HTML pronto da secao Stack
#
# Tudo local: o site nao depende de CDN nenhuma.
# Para acrescentar tecnologia, adicione em TECNOLOGIAS e rode de novo.
#
# Os nomes seguem o padrao do Devicon: pasta/arquivo-variante.svg
# Catalogo completo: https://devicon.dev

import os, io, urllib.request

CDN = 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{}.svg'

# (caminho no devicon, nome do arquivo local, nome exibido)
TECNOLOGIAS = {
    'Linguagem': [
        ('typescript/typescript-original',   'typescript',   'TypeScript'),
        ('javascript/javascript-original',   'javascript',   'JavaScript'),
    ],
    'Frontend': [
        ('react/react-original',             'react',        'React'),
        ('vitejs/vitejs-original',           'vite',         'Vite'),
        ('nextjs/nextjs-original',           'nextjs',       'Next.js'),
        ('antdesign/antdesign-original',     'antdesign',    'Ant Design'),
        ('reactquery/reactquery-original',   'reactquery',   'TanStack Query'),
        ('tailwindcss/tailwindcss-original', 'tailwind',     'TailwindCSS'),
    ],
    'Backend': [
        ('nodejs/nodejs-original',           'nodejs',       'Node.js'),
        ('nestjs/nestjs-original',           'nestjs',       'NestJS'),
        ('express/express-original',         'express',      'Express'),
        ('prisma/prisma-original',           'prisma',       'Prisma'),
    ],
    'Mobile': [
        ('react/react-original',             'react',        'React Native'),
        ('expo/expo-original',               'expo',         'Expo'),
    ],
    'Dados': [
        ('postgresql/postgresql-original',   'postgresql',   'PostgreSQL'),
    ],
    'Testes &amp; Infra': [
        ('vitest/vitest-original',           'vitest',       'Vitest'),
        ('jest/jest-plain',                  'jest',         'Jest'),
        ('docker/docker-original',           'docker',       'Docker'),
        ('vercel/vercel-original',           'vercel',       'Vercel'),
        ('jsonwebtokens/jsonwebtokens-original', 'jwt',      'JWT'),
        ('swagger/swagger-original',         'swagger',      'Swagger'),
    ],
}


def baixar(caminho, destino):
    with urllib.request.urlopen(CDN.format(caminho), timeout=25) as r:
        if r.status != 200:
            raise ValueError(f'HTTP {r.status}')
        svg = r.read().decode('utf-8')
    with io.open(destino, 'w', encoding='utf-8') as f:
        f.write(svg)
    return len(svg)


def gerar():
    base = os.path.dirname(os.path.abspath(__file__))
    pasta = os.path.join(base, 'assets', 'tec')
    os.makedirs(pasta, exist_ok=True)

    baixados, falhas = set(), []

    for itens in TECNOLOGIAS.values():
        for caminho, arquivo, nome in itens:
            if arquivo in baixados:
                continue
            destino = os.path.join(pasta, f'{arquivo}.svg')
            try:
                tam = baixar(caminho, destino)
                baixados.add(arquivo)
                print(f'  {arquivo:12} {tam:>6}B')
            except Exception as e:
                falhas.append((arquivo, caminho, str(e)[:50]))
                print(f'  {arquivo:12} FALHOU  ({caminho})')

    # monta o HTML da secao
    blocos, atraso = [], 0
    for grupo, itens in TECNOLOGIAS.items():
        linhas = ''.join(
            f'''
            <li>
              <img src="assets/tec/{arquivo}.svg" alt="" width="28" height="28" loading="lazy">
              {nome}
            </li>''' for _, arquivo, nome in itens
            if arquivo in baixados)
        atr = f' data-atraso="{atraso}"' if atraso else ''
        blocos.append(f'''        <div class="stack-bloco revelar"{atr}>
          <h3>{grupo}</h3>
          <ul class="stack stack-icones">{linhas}
          </ul>
        </div>''')
        atraso += 70

    with io.open(os.path.join(base, 'icones_stack.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(blocos))

    print(f'\n{len(baixados)} icones em assets/tec/')
    if falhas:
        print(f'\n{len(falhas)} falha(s) — confira o caminho em devicon.dev:')
        for a, c, e in falhas:
            print(f'  {a}: {c} ({e})')


if __name__ == '__main__':
    gerar()

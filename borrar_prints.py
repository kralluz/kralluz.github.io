# Borra as areas com dado pessoal nos prints do painel, mantendo a estrutura da
# tela intacta (filtros, colunas, graficos, botoes).
# Rode de novo se trocar algum print: python borrar_prints.py

import os, subprocess, sys

FFMPEG = (r"C:\Users\Carlos Henrique\AppData\Local\Microsoft\WinGet\Packages"
          r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
          r"\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe")

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'prints')

# arquivo -> lista de regioes (x, y, largura, altura) a borrar
ALVOS = {
    'vacinas.png': [
        (245, 552, 440, 440),    # coluna Cidadao (nome + nascimento) e CNS/CPF
    ],
    'mapa-visitas.png': [
        (520, 700, 700, 288),    # Morador, Documentos (CNS/Nasc) e nome da ACS
    ],
    'bpa.png': [
        (556, 428, 300, 570),    # coluna Paciente
        (1396, 428, 340, 570),   # coluna Profissional (nome + CNS)
    ],
    'absenteismo.png': [
        (722, 715, 350, 101),    # coluna Cidadao (nome + CNS + telefone)
    ],
    # Atende Facil — a lista de conversas mostra nome, telefone e foto de perfil
    'af-conversas.png': [
        (108, 310, 520, 690),    # avatares, nomes e numeros dos contatos
    ],
    # Alcance — a trilha de auditoria mostra nome e e-mail corporativo de quem operou
    # GetMoto — placa de veiculo identifica o proprietario (dado pessoal sob GDPR)
    'gm-veiculos.png': [
        (482, 388, 140, 610),    # coluna Placa
    ],
    'gm-ordens.png': [
        (632, 462, 180, 535),    # coluna Cliente (a placa e o identificador)
        (822, 462, 240, 535),    # coluna Veiculo (repete a placa no subtexto)
    ],
    'alc-contratos.png': [
        (280, 205, 480, 360),    # coluna Cliente (razao social de clientes reais)
    ],
    'alc-auditoria.png': [
        (1572, 200, 320, 790),   # coluna Usuario (nome + email)
    ],
}


def borrar(arquivo, regioes):
    entrada = os.path.join(PASTA, arquivo)
    saida = os.path.join(PASTA, 'tmp_' + arquivo)
    if not os.path.exists(entrada):
        print(f'  ! nao encontrado: {arquivo}')
        return False

    # monta o filtro: para cada regiao, recorta, borra forte e sobrepoe no original
    partes, ultimo = [], '[0:v]'
    for i, (x, y, w, h) in enumerate(regioes):
        a, b = f'[base{i}]', f'[bl{i}]'
        partes.append(f'{ultimo}split[cp{i}]{a}')
        partes.append(f'[cp{i}]crop={w}:{h}:{x}:{y},boxblur=18:2{b}')
        prox = f'[out{i}]'
        partes.append(f'{a}{b}overlay={x}:{y}{prox}')
        ultimo = prox
    filtro = ';'.join(partes)
    # o ultimo rotulo precisa virar a saida
    filtro = filtro.rsplit(prox, 1)[0] + prox

    r = subprocess.run(
        [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', entrada,
         '-filter_complex', filtro, '-map', prox, saida],
        capture_output=True, text=True)

    if r.returncode != 0 or not os.path.exists(saida):
        print(f'  ! falhou: {arquivo} — {r.stderr.strip()[:120]}')
        return False

    os.replace(saida, entrada)
    print(f'  {arquivo:20} {len(regioes)} regiao(oes) borrada(s)')
    return True


if __name__ == '__main__':
    ok = sum(borrar(a, r) for a, r in ALVOS.items())
    print(f'\n{ok}/{len(ALVOS)} prints tratados')

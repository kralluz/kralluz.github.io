# Prompt para levantar detalhes de um projeto

**Como usar:** abra o Claude Code **dentro da pasta do projeto** e cole o bloco abaixo.
Ao terminar, ele gera um arquivo `LEVANTAMENTO.md` na raiz — traga o conteúdo de volta
para eu transformar na página do portfólio.

Repita em cada projeto: Saúde Brasil 360, Atende Fácil, Alcance, Distribuição Financeira,
Eventa Pro e CRM GetMoto.

---

## 📋 O PROMPT (copie daqui para baixo)

```
Faça um levantamento técnico deste projeto para alimentar meu portfólio profissional.

Explore o código de verdade antes de responder — não deduza pelo nome das pastas.
Leia package.json, o schema do banco, as rotas/controllers, as telas e o README.
Se for monorepo (api + web + app), cubra todas as partes.

Escreva o resultado em LEVANTAMENTO.md na raiz, exatamente nesta estrutura:

## 1. O que o produto faz
Três a cinco linhas, em linguagem de negócio, como se explicasse para o cliente que paga.
Nada de jargão técnico aqui.

## 2. Quem usa
Os perfis de usuário do sistema (ex.: admin, gestor municipal, atendente, cidadão).
Se houver controle de acesso por papel, liste os papéis reais que encontrar no código.

## 3. Módulos
Liste TODOS os módulos/funcionalidades que encontrar, um por linha, no formato:
- **Nome do módulo** — o que ele resolve, em uma frase
Baseie-se nas rotas, nas telas e nos models. Seja exaustivo: quero o mapa completo.

## 4. Arquitetura
- Estrutura de pastas (monorepo? camadas? padrão usado)
- Como as partes conversam (REST, webhook, fila, cron)
- Decisões de arquitetura que apareçam no código (ex.: repository pattern, DTO, guards)

## 5. Stack com versões
Extraia dos package.json / requirements / go.mod as versões REAIS.
Separe por: linguagem, frontend, backend, banco, testes, infra.

## 6. Banco de dados
- Quantas tabelas/models
- As 8 a 12 entidades mais importantes e o que cada uma guarda
- Relacionamentos que revelem a complexidade do domínio

## 7. Integrações externas
APIs, serviços e sistemas de terceiros com que o projeto conversa
(ex.: gateway de pagamento, WhatsApp, sistemas de governo, storage, e-mail).

## 8. Números do projeto
Conte de verdade, rodando comandos:
- arquivos de código (sem node_modules)
- linhas de código aproximadas
- quantidade de rotas/endpoints
- quantidade de telas/páginas
- quantidade de testes
- quantidade de migrations

## 9. Desafios técnicos
Os 2 a 4 problemas mais difíceis que o código revela ter sido preciso resolver.
Procure por: lógica de cálculo complexa, tratamento de concorrência, integração
com dado sujo, performance, regra de negócio não óbvia.
Para cada um: qual era o problema e como foi resolvido.

## 10. Telas principais
Liste as telas/páginas mais importantes com o caminho do arquivo,
para eu saber onde tirar print depois.

## ⚠️ REGRAS IMPORTANTES
- NÃO inclua credenciais, tokens, .env, connection strings ou chaves de API
- NÃO inclua nome, CPF, CNPJ, telefone ou qualquer dado real de cliente/paciente
  que encontrar em seeds, fixtures ou testes — se precisar exemplificar, invente
- Se algo não existir no projeto, escreva "não se aplica" em vez de inventar
- Prefira o que está no código ao que está no README (README envelhece)

Ao final, me diga em uma linha: quantos módulos encontrou e qual a parte mais
complexa do sistema na sua avaliação.
```

---

## 💡 Dicas

**Se o projeto for monorepo separado em repositórios** (ex.: `alcance-api` e `alcance-web`
em pastas diferentes), rode na pasta-mãe que contém as duas, ou rode duas vezes e junte
os arquivos.

**Se o levantamento ficar raso**, complemente com:

```
Aprofunde o item 3: abra cada arquivo de rota/controller e liste os endpoints
por módulo. Quero ver a superfície real da API.
```

**Para o app mobile**, acrescente:

```
Liste também as telas do app por fluxo de navegação, e diga quais recursos
nativos são usados (câmera, notificação, storage, biometria).
```

---

## 📥 O que fazer com o resultado

Me traga o conteúdo do `LEVANTAMENTO.md`. Com ele eu:

1. Reescrevo a página do projeto com módulos e números reais
2. Troco as descrições genéricas por fatos verificáveis
3. Ajusto a seção "O desafio técnico" com o que o código mostra
4. Monto a lista de telas para você saber exatamente onde tirar print

Pode trazer um por vez — não precisa juntar os seis.

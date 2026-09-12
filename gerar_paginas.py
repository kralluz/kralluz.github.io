# Gera as paginas de detalhe dos projetos a partir do dicionario PROJETOS.
# Rode de novo depois de editar qualquer texto aqui: python gerar_paginas.py
# (as paginas sao sobrescritas, entao edite AQUI, nao no HTML gerado)

import os, io

PROJETOS = [
    {
        "arquivo": "saude-brasil-360.html",
        "nome": "Saúde Brasil 360",
        "etiqueta": "saúde pública",
        "resumo": "Sistema de gestão usado por prefeituras e secretarias municipais de saúde para "
                  "acompanhar, calcular e comprovar os indicadores exigidos pelo Ministério da "
                  "Saúde — de que depende o repasse do financiamento federal da Atenção Primária.",
        "papel": "Desenvolvimento full stack e arquitetura",
        "periodo": "Em produção",
        "situacao": "Ativo",
        "stack": ["TypeScript", "React 18", "Express 5", "Prisma 6", "PostgreSQL",
                  "Ant Design", "TanStack Query", "MinIO", "OpenTelemetry"],
        "numeros": [
            ("358 mil", "linhas de código"),
            ("598", "endpoints na API"),
            ("92", "tabelas no banco"),
            ("214", "migrations"),
            ("30+", "módulos"),
            ("50+", "telas"),
        ],
        "problema": "O financiamento federal da Atenção Primária (Previne Brasil) depende de "
                    "indicadores que o município precisa <strong>calcular, comprovar e atingir</strong>. "
                    "O dado existe — está espalhado no prontuário eletrônico de cada equipe — mas "
                    "chega ao gestor tarde demais e agregado demais: um percentual fechado no fim "
                    "do quadrimestre, quando não dá mais para corrigir, e que não diz <strong>quem</strong> "
                    "precisa ser atendido.",
        "solucao": [
            "Cálculo dos indicadores <strong>C1–C7</strong> da Atenção Primária conforme a nota "
            "metodológica oficial do Ministério da Saúde",
            "Indicadores de <strong>Saúde Bucal (B1–B6)</strong>, <strong>eMulti</strong> e "
            "cofinanciamento estadual",
            "<strong>Listas nominais</strong> para busca ativa — o agente sabe quem visitar hoje",
            "Geração de <strong>BPA e RAAS</strong>, os documentos oficiais de faturamento do SUS",
            "Acompanhamento <strong>parcial</strong> do quadrimestre, não só o resultado final",
            "Matriz de permissão por módulo com <strong>15 perfis</strong> de usuário e restrição "
            "geográfica por município",
        ],
        "modulos_intro": "Mais de 30 módulos, do cálculo de indicador ao faturamento do SUS.",
        "modulos": [
            ("Indicadores", [
                "Atenção Primária (C1–C7)",
                "Saúde Bucal (B1–B6)",
                "eMulti (M1–M2)",
                "Vínculo e acompanhamento territorial",
                "Componente III — qualidade",
                "Cofinanciamento estadual",
            ]),
            ("Cidadãos e território", [
                "Cadastro único de cidadãos",
                "Cadastros duplicados e unificação",
                "Integração CADSUS",
                "Gestantes de risco",
                "Idosos acamados",
                "Deficiências, etnias e Bolsa Família",
                "Controle de insulinas",
                "Mapa de visitas do ACS",
            ]),
            ("Faturamento SUS", [
                "BPA individual e consolidado",
                "RAAS por competência",
                "Tabela SIGTAP",
            ]),
            ("Operação", [
                "Atendimento nominal",
                "Atividade coletiva",
                "Absenteísmo",
                "Fila de atendimento",
                "Vacinas e busca ativa",
                "Encaminhamentos",
                "Próteses dentárias",
            ]),
            ("Gestão e suporte", [
                "Mensalidades e financeiro",
                "Chamados em kanban",
                "Notificações por WhatsApp",
                "Pesquisa de satisfação",
                "Certificados",
                "Assistente de IA",
                "Auditoria e permissões (RBAC)",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> com frontend, API e um repositório de queries e normas "
            "metodológicas dos indicadores",
            "Organização <strong>feature-based</strong> nas duas pontas: cada módulo carrega suas "
            "próprias camadas (Routes → Controller → Service → Repository)",
            "<strong>Multi-tenant real</strong>: além do banco principal, o backend abre conexões "
            "dinâmicas por código IBGE para a base de e-SUS/PEC de cada prefeitura",
            "<strong>Snapshots versionados</strong> por município e competência — o indicador é "
            "publicado, não recalculado a cada acesso",
            "<strong>Eleição de líder</strong> via lock em banco para coordenar jobs agendados "
            "entre múltiplas instâncias",
            "Observabilidade com <strong>OpenTelemetry</strong>, correlation-id por requisição e "
            "log estruturado",
        ],
        "integracoes": [
            "CADSUS / DATASUS (SOAP)", "e-SUS PEC", "IBGE", "SIGTAP",
            "WhatsApp", "OpenAI", "MinIO", "Axiom",
        ],
        "desafio": [
            ("Cálculo com regra metodológica oficial",
             "Cada indicador segue nota técnica do Ministério da Saúde. Em vez de recalcular a "
             "métrica a cada acesso — o que significaria varrer a população inteira do município "
             "toda vez — criei um padrão genérico de <strong>serviço de snapshot</strong>, "
             "reaproveitado por cerca de 15 indicadores diferentes: o resultado é publicado e "
             "versionado por competência, o que dá auditoria histórica e elimina o recálculo."),
            ("Um banco de dados por prefeitura",
             "Cada município roda sua própria instância de e-SUS/PEC, com credenciais próprias. "
             "O backend precisa abrir e manter conexões separadas por código IBGE. A primeira "
             "versão criava uma conexão nova a cada requisição e vazava conexões; substituí por "
             "uma <strong>factory com cache, TTL e limite duro</strong> de conexões simultâneas."),
            ("Jobs agendados com várias instâncias no ar",
             "A aplicação roda em múltiplas instâncias sob PM2. Um cron ingênuo dispararia a "
             "sincronização noturna N vezes ao mesmo tempo. Resolvi com <strong>eleição de líder "
             "por lock em tabela</strong>, com heartbeat: só a instância dona renova o lock, e "
             "outra assume sozinha quando a líder morre."),
            ("Dado que chega sujo",
             "A base de cidadãos vinda das prefeituras tem o mesmo cidadão cadastrado mais de uma "
             "vez, com CPF ou CNS divergente. O módulo de cadastros duplicados normaliza os "
             "documentos e sinaliza os registros unificados, para a equipe do município tratar as "
             "duplicidades sem perder histórico."),
        ],
        "prints": [
            ("painel-equipe.png", "Indicadores da Atenção Primária por equipe"),
            ("rbac.png", "Matriz de permissões — 15 perfis e 47 módulos"),
            ("vacinas.png", "Busca ativa de vacinas — pendências por calendário"),
            ("bpa.png", "BPA — faturamento SUS por competência"),
            ("mapa-visitas.png", "Mapa de visitas domiciliares do ACS"),
            ("absenteismo.png", "Absenteísmo — agendamentos e comparecimento"),
        ],
    },
    {
        "arquivo": "atende-facil.html",
        "nome": "Atende Fácil",
        "etiqueta": "atendimento público",
        "resumo": "Plataforma de atendimento ao cidadão para prefeituras: reúne num só painel o "
                  "WhatsApp oficial da organização, o chamado formal com protocolo e prazo, um "
                  "quadro Kanban para a equipe e um robô de atendimento montado em tela. O "
                  "cidadão abre e acompanha a solicitação sem precisar de cadastro.",
        "papel": "Desenvolvimento full stack e arquitetura",
        "periodo": "2026 — em produção",
        "situacao": "Ativo",
        "stack": ["TypeScript", "React 18", "Express 5", "Prisma 6", "PostgreSQL",
                  "Ant Design", "TanStack Query", "React Flow", "MinIO", "OpenTelemetry"],
        "numeros": [
            ("103 mil", "linhas de código"),
            ("293", "endpoints na API"),
            ("66", "tabelas no banco"),
            ("29", "migrations"),
            ("29", "telas do painel"),
            ("97", "arquivos de teste"),
        ],
        "problema": "O cidadão manda mensagem no WhatsApp da prefeitura e a solicitação morre na "
                    "conversa: sem protocolo, sem prazo, sem setor responsável, sem ninguém "
                    "sabendo se foi resolvida. Do outro lado, o atendente abre <strong>um "
                    "aparelho por número</strong> e a gestão não tem como saber o que está em "
                    "aberto — nem provar o que foi atendido.",
        "solucao": [
            "<strong>Vários números de WhatsApp</strong> num painel só, por Z-API, Meta oficial "
            "ou Telegram, com a mesma abstração de canal",
            "<strong>Chamado com protocolo</strong> público sequencial, prazo, transferência "
            "entre setores e histórico que não pode ser reescrito",
            "<strong>Robô montado em tela</strong> — construtor visual de fluxos que responde, "
            "encaminha ou coleta dados antes do atendente entrar",
            "<strong>Portal público sem login</strong>: o cidadão abre a solicitação, anexa foto "
            "e acompanha pelo protocolo",
            "<strong>Kanban</strong> sincronizado com o status do chamado, para a equipe interna",
            "<strong>Multi-organização</strong> desde a raiz, com venda direta ou por revenda "
            "que administra a própria carteira",
        ],
        "modulos_intro": "Vinte e cinco módulos, do webhook do WhatsApp ao relatório de acesso a dado pessoal.",
        "modulos": [
            ("Atendimento", [
                "Conversas em tempo real (SSE)",
                "Notas internas que não vão ao cidadão",
                "Mensagens agendadas",
                "Respostas rápidas com anexo",
                "Contatos e bloqueio de abuso",
                "Avaliação de satisfação (NPS/CSAT)",
            ]),
            ("Chamados", [
                "Protocolo sequencial por organização",
                "Triagem, atribuição e transferência",
                "Pausa de SLA em espera de resposta",
                "Reabertura com vínculo à origem",
                "Setores e categorias",
                "Portal público do cidadão",
            ]),
            ("Automação", [
                "Motor de fluxos com editor visual",
                "Versionamento imutável do grafo",
                "Timers de inatividade",
                "URA de texto (legado)",
                "Feriados por organização",
                "Templates HSM da Meta",
            ]),
            ("Plataforma", [
                "Canais Z-API, Meta e Telegram",
                "Quadros Kanban",
                "Revendas e white-label",
                "Módulos contratuais por cliente",
                "Integração CENTI (débitos e certidões)",
                "Auditoria e relatório LGPD",
                "RBAC com 7 papéis",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> com API e painel independentes, mais a orquestração de "
            "deploy em Python via SSH e Docker",
            "Backend organizado <strong>por domínio</strong>, não por camada técnica — a máquina "
            "de estados de chamado não importa Prisma nem Express",
            "<strong>Isolamento entre organizações no banco</strong>: uma extensão do Prisma "
            "Client intercepta toda query para forçar o filtro de tenant",
            "Invariantes que o Prisma não expressa garantidos por <strong>índice único "
            "parcial</strong> escrito à mão no SQL da migration",
            "Histórico de chamado e de cartão <strong>append-only</strong>, garantido por trigger "
            "de banco",
            "Webhook dos provedores autenticado por <strong>segredo por canal</strong> (HMAC), "
            "não por JWT",
            "Credencial de canal e de integração cifrada em <strong>AES-256-CBC</strong>, nunca "
            "devolvida em resposta de API",
            "CI roda contra <strong>Postgres real</strong>, valida o schema e trava drift entre "
            "migration e modelo — deploy nunca é automático no merge",
        ],
        "integracoes": [
            "WhatsApp (Z-API)", "WhatsApp Cloud API (Meta)", "Telegram", "CENTI",
            "MinIO", "OpenTelemetry", "Axiom", "Cloudflare Tunnel",
        ],
        "desafio": [
            ("Um robô que não pode encerrar quem ainda está falando",
             "O motor de fluxo é uma máquina de estados persistida, com turno de execução, "
             "orçamento de saltos por turno (para conter um grafo em laço publicado por engano) e "
             "timers disparados por cron. O ponto difícil é o timer de inatividade: no momento do "
             "disparo ele <strong>revalida a própria razão de existir</strong>, comparando a "
             "última atividade da conversa contra a marca salva no agendamento. Assim o "
             "atendimento nunca é encerrado com a pessoa ainda escrevendo, mesmo que o "
             "cancelamento explícito do timer falhe — a revalidação é a rede primária, não o "
             "plano B. Um índice único parcial impede duas execuções vivas do mesmo robô para o "
             "mesmo cidadão, e uma rotina diária destrava as que travaram."),
            ("HTTP 200 que não significa entregue",
             "O provedor não-oficial de WhatsApp pode responder 200 com um id de mensagem e nunca "
             "entregar nada — foi o que aconteceu num incidente real: dez mensagens gravadas como "
             "enviadas que não chegaram a lugar nenhum. A regra passou a ser "
             "<strong>sem prova de entrega, o estado é FALHA</strong>: id externo vazio é tratado "
             "como falha mesmo sem exceção lançada. A ambiguidade entre telefone e LID é resolvida "
             "em cascata — o caminho barato primeiro, o caro só como fallback, com cache por canal."),
            ("A mesma pessoa em duas conversas",
             "O WhatsApp identifica o mesmo interlocutor ora pelo telefone, ora por um "
             "identificador interno (LID). Tratar os dois como threads separadas produziu o "
             "sintoma relatado como <strong>conversa partida ao meio</strong>. A correção combina "
             "dois índices únicos por canal — telefone e LID — com uma chave de idempotência de "
             "mensagem por organização, para que o mesmo evento do provedor não seja processado "
             "duas vezes quando chega por caminhos diferentes."),
            ("Isolamento que não depende de disciplina",
             "Numa plataforma onde cada município é um tenant, um <code>where</code> esquecido "
             "vaza dado de uma prefeitura para outra. A guarda é uma extensão do Prisma que "
             "injeta o filtro em toda query, e uma suíte de testes que <strong>tenta furar a "
             "própria guarda</strong> — foi assim que apareceram o <code>select</code> que omitia "
             "o campo de tenant e deixava a verificação comparar contra <code>undefined</code>, e "
             "a leitura aninhada por <code>include</code> que escapava da extensão."),
        ],
        "prints": [
            ("af-login.png", "Tela de entrada"),
            ("af-conversas.png", "Conversas — chats, fila, grupos e contatos"),
            ("af-kanban.png", "Quadro de chamados por protocolo"),
            ("af-setores.png", "Setores e roteamento por departamento"),
            ("af-mensagens.png", "Respostas rápidas por organização"),
        ],
    },
    {
        "arquivo": "alcance.html",
        "nome": "Alcance",
        "etiqueta": "gestão comercial",
        "resumo": "Sistema de gestão para administradora de benefícios: controla contratos entre "
                  "fornecedores e empresas-clientes, calcula a comissão devida a cada representante "
                  "sobre cada fatura recebida e substitui a digitação de planilhas por importação "
                  "com leitura automática de arquivo.",
        "papel": "Desenvolvimento full stack e arquitetura",
        "periodo": "2026 — em produção",
        "situacao": "Ativo",
        "stack": ["TypeScript", "React 18", "Express 5", "Prisma 6", "PostgreSQL 16",
                  "Ant Design", "TanStack Query", "Better Auth", "Tesseract", "Docker"],
        "numeros": [
            ("43,8 mil", "linhas de código"),
            ("91", "endpoints na API"),
            ("26", "tabelas no banco"),
            ("26", "migrations"),
            ("35", "telas"),
            ("62", "arquivos de teste"),
        ],
        "problema": "Contratos e comissionamento controlados em planilha. Cada fornecedor manda o "
                    "faturamento em um layout diferente — Excel, CSV, PDF, às vezes uma foto da "
                    "tela — e alguém redigita tudo à mão. Ninguém sabe quem alterou o quê, e a "
                    "divisão entre representantes depende de conta manual, com "
                    "<strong>casas decimais que a planilha arredonda e o dinheiro não</strong>.",
        "solucao": [
            "<strong>Importação com leitura automática</strong> de Excel, CSV, PDF e imagem, com "
            "OCR e reconhecimento do layout de cada fornecedor",
            "Casamento automático de cada linha com <strong>cliente e contrato</strong>, por CNPJ "
            "com fallback por nome, separando o que precisa de revisão humana",
            "Divisão de comissão entre <strong>vários representantes</strong> por contrato, com "
            "centavos que fecham",
            "<strong>Vigilância da carteira</strong>: e-mail automático quando um cliente para de "
            "faturar, um contrato se aproxima do vencimento ou falta alíquota de imposto",
            "Relatórios e demonstrativos em <strong>PDF e Excel</strong>, incluindo curva ABC de "
            "concentração de clientes",
            "<strong>Multi-tenant</strong>: várias empresas do grupo isoladas, com troca de "
            "empresa ativa e três perfis de acesso",
        ],
        "modulos_intro": "Quinze módulos, do cadastro comercial ao demonstrativo enviado por e-mail.",
        "modulos": [
            ("Comercial", [
                "Clientes, com importação em massa",
                "Transferência de cliente entre empresas",
                "Fornecedores e subgrupos",
                "Representantes comerciais",
                "Contratos com vigência e percentual",
                "Histórico de repactuação do percentual",
            ]),
            ("Financeiro", [
                "Importação de faturamento",
                "Pendências de importação",
                "Recebimentos e alíquota de imposto",
                "Comissões por representante",
                "Reprocessamento por competência",
            ]),
            ("Inteligência", [
                "Dashboard e série temporal",
                "Ranking de representantes",
                "Curva ABC de clientes",
                "Relatórios com exportação",
                "Alertas automáticos de carteira",
            ]),
            ("Administração", [
                "Empresas do grupo (workspaces)",
                "Usuários e reset de senha",
                "Matriz de acesso usuário e empresa",
                "Auditoria de alterações",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> com API e web versionadas separadamente, organização "
            "<strong>feature-based</strong> espelhada nas duas pontas",
            "Contrato de API tipado de ponta a ponta: o OpenAPI é gerado do Zod e vira tipo "
            "TypeScript no frontend via <strong>openapi-typescript</strong>",
            "<strong>Escopo multi-tenant em middleware</strong> — o servidor nunca aceita um "
            "identificador de empresa vindo do cliente, resolve sempre pelo usuário autenticado",
            "RBAC reutilizável aplicado rota a rota, com três perfis reais",
            "Cálculo financeiro isolado em <strong>funções puras</strong>, reaproveitadas por "
            "importação, recebimentos e relatórios",
            "Confirmação de importação em <strong>transação única</strong>, recalculando os "
            "valores no servidor em vez de aceitar os totais do arquivo",
            "Upload verificado por <strong>magic bytes</strong> do arquivo real, não pelo mimetype "
            "declarado, com hash SHA-256 na trilha de auditoria",
            "Cron in-process diário para alertas e reenvio de e-mails que falharam",
        ],
        "integracoes": [
            "Brevo (e-mail)", "Better Auth", "Tesseract OCR", "pdf.js",
            "GHCR", "Docker", "GitHub Actions", "Snyk",
        ],
        "desafio": [
            ("Cada fornecedor manda o arquivo de um jeito",
             "O mesmo dado chega com nome de coluna, ordem e formato diferentes — às vezes só uma "
             "foto da tela. A leitura combina três camadas: um dicionário de apelidos de coluna "
             "tolerante a erro de digitação e de OCR; um <strong>molde salvo por fornecedor</strong> "
             "que memoriza o mapeamento certo assim que é feito uma vez, de modo que a importação "
             "seguinte já entra reconhecida; e reconstrução posicional da tabela a partir do OCR, "
             "com remoção das linhas de grade que atrapalham o reconhecimento do texto."),
            ("Nunca confiar no número que veio no arquivo",
             "Cada linha é casada com cliente e contrato por CNPJ, com fallback por nome quando o "
             "OCR erra dígito, e validada contra a vigência do contrato naquela competência. O "
             "ponto crítico é o fechamento: os valores financeiros são "
             "<strong>recalculados no servidor</strong> na hora de confirmar, em vez de aceitar os "
             "totais do arquivo ou do preview aprovado — um preview manipulado ou desatualizado "
             "não vira dinheiro lançado."),
            ("Centavos que precisam fechar",
             "Quando um contrato tem vários representantes com percentuais diferentes, arredondar "
             "antes de dividir faz a soma das partes não bater com o total — o erro clássico de "
             "sistema financeiro. A divisão parte do <strong>valor não arredondado</strong> e só "
             "arredonda no fim, por representante."),
            ("Avisar sozinho sem gritar lobo",
             "A detecção de queda de faturamento roda diariamente e precisa distinguir ausência de "
             "dado de configuração legítima — <strong>alíquota 0% é um cliente cashback</strong>, "
             "não um campo em branco. Os alertas são deduplicados por chave própria de cliente e "
             "mês, e os e-mails que falham são reprocessados em silêncio em vez de se perderem."),
        ],
        "prints": [
            ("alc-dashboard.png", "Dashboard — faturado, comissão e alertas da carteira"),
            ("alc-contratos.png", "Contratos com percentual de comissão e vigência"),
            ("alc-auditoria.png", "Auditoria — rastro de quem alterou o quê, por área e operação"),
        ],
    },
    {
        "arquivo": "distribuicao-financeira.html",
        "nome": "Distribuição Financeira",
        "etiqueta": "mobile",
        "resumo": "Aplicativo de organização financeira pessoal: divide a renda do mês entre "
                  "categorias que o próprio usuário define, acompanha dívidas e despesas de casa "
                  "e fecha cada mês num retrato que não muda depois. Funciona sem internet e "
                  "sincroniza quando a conexão volta.",
        "papel": "Desenvolvimento full stack e publicação nas lojas",
        "periodo": "2026 — publicação em andamento",
        "situacao": "Em lançamento",
        "stack": ["TypeScript", "React Native 0.81", "Expo SDK 54", "NestJS 11", "Prisma 7",
                  "PostgreSQL", "SQLite", "Zod", "Sentry", "Google Play Billing"],
        "numeros": [
            ("51,7 mil", "linhas de código"),
            ("73", "endpoints na API"),
            ("25", "tabelas no banco"),
            ("27", "migrations"),
            ("24", "telas do app"),
            ("105", "arquivos de teste"),
        ],
        "problema": "Quem tenta organizar as contas em planilha desiste na terceira semana. Falta "
                    "um lugar simples para <strong>distribuir a renda</strong> por categoria, "
                    "acompanhar o que já foi pago e ver o que sobra — sem virar contabilidade. E "
                    "o app precisa funcionar <strong>no elevador, no ônibus, sem sinal</strong>, "
                    "porque é onde a conta é lançada.",
        "solucao": [
            "<strong>Rateio percentual</strong> da renda entre 6 categorias fixas e até 4 "
            "criadas pelo usuário, somando 100%",
            "<strong>Funciona offline</strong>: o lançamento entra na hora e sobe sozinho quando "
            "a conexão volta",
            "Dívidas com <strong>três formas de evolução</strong> — parcela fixa, incremento "
            "mensal em reais ou juros compostos",
            "<strong>Fechamento mensal congelado</strong> — mudar o percentual hoje não reescreve "
            "o mês passado",
            "<strong>Regras recorrentes</strong> que se repetem a cada ciclo, sem relançar à mão",
            "Assinatura pela Google Play, com teste gratuito e renovação tratada por webhook",
        ],
        "modulos_intro": "Dezoito módulos, do onboarding à sincronização offline e ao billing.",
        "modulos": [
            ("Orçamento", [
                "Distribuições (pessoal e empresa)",
                "Configuração de rateio percentual",
                "Categorias customizadas",
                "Dashboard do mês",
                "Histórico de meses fechados",
                "Regras recorrentes",
            ]),
            ("Lançamentos", [
                "Despesas de casa",
                "Renda extra parcelada",
                "Dívidas e pagamentos",
                "Quitação antecipada",
                "Lista de mercado com orçamento",
            ]),
            ("Plataforma", [
                "Sincronização offline-first",
                "Fila de operações pendentes",
                "Tela de falhas de sincronização",
                "Relato de erros do dispositivo",
                "Preferências de notificação",
            ]),
            ("Conta e billing", [
                "Autenticação e recuperação de senha",
                "Onboarding por perguntas",
                "Assinatura Google Play",
                "Exportação de dados (LGPD)",
                "Exclusão de conta agendada",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> com API NestJS e app Expo independentes, ligados por tipos "
            "gerados do OpenAPI da API",
            "Backend com <strong>guards globais</strong> — autenticação, escopo de distribuição, "
            "controle de trial e rate limit ficam fora dos controllers",
            "Validação por <strong>Zod</strong> em vez de class-validator, com o mesmo schema "
            "servindo de DTO e de documentação",
            "App com <strong>Expo Router</strong>, Context API e uma camada SQLite local no "
            "padrão <strong>outbox</strong>",
            "Escrita <strong>idempotente</strong>: cada operação carrega um id próprio, e um "
            "replay devolve a mesma resposta em vez de duplicar o lançamento",
            "<strong>Concorrência otimista</strong> por campo <code>version</code> nas entidades "
            "sincronizáveis",
            "Dinheiro em <strong>centavos inteiros</strong> e percentual em basis points — nunca "
            "ponto flutuante, em todo o schema",
            "Jobs agendados para materializar o ciclo mensal, efetivar exclusões e limpar dado "
            "antigo",
        ],
        "integracoes": [
            "Google Play Billing", "Pub/Sub RTDN", "Brevo (e-mail)", "Sentry",
            "Expo", "Maestro", "Scalar", "SQLite",
        ],
        "desafio": [
            ("O app tem que funcionar sem sinal",
             "Lançar uma despesa é coisa de trinta segundos, quase sempre longe do wi-fi. O app "
             "grava local num SQLite e enfileira a mutação num <strong>outbox</strong> com id "
             "próprio, tentativa e backoff; o backend guarda o resultado da primeira execução e "
             "devolve a mesma resposta se a operação chegar de novo. A reconciliação não é uma "
             "regra só: <strong>servidor vence por padrão</strong>, cliente vence em despesa e "
             "renda extra, e item de lista de mercado é mesclado — com a opção de desfazer um "
             "ajuste automático que o usuário não quis."),
            ("O mês que já fechou não pode mudar",
             "A base de rateio de um mês — salário mais renda extra recebida — precisa ser "
             "calculada, congelada e nunca mais mexida, mesmo que o usuário mude os percentuais "
             "em janeiro. Resolvido com um <strong>snapshot imutável</strong> materializado uma "
             "única vez por distribuição e mês, via upsert idempotente, mais um registro de "
             "ciclo que impede o fechamento de rodar duas vezes."),
            ("Três dívidas diferentes no mesmo registro",
             "Uma dívida pode ter parcela fixa, incremento fixo em centavos por mês (consórcio) "
             "ou juros compostos mensais em basis points. São três comportamentos financeiros "
             "distintos no mesmo modelo, e só um pode estar ativo por vez — uma regra que "
             "<strong>o schema garante</strong>, não o código de aplicação."),
            ("Dois aparelhos, a mesma conta",
             "O usuário pode ter mais de uma distribuição e usar o app em mais de um celular. Um "
             "guard dedicado resolve qual distribuição está em uso a cada requisição, e o campo "
             "<code>version</code> em quase toda entidade sincronizável impede que uma escrita "
             "atrasada de um aparelho <strong>sobrescreva em silêncio</strong> uma alteração "
             "mais recente feita no outro."),
        ],
        "prints": [
            "Dashboard do mês",
            "Configuração de rateio percentual",
            "Controle de dívidas",
        ],
    },
    {
        "arquivo": "eventa-pro.html",
        "nome": "Eventa Pro",
        "etiqueta": "eventos",
        "resumo": "Plataforma de eventos esportivos: inscrição de atletas, pagamento, emissão de "
                  "ingresso e painel do organizador.",
        "papel": "Arquitetura e desenvolvimento full stack",
        "periodo": "2026 — piloto",
        "situacao": "Em piloto",
        "stack": ["NestJS 11", "Prisma 7", "PostgreSQL 16", "React", "TailwindCSS", "TypeScript"],
        "problema": "Organizador de corrida controla inscrição por formulário de internet e recebe "
                    "por Pix na mão. <strong>Sem emissão de ingresso, sem controle de lote e sem "
                    "saber quem realmente pagou</strong> até conferir o extrato linha a linha.",
        "solucao": [
            "<strong>Inscrição de atletas</strong> com dados de prova e categoria",
            "Pagamento com <strong>taxa por inscrição</strong> para o organizador",
            "<strong>Emissão de ingresso</strong> e validação",
            "Painel do organizador com acompanhamento em tempo real",
        ],
        "desafio": "É a primeira operação com dinheiro de terceiro passando pela plataforma. "
                   "Cobrança, conciliação e emissão precisam funcionar na primeira corrida — "
                   "porque não existe segunda chance com o organizador que confiou.",
        "prints": [
            "Página de inscrição",
            "Checkout",
            "Painel do organizador",
        ],
    },
    {
        "arquivo": "crm-getmoto.html",
        "nome": "CRM GetMoto",
        "etiqueta": "gestão",
        "resumo": "Gestão completa de oficina de motos: ordens de serviço, estoque, fluxo de caixa "
                  "e controle de acesso por perfil.",
        "papel": "Desenvolvimento full stack",
        "periodo": "2026",
        "situacao": "Entregue",
        "stack": ["React", "TypeScript", "Express", "Prisma", "PostgreSQL", "JWT"],
        "problema": "A oficina anotava ordem de serviço em caderno. Não sabia quanto tinha em "
                    "peças, quanto entrou no mês, nem <strong>qual mecânico atendeu qual moto</strong> "
                    "quando o cliente voltava reclamando.",
        "solucao": [
            "<strong>Ordens de serviço</strong> com status, diagnóstico e profissional responsável",
            "Cadastro de motos por marca, modelo, placa e ano",
            "<strong>Estoque</strong> com categorias, preços e movimentações",
            "<strong>Fluxo de caixa</strong> com receitas, despesas e relatórios",
            "Acesso por perfil: admin, gerente, mecânico e atendente",
        ],
        "desafio": "Quem ia usar o sistema estava acostumado com caderno. A interface precisava ser "
                   "mais rápida que escrever à mão — senão o caderno vence.",
        "prints": [
            "Ordem de serviço",
            "Controle de estoque",
            "Fluxo de caixa",
        ],
    },
]


MODELO = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{nome} — Carlos Henrique</title>
<meta name="description" content="{resumo_limpo}">
<link rel="icon" href="../assets/perfil.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
<link rel="stylesheet" href="projeto.css">
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-seta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M5 12h14M13 6l6 6-6 6"/>
  </symbol>
</svg>

<div class="topo-fixo">
  <div class="container">
    <a class="voltar" href="../index.html#projetos">
      <svg class="ico"><use href="#i-seta"/></svg>
      Todos os projetos
    </a>
    <a class="btn" href="../index.html#contato">Contato</a>
  </div>
</div>

<header class="projeto-hero">
  <div class="container">
    <span class="etiqueta">{etiqueta}</span>
    <h1 class="revelar">{nome}</h1>
    <p class="projeto-resumo revelar" data-atraso="80">{resumo}</p>
    <ul class="stack revelar" data-atraso="140">{stack_html}</ul>

    <div class="fatos revelar" data-atraso="200">
      <div class="fato"><span>Papel</span><strong>{papel}</strong></div>
      <div class="fato"><span>Período</span><strong>{periodo}</strong></div>
      <div class="fato"><span>Situação</span><strong>{situacao}</strong></div>
    </div>
  </div>
</header>

<main class="conteudo">
  <div class="container">
{numeros_html}
    <h2 class="revelar">O problema</h2>
    <div class="destaque revelar" data-atraso="60">
      <p>{problema}</p>
    </div>

    <h2 class="revelar">O que foi construído</h2>
    <ul class="entregas revelar" data-atraso="60">{solucao_html}
    </ul>
{modulos_html}{arquitetura_html}{integracoes_html}
    <h2 class="revelar">Desafios técnicos</h2>
{desafios_html}

    <h2 class="revelar">Telas</h2>
    <p class="revelar">Prints do sistema em funcionamento.</p>
    <div class="galeria">{galeria_html}
    </div>

    <div class="nav-projetos">
      <a class="btn" href="../index.html#projetos">
        <svg class="ico" style="transform:rotate(180deg)"><use href="#i-seta"/></svg>
        Todos os projetos
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
    <p>Carlos Henrique · Ceres, Goiás</p>
  </div>
</footer>

<script src="../script.js"></script>
</body>
</html>
"""


def limpa(txt):
    """tira as tags do texto para usar em atributo meta"""
    return (txt.replace('<strong>', '').replace('</strong>', '')
               .replace('"', "'"))


def gerar():
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projetos')
    os.makedirs(pasta, exist_ok=True)

    for i, p in enumerate(PROJETOS):
        prox = PROJETOS[(i + 1) % len(PROJETOS)]

        stack_html = ''.join(f'<li>{t}</li>' for t in p['stack'])

        solucao_html = ''.join(
            f'\n      <li>{item}</li>' for item in p['solucao'])

        # cada print vira uma figura com espaco reservado ate a imagem existir.
        # para publicar: troque o div.vaga-print por <img src="../assets/nome.png" alt="...">
        # --- blocos opcionais: so aparecem se o projeto tiver os dados ---
        numeros_html = ''
        if p.get('numeros'):
            cartoes = ''.join(f'''
        <div class="num-cartao">
          <strong>{v}</strong>
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
    <h2 class="revelar">Módulos</h2>
    <p class="revelar">{p.get('modulos_intro', '')}</p>
    <div class="modulos">{grupos}
    </div>
'''

        arquitetura_html = ''
        if p.get('arquitetura'):
            itens = ''.join(f'\n      <li>{a}</li>' for a in p['arquitetura'])
            arquitetura_html = f'''
    <h2 class="revelar">Arquitetura</h2>
    <ul class="entregas revelar">{itens}
    </ul>
'''

        integracoes_html = ''
        if p.get('integracoes'):
            chips = ''.join(f'<li>{i}</li>' for i in p['integracoes'])
            integracoes_html = f'''
    <h2 class="revelar">Integrações</h2>
    <p class="revelar">Sistemas externos com que o produto conversa.</p>
    <ul class="stack revelar">{chips}</ul>
'''

        # desafios: lista de (titulo, texto) ou string unica (formato antigo)
        if isinstance(p['desafio'], str):
            desafios_html = f'    <p class="revelar">{p["desafio"]}</p>'
        else:
            desafios_html = ''.join(f'''
    <div class="desafio revelar">
      <h3>{titulo}</h3>
      <p>{texto}</p>
    </div>''' for titulo, texto in p['desafio'])

        # cada print pode ser so a legenda (vaga reservada) ou (arquivo, legenda)
        figuras = []
        for item in p['prints']:
            if isinstance(item, tuple):
                arq, legenda = item
                figuras.append(f'''
      <figure>
        <a href="../assets/prints/{arq}" target="_blank" rel="noopener">
          <img src="../assets/prints/{arq}" alt="{legenda}" loading="lazy">
        </a>
        <figcaption>{legenda}</figcaption>
      </figure>''')
            else:
                figuras.append(f'''
      <figure>
        <div class="vaga-print">adicione aqui:<br>{item}</div>
        <figcaption>{item}</figcaption>
      </figure>''')
        galeria_html = ''.join(figuras)

        html = MODELO.format(
            nome=p['nome'],
            etiqueta=p['etiqueta'],
            resumo=p['resumo'],
            resumo_limpo=limpa(p['resumo']),
            papel=p['papel'],
            periodo=p['periodo'],
            situacao=p['situacao'],
            stack_html=stack_html,
            problema=p['problema'],
            solucao_html=solucao_html,
            desafios_html=desafios_html,
            numeros_html=numeros_html,
            modulos_html=modulos_html,
            arquitetura_html=arquitetura_html,
            integracoes_html=integracoes_html,
            galeria_html=galeria_html,
            proximo_arquivo=prox['arquivo'],
            proximo_nome=prox['nome'],
        )

        destino = os.path.join(pasta, p['arquivo'])
        with io.open(destino, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  {p['arquivo']}")

    print(f"\n{len(PROJETOS)} paginas geradas em projetos/")


if __name__ == '__main__':
    gerar()

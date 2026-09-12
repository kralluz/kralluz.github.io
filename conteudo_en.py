# Traducao do conteudo dos projetos para ingles.
# Chaveado pelo nome do arquivo em PROJETOS (gerar_paginas.py).
# So os campos de texto aparecem aqui: numeros, stack, integracoes, prints e
# loja sao reaproveitados do portugues quando nao houver traducao.

PROJETOS_EN = {

    # =====================================================================
    "saude-brasil-360.html": {
        "etiqueta": "public health",
        "resumo": "Management system used by Brazilian city halls and municipal health "
                  "departments to track, calculate and prove the indicators required by the "
                  "Ministry of Health — the ones federal primary-care funding depends on.",
        "papel": "Full stack development and architecture",
        "periodo": "In production",
        "situacao": "Active",
        "numeros": [
            ("358k", "lines of code"),
            ("598", "API endpoints"),
            ("92", "database tables"),
            ("214", "migrations"),
            ("30+", "modules"),
            ("50+", "screens"),
        ],
        "problema": "Federal primary-care funding depends on indicators each municipality has to "
                    "<strong>calculate, prove and hit</strong>. The data exists — scattered across "
                    "every team's electronic health record — but reaches the manager too late and "
                    "too aggregated: a single percentage closed at the end of the term, when "
                    "nothing can be fixed any more, and which never says <strong>who</strong> "
                    "still needs care.",
        "solucao": [
            "Calculation of the <strong>C1–C7</strong> primary-care indicators following the "
            "Ministry of Health's official methodology",
            "<strong>Oral health (B1–B6)</strong>, <strong>multi-professional teams</strong> and "
            "state co-funding indicators",
            "<strong>Named patient lists</strong> for outreach — the health agent knows who to "
            "visit today",
            "Generation of <strong>BPA and RAAS</strong>, the official billing documents of the "
            "Brazilian public health system",
            "<strong>Partial</strong> tracking through the term, not just the closing result",
            "Per-module permission matrix with <strong>15 user profiles</strong> and geographic "
            "restriction by municipality",
        ],
        "modulos_intro": "More than 30 modules, from indicator calculation to public-health billing.",
        "modulos": [
            ("Indicators", [
                "Primary care (C1–C7)",
                "Oral health (B1–B6)",
                "Multi-professional teams (M1–M2)",
                "Territorial tracking",
                "Component III — quality",
                "State co-funding",
            ]),
            ("Citizens and territory", [
                "Single citizen registry",
                "Duplicate records and merging",
                "National health card integration",
                "High-risk pregnancies",
                "Homebound elderly",
                "Disabilities, ethnicity and welfare data",
                "Insulin control",
                "Home-visit mapping",
            ]),
            ("Public health billing", [
                "Individual and consolidated BPA",
                "RAAS per period",
                "Official procedure table",
            ]),
            ("Operations", [
                "Named appointments",
                "Group activities",
                "No-show tracking",
                "Service queue",
                "Vaccines and outreach",
                "Referrals",
                "Dental prosthetics",
            ]),
            ("Management and support", [
                "Billing and finance",
                "Kanban ticketing",
                "WhatsApp notifications",
                "Satisfaction surveys",
                "Certificates",
                "AI assistant",
                "Audit trail and permissions (RBAC)",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> with frontend, API and a dedicated repository for indicator "
            "queries and methodology",
            "<strong>Feature-based</strong> organisation on both ends: each module carries its own "
            "layers (Routes → Controller → Service → Repository)",
            "<strong>Real multi-tenancy</strong>: beyond the main database, the backend opens "
            "dynamic connections per municipality code to each city's health-record database",
            "<strong>Versioned snapshots</strong> per municipality and period — the indicator is "
            "published, not recomputed on every request",
            "<strong>Leader election</strong> via a database lock to coordinate scheduled jobs "
            "across multiple instances",
            "Observability with <strong>OpenTelemetry</strong>, per-request correlation id and "
            "structured logging",
        ],
        "desafio": [
            ("Calculation bound to official methodology",
             "Every indicator follows a technical note from the Ministry of Health. Instead of "
             "recomputing the metric on every request — which would mean scanning the entire "
             "municipal population each time — I built a generic <strong>snapshot service</strong> "
             "pattern, reused by around 15 different indicators: the result is published and "
             "versioned per period, which gives historical auditability and removes the recompute."),
            ("One database per city hall",
             "Each municipality runs its own health-record instance with its own credentials. The "
             "backend has to open and keep separate connections per municipality code. The first "
             "version created a fresh connection on every request and leaked them; I replaced it "
             "with a <strong>factory with cache, TTL and a hard cap</strong> on concurrent "
             "connections."),
            ("Scheduled jobs with several instances running",
             "The application runs across multiple instances under a process manager. A naive cron "
             "would fire the nightly sync N times at once. Solved with <strong>leader election via "
             "a table lock</strong> and a heartbeat: only the owning instance renews the lock, and "
             "another takes over on its own when the leader dies."),
            ("Data that arrives dirty",
             "The citizen base coming from city halls has the same person registered more than "
             "once, with conflicting national ids. The duplicate-records module normalises the "
             "documents and flags merged records so the municipal team can resolve duplicates "
             "without losing history."),
        ],
        "prints": [
            ("painel-equipe.png", "Primary-care indicators by health team"),
            ("rbac.png", "Permission matrix — 15 profiles across 47 modules"),
            ("vacinas.png", "Vaccine outreach — pending doses by schedule"),
            ("bpa.png", "Public health billing per period"),
            ("mapa-visitas.png", "Home-visit map for community health agents"),
            ("absenteismo.png", "No-show tracking — bookings versus attendance"),
        ],
    },

    # =====================================================================
    "atende-facil.html": {
        "etiqueta": "citizen services",
        "resumo": "Citizen-service platform for city halls: it brings the organisation's official "
                  "WhatsApp numbers, formal tickets with protocol and deadline, a Kanban board for "
                  "the team and a visually built service bot into a single panel. Citizens open "
                  "and track requests without signing up.",
        "papel": "Full stack development and architecture",
        "periodo": "2026 — in production",
        "situacao": "Active",
        "numeros": [
            ("103k", "lines of code"),
            ("293", "API endpoints"),
            ("66", "database tables"),
            ("29", "migrations"),
            ("29", "panel screens"),
            ("97", "test files"),
        ],
        "problema": "A citizen messages the city hall's WhatsApp and the request dies inside the "
                    "conversation — no protocol, no deadline, no owner. On the other side, the "
                    "agent juggles <strong>one phone per number</strong> and management has no way "
                    "to know what is still open — or to prove what was handled.",
        "solucao": [
            "<strong>Several WhatsApp numbers</strong> in one panel, through an unofficial "
            "provider, the official Meta API or Telegram, behind the same channel abstraction",
            "<strong>Tickets with a public sequential protocol</strong>, deadline, transfer "
            "between departments and a history that cannot be rewritten",
            "<strong>A bot built on screen</strong> — a visual flow editor that answers, routes or "
            "collects data before a human takes over",
            "<strong>Public portal with no login</strong>: the citizen opens the request, attaches "
            "a photo and tracks it by protocol",
            "<strong>Kanban</strong> synchronised with ticket status for the internal team",
            "<strong>Multi-organisation</strong> from the ground up, sold directly or through "
            "resellers managing their own portfolio",
        ],
        "modulos_intro": "Twenty-five modules, from the WhatsApp webhook to the personal-data access report.",
        "modulos": [
            ("Service desk", [
                "Real-time conversations (SSE)",
                "Internal notes never sent to the citizen",
                "Scheduled messages",
                "Quick replies with attachments",
                "Contacts and abuse blocking",
                "Satisfaction survey (NPS/CSAT)",
            ]),
            ("Tickets", [
                "Sequential protocol per organisation",
                "Triage, assignment and transfer",
                "SLA pause while awaiting reply",
                "Reopening linked to the original",
                "Departments and categories",
                "Public citizen portal",
            ]),
            ("Automation", [
                "Flow engine with visual editor",
                "Immutable graph versioning",
                "Inactivity timers",
                "Legacy text menu",
                "Holiday calendar per organisation",
                "Meta message templates",
            ]),
            ("Platform", [
                "WhatsApp, Meta Cloud API and Telegram channels",
                "Kanban boards",
                "Resellers and white-label",
                "Contracted modules per customer",
                "Municipal debt-lookup integration",
                "Audit trail and privacy report",
                "RBAC with 7 roles",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> with independent API and panel, plus deploy orchestration "
            "in Python over SSH and Docker",
            "Backend organised <strong>by domain</strong>, not by technical layer — the ticket "
            "state machine imports neither Prisma nor Express",
            "<strong>Tenant isolation at the database level</strong>: a Prisma Client extension "
            "intercepts every query to force the tenant filter",
            "Invariants Prisma cannot express are enforced by <strong>partial unique indexes</strong> "
            "hand-written in the migration SQL",
            "Ticket and card history is <strong>append-only</strong>, guaranteed by a database "
            "trigger",
            "Provider webhooks authenticated by a <strong>per-channel secret</strong> (HMAC), not "
            "by JWT",
            "Channel and integration credentials encrypted with <strong>AES-256-CBC</strong>, "
            "never returned in an API response",
            "CI runs against <strong>a real Postgres</strong>, validates the schema and blocks "
            "drift between migration and model — deploy is never automatic on merge",
        ],
        "desafio": [
            ("A bot that must not hang up on someone still typing",
             "The flow engine is a state machine persisted in the database, with an execution turn, "
             "a per-turn hop budget (to contain a looping graph published by mistake) and timers "
             "fired by cron. The hard part is the inactivity timer: at fire time it "
             "<strong>revalidates its own reason to exist</strong>, comparing the conversation's "
             "last activity against the mark saved when it was scheduled. The session is never "
             "closed while the person is still writing, even if the explicit timer cancellation "
             "failed — revalidation is the primary safety net, not the fallback. A partial unique "
             "index prevents two live executions of the same bot for the same citizen, and a daily "
             "routine unsticks the ones that froze."),
            ("HTTP 200 does not mean delivered",
             "The unofficial WhatsApp provider can answer 200 with a message id and never deliver "
             "anything — which is exactly what happened in a real incident: ten messages recorded "
             "as sent that reached nobody. The rule became <strong>no proof of delivery, the state "
             "is FAILED</strong>: an empty external id counts as failure even with no exception "
             "thrown. The ambiguity between phone number and internal identifier is resolved in "
             "cascade — the cheap path first, the expensive one only as fallback, cached per "
             "channel."),
            ("The same person in two conversations",
             "WhatsApp identifies the same contact sometimes by phone number, sometimes by an "
             "internal identifier. Treating them as separate threads produced the symptom reported "
             "as <strong>a conversation split in half</strong>. The fix combines two unique indexes "
             "per channel — phone and internal id — with a per-organisation message idempotency "
             "key, so the same provider event is never processed twice when it arrives by "
             "different routes."),
            ("Isolation that does not rely on discipline",
             "On a platform where each municipality is a tenant, one forgotten <code>where</code> "
             "leaks one city hall's data into another's. The guard is a Prisma extension that "
             "injects the filter into every query, plus a test suite that <strong>actively tries to "
             "break that guard</strong> — which is how the <code>select</code> omitting the tenant "
             "field (leaving the later check comparing against <code>undefined</code>) and the "
             "nested <code>include</code> read that escaped the extension were both found."),
        ],
        "prints": [
            ("af-login.png", "Sign-in screen"),
            ("af-conversas.png", "Conversations — chats, queue, groups and contacts"),
            ("af-kanban.png", "Ticket board by protocol"),
            ("af-setores.png", "Departments and routing"),
            ("af-mensagens.png", "Quick replies per organisation"),
        ],
    },

    # =====================================================================
    "alcance.html": {
        "etiqueta": "commercial management",
        "resumo": "Management system for a benefits broker: it controls contracts between suppliers "
                  "and corporate clients, computes the commission owed to each sales rep on every "
                  "invoice received, and replaces spreadsheet data entry with an import that reads "
                  "the file itself.",
        "papel": "Full stack development and architecture",
        "periodo": "2026 — in production",
        "situacao": "Active",
        "numeros": [
            ("43.8k", "lines of code"),
            ("91", "API endpoints"),
            ("26", "database tables"),
            ("26", "migrations"),
            ("35", "screens"),
            ("62", "test files"),
        ],
        "problema": "Contracts and commissions ran on spreadsheets. Every supplier sends billing in "
                    "a different layout — Excel, CSV, PDF, sometimes a photo of a screen — and "
                    "someone retypes all of it by hand. Nobody knows who changed what, and splitting "
                    "between reps depends on manual arithmetic, with "
                    "<strong>decimal places the spreadsheet rounds and money does not</strong>.",
        "solucao": [
            "<strong>Import with automatic reading</strong> of Excel, CSV, PDF and images, with OCR "
            "and per-supplier layout recognition",
            "Automatic matching of each row to <strong>client and contract</strong>, by company id "
            "with a name fallback, separating whatever needs human review",
            "Commission split across <strong>several sales reps</strong> per contract, with cents "
            "that add up",
            "<strong>Portfolio monitoring</strong>: automatic email when a client stops billing, a "
            "contract approaches expiry or a tax rate is missing",
            "Reports and statements in <strong>PDF and Excel</strong>, including ABC analysis of "
            "client concentration",
            "<strong>Multi-tenant</strong>: several group companies isolated from each other, with "
            "workspace switching and three access roles",
        ],
        "modulos_intro": "Fifteen modules, from commercial records to the statement sent by email.",
        "modulos": [
            ("Commercial", [
                "Clients, with bulk import",
                "Client transfer between companies",
                "Suppliers and subgroups",
                "Sales representatives",
                "Contracts with term and rate",
                "Rate renegotiation history",
            ]),
            ("Finance", [
                "Billing import",
                "Import exceptions",
                "Receipts and tax rates",
                "Commission per representative",
                "Reprocessing by period",
            ]),
            ("Intelligence", [
                "Dashboard and time series",
                "Representative ranking",
                "ABC client analysis",
                "Reports with export",
                "Automatic portfolio alerts",
            ]),
            ("Administration", [
                "Group companies (workspaces)",
                "Users and password reset",
                "User-to-company access matrix",
                "Change audit trail",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> with separately versioned API and web, mirrored "
            "<strong>feature-based</strong> organisation on both ends",
            "End-to-end typed API contract: the OpenAPI spec is generated from Zod and becomes "
            "TypeScript types on the frontend via <strong>openapi-typescript</strong>",
            "<strong>Multi-tenant scoping in middleware</strong> — the server never accepts a "
            "company id coming from the client, it always resolves it from the authenticated user",
            "Reusable RBAC applied route by route, with three real roles",
            "Financial calculation isolated in <strong>pure functions</strong>, reused by import, "
            "receipts and reports",
            "Import confirmation in a <strong>single transaction</strong>, recomputing the values "
            "on the server instead of trusting the file's totals",
            "Uploads verified by the real file's <strong>magic bytes</strong>, not the declared "
            "mime type, with a SHA-256 hash on the audit trail",
            "In-process daily cron for alerts and retrying failed emails",
        ],
        "desafio": [
            ("Every supplier sends the file its own way",
             "The same data arrives with different column names, order and format — sometimes just "
             "a photo of a screen. Reading combines three layers: a dictionary of column aliases "
             "tolerant to typos and OCR errors; a <strong>per-supplier template</strong> that "
             "memorises the right mapping once it is done a single time, so the next import comes "
             "in already recognised; and positional table reconstruction from OCR, including "
             "removal of the grid lines that interfere with text recognition."),
            ("Never trust the number that came in the file",
             "Each row is matched to client and contract by company id, falling back to name when "
             "OCR misreads a digit, and validated against the contract's term for that period. The "
             "critical part is the close: financial values are <strong>recomputed on the "
             "server</strong> at confirmation time rather than accepting the totals from the file "
             "or the approved preview — a tampered or stale preview never becomes posted money."),
            ("Cents that have to add up",
             "When a contract has several representatives on different percentages, rounding before "
             "splitting makes the parts stop matching the total — the classic financial-system bug. "
             "The split starts from the <strong>unrounded value</strong> and only rounds at the "
             "end, per representative."),
            ("Raising the alarm without crying wolf",
             "Billing-drop detection runs daily and has to tell missing data apart from legitimate "
             "configuration — <strong>a 0% rate is a cashback client</strong>, not a blank field. "
             "Alerts are deduplicated by their own client-and-month key, and emails that fail are "
             "reprocessed quietly instead of being lost."),
        ],
        "prints": [
            ("alc-dashboard.png", "Dashboard — billed, commission and portfolio alerts"),
            ("alc-contratos.png", "Contracts with commission rate and term"),
            ("alc-auditoria.png", "Audit trail — who changed what, by area and operation"),
        ],
    },

    # =====================================================================
    "distribuicao-financeira.html": {
        "etiqueta": "mobile",
        "resumo": "Personal budgeting app: it splits the month's income across categories the user "
                  "defines, tracks debts and household bills, and closes each month into a snapshot "
                  "that never changes afterwards. Works offline and syncs when the connection "
                  "comes back.",
        "papel": "Full stack development and store release",
        "periodo": "2026 — live",
        "situacao": "Published on Google Play",
        "loja": {
            "url": "https://play.google.com/store/apps/details?id=com.distribuicao_financeira.app&amp;hl=en",
            "selo": "Available now for Android",
            "nome": "Get it on Google Play",
        },
        "numeros": [
            ("51.7k", "lines of code"),
            ("73", "API endpoints"),
            ("25", "database tables"),
            ("27", "migrations"),
            ("24", "app screens"),
            ("105", "test files"),
        ],
        "problema": "People who try to organise their finances in a spreadsheet quit in the third "
                    "week. What is missing is a simple place to <strong>split income</strong> by "
                    "category, follow what is already paid and see what is left — without turning "
                    "into accounting. And the app has to work <strong>in a lift, on a bus, with no "
                    "signal</strong>, because that is where the expense actually gets entered.",
        "solucao": [
            "<strong>Percentage split</strong> of income across 6 fixed categories and up to 4 the "
            "user creates, adding up to 100%",
            "<strong>Works offline</strong>: the entry lands immediately and uploads itself when "
            "the connection returns",
            "Debts with <strong>three growth rules</strong> — fixed instalment, fixed monthly "
            "increment or compound interest",
            "<strong>Frozen monthly close</strong> — changing a percentage today does not rewrite "
            "last month",
            "<strong>Recurring rules</strong> that repeat each cycle without re-entry",
            "Subscription through Google Play, with a free trial and renewal handled by webhook",
        ],
        "modulos_intro": "Eighteen modules, from onboarding to offline sync and billing.",
        "modulos": [
            ("Budget", [
                "Multiple distributions (personal and business)",
                "Percentage split configuration",
                "Custom categories",
                "Monthly dashboard",
                "History of closed months",
                "Recurring rules",
            ]),
            ("Entries", [
                "Household bills",
                "Instalment-based extra income",
                "Debts and payments",
                "Early settlement",
                "Shopping list with budget",
            ]),
            ("Platform", [
                "Offline-first synchronisation",
                "Pending operation queue",
                "Sync failure screen",
                "Device error reporting",
                "Notification preferences",
            ]),
            ("Account and billing", [
                "Authentication and password recovery",
                "Question-based onboarding",
                "Google Play subscription",
                "Data export (privacy law)",
                "Scheduled account deletion",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> with an independent NestJS API and Expo app, linked by types "
            "generated from the API's OpenAPI spec",
            "Backend with <strong>global guards</strong> — authentication, distribution scope, "
            "trial control and rate limiting live outside the controllers",
            "Validation through <strong>Zod</strong> instead of class-validator, with the same "
            "schema serving as DTO and as documentation",
            "App built on <strong>Expo Router</strong>, Context API and a local SQLite layer in the "
            "<strong>outbox</strong> pattern",
            "<strong>Idempotent writes</strong>: every operation carries its own id, and a replay "
            "returns the same response instead of duplicating the entry",
            "<strong>Optimistic concurrency</strong> through a <code>version</code> field on "
            "syncable entities",
            "Money as <strong>integer cents</strong> and percentages as basis points — never "
            "floating point, anywhere in the schema",
            "Scheduled jobs to materialise the monthly cycle, execute deletions and purge old data",
        ],
        "desafio": [
            ("The app has to work with no signal",
             "Logging an expense takes thirty seconds and almost always happens away from wifi. The "
             "app writes locally to SQLite and queues the mutation in an <strong>outbox</strong> "
             "with its own id, retry count and backoff; the backend stores the result of the first "
             "execution and returns the same response if the operation arrives again. Reconciliation "
             "is not one single rule: <strong>server wins by default</strong>, client wins for "
             "expenses and extra income, and shopping-list items are merged — with the option to "
             "undo an automatic adjustment the user did not want."),
            ("A closed month cannot change",
             "A month's distribution base — salary plus extra income received — has to be computed, "
             "frozen and never touched again, even if the user changes the percentages in January. "
             "Solved with an <strong>immutable snapshot</strong> materialised exactly once per "
             "distribution and month through an idempotent upsert, plus a cycle record that stops "
             "the close from running twice."),
            ("Three different debts in one record",
             "A debt can carry a fixed instalment, a fixed monthly increment in cents, or compound "
             "monthly interest in basis points. Three distinct financial behaviours in the same "
             "model, and only one can be active at a time — a rule <strong>the schema "
             "enforces</strong>, not the application code."),
            ("Two devices, the same account",
             "A user can have more than one distribution and use the app on more than one phone. A "
             "dedicated guard resolves which distribution is in use on each request, and a "
             "<code>version</code> field on nearly every syncable entity stops a late write from "
             "one device from <strong>silently overwriting</strong> a newer change made on the "
             "other."),
        ],
        "prints": [
            ("df-inicio.jpg", "Home — monthly income and distribution rule by category"),
            ("df-despesas.jpg", "Household bills with due date and status"),
            ("df-dividas.jpg", "Debts — instalments paid, balance and overspend warning"),
            ("df-nova-divida.jpg", "New debt: instalment, count, due day and recurrence"),
            ("df-notificacoes.jpg", "Alert preferences — lead time and delivery hour"),
        ],
    },

    # =====================================================================
    "eventa-pro.html": {
        "etiqueta": "events",
        "resumo": "Running-event platform with two sides: organisers build the event, its distances, "
                  "price tiers and coupons; runners sign up, pay by instant transfer or card, get a "
                  "digital ticket with a QR code and later download results and certificates. The "
                  "platform keeps a fee and controls the payout.",
        "papel": "Full stack development and architecture",
        "periodo": "2026 — in production",
        "situacao": "Active",
        "numeros": [
            ("47k", "lines of code"),
            ("143", "API endpoints"),
            ("19", "database tables"),
            ("19", "migrations"),
            ("71", "screens"),
            ("18", "modules"),
        ],
        "problema": "Race organisers run sign-ups through a form and take payments by hand — no "
                    "ticket, no seat control, no idea what is left after the fee. At the start "
                    "line, someone checks names on printed paper. The runner, on the other side, "
                    "has nowhere to see <strong>whether the entry actually counted</strong>.",
        "solucao": [
            "<strong>Date-based price tiers</strong> inside each distance, with seat control and "
            "discount coupons",
            "<strong>Payment by instant transfer or card</strong>, with a gateway webhook and refunds",
            "<strong>Digital ticket with a QR code</strong> — check-in and kit pickup on race day",
            "<strong>Results and PDF certificates</strong>, with public verification by number",
            "<strong>Per-event team roles</strong>: grant check-in access without opening the "
            "finances",
            "<strong>Organiser payouts</strong> with the platform fee frozen at payment time",
        ],
        "modulos_intro": "Eighteen modules, from event creation to the runner's certificate.",
        "modulos": [
            ("Organiser", [
                "Event with draft, publish and archive",
                "Distances with seats and age brackets",
                "Price tiers by date window",
                "Percentage or fixed-value coupons",
                "Custom form fields",
                "Event analytics and finance",
            ]),
            ("Runner", [
                "Catalogue and public event page",
                "Sign-up with temporary hold",
                "Checkout by instant transfer or card",
                "Ticket with QR code",
                "Race results",
                "PDF certificate",
            ]),
            ("Race day", [
                "QR check-in",
                "Kit pickup",
                "Attendance statistics",
                "Per-event team roles",
                "Bulk results import",
            ]),
            ("Platform", [
                "Admin panel",
                "Event moderation",
                "Organiser payouts",
                "Support with SLA",
                "Privacy: export and delete account",
                "Audit trail and logs",
            ]),
        ],
        "arquitetura": [
            "<strong>Monorepo</strong> with a NestJS API organised by feature module and a React "
            "front split by domain — public, participant, organiser and admin",
            "DTOs validated with <strong>Zod</strong>, and global guards for authentication, role "
            "and event ownership",
            "<strong>Provider interfaces</strong> for email and storage: SMTP can be swapped for a "
            "self-hosted server, or one image host for another, without touching the rest",
            "Frontend HTTP client <strong>generated from the OpenAPI spec</strong> published by the API",
            "Gateway webhook with <strong>per-event deduplication</strong> — the same notice "
            "arriving twice does not charge twice",
            "Money as <strong>integer cents</strong> and the fee in basis points, never decimal",
            "Recurring jobs (expire holds, reconcile payments, purge logs) running in-process, with "
            "no external queue",
        ],
        "desafio": [
            ("The last seat, two people at once",
             "Two simultaneous sign-ups for the last seat of a distance cannot both succeed. "
             "Creation runs inside a <strong>transaction that only increments the counter if a seat "
             "is still free at that instant</strong> — if the condition fails, the whole operation "
             "is rolled back. More seats than the limit are never sold, even under concurrent "
             "requests. The same mechanism protects each coupon's usage limit."),
            ("The abandoned cart that holds a seat",
             "A sign-up holds the seat for 15 minutes waiting for payment. If the runner walks "
             "away, that seat cannot stay locked forever. A routine sweeps expired holds, cancels "
             "each one <strong>with no risk of processing the same record twice</strong> and "
             "returns the seat to both the distance and the price tier, all inside a transaction."),
            ("Paid and never got the ticket",
             "Between the gateway confirming the payment and the system issuing the ticket there is "
             "a window where anything can fail. A <strong>reconciliation</strong> routine looks for "
             "confirmed payments left without a ticket and reissues idempotently. Together with "
             "webhook deduplication, the runner gets the ticket once — and always."),
            ("All the money lands in one account",
             "The gateway does not split the payment between platform and organiser, so tracking "
             "who is owed what is the system's job. The fee is computed in <strong>basis "
             "points</strong>, rounded so cents are not systematically lost, capped so it never "
             "exceeds what was charged — and <strong>frozen at payment time</strong>, so changing "
             "the fee tomorrow does not rewrite yesterday's financial history."),
        ],
        "prints": [
            "Public event page",
            "Checkout and instant payment",
            "Ticket with QR code",
        ],
    },

    # =====================================================================
    "crm-getmoto.html": {
        "etiqueta": "management",
        "resumo": "Management system for a motorcycle workshop operating in the United Kingdom. It "
                  "covers the whole cycle — vehicle, work order, stock, purchases and expenses — "
                  "and goes all the way to payroll, with everything flowing into a single cash book.",
        "papel": "Full stack development and architecture",
        "periodo": "2026 — in production",
        "situacao": "Active",
        "numeros": [
            ("50k", "lines of code"),
            ("96", "API endpoints"),
            ("18", "database tables"),
            ("39", "screens"),
            ("19", "modules"),
            ("3", "languages"),
        ],
        "problema": "The workshop tracked work orders, stock and payroll in separate places — and "
                    "none of them spoke to the cash book. There was no way to know how much margin "
                    "a work order left after the parts it consumed, nor what the month actually "
                    "closed at once suppliers, expenses and staff were paid.",
        "solucao": [
            "<strong>Work orders</strong> that add parts and labour, deduct stock and post to the "
            "cash book in the same operation",
            "<strong>A single cash book</strong> fed by sales, purchases, expenses, payroll and "
            "advances — every entry knows where it came from",
            "<strong>Payroll</strong> with time tracking, overtime, bonuses, deductions and "
            "advances offset automatically",
            "<strong>Reversal entries instead of deletes</strong>: cancelling does not erase, it "
            "posts the opposite and keeps both sides in the history",
            "<strong>Stock</strong> with automatic movements, manual adjustments and low-level alerts",
            "Interface in <strong>English, Portuguese and Spanish</strong>",
        ],
        "modulos_intro": "Nineteen modules, from opening a work order to the mechanic's payslip.",
        "modulos": [
            ("Workshop", [
                "Vehicles and per-bike history",
                "Work orders with discounts",
                "Service catalogue and categories",
                "Products and categories",
                "Work-order report by period",
                "Global search",
            ]),
            ("Stock and purchasing", [
                "Automatic movements",
                "Manual adjustment without touching cash",
                "Low-stock alerts",
                "Supplier purchase orders",
                "Position report",
            ]),
            ("Finance", [
                "Central cash book",
                "Operating expenses",
                "Summary by category",
                "Dashboard with charts",
                "PDF reporting",
            ]),
            ("People", [
                "Employee records",
                "Time tracking",
                "Payroll and payslips",
                "Salary advances",
                "Users and access roles",
            ]),
        ],
        "arquitetura": [
            "Layered backend — <strong>route → controller → service → Prisma</strong> — with Zod "
            "validation and central error handling that tells domain, schema and database errors apart",
            "Every operation touching <strong>more than one table</strong> — work order plus stock "
            "plus cash, payroll plus advances plus time entries — runs inside a transaction",
            "<strong>Soft delete</strong> and an audit trail (who created, who cancelled, why) on "
            "financial entities",
            "Reversal through a <strong>linked opposite record</strong>, never by editing the "
            "original entry",
            "Frontend with role-protected routes, per-screen code splitting, session state in "
            "Zustand and server data in TanStack Query",
            "API client <strong>generated by Orval</strong> from the backend's OpenAPI spec — "
            "frontend types come from the contract, not from hand copying",
            "Access token in browser memory and <strong>refresh in an HttpOnly cookie</strong>, "
            "with a queue for concurrent requests during renewal",
            "Multi-stage Docker with a non-root user, image on GHCR and frontend on Vercel with CSP "
            "and HSTS",
        ],
        "desafio": [
            ("Payroll does not tolerate a wrong penny",
             "Hours worked times hourly rate has to produce an exact figure, and floating point "
             "accumulates error precisely there. Every monetary value is <strong>pence in "
             "BigInt</strong>, from the schema down to the service: hours become an integer base "
             "before multiplying by the rate, and division only happens at the end. No intermediate "
             "calculation goes through <code>float</code>."),
            ("Cancel without erasing",
             "Cancelling a work order, a purchase or a payroll run cannot delete the entry — that "
             "would break the cash history — but it cannot leave the financial effect standing "
             "either. The answer is the <strong>reversal entry</strong>: a record with the opposite "
             "direction, flagged as a reversal and linked to the original, with stock and balance "
             "returned atomically. Reports keep showing both sides."),
            ("Four writes that must all hold or all fail",
             "Opening a work order validates the discount, deducts each part from stock, records "
             "the movement and posts to the cash book. If the third part has no balance, the first "
             "two cannot have left. It all runs in a <strong>single transaction</strong>, with "
             "atomic stock decrement so two simultaneous work orders never sell the same part."),
            ("Two payroll periods that touch",
             "Two payment ranges can overlap in four ways — starting inside the other, ending "
             "inside it, fully containing it, or being identical. The check uses three conditions "
             "equivalent to <strong>interval intersection</strong>, written that way because the "
             "ORM translates them better than the direct formula; the reasoning is commented right "
             "there in the code."),
        ],
        "prints": [
            ("gm-financeiro.png", "Financial dashboard — balance, inflow, outflow and cash curve"),
            ("gm-ordens.png", "Work orders with vehicle, description and assigned mechanic"),
            ("gm-servicos.png", "Service catalogue with unit cost"),
            ("gm-veiculos.png", "Registered vehicles — make, model, odometer and linked orders"),
            ("gm-estoque.png", "Stock report with inventory and movements"),
        ],
    },
}

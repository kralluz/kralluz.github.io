/* =========================================================================
   Animações do portfolio
   - revelar elementos conforme a rolagem
   - contar os números quando entram na tela
   Sem biblioteca nenhuma. Respeita quem pediu menos movimento no sistema.
   ========================================================================= */

(function () {
  'use strict';

  /* ---------------------------------------------------------------
     4. Navegação: barra de progresso, borda ao rolar e seção ativa
     --------------------------------------------------------------- */
  const nav        = document.getElementById('nav');
  const progresso  = document.getElementById('progresso');
  const linksNav   = Array.from(document.querySelectorAll('.nav-links a'));
  const secoes     = linksNav
        .map(a => document.querySelector(a.getAttribute('href')))
        .filter(Boolean);

  function aoRolar() {
    const y = window.scrollY;

    // borda da nav aparece depois dos primeiros pixels
    if (nav) nav.classList.toggle('rolou', y > 20);

    // progresso da leitura
    if (progresso) {
      const total = document.documentElement.scrollHeight - window.innerHeight;
      progresso.style.width = (total > 0 ? (y / total) * 100 : 0) + '%';
    }

    // qual seção está ativa.
    // usa getBoundingClientRect (relativo à tela) em vez de offsetTop, que é
    // relativo ao elemento pai posicionado e dava a seção errada.
    const alturaTela = window.innerHeight;
    const alturaNav  = nav ? nav.offsetHeight : 0;
    const fimDaPagina = y + alturaTela >= document.documentElement.scrollHeight - 2;

    let atual = -1;
    if (fimDaPagina) {
      // no fim da página a última seção é sempre a ativa — senão ela nunca
      // fica marcada quando não há scroll suficiente para levá-la ao topo
      atual = secoes.length - 1;
    } else {
      // escolhe a seção que ocupa mais da área útil (abaixo da nav)
      let maior = 0;
      secoes.forEach((sec, i) => {
        const r = sec.getBoundingClientRect();
        const visivel = Math.min(r.bottom, alturaTela) - Math.max(r.top, alturaNav);
        if (visivel > maior) { maior = visivel; atual = i; }
      });
    }

    linksNav.forEach((a, i) => a.classList.toggle('ativo', i === atual));
  }

  // throttle por frame: evita recalcular dezenas de vezes por segundo
  let agendado = false;
  window.addEventListener('scroll', () => {
    if (agendado) return;
    agendado = true;
    requestAnimationFrame(() => { aoRolar(); agendado = false; });
  }, { passive: true });

  aoRolar();


  const semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (semMovimento) {
    document.querySelectorAll('.revelar').forEach(el => el.classList.add('visivel'));
    document.querySelectorAll('[data-contar]').forEach(el => {
      el.textContent = el.dataset.formato || el.dataset.contar;
    });
    return;
  }

  /* ---------------------------------------------------------------
     1. Revelar na rolagem
     Cada elemento com .revelar sobe e aparece ao entrar na tela.
     O atraso em cascata vem do data-atraso (em ms).
     --------------------------------------------------------------- */
  const observadorRevelar = new IntersectionObserver((entradas) => {
    entradas.forEach(entrada => {
      if (!entrada.isIntersecting) return;
      const el = entrada.target;
      const atraso = Number(el.dataset.atraso || 0);
      setTimeout(() => el.classList.add('visivel'), atraso);
      observadorRevelar.unobserve(el);   // anima uma vez só
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -60px 0px'   // dispara um pouco antes de entrar de fato
  });

  document.querySelectorAll('.revelar').forEach(el => observadorRevelar.observe(el));


  /* ---------------------------------------------------------------
     2. Contador dos números
     Sobe de 0 até o valor, desacelerando no fim (easeOutExpo).
     --------------------------------------------------------------- */
  function animarNumero(el) {
    const alvo = Number(el.dataset.contar);
    const sufixo = el.dataset.sufixo || '';
    const duracao = 1600;
    const inicio = performance.now();

    // separador de milhar no padrão brasileiro
    const formatar = (n) => n.toLocaleString('pt-BR');

    function passo(agora) {
      const t = Math.min((agora - inicio) / duracao, 1);
      // easeOutExpo: rápido no começo, quase parado no fim
      const suave = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
      el.textContent = formatar(Math.round(alvo * suave)) + sufixo;
      if (t < 1) requestAnimationFrame(passo);
    }

    requestAnimationFrame(passo);
  }

  const observadorNumero = new IntersectionObserver((entradas) => {
    entradas.forEach(entrada => {
      if (!entrada.isIntersecting) return;
      animarNumero(entrada.target);
      observadorNumero.unobserve(entrada.target);
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-contar]').forEach(el => {
    el.textContent = '0' + (el.dataset.sufixo || '');
    observadorNumero.observe(el);
  });


  /* ---------------------------------------------------------------
     3. Brilho que segue o cursor nos cards de projeto
     Detalhe sutil: um halo acompanha o mouse dentro do card.
     --------------------------------------------------------------- */
  document.querySelectorAll('.projeto').forEach(card => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      card.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    });
  });


})();
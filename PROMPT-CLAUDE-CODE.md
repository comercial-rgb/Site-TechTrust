# PROMPT EXECUTÁVEL — Refatoração completa Site TechTrust AutoSolutions

> **Instruções para Claude Code:** Execute este prompt de cima para baixo, na ordem. Cada seção é um checkpoint. Ao terminar cada fase, rode os comandos de verificação indicados e só avance se todos passarem. Nada de criatividade fora do escopo. Nada de adicionar bibliotecas sem pedir. Preserve o i18n (EN/PT/ES). Mantenha a semântica HTML existente. Faça commits atômicos por fase.

---

## CONTEXTO DO PROJETO

- **Empresa:** TechTrust AutoSolutions LLC (Port St. Lucie, FL + operação no Brasil)
- **Setor:** Manutenção de frotas comerciais + Fleet Management Software (SaaS)
- **Público:** Gerentes de frota B2B (logística, construção, delivery)
- **Compliance:** SAM.gov (EUA) + Lei 14.133/2021 (Brasil)
- **Stack atual:** HTML estático + CSS inline + JS vanilla + Vercel + Resend + Google Calendar API
- **Arquivo principal:** `Site-TechTrust/index.html`
- **Deploy:** Vercel

## REGRAS GERAIS

1. **Não introduzir frameworks** (React, Tailwind, Vue etc.). Manter HTML/CSS/JS puro.
2. **Não quebrar o i18n** — toda string visível deve ter chave em `I18N.en`, `I18N.pt` e `I18N.es`.
3. **Não remover funcionalidades existentes** (form de contato, language switcher, links do menu).
4. **Extrair CSS e JS para arquivos separados** somente onde explicitamente pedido (Fase 3).
5. **Preservar IDs de seção** (`#home`, `#about`, `#services`, `#software`, `#industries`, `#contact`) — são usados na navegação.
6. **Criar branch antes de começar:** `git checkout -b refactor/site-v2`.
7. **Commit por fase** com mensagem `feat(site): fase N - <descrição>`.

---

# FASE 1 — Correções críticas (placeholders, assets locais, copy)

## 1.1 Remover textos de desenvolvimento vazados

No arquivo `Site-TechTrust/index.html`:

**Remover completamente** a linha:
```html
<small style="color:var(--muted);display:block;margin-top:10px">Imagens ilustrativas — trocaremos por fotos próprias e telas do Fleet Management Software.</small>
```

**Remover completamente** o parágrafo:
```html
<p style="margin:6px 0 0;color:var(--muted)">Stack recomendado: Google Workspace (Gmail, Drive, Meet). Hosting: AWS / GCP / Hostinger US.</p>
```

## 1.2 Servir assets localmente (sem dependência do GitHub raw)

Substituir todas as ocorrências no `<head>` e no `<header>`:

| De (GitHub raw) | Para (local) |
|-----------------|--------------|
| `https://raw.githubusercontent.com/comercial-rgb/Site-TechTrust/main/favicon.ico` | `/favicon.ico` |
| `https://raw.githubusercontent.com/comercial-rgb/Site-TechTrust/main/favicon-32x32.png` | `/favicon-32x32.png` |
| `https://raw.githubusercontent.com/comercial-rgb/Site-TechTrust/main/apple-touch-icon.png` | `/apple-touch-icon.png` |
| `https://raw.githubusercontent.com/comercial-rgb/Site-TechTrust/main/botao-pequeno.png` | `/botao-pequeno.png` |
| `https://raw.githubusercontent.com/comercial-rgb/Site-TechTrust/main/botao-pequeno@2x.png` | `/botao-pequeno@2x.png` |

Os arquivos já existem em `Site-TechTrust/` e `Site-TechTrust/public/`. Confirme que o `vercel.json` serve a raiz corretamente — se não, adicione rewrite.

## 1.3 Adicionar tagline oficial da marca

Dentro do hero, logo abaixo do `<h1>`, inserir:
```html
<p class="tagline" data-i18n="tagline">Driven by Technology. Trusted by You.</p>
```

Adicionar chaves de tradução em `I18N`:
- `en.tagline`: `"Driven by Technology. Trusted by You."`
- `pt.tagline`: `"Movidos por tecnologia. De confiança."`
- `es.tagline`: `"Impulsados por la tecnología. De confianza."`

## 1.4 Traduzir mensagens do formulário via i18n

No handler `form?.addEventListener('submit', ...)` substituir os `alert()` hardcoded:

```js
const t = I18N[document.documentElement.lang] || I18N.en;
alert(t.form_success.replace('{email}', data.email));
// ...
alert(t.form_error);
```

Adicionar em cada idioma:
- `en.form_success`: `"Thanks! We'll get back to you at {email}."`
- `en.form_error`: `"Could not send right now. Please try again or email contact@techtrustautosolutions.com"`
- `pt.form_success`: `"Obrigado! Entraremos em contato em {email}."`
- `pt.form_error`: `"Não foi possível enviar agora. Tente novamente ou envie para contact@techtrustautosolutions.com"`
- `es.form_success`: `"¡Gracias! Le responderemos a {email}."`
- `es.form_error`: `"No se pudo enviar ahora. Inténtelo de nuevo o escriba a contact@techtrustautosolutions.com"`

## 1.5 Criar OG image placeholder

Se `/assets/og-image.jpg` não existir, crie uma imagem 1200×630 (pode ser cópia do `hero-brand-bg.jpg` redimensionado, ou gere com Python/Pillow usando o logo `logo-horizontal-400w.png` sobre fundo `#0B1220`). Salve em `Site-TechTrust/assets/og-image.jpg`. Atualize o meta tag para o caminho correto.

## VERIFICAÇÃO FASE 1

```bash
cd Site-TechTrust
grep -c "Imagens ilustrativas" index.html       # deve retornar 0
grep -c "Stack recomendado" index.html           # deve retornar 0
grep -c "raw.githubusercontent" index.html       # deve retornar 0
grep -c "tagline" index.html                     # deve retornar >= 4
ls public/ | grep -c "og-image"                  # deve retornar >= 1 (ou em assets/)
```

**Commit:** `feat(site): fase 1 - placeholders removidos, assets locais, tagline oficial`

---

# FASE 2 — Identidade visual (paleta, tipografia, ícones)

## 2.1 Nova paleta de cores (tokens CSS)

Substituir o bloco `:root` completo por:

```css
:root {
  /* NEUTROS */
  --bg: #0B1220;
  --bg-alt: #111A2E;
  --surface: #142038;
  --surface-2: #1A2847;
  --card: #111827;
  --border: rgba(203, 213, 225, .12);
  --border-strong: rgba(203, 213, 225, .25);

  /* MARCA — AZUL COBALTO (do logo) */
  --brand-blue: #1D2B5C;
  --brand-blue-600: #2A3B7A;
  --brand-blue-500: #3A4E99;
  --brand-blue-400: #4A5FA8;
  --brand-blue-glow: rgba(74, 95, 168, .35);

  /* MARCA — VERMELHO (do logo, CTAs) */
  --brand-red: #C8102E;
  --brand-red-600: #A80D26;
  --brand-red-500: #D92D27;
  --brand-red-100: rgba(200, 16, 46, .12);
  --brand-red-glow: rgba(200, 16, 46, .4);

  /* TEXTO */
  --text: #E8ECF5;
  --text-muted: #9AA7C2;
  --silver: #CBD5E1;

  /* LAYOUT */
  --maxw: 1200px;
  --radius: 16px;
  --radius-sm: 10px;
  --shadow: 0 10px 30px rgba(2, 6, 23, .3);
  --shadow-red: 0 8px 24px rgba(200, 16, 46, .35);
  --shadow-blue: 0 8px 24px rgba(29, 43, 92, .45);

  /* LEGACY ALIASES (para não quebrar código existente durante a refatoração) */
  --accent: var(--brand-red);
  --accent-2: var(--brand-red-500);
  --muted: var(--text-muted);
}
```

## 2.2 Aplicar nova paleta aos componentes

- **CTAs primários** (`.cta`): fundo `linear-gradient(135deg, var(--brand-red), var(--brand-red-600))`, cor do texto `#FFFFFF`, sombra `var(--shadow-red)`.
- **CTAs secundários** (`.cta.secondary`): borda `1px solid var(--brand-blue-400)`, texto `var(--text)`, fundo transparente.
- **Hover em CTA primário**: `filter: brightness(1.05)` + `transform: translateY(-1px)` + `box-shadow: 0 12px 32px rgba(200,16,46,.5)`.
- **Badge do hero** (`.badge`): fundo `var(--brand-red-100)`, borda `1px solid rgba(200,16,46,.35)`, cor `#FFB0B8`.
- **Ícones** (`.icon`): fundo `linear-gradient(135deg, var(--brand-blue), var(--brand-blue-500))`, cor `#FFFFFF`, sombra `var(--shadow-blue)`.
- **Link ativo do language switcher** (`.lang button.active`): fundo `linear-gradient(135deg, var(--brand-red), var(--brand-red-600))`, cor `#FFFFFF`, borda transparente.
- **`body` gradient**: substituir por `linear-gradient(180deg, #0B1220 0%, #0F1730 60%, #0B1529 100%)`.
- **`.panel`**: substituir `radial-gradient` com ciano por `radial-gradient(1200px 600px at 80% -10%, rgba(74,95,168,.2), transparent 50%), linear-gradient(180deg, rgba(2,6,23,.6), rgba(2,6,23,.35))`.
- **`.logo` (placeholder CSS)**: remover o gradiente ciano, deixar fallback com `var(--brand-blue)`.

## 2.3 Adicionar Oswald para títulos

No `<head>`, substituir o link de fontes por:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
```

Adicionar regras:
```css
h1, h2, .section-title {
  font-family: 'Oswald', 'Montserrat', system-ui, sans-serif;
  letter-spacing: .5px;
  text-transform: uppercase;
  font-weight: 700;
}
h1 { line-height: 1.1; }
h2, .section-title { line-height: 1.15; }
.tagline {
  color: var(--brand-red-500);
  font-family: 'Oswald', Montserrat, sans-serif;
  font-weight: 600;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  font-size: .95rem;
  margin: 6px 0 18px;
}
```

## 2.4 Substituir emojis por SVG inline

Nos cards onde aparecem `🔧`, `📊`, `✅`, `⛽`, `🧰`, substituir por SVGs inline (padrão Lucide, 24px, `stroke-width:2`, `stroke:currentColor`, `fill:none`).

Criar no início do `<body>` um `<svg>` sprite escondido:
```html
<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
  <symbol id="i-wrench" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
  </symbol>
  <symbol id="i-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>
  </symbol>
  <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>
    <path d="m9 12 2 2 4-4"/>
  </symbol>
  <symbol id="i-fuel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="3" y1="22" x2="15" y2="22"/><line x1="4" y1="9" x2="14" y2="9"/>
    <path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/>
    <path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2a2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L18 5"/>
  </symbol>
  <symbol id="i-tool" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
  </symbol>
</svg>
```

E usar via `<use>`:
```html
<div class="icon" aria-hidden="true"><svg width="22" height="22"><use href="#i-wrench"/></svg></div>
```

Mapeamento:
| Card | Ícone |
|------|-------|
| Pilar 1 — Certified Fleet Maintenance | `#i-wrench` |
| Pilar 2 — Advanced FMS | `#i-chart` |
| Software — Compliance & Driver Safety | `#i-shield` |
| Software — Cost Control & Fuel | `#i-fuel` |
| Software — Maintenance Management | `#i-tool` |

## 2.5 Micro-interações

Adicionar ao CSS:
```css
.card { transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease; }
.card:hover { transform: translateY(-2px); border-color: var(--border-strong); box-shadow: 0 16px 40px rgba(2,6,23,.5); }
.cta { transition: transform .2s ease, box-shadow .2s ease, filter .2s ease; }
.cta:hover { transform: translateY(-1px); filter: brightness(1.06); }
a:focus-visible, button:focus-visible, .cta:focus-visible {
  outline: 2px solid var(--brand-red-500);
  outline-offset: 3px;
  border-radius: 8px;
}
```

## VERIFICAÇÃO FASE 2

```bash
grep -c "#38bdf8" Site-TechTrust/index.html   # deve retornar 0
grep -c "#60a5fa" Site-TechTrust/index.html   # deve retornar 0
grep -c "brand-red" Site-TechTrust/index.html # deve retornar >= 5
grep -c "Oswald" Site-TechTrust/index.html    # deve retornar >= 2
grep -c "🔧\|📊\|⛽\|🧰" Site-TechTrust/index.html  # deve retornar 0
grep -c "#i-wrench\|#i-chart\|#i-shield" Site-TechTrust/index.html  # deve retornar >= 3
```

**Commit:** `feat(site): fase 2 - paleta da marca, Oswald, icones SVG`

---

# FASE 3 — Estrutura, conversão, prova social

## 3.1 Stats bar no hero

Após o bloco `.hero-cta`, adicionar:
```html
<div class="stats" role="list">
  <div class="stat" role="listitem">
    <strong data-i18n="stat_1_val">25+</strong>
    <span data-i18n="stat_1_lbl">Years combined experience</span>
  </div>
  <div class="stat" role="listitem">
    <strong data-i18n="stat_2_val">10%</strong>
    <span data-i18n="stat_2_lbl">Maintenance cost reduction</span>
  </div>
  <div class="stat" role="listitem">
    <strong data-i18n="stat_3_val">5%</strong>
    <span data-i18n="stat_3_lbl">Fuel spend reduction</span>
  </div>
  <div class="stat" role="listitem">
    <strong data-i18n="stat_4_val">DOT</strong>
    <span data-i18n="stat_4_lbl">FMCSA compliant</span>
  </div>
</div>
```

CSS:
```css
.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:28px; padding-top:24px; border-top:1px solid var(--border); }
.stat { display:flex; flex-direction:column; gap:4px; }
.stat strong { font-family:'Oswald',sans-serif; font-size:2rem; color:var(--brand-red-500); line-height:1; font-weight:700; }
.stat span { color:var(--text-muted); font-size:.82rem; text-transform:uppercase; letter-spacing:.5px; }
@media (max-width: 760px){ .stats{ grid-template-columns:repeat(2,1fr); } }
```

Adicionar as chaves `stat_*` nos 3 idiomas (EN/PT/ES). Para PT/ES, traduzir apenas os labels; valores numéricos mantêm-se.

## 3.2 Seção de prova social (certificações)

Inserir uma nova `<section id="trust">` entre a seção "Proof & CTA" e "About":
```html
<section id="trust" class="trust-section">
  <div class="container">
    <p class="trust-label" data-i18n="trust_label">Certifications & Compliance</p>
    <div class="trust-grid">
      <div class="trust-item"><strong>DOT</strong><span>Department of Transportation</span></div>
      <div class="trust-item"><strong>FMCSA</strong><span>Federal Motor Carrier Safety</span></div>
      <div class="trust-item"><strong>ASE</strong><span>Automotive Service Excellence</span></div>
      <div class="trust-item"><strong>SAM.gov</strong><span>Registered Government Vendor</span></div>
    </div>
  </div>
</section>
```

CSS:
```css
.trust-section { padding: 40px 0; border-top:1px solid var(--border); border-bottom:1px solid var(--border); background:rgba(29,43,92,.08); }
.trust-label { text-align:center; color:var(--text-muted); font-size:.82rem; letter-spacing:3px; text-transform:uppercase; margin:0 0 22px; font-family:'Oswald',sans-serif; }
.trust-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; }
.trust-item { text-align:center; padding:14px; border:1px solid var(--border); border-radius:var(--radius-sm); }
.trust-item strong { display:block; font-family:'Oswald',sans-serif; font-size:1.4rem; color:var(--text); letter-spacing:1px; }
.trust-item span { display:block; font-size:.78rem; color:var(--text-muted); margin-top:4px; }
@media (max-width: 760px){ .trust-grid{ grid-template-columns:repeat(2,1fr); } }
```

Traduções `trust_label`:
- EN: `"Certifications & Compliance"`
- PT: `"Certificações e Conformidade"`
- ES: `"Certificaciones y Cumplimiento"`

Adicionar `<a href="#trust" data-i18n="nav_trust">...</a>` na navegação entre "About" e "Services". Chaves de i18n: `nav_trust` → `Trust` / `Confiança` / `Confianza`.

## 3.3 Footer de 4 colunas

Substituir o `<footer>` existente por:
```html
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <img src="/logo-horizontal-300w.png" alt="TechTrust AutoSolutions" width="180" style="margin-bottom:14px" />
        <p data-i18n="tagline">Driven by Technology. Trusted by You.</p>
        <p class="muted">Port St. Lucie, Florida, USA</p>
        <p class="muted"><a href="mailto:contact@techtrustautosolutions.com">contact@techtrustautosolutions.com</a></p>
      </div>
      <div class="footer-col">
        <h4 data-i18n="footer_company">Company</h4>
        <a href="#about" data-i18n="nav_about">About</a>
        <a href="#services" data-i18n="nav_services">Services</a>
        <a href="#software" data-i18n="nav_software">Software</a>
        <a href="#industries" data-i18n="nav_industries">Industries</a>
        <a href="#contact" data-i18n="nav_contact">Contact</a>
      </div>
      <div class="footer-col">
        <h4 data-i18n="footer_resources">Resources</h4>
        <a href="#" data-i18n="footer_capability">Capability Statement</a>
        <a href="#" data-i18n="footer_licitacoes">Licitações (BR)</a>
        <a href="#" data-i18n="footer_blog">Fleet Insights Blog</a>
        <a href="#" data-i18n="footer_docs">Documentation</a>
      </div>
      <div class="footer-col">
        <h4 data-i18n="footer_legal">Legal</h4>
        <a href="/privacy" data-i18n="footer_privacy">Privacy Policy</a>
        <a href="/terms" data-i18n="footer_terms">Terms of Service</a>
        <a href="/accessibility" data-i18n="footer_accessibility">Accessibility</a>
        <div class="footer-social" style="margin-top:14px">
          <a href="https://www.linkedin.com/company/techtrust-autosolutions" aria-label="LinkedIn" target="_blank" rel="noopener">LinkedIn</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span data-i18n="footer_rights"></span>
      <span class="muted">techtrustautosolutions.com</span>
    </div>
  </div>
</footer>
```

CSS:
```css
footer { padding: 56px 0 28px; border-top:1px solid var(--border); color:var(--text-muted); background: linear-gradient(180deg, transparent, rgba(2,6,23,.4)); }
.footer-grid { display:grid; grid-template-columns: 1.4fr repeat(3, 1fr); gap:32px; }
.footer-col h4 { font-family:'Oswald',sans-serif; color:var(--text); font-size:.95rem; letter-spacing:1.5px; text-transform:uppercase; margin:0 0 14px; }
.footer-col a { display:block; color:var(--text-muted); text-decoration:none; font-size:.9rem; margin-bottom:8px; transition:color .2s; }
.footer-col a:hover { color:var(--brand-red-500); }
.footer-col p { margin:4px 0; font-size:.88rem; }
.footer-col p.muted { color:var(--text-muted); }
.footer-bottom { display:flex; justify-content:space-between; align-items:center; margin-top:36px; padding-top:20px; border-top:1px solid var(--border); font-size:.82rem; }
@media (max-width: 940px){ .footer-grid{ grid-template-columns: 1fr 1fr; } }
@media (max-width: 560px){ .footer-grid{ grid-template-columns: 1fr; } .footer-bottom{ flex-direction:column; gap:10px; text-align:center; } }
```

Adicionar todas as chaves novas nos 3 idiomas (`footer_company`, `footer_resources`, `footer_legal`, `footer_capability`, `footer_licitacoes`, `footer_blog`, `footer_docs`, `footer_privacy`, `footer_terms`, `footer_accessibility`).

## 3.4 Substituir iframe do Google Maps por Static Maps

Na seção `#contact`, dentro do `.panel`, trocar o `<iframe>` por:
```html
<a href="https://www.google.com/maps?q=Port+St.+Lucie,+FL" target="_blank" rel="noopener" class="map-link" aria-label="Open Port St. Lucie on Google Maps">
  <img src="https://staticmap.openstreetmap.de/staticmap.php?center=27.2730,-80.3582&zoom=11&size=600x280&markers=27.2730,-80.3582,red-pushpin" alt="Map of Port St. Lucie, FL" loading="lazy" style="width:100%;height:280px;object-fit:cover;border-radius:12px;border:1px solid var(--border)" />
</a>
```

> **Observação:** OpenStreetMap static é grátis e sem API key. Se o Winner preferir Google Maps Static API, ele precisa de uma key — comentar no código.

## 3.5 CTA intermediário entre seções

Adicionar após a seção `#services` (antes de `#software`):
```html
<section class="cta-strip">
  <div class="container cta-strip-inner">
    <div>
      <h3 data-i18n="strip_title">Not sure which service fits your fleet?</h3>
      <p data-i18n="strip_sub">Talk to a specialist and get a tailored plan in 24 hours.</p>
    </div>
    <a href="#contact" class="cta" data-i18n="strip_cta">Talk to a Specialist</a>
  </div>
</section>
```

CSS:
```css
.cta-strip { padding: 44px 0; background: linear-gradient(135deg, var(--brand-blue), #0F1A3D); border-top:1px solid var(--border); border-bottom:1px solid var(--border); }
.cta-strip-inner { display:flex; align-items:center; justify-content:space-between; gap:24px; }
.cta-strip h3 { margin:0 0 4px; font-size:1.6rem; }
.cta-strip p { margin:0; color:var(--silver); }
@media (max-width: 760px){ .cta-strip-inner{ flex-direction:column; text-align:center; } }
```

Traduções:
- EN: `strip_title`: `"Not sure which service fits your fleet?"`, `strip_sub`: `"Talk to a specialist and get a tailored plan in 24 hours."`, `strip_cta`: `"Talk to a Specialist"`
- PT: `"Não sabe qual serviço se encaixa na sua frota?"`, `"Fale com um especialista e receba um plano em 24 horas."`, `"Falar com Especialista"`
- ES: `"¿No sabe qué servicio conviene a su flota?"`, `"Hable con un especialista y reciba un plan en 24 horas."`, `"Hablar con Especialista"`

## 3.6 Sticky CTA mobile

Adicionar antes de `</body>`:
```html
<a href="#contact" class="sticky-cta" data-i18n="cta_demo">REQUEST A FREE DEMO</a>
```

CSS:
```css
.sticky-cta { display:none; }
@media (max-width: 760px){
  .sticky-cta {
    display:flex; justify-content:center; align-items:center;
    position:fixed; bottom:16px; left:16px; right:16px; z-index:60;
    padding:14px 18px; border-radius:999px;
    background:linear-gradient(135deg, var(--brand-red), var(--brand-red-600));
    color:#fff; text-decoration:none; font-weight:800;
    box-shadow: var(--shadow-red);
  }
  body { padding-bottom: 72px; }
}
```

## VERIFICAÇÃO FASE 3

```bash
grep -c "class=\"stats\"" Site-TechTrust/index.html        # >= 1
grep -c "id=\"trust\"" Site-TechTrust/index.html           # >= 1
grep -c "footer-grid" Site-TechTrust/index.html            # >= 1
grep -c "cta-strip" Site-TechTrust/index.html              # >= 1
grep -c "sticky-cta" Site-TechTrust/index.html             # >= 1
grep -c "iframe" Site-TechTrust/index.html                 # 0 (removido)
```

**Commit:** `feat(site): fase 3 - stats, trust, footer 4-col, CTAs intermediarios`

---

# FASE 4 — SEO, performance, analytics, compliance

## 4.1 Hreflang

No `<head>`, adicionar:
```html
<link rel="alternate" hreflang="en" href="https://techtrustautosolutions.com/?lang=en" />
<link rel="alternate" hreflang="pt" href="https://techtrustautosolutions.com/?lang=pt" />
<link rel="alternate" hreflang="es" href="https://techtrustautosolutions.com/?lang=es" />
<link rel="alternate" hreflang="x-default" href="https://techtrustautosolutions.com/" />
```

Na função `setLang(l)`, ao final adicionar `history.replaceState(null, '', '?lang=' + l)` e, no `DOMContentLoaded`, ler `new URLSearchParams(location.search).get('lang')` para idioma inicial (fallback `'en'`).

## 4.2 Title dinâmico por idioma

Adicionar chaves `page_title` em cada idioma:
- EN: `"TechTrust AutoSolutions — Fleet Performance, Beyond Repair"`
- PT: `"TechTrust AutoSolutions — Performance de Frotas, Além do Conserto"`
- ES: `"TechTrust AutoSolutions — Rendimiento de Flotas, Más Allá de la Reparación"`

Em `setLang(l)`:
```js
document.title = (I18N[l] && I18N[l].page_title) || document.title;
```

## 4.3 Schema.org expandido

Substituir o `application/ld+json` existente por dois blocos:

**Bloco 1 — Organization + LocalBusiness:**
```json
{
  "@context": "https://schema.org",
  "@type": "AutomotiveBusiness",
  "name": "TechTrust AutoSolutions LLC",
  "url": "https://techtrustautosolutions.com/",
  "logo": "https://techtrustautosolutions.com/logo-horizontal-400w.png",
  "image": "https://techtrustautosolutions.com/assets/og-image.jpg",
  "email": "contact@techtrustautosolutions.com",
  "telephone": "+1-772-XXX-XXXX",
  "priceRange": "$$",
  "slogan": "Driven by Technology. Trusted by You.",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Port St. Lucie",
    "addressRegion": "FL",
    "addressCountry": "US"
  },
  "areaServed": { "@type": "State", "name": "Florida" },
  "sameAs": ["https://www.linkedin.com/company/techtrust-autosolutions"],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "17:00"
  }]
}
```

> **Nota:** Substituir `+1-772-XXX-XXXX` pelo telefone real quando disponível. Se ainda não houver, deixar o campo ausente em vez de placeholder.

**Bloco 2 — Service (um por serviço principal):** gere 3 objetos do tipo `Service` vinculados ao `provider` acima (Certified Fleet Maintenance, Predictive Diagnostics, DOT Compliance Inspections).

## 4.4 Sitemap e robots

Criar `Site-TechTrust/public/sitemap.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://techtrustautosolutions.com/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://techtrustautosolutions.com/?lang=en"/>
    <xhtml:link rel="alternate" hreflang="pt" href="https://techtrustautosolutions.com/?lang=pt"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://techtrustautosolutions.com/?lang=es"/>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

Criar `Site-TechTrust/public/robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://techtrustautosolutions.com/sitemap.xml
```

## 4.5 Extrair CSS e JS para arquivos externos

- Criar `Site-TechTrust/assets/css/main.css` com todo o bloco CSS atual do `<style>`.
- Criar `Site-TechTrust/assets/js/i18n.js` com o objeto `I18N` + função `setLang` + initializer do form.
- No `index.html`, substituir por:
  ```html
  <link rel="stylesheet" href="/assets/css/main.css">
  <script defer src="/assets/js/i18n.js"></script>
  ```
- Adicionar no `<head>`:
  ```html
  <link rel="preload" as="style" href="/assets/css/main.css">
  <link rel="preload" as="script" href="/assets/js/i18n.js">
  ```

## 4.6 Performance — imagens e lazy load

- Adicionar `loading="lazy"` e `decoding="async"` em toda `<img>` que não esteja no hero.
- No hero, manter a imagem com `fetchpriority="high"` e `loading="eager"`.
- Trocar `foto-site.png` (grande) por `foto-site-1.webp` com fallback `<picture>`.

## 4.7 Analytics e pixels

Antes de `</head>`, adicionar snippets (com TODO para chaves reais):

```html
<!-- Google Analytics 4 — TODO: substituir G-XXXXXXX -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX', { anonymize_ip: true });
</script>

<!-- Microsoft Clarity — TODO: substituir CLARITY_ID -->
<script>
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "CLARITY_ID");
</script>

<!-- LinkedIn Insight Tag — TODO: substituir LINKEDIN_PARTNER_ID -->
<script type="text/javascript">
  _linkedin_partner_id = "LINKEDIN_PARTNER_ID";
  window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
  window._linkedin_data_partner_ids.push(_linkedin_partner_id);
</script>
<script type="text/javascript">
  (function(l) { if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])}; window.lintrk.q=[]}
  var s = document.getElementsByTagName("script")[0]; var b = document.createElement("script");
  b.type = "text/javascript";b.async = true; b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
  s.parentNode.insertBefore(b, s);})(window.lintrk);
</script>
```

## 4.8 Headers de segurança no `vercel.json`

Adicionar no `vercel.json` (criar se não existir):
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(self)" }
      ]
    }
  ]
}
```

Mesclar com as rotas existentes do `vercel.json` atual (não sobrescrever builds/routes).

## VERIFICAÇÃO FASE 4

```bash
grep -c "hreflang" Site-TechTrust/index.html                   # >= 4
grep -c "AutomotiveBusiness" Site-TechTrust/index.html         # >= 1
ls Site-TechTrust/public/sitemap.xml                            # arquivo existe
ls Site-TechTrust/public/robots.txt                             # arquivo existe
ls Site-TechTrust/assets/css/main.css                           # arquivo existe
ls Site-TechTrust/assets/js/i18n.js                             # arquivo existe
grep -c "Strict-Transport-Security" Site-TechTrust/vercel.json  # >= 1
grep -c "gtag\|clarity\|lintrk" Site-TechTrust/index.html       # >= 3
```

**Commit:** `feat(site): fase 4 - SEO, performance, analytics, security headers`

---

# ACEITE FINAL — Testes end-to-end

Depois das 4 fases:

1. Rodar localmente: `cd Site-TechTrust && python3 -m http.server 8000` → abrir `http://localhost:8000`.
2. Testar os 3 idiomas (EN/PT/ES) — todas as strings devem traduzir, nenhum `undefined`.
3. Testar formulário de contato (com backend local `vercel dev`).
4. Testar responsividade em 360px / 768px / 1280px / 1920px.
5. Lighthouse (Chrome DevTools):
   - Performance ≥ 85
   - Accessibility ≥ 95
   - Best Practices ≥ 95
   - SEO ≥ 95
6. Validar HTML: https://validator.w3.org
7. Validar schema.org: https://validator.schema.org

**Pull request para `main`:** título `Refactor Site v2 — brand, conversion, SEO`.  
**Descrição:** listar as 4 fases + antes/depois de Lighthouse.

---

# O QUE ESTE PROMPT NÃO FAZ (escopo excluído)

- Criar páginas separadas `/government`, `/licitacoes`, `/blog` — isso fica para uma fase 5 futura.
- Migrar para Astro / Next.js.
- Criar dashboard de clientes / portal.
- Refatorar `api/contact.js` ou `api/availability.js` — manter como estão.
- Mudar provedor de email, calendar ou hosting.
- Gerar novo logo ou fotos.

Se o Claude Code sugerir fazer qualquer um desses, dizer **"fora do escopo deste prompt"** e pedir para continuar.

---

**Entregue ao Winner:** link do PR, screenshots antes/depois (desktop + mobile) e log dos comandos de verificação de cada fase passando.

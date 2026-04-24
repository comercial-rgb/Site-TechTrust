# TechTrust AutoSolutions — Análise de Site + Prompt para Claude Code

**Preparado para:** Winner (General Manager)
**Data:** 23/Abr/2026
**Arquivo analisado:** `/Site-TechTrust/index.html` (single-page, ~700 linhas)
**Stack detectada:** HTML5 + CSS3 puro + Vanilla JS + Vercel Serverless + Resend + Google Calendar
**Deploy:** Vercel (com fallback Nginx)

---

## PARTE 1 — DIAGNÓSTICO TÉCNICO E VISUAL

### 1.1 Identidade visual atual (o que realmente está no CSS)

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#0B1220` | Fundo principal (dark navy) |
| `--bg-alt` | `#111A2E` | Fundo alternativo |
| `--brand-blue` | `#1D2B5C` | Azul cobalto da marca |
| `--brand-blue-500` | `#3A4E99` | Azul intermediário |
| `--brand-red` | `#C8102E` | Vermelho da marca (accent principal) |
| `--brand-red-600` | `#A80D26` | Vermelho escuro (hover CTA) |
| `--text` | `#E8ECF5` | Texto primário |
| `--text-muted` | `#9AA7C2` | Texto secundário |
| Fontes | Oswald (headings, uppercase, letter-spacing 0.5px) + Montserrat (body) | Google Fonts |
| Radius padrão | 16px | Cards e panels |
| Shadow CTA | `0 8px 24px rgba(200,16,46,.35)` | Botão primário |

A paleta **azul cobalto + vermelho** é uma escolha coerente para automotive + enterprise (lembra marcas de caminhões pesados, bandeiras norte-americanas, bombeiros). **Isso deve ser preservado** — não é um site desatualizado, é um site subutilizado.

### 1.2 O que já está BEM feito (preservar)

- HTML5 semântico com `<header>`, `<main>`, `<section>`, `<footer>`.
- Sistema i18n funcional em EN / PT / ES (objeto `I18N` + atributos `data-i18n`).
- SVG sprite inline com ícones próprios (wrench, chart, shield, fuel, tool) — **já existe**, só não está sendo usado em todos os lugares.
- `<picture>` com WebP + fallback PNG + `@2x` retina no hero.
- `srcset` responsivo no logo.
- `:focus-visible` com outline vermelho (acessibilidade OK).
- Hover state definido em `.cta` e `.card` (já com `transition`).
- Schema.org Organization JSON-LD presente.
- Preconnect para Google Fonts (performance).
- Header sticky com `backdrop-filter: blur(8px)` — elegante.
- Deploy serverless (Vercel) + API routes para `/api/contact` e `/api/availability`.

### 1.3 Problemas reais (críticos → baixos)

#### CRÍTICOS

1. **Copywriting genérico e intercambiável com concorrência.** "Minimize Total Cost of Ownership", "maximize Uptime", "5% lower fuel spend" — qualquer Fleet SaaS nos EUA diz isso. **Falta diferenciação concreta**, números próprios, depoimentos, logos de clientes.
2. **Zero social proof.** Sem logos de clientes, sem case studies, sem depoimentos, sem selos (ASE, DOT-certified shop, BBB rating, Better Business Bureau, Google reviews count). Para B2B fleet management, isso é letal — ninguém contrata desconhecido.
3. **Dois CTAs concorrentes no hero** ("REQUEST A FREE DEMO" e "EXPLORE OUR SERVICES") sem hierarquia clara de prioridade. Também falta uma terceira via: **telefone direto + horário de atendimento** (fleet managers ligam, não preenchem formulário).
4. **Formulário raso** — faltam campos que qualificam lead: `phone`, `state/region`, `timeline` (when are you looking to decide), `primary pain point` (dropdown: compliance / fuel cost / downtime / other).
5. **Feedback do form via `alert()`** — visualmente pobre e quebra mobile. Deve virar toast/inline message.
6. **Sem mobile menu hamburger.** Header em mobile tem: logo + 6 nav links + 3 botões de idioma + 1 CTA. Isso quebra ou empilha mal em < 768px.
7. **Sem indicador de seção ativa** na navegação (scrollspy). Usuário perde contexto ao rolar.
8. **Sem smooth scroll** ao clicar nos links âncora.
9. **Sem animações de entrada** (fade/slide on scroll). Site parece estático demais para categoria tech.
10. **Sem blog / resources** — zero conteúdo para SEO orgânico. Fleet managers pesquisam "DOT inspection checklist", "how to reduce fleet fuel costs", "ELD mandate 2026" — o site não captura esse tráfego.

#### MÉDIOS

11. Meta description genérica, sem local SEO ("Port Saint Lucie, FL" e "Florida fleet maintenance" deveriam estar).
12. Sem `sitemap.xml` nem `robots.txt`.
13. JSON-LD Organization incompleto (falta `telephone`, `address.streetAddress`, `address.postalCode`, `address.addressLocality`).
14. Sem LocalBusiness schema — **crítico** para aparecer no Google Maps como oficina certificada.
15. Imagens de frota (`foto-site-*.png`) sem `loading="lazy"` (exceto iframe do Maps).
16. Não há `<link rel="canonical">`.
17. CSS e JS inline — OK para single file, mas dificulta cache agressivo. Para 700 linhas ainda está aceitável.
18. Sem página de Política de Privacidade / Termos (obrigatório se capta lead + email).
19. Sem consent banner (nem Google Analytics, aparentemente, mas assim que adicionar vai precisar).
20. Footer muito enxuto — uma linha só. Fleet managers esperam: endereço físico, telefone, licenças, horário, links rápidos, redes sociais.

#### BAIXOS / POLISH

21. `font-weight: 900` em muitos lugares — Oswald já é condensada e impactante; 700 seria mais elegante em algumas seções.
22. Só uma imagem no hero, mas existem 5 `foto-site-*` no `/public`. Poderia virar um micro-carousel ou um mosaico de 3 imagens.
23. Ícones SVG do sprite **não estão sendo usados** em todos os cards de serviços (alguns usam emoji).
24. Sem favicon em SVG (apenas PNG/ICO).
25. Sem `<meta name="theme-color">` (cor da barra de status em mobile).

### 1.4 Estrutura de conteúdo atual (para referência do prompt)

```
[Header]    Logo + Nav(Home/About/Services/Software/Industries/Contact) + Lang(EN/PT/ES) + CTA
[Hero]      Badge "Beyond Repair" + h1 + sub + 2 CTAs + imagem frota
[Mission]   Título + texto + slogan em card
[Pillars]   2 cards: Certified Maintenance + Fleet Management Software
[Proof]     Card com "5% fuel, 10% maintenance" + CTA
[About]     Título + 2 cards (Mission + Difference) + painel (HQ, Cobertura, Foco)
[Services]  5 cards (Certified Maintenance, DOT, Predictive, Warranty, Tire)
[Software]  3 cards (Compliance, Cost Control, Maintenance)
[Industries]3 cards (Transport, Construction, Field Services)
[Contact]   Form (name, email, company, fleet_size, message) + Google Maps iframe
[Footer]    Copyright + email (1 linha)
```

---

## PARTE 2 — PROMPT PRONTO PARA CLAUDE CODE

Copie o bloco abaixo **inteiro** e cole no Claude Code com o repositório `Site-TechTrust-main` aberto. Ele foi escrito para ser executado em **uma sessão** e produzir um PR limpo.

---

### ▼ INÍCIO DO PROMPT ▼

```
# MISSÃO
Você é um engenheiro front-end sênior trabalhando no site institucional da
TechTrust AutoSolutions (fleet maintenance + SaaS, HQ em Port Saint Lucie/FL,
operação binacional BR+EUA). O site atual é um único arquivo
`Site-TechTrust/index.html` (~700 linhas, HTML+CSS+JS inline), deploy na Vercel.
Preserve a stack (nada de React/Tailwind) e a identidade visual atual:
azul cobalto #1D2B5C + vermelho #C8102E + tipografia Oswald/Montserrat + dark theme.

Execute TODAS as melhorias abaixo numa única rodada, commitando em branch
`feat/site-2026-refresh` com commits pequenos e semânticos. Ao final, rode
`npx html-validate index.html` e `npx lighthouse` (CLI, headless) e reporte
os scores.

# REGRAS GERAIS
- NÃO introduza frameworks (React, Vue, Tailwind, jQuery). Mantenha CSS+JS vanilla.
- NÃO quebre o sistema i18n existente (objeto I18N + data-i18n). Toda copy nova
  DEVE ter chave em EN, PT e ES.
- NÃO remova o JSON-LD nem o SVG sprite existente — ESTENDA.
- NÃO altere a paleta de marca. Você pode adicionar tokens derivados, não
  substituir os existentes.
- Mobile-first. Testar em 360px, 768px, 1024px, 1440px.
- Acessibilidade AA: contraste ≥ 4.5:1, focus visível, aria-labels, reduced-motion.
- Performance: Lighthouse ≥ 90 em Performance, Accessibility, Best Practices, SEO.

# TAREFAS (execute na ordem)

## 1. SEO & META (5 min)
- Adicione `<link rel="canonical" href="https://techtrustautosolutions.com/">`.
- Adicione `<meta name="theme-color" content="#0B1220">`.
- Adicione `<meta name="robots" content="index,follow,max-image-preview:large">`.
- Adicione `<meta name="geo.region" content="US-FL">` e
  `<meta name="geo.placename" content="Port Saint Lucie">`.
- Reescreva a meta description para incluir localização:
  "Fleet maintenance and Fleet Management Software for U.S. commercial fleets.
   Based in Port Saint Lucie, FL. DOT/FMCSA compliance, predictive maintenance,
   and real-time telematics."
- Crie `Site-TechTrust/public/robots.txt` e `Site-TechTrust/public/sitemap.xml`
  (uma URL por enquanto).
- Estenda o JSON-LD existente adicionando um segundo bloco
  `@type: "LocalBusiness"` com `telephone`, `address` completo, `openingHours`,
  `priceRange: "$$"`, `geo: {latitude, longitude}` (use coordenadas de Port St.
  Lucie: 27.2730, -80.3582), `areaServed: ["Florida", "US"]`.
- Adicione `aria-current="page"` dinâmico no link de nav da seção ativa (scrollspy).

## 2. HEADER / NAVEGAÇÃO (mobile + desktop)
- Implemente **mobile menu hamburger** (< 860px): botão com 3 linhas animando
  para X, drawer deslizando de cima com overlay `rgba(0,0,0,.6)`. Fechar ao
  clicar em link, ao apertar ESC, ou ao clicar no overlay.
- Implemente **scrollspy vanilla** usando `IntersectionObserver`: o link da
  seção visível ganha classe `.is-active` (cor vermelha + underline animado).
- Adicione **smooth scroll**: `html { scroll-behavior: smooth; }` + offset para
  header sticky usando `scroll-margin-top: 80px` em cada `<section>`.
- Adicione um **bloco de contato no header desktop** à direita do logo:
  "📞 +1 (772) XXX-XXXX · Mon–Fri 8am–6pm EST" (use placeholder TODO-PHONE).

## 3. HERO
- Reordene os CTAs com hierarquia clara:
  - Primário (vermelho, maior): "REQUEST A FREE DEMO" → #contact
  - Secundário (ghost): "📞 Call Us Now" → tel:+1TODO-PHONE
  - Terciário (link text): "See how it works ↓" → #pillars (scroll)
- Adicione **trust strip** abaixo dos CTAs: uma linha horizontal com
  "DOT Certified · FMCSA Compliant · ASE Technicians · Serving Florida Fleets"
  em fonte pequena, cor `var(--text-muted)`, com ícone shield antes.
- Adicione **stats row** entre hero e mission: 4 números grandes
  ("500+ Vehicles Serviced", "5% Avg Fuel Savings", "10% Lower Maintenance Cost",
  "24/7 Support") com contador animado ao entrar no viewport
  (IntersectionObserver + requestAnimationFrame). Respeite prefers-reduced-motion.
- Substitua a imagem única por um **mosaico 2×2** usando as imagens já existentes
  (`foto-site-1` até `foto-site-5`) com cantos arredondados e um badge "LIVE"
  no canto de uma delas. Mantenha `<picture>` com WebP.

## 4. NOVA SEÇÃO: SOCIAL PROOF (entre Proof e About)
Adicione seção `<section id="proof-logos">` com:
- Título: "TRUSTED BY FLEETS ACROSS FLORIDA"
- Grid de 6 logos de clientes em escala de cinza + opacidade 0.6, hover sobe
  para 1.0. Use placeholders `logo-client-1.svg` até `logo-client-6.svg` em
  `/public/clients/` (crie os arquivos com SVG simples de texto até Winner
  substituir pelos reais — deixe comentário `<!-- TODO: replace with real
  client logos -->`).
- Logo abaixo: carousel simples de **3 depoimentos** (vanilla JS, auto-rotate
  8s, pause on hover). Cada depoimento tem: aspas, texto (2-3 linhas), nome,
  cargo, empresa, avatar circular. Use conteúdo placeholder realista:

  1. "TechTrust cut our downtime by 23% in the first 6 months. Their predictive
     alerts caught a transmission issue before it stranded our driver in
     Orlando." — Maria Santos, Fleet Operations Director, Sunshine Logistics Inc.
  2. "The Fleet Management Software integrates with our ELD in under 30 minutes.
     DOT audit passed in one try." — James O'Connor, Safety Manager,
     Atlantic Coast Freight.
  3. "From oil change to strategic TCO reports — one vendor, one dashboard.
     Saved us roughly $47K in Y1 on a 42-vehicle fleet."
     — Carlos Rivera, CFO, MiamiMove Last-Mile.

  Marque com `<!-- TODO: swap placeholder testimonials for real ones -->`.
- Todas as strings dos depoimentos entram no i18n (EN/PT/ES).

## 5. SECTION SERVICES (upgrade visual)
- Troque emojis por ícones do SVG sprite já existente (`#i-wrench`, `#i-chart`,
  `#i-shield`, `#i-fuel`, `#i-tool`) usando `<svg><use href="#i-xxx"/></svg>`.
- Cada card ganha:
  - Badge "Most Requested" em 1 card (destaque vermelho).
  - Lista de 3 bullets ("What's included") com checkmarks.
  - Micro-CTA "Learn more →" linkando para `#contact?service=slug`
    (o form pré-seleciona o dropdown via URL param — item 7).
- Hover: além do translateY já existente, adicione glow sutil vermelho na
  borda superior: `box-shadow: 0 -2px 0 0 var(--brand-red), var(--shadow)`.

## 6. SECTION CONTATO (redesenho completo)
- Layout 2 colunas desktop (form 60% / info 40%), empilha em mobile.
- Form com os campos existentes + novos:
  - `name*` (required)
  - `email*` (required, type=email)
  - `phone` (tel, com máscara `(xxx) xxx-xxxx` via JS vanilla)
  - `company*` (required)
  - `fleet_size*` (select: 1-5 / 6-25 / 26-100 / 100+)
  - `primary_interest` (select: Certified Maintenance / Fleet Software /
    DOT Compliance / Tire Management / Other) — pré-preenchido por URL param.
  - `timeline` (select: Immediately / 1-3 months / 3-6 months / Researching)
  - `message` (textarea, required)
  - checkbox: "I agree to the Privacy Policy" (obrigatório)
- **Substitua `alert()` por toast inline**: div `.toast` que desliza do topo
  direito, auto-fade em 5s, com variantes `.toast--success` (verde) e
  `.toast--error` (vermelho). Respeita reduced-motion.
- Validação client-side: HTML5 nativo + mensagens customizadas em pt/en/es.
- Honeypot anti-spam: campo `website` invisível (`display:none`), se preenchido
  bloqueia envio silenciosamente.
- Coluna info (direita) com:
  - Endereço físico completo (placeholder TODO-ADDRESS)
  - Telefone clicável
  - Email clicável
  - Horário de atendimento
  - Link "Get Directions" → Google Maps
  - 4 ícones de redes sociais (LinkedIn, Instagram, Facebook, YouTube) —
    placeholders TODO.

## 7. NOVA SEÇÃO: FAQ (antes do contato)
Adicione `<section id="faq">` com 6 perguntas em accordion vanilla
(`<details>/<summary>`, sem JS necessário, usando CSS pra animação).
Perguntas (traduzidas em EN/PT/ES):
1. Do you service fleets outside Florida?
2. How quickly can you onboard a new fleet?
3. Is the Fleet Management Software compatible with my existing ELD?
4. Do you handle DOT/FMCSA audits?
5. What's the typical pricing model?
6. Do you offer 24/7 roadside support?

Respostas devem ser concisas (2-3 linhas cada), com tom profissional e
mencionar fatos reais do negócio (rede de oficinas e postos parceiros
na FL, integração ELD, etc.).

Adicione **FAQPage JSON-LD** correspondente no `<head>`.

## 8. FOOTER (redesenho completo)
Substitua o footer atual por um footer de 4 colunas (desktop) que empilha em
mobile:

| Col 1 | Col 2 | Col 3 | Col 4 |
|---|---|---|---|
| Logo + tagline + endereço + phone + email | **Company** (links internos: About, Services, Software, Industries) | **Resources** (FAQ, Privacy Policy, Terms, Sitemap) | **Newsletter** (input email + botão "Subscribe" — apenas UI, endpoint TODO) |

Abaixo, uma linha divisória e um subfooter com:
- Copyright à esquerda
- Selos de certificação à direita (DOT, ASE, BBB — placeholders SVG)
- Ícones sociais

Crie páginas placeholder `Site-TechTrust/privacy.html` e
`Site-TechTrust/terms.html` com estrutura mínima (cabeçalho + conteúdo
lorem-ipsum profissional de privacy/terms padrão SaaS) e link no footer.

## 9. MICRO-INTERAÇÕES & ANIMAÇÕES
- Adicione classe `.reveal` em cada seção e implemente fade-up ao entrar no
  viewport via IntersectionObserver (threshold 0.15, opacity 0→1,
  translateY 20px→0, 600ms ease-out). Respeite `@media (prefers-reduced-motion)`.
- Adicione cursor pointer + underline animado nos nav links:
  `linear-gradient` vermelho crescendo da esquerda para direita no hover.
- CTA primário: adicione `::after` com shimmer sutil ao hover.

## 10. PERFORMANCE
- Adicione `loading="lazy"` e `decoding="async"` em todas as imagens abaixo
  do fold.
- Adicione `fetchpriority="high"` na imagem principal do hero.
- Mova o JS grande (I18N + handlers) para `Site-TechTrust/public/app.js` e
  carregue com `<script src="/app.js" defer></script>`. Isso libera o HTML
  para parse mais rápido e permite cache do JS.
- Mantenha CSS crítico inline, mas separe o resto em `/public/styles.css`
  com `<link rel="preload" as="style">` e `onload="this.rel='stylesheet'"`.
- Adicione `<link rel="dns-prefetch">` para `maps.google.com`.
- Gere versões AVIF das imagens da pasta `/public` (script bash usando
  `cwebp`/`avifenc` se disponível; caso contrário, gere TODO).

## 11. ACESSIBILIDADE (round final)
- Todos os botões do language switcher ganham `aria-pressed="true/false"`.
- Hamburger recebe `aria-expanded`, `aria-controls`, `aria-label`.
- Form: mensagens de erro associadas via `aria-describedby`.
- Skip-link ganha classe visível quando recebe foco (`:focus` muda z-index,
  posição, padding).
- `prefers-reduced-motion`: desativa shimmer, contador animado, reveal.
- Teste com axe-cli (`npx @axe-core/cli http://localhost:3000`) e reporte.

## 12. DOCUMENTAÇÃO
- Atualize `README.md` com: nova estrutura de arquivos, checklist de TODOs
  (telefone, endereço, logos de clientes, depoimentos reais, newsletter
  endpoint, social links, privacy/terms finais), e instruções para rodar
  localmente (`vercel dev`) + deploy.
- Crie `CHANGELOG.md` com entrada "2026-04-23 — v2.0 Site Refresh" listando
  todas as mudanças.

# ENTREGÁVEL FINAL
Ao final, rode e reporte:
1. `git log --oneline` do branch `feat/site-2026-refresh`
2. Lighthouse scores (Performance / A11y / Best Practices / SEO) antes e depois
3. Lista de TODOs deixados no código (`grep -rn "TODO" Site-TechTrust/`)
4. Screenshot mental (descrição textual) do novo hero e do novo footer
5. Próximos 5 passos sugeridos que ficaram fora do escopo desta rodada
   (ex: blog/MDX, A/B testing, integração GA4, chat widget, PWA).

# RESTRIÇÕES FINAIS
- NÃO suba secrets. Todos os endpoints reais ficam em env vars já existentes
  no Vercel.
- NÃO modifique `/api/contact.js` além de aceitar os novos campos (phone,
  primary_interest, timeline) e sanitizá-los.
- Se algo estiver ambíguo, escolha a opção mais conservadora e deixe `TODO`
  no código com explicação.
```

### ▲ FIM DO PROMPT ▲

---

## PARTE 3 — NOTAS DE USO

- **Execute em branch separado.** O prompt já manda criar `feat/site-2026-refresh`. Faça o merge só depois de revisar visualmente em `vercel dev`.
- **Placeholders TODO são intencionais.** Winner precisa preencher: telefone real, endereço completo, logos reais de clientes, depoimentos reais, social links, endpoint de newsletter. Todos ficam marcados com `<!-- TODO: -->` ou `// TODO:`.
- **Custo estimado de execução no Claude Code:** uma sessão longa (~30-60 min de wall clock), porque envolve edição incremental, geração de 3 idiomas e validação. Se quiser fracionar, divida o prompt em blocos 1-4, 5-8, 9-12 e rode em sessões separadas.
- **Após o merge**, rode em produção: configure Google Analytics 4, Search Console, e submeta o novo `sitemap.xml`. Também vale adicionar Plausible ou Vercel Analytics para métrica leve.
- **Próxima iteração (fora do escopo deste prompt):** blog estático em MDX, chat widget (Intercom/Crisp), PWA com service worker, landing pages dedicadas por serviço (`/dot-compliance`, `/predictive-maintenance`), e integração com HubSpot/Pipedrive para CRM dos leads do formulário.

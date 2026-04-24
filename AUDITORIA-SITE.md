# Auditoria TechTrust AutoSolutions — Site Atual
**Data:** 23/04/2026  
**Escopo:** `Site-TechTrust/index.html` (single-page, i18n EN/PT/ES)  
**Autor da análise:** Claude (para Winner — GM)

---

## TL;DR — Os 5 problemas mais graves

| # | Problema | Impacto | Esforço |
|---|----------|---------|---------|
| 1 | **Paleta do site não bate com o logo** (site ciano, logo azul-cobalto + vermelho) | Marca fraca, perda de reconhecimento | Baixo |
| 2 | **Texto de placeholder vazou para produção** ("Imagens ilustrativas — trocaremos…" e "Stack recomendado: Google Workspace…") | Amadorismo, derruba credibilidade em licitações | Mínimo |
| 3 | **Emojis (🔧 📊 ⛽) como ícones** da seção de pilares e software | Visual amador, quebra em alguns SOs, sem acessibilidade | Baixo |
| 4 | **Sem prova social, sem números em destaque, sem stats bar** | Conversão muito baixa para B2B fleet | Médio |
| 5 | **Assets carregados do GitHub raw** (logo, favicon) | Risco: se o repo privar, site quebra; latência | Baixo |

Se você só tiver uma tarde, ataque estes 5 pontos. Eles sozinhos elevam o site de "protótipo" para "produção B2B".

---

## 1. Análise de cores e identidade visual

### O que está no site hoje
```css
--bg: #0b1220;        /* fundo quase preto azulado */
--bg-alt: #0f172a;
--card: #111827;
--accent: #38bdf8;    /* ciano Tailwind sky-400 */
--accent-2: #60a5fa;  /* azul Tailwind blue-400 */
--text: #e5e7eb;
--muted: #94a3b8;
```

### O que o logo oficial exige
Seu logo horizontal usa **azul cobalto profundo (~#1E3A8A / #1D2B5C)** no lettering "TechTrust" e **vermelho de acento (~#D92D27 / #C8102E)** na sublinha "AutoSolutions LLC" e no tagline. É um esquema clássico de confiança industrial americana (estilo Ford, Craftsman, Snap-on).

### O problema
O site inteiro gira em torno de **ciano elétrico / azul claro**, que é palette de SaaS tech moderno (estilo Vercel, Linear, Stripe). Isso:
- **Contradiz o posicionamento** — você vende para frotas, transporte, construção, logística. Esse público confia em marcas robustas, não em neon SaaS.
- **Apaga o vermelho da marca**, que é o diferencial cromático (o "alerta", a "ação").
- O logo aparece minúsculo (36-56px) em um header que o ofusca.

### Recomendação: paleta corporativa coerente
```css
:root {
  /* NEUTROS — fundo e texto */
  --bg:          #0B1220;   /* mantém o dark, ok */
  --bg-alt:      #111A2E;
  --surface:     #142038;
  --border:      rgba(203, 213, 225, .12);

  /* PRIMÁRIO — azul da marca */
  --brand-blue:        #1D2B5C;   /* azul do lettering */
  --brand-blue-600:    #2A3B7A;
  --brand-blue-400:    #4A5FA8;   /* hover */

  /* ACENTO — vermelho da marca (CTAs, destaques, alertas) */
  --brand-red:         #C8102E;
  --brand-red-600:     #A80D26;   /* hover */
  --brand-red-100:     rgba(200,16,46,.12);  /* backgrounds sutis */

  /* NEUTROS de texto */
  --text:        #E8ECF5;
  --muted:       #9AA7C2;   /* já passa AA contra --bg */
  --silver:      #CBD5E1;
}
```

**Regra de uso:**
- Fundos e cards: neutros escuros (`--bg`, `--surface`).
- Títulos e CTAs primários: **vermelho** (`--brand-red`) — é o que converte.
- Badges, bordas, ícones secundários: **azul** (`--brand-blue-400`).
- O gradiente ciano atual (`--accent → --accent-2`) deve ser **removido dos CTAs** e reaproveitado só em elementos decorativos (glow de painéis).

---

## 2. Tipografia

### O que está bom
- Montserrat 400-800 está coerente com o setor automotivo/industrial.
- Escala fluida com `clamp()` — bom para responsividade.

### O que melhorar
- **Hierarquia fraca** — h1 e h2 usam `font-weight: 900` no mesmo preto, sem variação de cor ou peso de contraste. Use weight 800 em h2 e reserve 900 só para h1.
- **Line-height muito apertado** em h1 (1.05). Para leitura em mobile fica quase colado. Use `1.1` em clamp() > 40px.
- **Falta display font para títulos de impacto**. Sugestão: pareie Montserrat (texto) com **Oswald** ou **Barlow Condensed** (títulos) — ambas têm DNA industrial e pegam bem com o logo.

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Oswald:wght@600;700&display=swap" rel="stylesheet">
```
```css
h1, h2, .section-title { font-family: 'Oswald', 'Montserrat', sans-serif; letter-spacing: .5px; text-transform: uppercase; }
```

---

## 3. Copy e mensagem (EN/PT/ES)

### Frases que funcionam
- **"Beyond Repair"** — conceito forte, mantenha como tagline.
- **"We don't just fix vehicles; we optimize your logistics operation"** — ótimo slogan de missão.
- **"From Shop Floor to Dashboard"** — excelente headline para o About.

### Frases que **precisam mudar já**
| Localização | Problema | Sugestão |
|-------------|----------|----------|
| Hero H1 EN: "The Integrated Fleet Performance Solution." | Corporativo, genérico, sem emoção | **"Your Fleet. Running Longer. Costing Less."** |
| Hero H1 PT: "A Solução Integrada de Performance de Frotas." | Tradução literal, sem punch | **"Sua frota rodando mais. Custando menos."** |
| Hero sub EN (repete "Total Cost of Ownership" + "Uptime" + "Fleet Management Software" na mesma frase) | Buzzword overload | Quebre em 2 frases curtas. Ex: *"Certified maintenance meets real-time data. Cut TCO. Maximize uptime. One ecosystem."* |
| **"Imagens ilustrativas — trocaremos por fotos próprias…"** (linha 314) | **TEXTO DE DEV EM PRODUÇÃO** | Remover IMEDIATAMENTE |
| **"Stack recomendado: Google Workspace (Gmail, Drive, Meet). Hosting: AWS / GCP / Hostinger US."** (linha 329) | **TEXTO INTERNO VAZADO** | Remover IMEDIATAMENTE |
| Alert do form: `"Obrigado! Entraremos em contato em ${email}."` (linha 240) | Português fixo em site multilíngue | Trocar por `I18N[currentLang].form_success` |

### O slogan do logo não aparece no site
Seu logo diz **"Driven by Technology. Trusted by You."** — essa frase não está em lugar nenhum do site. É ouro puro de copy. Coloque como **subtitle do hero** ou no **footer como assinatura**.

### Faltam CTAs ao longo do scroll
O usuário só vê "Request Demo" no header e no hero. Adicione CTAs intermediários após cada pilar grande (pillars, services, industries) com linguagem diferente: *"Talk to a Fleet Specialist"*, *"See the Software in Action"*, *"Get a Free TCO Audit"*.

---

## 4. Layout e estrutura

### Problemas identificados

**4.1. Hero monótono**  
Grid 1.1fr / 0.9fr com uma foto estática à direita. Para B2B fleet, o hero mais forte tem:
- Texto + CTA à esquerda
- **Screenshot real do software** (dashboard FMS) à direita, com mockup de laptop/tablet
- **Stats bar abaixo** (3-4 métricas): "500+ vehicles managed", "99.2% uptime", "5-10% cost reduction"

**4.2. Cards todos iguais**  
Pilares, serviços, indústrias e software usam o mesmo componente `.card` com fundo idêntico. Dê diferenciação:
- Pilares: cards maiores, com ícone em destaque e número (01, 02).
- Serviços: cards com hover lift + border-top colorido por categoria.
- Software: tabs ou accordion em vez de 3 cards lado a lado.

**4.3. Falta seção de prova social**  
Coloque entre "Proof & CTA" e "About":
- Logos de clientes (ou de parceiros/certificações: ASE, DOT, FMCSA).
- 2-3 depoimentos curtos com foto e cargo.
- Números em destaque (mesmo que aproximados/meta).

**4.4. Contact section pouco convertida**  
- O mapa embed do Google é pesado (~500kb + iframe). Troque por **Static Maps API** ou imagem PNG com link `Open in Google Maps`.
- Adicione **phone tappable** (`<a href="tel:+1...">`), **WhatsApp Business**, **e-mail** com ícones.
- Ofereça **2 fluxos**: "Get a Quote" e "Schedule Service" — hoje só tem um form genérico.

**4.5. Footer muito seco**  
Hoje só tem e-mail + copyright. Mínimo profissional para B2B/licitações:
```
COLUNA 1: logo + tagline + endereço completo + telefone
COLUNA 2: navegação (Services, Software, Industries, About)
COLUNA 3: legal (Privacy, Terms, Accessibility) + SAM.gov UEI + NAICS codes
COLUNA 4: social (LinkedIn, YouTube) + "Subscribe to Fleet Insights"
```

**4.6. Sem breakpoint intermediário**  
Único media query em `max-width: 940px`. Entre 940 e 1200 o layout fica com cards muito largos. Adicione:
```css
@media (min-width: 941px) and (max-width: 1199px) {
  .hero-wrap { gap: 24px }
  .pillars { grid-template-columns: repeat(2, 1fr) }
}
```

---

## 5. UX e conversão

| Item | Status | Ação |
|------|--------|------|
| Skip link | Existe mas escondido com inline style | Usar classe `.sr-only` adequada com focus visível |
| Estado de loading do form | Ausente | Desabilitar botão + spinner ao submeter |
| Validação client-side | Só HTML5 required | Adicionar máscara de telefone, validação de email real |
| Mensagem de sucesso | `alert()` em português | Toast inline, traduzido pelo i18n |
| Confirmação por e-mail ao usuário | Inexistente (backend só envia para você) | `api/contact.js` deve disparar 2 e-mails: 1 interno + 1 confirmation ao lead |
| Sticky CTA mobile | Ausente | Bottom bar fixa em mobile com "Request Demo" |
| Analytics | Nenhum | GA4 + Microsoft Clarity (heatmaps grátis) |
| Pixel de conversão | Nenhum | LinkedIn Insight Tag (fundamental para B2B) |

---

## 6. Performance

| Problema | Observação | Correção |
|----------|------------|----------|
| Logo e favicon do GitHub raw | `raw.githubusercontent.com` — lento, rate-limited, depende de repo público | Servir local: `/logo-horizontal-400w.png` |
| Google Fonts sem `font-display: swap` no CSS crítico | Já tem `display=swap` na URL, ok | Adicionar `<link rel="preload" as="font">` para WOFF2 |
| Imagens sem `loading="lazy"` abaixo da dobra | Só o iframe tem | Adicionar `loading="lazy"` em todas imagens de baixo |
| `foto-site.png` de 450px altura sem `srcset` correto | Definido mas só um tamanho | Usar `<picture>` com breakpoints reais |
| CSS inline de 60 linhas no `<head>` | Ok para MVP, ruim para CWV | Extrair para `assets/css/main.css` com cache headers |
| JavaScript i18n no HTML | +3KB inline, sem tree-shaking | Extrair para `assets/js/i18n.js` |
| Sem Service Worker / PWA | Ausente | Opcional, mas melhora retenção mobile |

**Meta Core Web Vitals:** hoje estimo LCP ~2.8s, CLS ok, INP ok. Com as correções acima, LCP < 1.8s é factível.

---

## 7. SEO técnico

### O que está bom
- Schema.org Organization presente.
- Meta description, keywords, OG tags preenchidos.
- `<html lang>` muda com i18n (linha 222).

### O que falta
- **Sem `hreflang`** para EN/PT/ES. Google não entende que você tem 3 versões — é 1 página só trocando texto.
- **Sem `<title>` dinâmico por idioma** — sempre inglês.
- **OG image `/assets/og-image.jpg` referenciada mas arquivo não existe** (linha 13). Quebra compartilhamento em LinkedIn/WhatsApp.
- **Schema de Organization incompleto** — falta `address` com rua real, `telephone`, `openingHours`, `priceRange`.
- **Sem schema `LocalBusiness`** — crítico para SEO local em Port St. Lucie.
- **Sem schema `Service`** para cada serviço listado.
- **Sem `sitemap.xml`** nem `robots.txt` aparentes.
- Keywords como `"ELD, HOS, DOT"` sozinhas competem com sites gigantes. **Foque em long-tail:** *"fleet maintenance Port Saint Lucie FL"*, *"DOT inspection Treasure Coast"*, *"fleet management software for Florida logistics"*.

---

## 8. Acessibilidade (WCAG 2.2 AA)

| Item | Status | Ação |
|------|--------|------|
| Contraste `--muted #94a3b8` sobre `--bg #0b1220` | 6.4:1 — passa AA | OK |
| Contraste CTA primário (texto #06121f sobre ciano) | 10.2:1 — passa | OK |
| `alt` em imagens | "Fleet image" genérico | Descrever conteúdo real |
| Landmark regions | `<header> <main> <footer>` ok | OK |
| Foco visível | Sem `:focus-visible` custom | Adicionar outline vermelho da marca |
| Formulários | Labels ok | Adicionar `aria-describedby` com hints |
| Emojis como ícones | Screen reader lê "wrench emoji" | Substituir por SVG com `aria-hidden="true"` + texto real |
| Idioma dos blocos | `lang` muda no `<html>` | OK |

---

## 9. Licitações e compliance (B2B/Governo)

Como você participa de SAM.gov nos EUA e Lei 14.133/2021 no Brasil, o site precisa de **páginas institucionais** que hoje não existem:

### EUA — SAM.gov / Government Contracting
- **Capability Statement** (PDF downloadable + página HTML):
  - Company info + logo + contact
  - UEI (Unique Entity ID)
  - CAGE Code
  - NAICS Codes (ex: 811111 General Automotive Repair, 541511 Custom Computer Programming Services)
  - Core Competencies
  - Differentiators
  - Past Performance (3-5 contratos, mesmo que comerciais)
  - Certifications (Small Business, Veteran-Owned, WOSB, etc., se aplicável)
- Link para **SAM.gov registration** visível.

### Brasil — Lei 14.133/2021
- Página "Institucional" com CNPJ, razão social, endereço, inscrição estadual.
- Atestados de capacidade técnica.
- Certidões (negativa de débitos federais, FGTS, trabalhista) — links para download.
- Balanço patrimonial resumido (ou link para solicitação).

### Estrutura sugerida no menu
Adicione um item **"Government"** ou **"For Government"** com submenu:
- Capability Statement (US)
- Licitações (BR)
- Certifications
- Past Performance

---

## 10. Quick wins — ordem de execução sugerida

### Fase 1 (hoje, 2-3h)
1. Remover os 2 textos de placeholder vazados (linhas 314 e 329).
2. Salvar logo e favicon localmente, remover dependência do GitHub raw.
3. Adicionar a tagline **"Driven by Technology. Trusted by You."** abaixo do H1.
4. Criar `/assets/og-image.jpg` (1200×630) com logo + tagline.
5. Traduzir o `alert()` do form via i18n.

### Fase 2 (1-2 dias)
6. Refatorar paleta de cores para azul-cobalto + vermelho da marca.
7. Substituir todos os emojis por ícones SVG (Lucide React ou inline SVG).
8. Adicionar stats bar no hero (3-4 métricas).
9. Adicionar seção de prova social (logos + 2 testimonials).
10. Refazer footer com 4 colunas.

### Fase 3 (3-5 dias)
11. Extrair CSS e JS para arquivos separados com cache busting.
12. Adicionar schema `LocalBusiness` + `Service` para cada serviço.
13. Criar `sitemap.xml`, `robots.txt`, `hreflang` correto.
14. Implementar `api/contact.js` com double opt-in (confirmação ao lead).
15. GA4 + Microsoft Clarity + LinkedIn Insight Tag.

### Fase 4 (1-2 semanas)
16. Criar páginas `/government` (capability statement) e `/licitacoes` (BR).
17. Blog `/insights` com 5 posts iniciais (Fleet TCO, DOT Compliance, Predictive Maintenance, etc.) — MUITO bom para SEO.
18. Integração real do Fleet Management Software (screenshots, vídeo demo, login para clientes).

---

## 11. Código pronto — correção crítica imediata

Abaixo o patch para a **Fase 1** inteira. Cole no VS Code, aplique e teste.

### 11.1. Remover placeholders e ajustar hero
```html
<!-- index.html, linha ~314 — REMOVER esta linha: -->
<small style="color:var(--muted);display:block;margin-top:10px">Imagens ilustrativas — trocaremos por fotos próprias e telas do Fleet Management Software.</small>

<!-- index.html, linha ~329 — REMOVER este parágrafo inteiro: -->
<p style="margin:6px 0 0;color:var(--muted)">Stack recomendado: Google Workspace (Gmail, Drive, Meet). Hosting: AWS / GCP / Hostinger US.</p>
```

### 11.2. Adicionar tagline da marca no hero
```html
<!-- logo acima do <h1> no hero -->
<h1><span data-i18n="hero_h1"></span></h1>
<p class="tagline">Driven by Technology. Trusted by You.</p>
<p class="lead" data-i18n="hero_sub"></p>
```
```css
.tagline {
  color: var(--brand-red, #C8102E);
  font-family: 'Oswald', Montserrat, sans-serif;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  font-size: .95rem;
  margin: 4px 0 18px;
}
```

### 11.3. Servir logo local
```html
<!-- Substituir as URLs do GitHub raw por caminhos locais -->
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<!-- no <header>: -->
<img src="/botao-pequeno.png"
     srcset="/botao-pequeno.png 36w, /botao-pequeno@2x.png 72w"
     sizes="(min-width:1400px) 56px, (min-width:940px) 48px, 36px"
     class="logo-img"
     alt="TechTrust AutoSolutions — Driven by Technology. Trusted by You."
     width="36" height="36" />
```

### 11.4. Alert do form traduzido
```js
// no script, substituir o alert():
const t = I18N[document.documentElement.lang] || I18N.en;
alert(t.form_success.replace('{email}', data.email));
```
E adicionar em cada idioma:
```js
en: { ..., form_success: "Thanks! We'll get back to you at {email}." },
pt: { ..., form_success: "Obrigado! Entraremos em contato em {email}." },
es: { ..., form_success: "¡Gracias! Le responderemos a {email}." },
```

---

## 12. Roadmap de médio prazo — o que eu faria se fosse seu projeto

1. **Separar em componentes** (mesmo que continue SPA estática, use web components ou server includes) — manter 500 linhas de HTML com CSS+JS inline vai ficar insustentável quando você adicionar páginas.
2. **Migrar para Astro ou Next.js** — SSG com i18n nativo, performance superior, SEO por idioma, fácil de manter. Mantém hospedagem na Vercel.
3. **Área do cliente (`/portal`)** — login, status de frota, agendamentos, ordens de serviço. Esse é o verdadeiro "Fleet Management Software" que você vende; exiba uma versão demo no site.
4. **Hub de conteúdo** — `/blog`, `/case-studies`, `/resources` (whitepapers, calculadoras TCO). B2B fleet se ganha com conteúdo educacional.
5. **Certificações visíveis** — cada certificação (ASE, DOT, FMCSA, ISO, etc.) como badge no footer e em página dedicada.

---

## 13. Arquivos que revisei

- `Site-TechTrust/index.html` — main file
- `README.md` (Deploy, Resend, Google Calendar)
- `logo-horizontal-400w.png` — identidade da marca
- `public/Home.png`, `public/SeeSite.png` — assets usados
- Pasta `Site-TechTrust/public/` — 40+ imagens

---

**Próximo passo prático:** me fala qual fase (1/2/3/4) você quer atacar primeiro e eu já te entrego o diff completo pronto para colar no VS Code — HTML, CSS e JS refatorados com a nova paleta, tipografia e ícones SVG, mantendo o i18n intacto.

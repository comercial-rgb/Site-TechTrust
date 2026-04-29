# Onboarding: pontos corrigidos e contrato operacional

Este documento registra os pontos de entrada que precisam permanecer alinhados entre site, app mobile, dashboard web, API e billing.

## Fluxo de cliente

- A pagina `register-client.html` envia agora o contexto do cadastro junto com o signup:
  - `accountType`
  - `companyName`
  - `phoneCountry`
  - `phoneCountryCode`
  - `selectedPlan`
  - `planKey`
  - `billingIntent`
  - `source`
- Planos pagos nao caem mais em sucesso silencioso quando a sessao Stripe falha.
- Se o checkout falhar, o usuario fica verificado, mas e direcionado para concluir o pagamento no dashboard.
- A URL do dashboard e a API podem ser sobrescritas por `window.TECHTRUST_CONFIG`.
- O plano Enterprise agora tambem pode iniciar pelo fluxo de registro, mantendo o site coerente com a pagina de cadastro.
- O campo de celular permite selecionar pais/DDI e envia o numero final em formato E.164 para entrega correta do SMS.

## Fluxo de prestador

- A pagina `register-provider.html` envia agora dados coletados que antes eram perdidos:
  - `phoneCountry`
  - `phoneCountryCode`
  - `businessType`
  - `ein` / `taxId`
  - `yearsInBusiness`
  - `contactTitle`
  - `notes`
  - `source`
- O formulario valida estado, ZIP e EIN antes de enviar.
- O campo de celular permite selecionar pais/DDI e envia o numero final em formato E.164 para entrega correta do SMS.
- A URL do dashboard de prestador pode ser sobrescrita por `window.TECHTRUST_CONFIG`.

## APIs do site

- `api/contact.js` valida campos obrigatorios e formato de email.
- `api/contact.js` escapa os valores enviados antes de montar email HTML.
- `api/availability.js` valida `datetime` e retorna indisponivel quando a consulta do calendario falha.

## Deploy

- `vercel.json` declara rotas explicitas para:
  - `/register-client.html`
  - `/register-provider.html`
  - `/privacy.html`
  - `/api/*`
- O rewrite generico para `index.html` fica apenas como fallback de SPA/site.

## Contrato recomendado para backend, mobile e dashboard

Todos os clientes devem usar os mesmos `planKey`:

- `free`
- `starter`
- `pro`
- `enterprise`

O backend deve tratar `billingIntent = checkout_required` como estado pendente ate o Stripe confirmar a assinatura. O dashboard deve exibir uma acao clara de retomar checkout quando receber:

```text
/dashboard?checkout=retry&plan=<planKey>
```

O mobile deve consumir o catalogo de planos da mesma fonte do dashboard/backend. Evite duplicar precos no app, site e dashboard sem uma fonte unica.

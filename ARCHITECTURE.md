# 🔄 Fluxo de Dados - TechTrust AutoSolutions

## Arquitetura Geral

```
┌─────────────────┐
│   User Browser  │
│  (index.html)   │
└────────┬────────┘
         │
         │ HTTP POST
         ▼
┌─────────────────┐
│  Vercel Edge    │
│   (CDN + DNS)   │
└────────┬────────┘
         │
         ├──────────────────┬─────────────────┐
         │                  │                 │
         ▼                  ▼                 ▼
┌──────────────┐   ┌──────────────┐   ┌─────────────┐
│/api/contact  │   │/api/avail    │   │Static Files │
│(Node.js)     │   │(Node.js)     │   │(HTML/CSS/JS)│
└──────┬───────┘   └──────┬───────┘   └─────────────┘
       │                  │
       │                  │
       ▼                  ▼
┌──────────────┐   ┌─────────────────┐
│   Resend     │   │Google Calendar  │
│   (Email)    │   │      API        │
└──────────────┘   └─────────────────┘
```

---

## 📋 Fluxo do Formulário de Contato

```
1. Usuário preenche formulário
   └─> Nome, Email, Empresa, Tamanho da Frota, Mensagem

2. JavaScript valida campos obrigatórios
   └─> Se inválido: mostra erro inline

3. fetch POST → /api/contact
   └─> Body: { name, email, company, fleet_size, message }

4. API contact.js processa:
   ├─> Normaliza dados
   ├─> Envia email via Resend (se configurado)
   └─> Retorna { ok: true }

5. Frontend mostra mensagem:
   └─> Sucesso: "Obrigado! Entraremos em contato..."
   └─> Erro: "Falha ao enviar. Tente novamente."
```

---

## 🗓️ Fluxo do Agendamento de Serviço

```
1. Usuário clica "Schedule a Service"
   └─> Form aparece

2. Preenche: Nome, Veículo, Data/Hora
   └─> HTML5 datetime-local picker

3. JavaScript valida horário comercial
   ├─> Se fora de 8am-5pm: mostra erro
   └─> Se válido: continua

4. fetch POST → /api/availability
   ├─> Body: { datetime: "2025-11-15T10:00" }
   └─> Response: { ok: true, available: true/false }

5. Se slot disponível:
   └─> fetch POST → /api/contact
       └─> Body: { type: 'schedule', name, vehicle, datetime }

6. API contact.js:
   ├─> Envia email de confirmação
   ├─> Cria evento no Google Calendar (1h)
   │   ├─> Summary: "Service: [vehicle]"
   │   ├─> Description: customer info
   │   ├─> Reminders: 1 dia e 1 hora antes
   │   └─> Color: Red (ID 11)
   └─> Retorna { ok: true }

7. Frontend mostra:
   └─> "Agendamento enviado! Confirmaremos por e-mail."
```

---

## 🚗 Fluxo do Mecânico Móvel

```
1. Usuário clica "Request Mobile Mechanic"
   └─> Form aparece

2. Preenche:
   ├─> Nome
   ├─> Veículo
   ├─> Endereço
   ├─> Resumo do problema
   └─> Data/hora preferida (opcional)

3. Vê aviso: "Serviço móvel disponível das 8h às 19h"

4. Submit → fetch POST /api/contact
   └─> Body: { type: 'mobile', name, vehicle, address, summary, datetime }

5. API contact.js:
   ├─> Envia email com detalhes da solicitação
   └─> NÃO cria evento (será confirmado manualmente)

6. Frontend mostra:
   └─> "Solicitação enviada! Entraremos em contato..."
```

---

## 📧 Template de Email (Resend)

### Formulário de Contato
```html
<h2>New website inquiry</h2>
<p><b>Type:</b> contact</p>
<p><b>Name:</b> John Doe</p>
<p><b>Email:</b> john@example.com</p>
<p><b>Company:</b> ABC Logistics</p>
<p><b>Fleet size:</b> 26-100</p>
<p><b>Summary:</b> Interested in fleet management software...</p>
<hr/>
<small>Submitted at 2025-11-11T15:30:00.000Z</small>
```

### Agendamento
```html
<h2>New service scheduling</h2>
<p><b>Type:</b> schedule</p>
<p><b>Name:</b> Maria Silva</p>
<p><b>Vehicle:</b> Ford Transit 2020</p>
<p><b>Date/Time:</b> 2025-11-15T10:00</p>
<hr/>
<small>Submitted at 2025-11-11T15:35:00.000Z</small>
```

### Mecânico Móvel
```html
<h2>New mobile mechanic request</h2>
<p><b>Type:</b> mobile</p>
<p><b>Name:</b> Carlos Santos</p>
<p><b>Vehicle:</b> Chevrolet Silverado 2019</p>
<p><b>Address:</b> 123 Main St, Port St. Lucie, FL</p>
<p><b>Date/Time:</b> 2025-11-12T14:00</p>
<p><b>Summary:</b> Engine overheating, needs urgent inspection</p>
<hr/>
<small>Submitted at 2025-11-11T15:40:00.000Z</small>
```

---

## 📅 Evento do Google Calendar

```javascript
{
  summary: "Service: Ford Transit 2020",
  description: "Customer: Maria Silva\nVehicle: Ford Transit 2020\nType: Scheduled Service\n\nBooked via website",
  start: {
    dateTime: "2025-11-15T10:00:00.000Z",
    timeZone: "America/New_York"
  },
  end: {
    dateTime: "2025-11-15T11:00:00.000Z",
    timeZone: "America/New_York"
  },
  colorId: "11", // Red
  reminders: {
    useDefault: false,
    overrides: [
      { method: "email", minutes: 1440 }, // 24h antes
      { method: "popup", minutes: 60 }    // 1h antes
    ]
  }
}
```

---

## 🔒 Segurança e Validação

### Frontend (index.html)
```javascript
✅ Required fields validation (HTML5)
✅ Business hours check (8am-5pm for schedule)
✅ Date format validation (datetime-local)
✅ Immediate feedback (inline status messages)
```

### Backend (API)
```javascript
✅ Method validation (POST only)
✅ JSON body parsing with fallback
✅ Data normalization
✅ Error handling with try/catch
✅ Environment variables validation
```

### External Services
```javascript
✅ Resend: API key authentication
✅ Google Calendar: JWT Service Account auth
✅ HTTPS everywhere (Vercel enforces)
```

---

## ⚡ Performance

### Static Assets (CDN)
- HTML, CSS, JS, Images → Vercel Edge (global CDN)
- Cache-Control: public, immutable
- Compression: Brotli + Gzip

### Serverless Functions
- Cold start: ~500ms
- Warm execution: ~50-150ms
- Region: us-east-1 (default)
- Timeout: 10s (Vercel Hobby)

### External API Calls
- Resend: ~200-500ms
- Google Calendar: ~300-800ms
- Total average response: ~1-2s

---

## 📊 Monitoramento

### Logs (Vercel Dashboard)
```bash
Functions → Logs → Select Function:
  • /api/contact
  • /api/availability

Ver:
  • Timestamp
  • Status Code
  • Duration
  • Console.log output
```

### Metrics
```bash
Analytics → Overview:
  • Page views
  • Top pages
  • Unique visitors
  • Geographic distribution
```

### Email Tracking (Resend Dashboard)
```bash
Emails → All Emails:
  • Sent count
  • Delivery rate
  • Bounce rate
  • Error logs
```

---

## 🔄 Estados do Formulário

```
┌──────────────┐
│   Initial    │ (hidden)
└──────┬───────┘
       │ User clicks button
       ▼
┌──────────────┐
│   Visible    │ (form shown)
└──────┬───────┘
       │ User submits
       ▼
┌──────────────┐
│  Validating  │ "Verificando disponibilidade..." (schedule only)
└──────┬───────┘
       │
       ├─────────────┬─────────────┐
       │             │             │
       ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Sending  │  │Unavailab.│  │  Error   │
│"Enviando"│  │(schedule)│  │(network) │
└────┬─────┘  └──────────┘  └──────────┘
     │
     ▼
┌──────────────┐
│   Success    │ "Enviado!"
└──────────────┘
     │
     ▼
┌──────────────┐
│   Reset      │ (form cleared)
└──────────────┘
```

---

Fluxo completo implementado e funcionando! 🎉

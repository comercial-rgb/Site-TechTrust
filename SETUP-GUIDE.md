# 🚀 Guia Rápido de Configuração - TechTrust AutoSolutions

## 📧 Configurar Envio de Email (Resend)

### 1. Criar conta e obter API Key
```bash
1. Acesse: https://resend.com/signup
2. Crie uma conta (grátis: 100 emails/dia, 3.000/mês)
3. Vá em: https://resend.com/api-keys
4. Clique "Create API Key"
5. Copie a chave (formato: re_xxxxxxxxxxxxx)
```

### 2. (Opcional) Verificar seu domínio
```bash
1. Dashboard Resend → Domains
2. Add Domain: techtrustautosolutions.com
3. Configure DNS records:
   - SPF: v=spf1 include:_spf.resend.com ~all
   - DKIM: [valor fornecido pelo Resend]
   - DMARC: v=DMARC1; p=none
4. Aguarde verificação (até 72h)
```

**Sem domínio verificado**: emails ainda funcionam, mas vêm de `onboarding@resend.dev`

---

## 📅 Configurar Google Calendar

### 1. Criar projeto no Google Cloud
```bash
1. Acesse: https://console.cloud.google.com
2. Criar novo projeto: "TechTrust AutoSolutions"
3. Ativar API:
   - Menu → APIs & Services → Library
   - Pesquisar "Google Calendar API"
   - Clicar "Enable"
```

### 2. Criar Service Account
```bash
1. Menu → IAM & Admin → Service Accounts
2. "Create Service Account"
   - Nome: techtrust-calendar
   - ID: techtrust-calendar
   - Descrição: Service account for scheduling
3. Click "Create and Continue"
4. Pular roles (opcional)
5. Click "Done"
```

### 3. Gerar chave JSON
```bash
1. Clique na Service Account criada
2. Aba "Keys"
3. "Add Key" → "Create new key"
4. Formato: JSON
5. Baixar arquivo (ex: techtrust-calendar-xxxxx.json)
```

### 4. Compartilhar calendário com Service Account
```bash
1. Abra Google Calendar: calendar.google.com
2. Seu calendário → ⚙️ Settings and sharing
3. "Share with specific people" → Add people
4. Email: [do arquivo JSON: client_email]
5. Permissão: "Make changes to events"
6. Send
```

### 5. Extrair credenciais do arquivo JSON
Abra o arquivo JSON baixado e extraia:

```json
{
  "client_email": "techtrust-calendar@project-id.iam.gserviceaccount.com",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n"
}
```

---

## ⚙️ Configurar Variáveis de Ambiente

### Desenvolvimento Local (arquivo `.env`)
Crie um arquivo `.env` na raiz do projeto:

```bash
# Resend
RESEND_API_KEY=re_your_resend_key_here

# Google Calendar
GOOGLE_CALENDAR_ID=primary
GOOGLE_CLIENT_EMAIL=techtrust-calendar@your-project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYourKeyHere...\n-----END PRIVATE KEY-----\n"

# Email destino
CONTACT_EMAIL=contact@techtrustautosolutions.com
```

**⚠️ IMPORTANTE**: No `GOOGLE_PRIVATE_KEY`, mantenha os `\n` (não quebre em linhas reais)

### Produção (Vercel)

1. **Acesse seu projeto no Vercel**
   ```
   https://vercel.com/[seu-usuario]/site-tech-trust
   ```

2. **Vá em Settings → Environment Variables**

3. **Adicione cada variável**:

   | Name | Value | Environment |
   |------|-------|-------------|
   | `RESEND_API_KEY` | `re_xxxxx` | Production, Preview, Development |
   | `GOOGLE_CALENDAR_ID` | `primary` | Production, Preview, Development |
   | `GOOGLE_CLIENT_EMAIL` | `techtrust-calendar@...` | Production, Preview, Development |
   | `GOOGLE_PRIVATE_KEY` | `-----BEGIN PRIVATE KEY-----\n...` | Production, Preview, Development |

4. **Redeploy** para aplicar as variáveis

---

## 🧪 Testar Localmente

### 1. Instalar dependências
```bash
npm install
```

### 2. Rodar servidor de desenvolvimento
```bash
vercel dev
```

### 3. Abrir no navegador
```
http://localhost:3000
```

### 4. Testar formulários
- **Contato**: Preencher e enviar → verificar email
- **Agendar serviço**: Escolher data/hora → verificar Calendar
- **Mecânico móvel**: Solicitar → verificar email

### 5. Verificar logs
No terminal onde rodou `vercel dev`, você verá:
```
[api/contact] incoming request...
[api/contact] Calendar event created for 2025-11-15T10:00:00
```

---

## ✅ Checklist de Verificação

### Email (Resend)
- [ ] Conta Resend criada
- [ ] API Key gerada e copiada
- [ ] Variável `RESEND_API_KEY` configurada
- [ ] Email de teste recebido em contact@techtrustautosolutions.com
- [ ] (Opcional) Domínio verificado

### Google Calendar
- [ ] Projeto no Google Cloud criado
- [ ] Google Calendar API ativada
- [ ] Service Account criada
- [ ] Arquivo JSON baixado
- [ ] Calendário compartilhado com service account
- [ ] Variáveis configuradas (ID, EMAIL, PRIVATE_KEY)
- [ ] Evento de teste criado no calendário

### Deploy
- [ ] Código commitado no GitHub
- [ ] Projeto importado no Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Site acessível em produção
- [ ] Formulários testados em produção

---

## 🆘 Troubleshooting

### Email não chega
```bash
1. Verificar RESEND_API_KEY está correta
2. Verificar logs no Vercel: Functions → Logs
3. Verificar cota não excedida (100/dia grátis)
4. Verificar spam/junk folder
```

### Calendar não cria evento
```bash
1. Verificar GOOGLE_PRIVATE_KEY tem \n preservados
2. Verificar calendário está compartilhado com client_email
3. Verificar Google Calendar API está ativada
4. Verificar logs: [api/contact] Calendar event creation failed
```

### Formulário não envia
```bash
1. Verificar se está usando vercel dev (não servidor estático)
2. Abrir DevTools (F12) → Console → ver erros
3. Verificar network tab → /api/contact → response
```

---

## 📞 Suporte

- **Resend**: https://resend.com/docs
- **Google Calendar API**: https://developers.google.com/calendar
- **Vercel**: https://vercel.com/docs

---

Feito com ❤️ para TechTrust AutoSolutions

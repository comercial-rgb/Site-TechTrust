# TechTrust AutoSolutions — Deploy & Integrations

## Arquivos
- `index.html` — site estático multilíngue (EN/PT/ES), hero, serviços com slider e formulários (agendamento e mecânico em casa).
- `vercel.json` — configuração Vercel (estático + funções serverless em `api/**/*.js`).
- `api/contact.js` — função serverless para envio do formulário (Resend opcional).
- `api/availability.js` — checagem de disponibilidade no Google Calendar (opcional).
- `nginx.conf` — alternativa se preferir VM/Docker com Nginx.

## Deploy na Vercel (recomendado)
1. Importe o repositório.
2. Em Settings → Environment Variables, defina:
   - `RESEND_API_KEY` (obrigatório para envio de e-mail)
   - `GOOGLE_CALENDAR_ID` (ex.: primary ou o ID do calendário específico)
   - `GOOGLE_CLIENT_EMAIL` (Service Account email)
   - `GOOGLE_PRIVATE_KEY` (Private key da Service Account, com quebras de linha como \n)
3. Faça o deploy. Os endpoints `/api/contact` e `/api/availability` serão publicados automaticamente.

## Configuração de Email (Resend)

### Passo 1: Criar conta Resend
1. Acesse https://resend.com
2. Crie uma conta gratuita (permite 100 emails/dia)
3. Verifique seu domínio ou use o domínio de teste

### Passo 2: Obter API Key
1. Acesse https://resend.com/api-keys
2. Clique em "Create API Key"
3. Copie a chave (começa com `re_`)
4. Adicione nas variáveis de ambiente da Vercel como `RESEND_API_KEY`

### Passo 3: Verificar domínio (opcional mas recomendado)
1. Em Resend Dashboard → Domains
2. Adicione `techtrustautosolutions.com`
3. Configure os registros DNS (SPF, DKIM, DMARC)
4. Aguarde verificação (pode levar até 72h)

**Importante**: Sem verificação de domínio, emails serão enviados de um domínio Resend, mas ainda funcionam.

## Configuração Google Calendar

### Passo 1: Criar Service Account
1. Acesse https://console.cloud.google.com
2. Crie um projeto ou selecione um existente
3. Ative a **Google Calendar API**:
   - Biblioteca → Pesquise "Google Calendar API" → Ativar
4. Vá em IAM & Admin → Service Accounts
5. Clique em "Create Service Account"
   - Nome: `techtrust-calendar`
   - Descrição: `Service account for TechTrust scheduling`
6. Clique em "Create and Continue"
7. Pule a permissão de projeto (opcional)
8. Clique em "Done"

### Passo 2: Gerar chave privada
1. Na lista de Service Accounts, clique na conta criada
2. Vá na aba "Keys"
3. Clique em "Add Key" → "Create new key"
4. Escolha formato **JSON**
5. Baixe o arquivo JSON

### Passo 3: Compartilhar calendário
1. Abra Google Calendar (calendar.google.com)
2. No calendário que deseja usar:
   - Clique nos 3 pontos → "Settings and sharing"
   - Em "Share with specific people", clique em "Add people"
   - Cole o email da Service Account (do JSON baixado: `client_email`)
   - Permissão: **"Make changes to events"**
   - Clique em "Send"

### Passo 4: Configurar variáveis de ambiente
Do arquivo JSON baixado, extraia:
- `client_email` → `GOOGLE_CLIENT_EMAIL`
- `private_key` → `GOOGLE_PRIVATE_KEY` (mantenha com \n, não quebre as linhas)
- ID do calendário → `GOOGLE_CALENDAR_ID` (use "primary" ou o ID específico do calendário)

Exemplo de `.env` local:
```bash
RESEND_API_KEY=re_your_key_here
GOOGLE_CALENDAR_ID=primary
GOOGLE_CLIENT_EMAIL=techtrust-calendar@your-project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n"
```

**Atenção**: No Vercel, cole a private key inteira com os `\n` preservados.

## Variáveis de ambiente
```
RESEND_API_KEY=your_resend_api_key
GOOGLE_CALENDAR_ID=primary
GOOGLE_CLIENT_EMAIL=service@project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nABC...\n-----END PRIVATE KEY-----\n"
```

## Regras de Agendamento
- Horário de atendimento: 08:00–17:00 (5pm exclusivo). Cada agendamento consome 1h.
- O formulário de agendamento consulta `/api/availability` antes de enviar.
- Se o calendário não estiver configurado, assume disponibilidade.

## Emails
Quando `RESEND_API_KEY` estiver configurada, `api/contact.js` envia um e-mail para `contact@techtrustautosolutions.com` com:
- **Formulário de contato**: informações do lead (nome, email, empresa, tamanho da frota, mensagem)
- **Agendamento**: detalhes do serviço (nome, veículo, data/hora)
- **Mecânico móvel**: solicitação (nome, veículo, endereço, resumo, data/hora preferida)

Se a chave não estiver configurada, os dados são apenas registrados no log do servidor.

## Google Calendar
Quando as credenciais do Google Calendar estiverem configuradas:
- **Verificação de disponibilidade**: `/api/availability` checa conflitos antes de permitir agendamento
- **Criação de evento**: Ao confirmar um agendamento, `api/contact.js` cria automaticamente um evento de 1 hora no calendário com:
  - Título: "Service: [modelo do veículo]"
  - Descrição: dados do cliente
  - Lembretes: 1 dia antes (email) e 1 hora antes (popup)
  - Cor: vermelho (colorId: 11) para identificação rápida

Se não estiver configurado, assume disponibilidade total e não cria eventos.

## Horários de Atendimento
- **Agendamento em oficina**: 8:00 AM – 5:00 PM (segunda a sexta)
- **Mecânico móvel**: 8:00 AM – 7:00 PM (segunda a sábado)
- Validação é feita no front-end antes de enviar ao backend

## Slider de Imagens
Coloque os arquivos PNG na raiz do projeto:
```
foto-02-site.png
foto-03-site.png
foto-04-site.png
foto-05-site.png
foto-06-site.png
foto-07-site.png
```
Se faltar algum arquivo, a imagem será ocultada automaticamente.

## Desenvolvimento Local
Para servidor estático: `python3 -m http.server 8000`
Para executar APIs localmente, use Vercel CLI:
```
npm i -g vercel
vercel dev
```

## Próximos passos
- ✅ Integrar envio real de email via Resend (implementado)
- ✅ Criar evento no Calendar no momento da confirmação (implementado)
- Persistir solicitações em banco de dados (opcional)
- Adicionar dashboard interno para gerenciar agendamentos (opcional)
- Implementar notificações SMS para confirmações urgentes (opcional)

# Configuração de E-mail e Google Calendar

Este documento explica como configurar o envio de e-mails e a integração com Google Calendar para os formulários do site TechTrust AutoSolutions.

## ✅ O que já está implementado

O código para envio de e-mails e criação de eventos no Google Calendar já está completo nos arquivos:
- `/api/contact.js` - Envia e-mails e cria eventos no calendar
- `/api/availability.js` - Verifica disponibilidade de horários

## 🔧 Configuração necessária no Vercel

Para que os formulários funcionem, você precisa adicionar as seguintes variáveis de ambiente no painel do Vercel:

### 1. Configurar Resend (Envio de E-mails)

**Passo a passo:**

1. Acesse [Resend.com](https://resend.com) e crie uma conta gratuita
2. Verifique seu domínio personalizado OU use o domínio de teste fornecido
3. Vá em **API Keys** e crie uma nova chave
4. No painel do Vercel:
   - Acesse seu projeto: https://vercel.com/insta-solutions-and-tech-trust/site-tech-trust
   - Vá em **Settings** → **Environment Variables**
   - Adicione a variável:
     ```
     Nome: RESEND_API_KEY
     Valor: re_xxxxxxxxxxxxxxxxxxxxxxxxxx (sua chave da Resend)
     ```

**Importante sobre o domínio de e-mail:**
- Se você verificou um domínio personalizado na Resend, atualize o `from` no arquivo `/api/contact.js` linha 66:
  ```javascript
  from: 'TechTrust <no-reply@SEU-DOMINIO.com>',
  ```
- Se estiver usando o domínio de teste, o formato é:
  ```javascript
  from: 'TechTrust <onboarding@resend.dev>',
  ```

### 2. Configurar Google Calendar (Agendamento)

**Passo a passo:**

1. **Criar Service Account no Google Cloud:**
   - Acesse [Google Cloud Console](https://console.cloud.google.com/)
   - Crie um novo projeto ou selecione um existente
   - Vá em **APIs & Services** → **Enable APIs and Services**
   - Busque e ative: **Google Calendar API**
   
2. **Criar credenciais:**
   - Vá em **APIs & Services** → **Credentials**
   - Clique em **Create Credentials** → **Service Account**
   - Preencha o nome (ex: "techtrustcalendar")
   - Clique em **Create and Continue**
   - Pule as permissões opcionais e clique em **Done**

3. **Gerar chave privada:**
   - Na lista de Service Accounts, clique no que você criou
   - Vá na aba **Keys**
   - Clique em **Add Key** → **Create New Key**
   - Escolha formato **JSON** e baixe o arquivo
   
4. **Compartilhar o Calendar:**
   - Abra [Google Calendar](https://calendar.google.com)
   - No calendar que deseja usar (ou crie um novo):
   - Clique nos 3 pontos → **Settings and sharing**
   - Em **Share with specific people**, clique **Add people**
   - Adicione o e-mail do Service Account (está no arquivo JSON baixado, campo `client_email`)
   - Permissão: **Make changes to events**
   - Copie o **Calendar ID** (está em Settings, seção "Integrate calendar")

5. **Adicionar variáveis no Vercel:**
   - No painel do Vercel (**Settings** → **Environment Variables**), adicione:
   
   ```
   Nome: GOOGLE_CALENDAR_ID
   Valor: seu-calendar-id@group.calendar.google.com
   
   Nome: GOOGLE_CLIENT_EMAIL
   Valor: techtrustcalendar@seu-projeto.iam.gserviceaccount.com
   
   Nome: GOOGLE_PRIVATE_KEY
   Valor: -----BEGIN PRIVATE KEY-----\nMIIE...sua chave completa...==\n-----END PRIVATE KEY-----\n
   ```
   
   **Importante:** Para a `GOOGLE_PRIVATE_KEY`:
   - Copie o conteúdo do campo `private_key` do arquivo JSON
   - Mantenha as quebras de linha como `\n` (não quebre em múltiplas linhas)
   - Inclua `-----BEGIN PRIVATE KEY-----` no início e `-----END PRIVATE KEY-----` no final

### 3. Fazer redeploy

Após adicionar todas as variáveis de ambiente:
1. Vá no terminal do projeto
2. Execute: `vercel --prod`

Ou no painel do Vercel:
- Vá em **Deployments**
- Clique nos 3 pontos do último deploy
- Clique em **Redeploy**

## 🧪 Como testar

1. **Testar envio de e-mail:**
   - Acesse o site publicado
   - Preencha o formulário de contato
   - Verifique se o e-mail chegou em `contact@techtrustautosolutions.com`

2. **Testar agendamento:**
   - Clique em "Schedule a Service"
   - Preencha o formulário e escolha uma data/hora
   - Verifique se:
     - O e-mail de notificação chegou
     - Um evento foi criado no Google Calendar

3. **Testar mecânico móvel:**
   - Clique em "Request Mobile Mechanic"
   - Preencha e envie
   - Verifique se o e-mail de notificação chegou

## ⚠️ Problemas comuns

### E-mails não chegam
- Verifique se `RESEND_API_KEY` está correto
- Verifique se o domínio de envio está verificado na Resend
- Verifique a pasta de SPAM

### Eventos não aparecem no Calendar
- Verifique se a API do Google Calendar está ativada
- Verifique se o Service Account tem permissão no calendar
- Verifique se `GOOGLE_CALENDAR_ID` está correto
- Verifique se a `GOOGLE_PRIVATE_KEY` está completa (com `\n` e sem quebras de linha extras)

### Erro 500 nos formulários
- Abra o painel do Vercel → **Functions** → Clique na função com erro
- Veja os logs para identificar o problema
- Geralmente é erro de formatação em `GOOGLE_PRIVATE_KEY`

## 📋 Checklist de configuração

- [ ] Conta criada na Resend
- [ ] API Key da Resend adicionada no Vercel
- [ ] Domínio verificado na Resend (ou usando domínio de teste)
- [ ] Projeto criado no Google Cloud
- [ ] Google Calendar API ativada
- [ ] Service Account criado
- [ ] Chave JSON baixada
- [ ] Calendar compartilhado com o Service Account
- [ ] Variáveis do Google adicionadas no Vercel
- [ ] Redeploy realizado
- [ ] Testes realizados e funcionando

## 📞 Suporte

Se precisar de ajuda adicional com a configuração, consulte:
- [Documentação da Resend](https://resend.com/docs)
- [Documentação do Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
- [Variáveis de Ambiente no Vercel](https://vercel.com/docs/concepts/projects/environment-variables)

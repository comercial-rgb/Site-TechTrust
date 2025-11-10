# TechTrust AutoSolutions — Deploy Package

## Files
- `index.html` — site estático multilíngue (EN/PT/ES), hero com galeria, copy revisada (Fleet Management Software, Total Cost of Ownership), cobertura Florida/Port St. Lucie, formulário integrado.
- `vercel.json` — configuração Vercel (roteia `/api/contact`).
- `api/contact.js` — função serverless para enviar o formulário (exemplos Resend e SMTP Workspace).
- `nginx.conf` — alternativa se preferir VM/Docker com Nginx.

## Deploy na Vercel (recomendado)
1. Crie um novo projeto e envie estes arquivos exatamente nesta estrutura.
2. Em **Settings → Domains**, adicione `techtrustautosolutions.com` e finalize a verificação DNS.
3. Em **Settings → Environment Variables**, defina:
   - `RESEND_API_KEY` (ou `SMTP_USER` e `SMTP_PASS` se optar por SMTP).
4. Faça o deploy. O formulário POSTará para `/api/contact` e encaminhará para `contact@techtrustautosolutions.com` conforme a opção escolhida no código.

## DNS (resumo)
- Se a Vercel for o host: adicione os registros sugeridos pela Vercel para `techtrustautosolutions.com`.
- Se usar VM/Nginx: aponte `A` para seu servidor e coloque os arquivos em `/var/www/techtrustautosolutions`.

## Observação
As imagens do hero usam URLs públicas (Unsplash). Substitua por fotos próprias e telas do software quando estiverem prontas.

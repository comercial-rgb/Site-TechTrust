# TechTrust AutoSolutions - AI Coding Agent Instructions

## Project Overview
Static multilingual website (EN/PT/ES) for auto repair services with serverless backend on Vercel. Integrates Resend (email) and Google Calendar (scheduling).

## Architecture

### Core Structure
- `index.html` - Single-page static site with embedded vanilla JS
- `api/contact.js` - Serverless function handling all form submissions (contact, scheduling, mobile mechanic)
- `api/availability.js` - Checks Google Calendar for appointment conflicts
- `vercel.json` - Routes config: static files + Node.js serverless functions

### Data Flow
1. User submits form → POST to `/api/contact` or `/api/availability`
2. API validates, sends email via Resend, creates calendar event
3. Graceful degradation: APIs log to console if env vars missing

## Critical Patterns

### Serverless Function JSON Parsing
Both API files use custom `readJson()` because Vercel body parsing is inconsistent:
```javascript
async function readJson(req){
  if (req.body) {
    if (typeof req.body === 'string') {
      try { return JSON.parse(req.body); } catch { return {}; }
    }
    return req.body;
  }
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8');
  try { return JSON.parse(raw); } catch { return {}; }
}
```
**Never replace this with standard body parsers** - it's intentional.

### Business Hours & Scheduling Rules
- **Shop scheduling**: 8:00 AM – 5:00 PM (Mon-Fri), 1-hour blocks
- **Mobile mechanic**: 8:00 AM – 7:00 PM (Mon-Sat), manual confirmation
- Frontend validates hours before calling API
- Calendar API checks conflicts via `timeMin`/`timeMax` queries

### Environment Variables (Required)
```bash
RESEND_API_KEY=re_xxxxx              # Email sending
GOOGLE_CALENDAR_ID=primary           # Calendar ID or "primary"
GOOGLE_CLIENT_EMAIL=x@x.iam.g...     # Service account email
GOOGLE_PRIVATE_KEY="-----BEGIN..."   # Must preserve \n escapes
```
**Fallback behavior**: APIs continue without errors if vars missing (log instead of email, assume availability).

## Key Files & Their Roles

| File | Purpose |
|------|---------|
| [api/contact.js](api/contact.js) | Handles 3 form types via `type` field: `contact`, `schedule`, `mobile`. Sends email + creates calendar event for scheduling. |
| [api/availability.js](api/availability.js) | Returns `{available: true/false}` based on Google Calendar conflicts. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Detailed data flow diagrams for each user journey. |
| [create_desktop_images.py](create_desktop_images.py) | PIL script to resize/crop hero images to 1920x480. Uses `crop_offset` for manual positioning. |

## Development Workflows

### Local Testing
```bash
# Install dependencies
npm install

# Set env vars in .env (git-ignored)
# Run Vercel CLI locally
vercel dev
```

### Deploying
Push to GitHub → Vercel auto-deploys. Set env vars in Vercel dashboard.

### Image Processing
```bash
# Batch process hero images
python3 create_desktop_images.py

# Single image with custom crop
python3 process_new_desktop_images.py
```

## Frontend Patterns

### Language Switching
Language data stored in `data-lang-*` attributes:
```html
<h1 data-lang-en="Hello" data-lang-pt="Olá" data-lang-es="Hola"></h1>
```
`setLang(lang)` function updates all elements with matching attributes.

### Form Handling
- Validates business hours before API calls
- Disables submit button during request
- Shows inline error/success messages (no alerts)
- All forms POST to `/api/contact` with different `type` values

## Common Tasks

### Adding New Form Field
1. Add to HTML form
2. Update `readJson()` payload normalization in [api/contact.js](api/contact.js#L28-L38)
3. Add to email template HTML in same file

### Changing Business Hours
1. Update validation in frontend: `withinBusinessHours()` function
2. Adjust documentation in [README.md](README.md#90-94)

### Adding New Language
1. Add `data-lang-[code]` attributes to all translatable elements
2. Add language button with corresponding `dataset.lang` value
3. Test entire flow including form error messages

## External Services Setup

See [SETUP-GUIDE.md](SETUP-GUIDE.md) for step-by-step:
- Resend domain verification & API key generation
- Google Cloud project, service account, Calendar API activation
- Calendar sharing with service account email

## Important Constraints

- **No build step** - site is pure static HTML/CSS/JS
- **No frameworks** - vanilla JavaScript only
- **Timezone**: All calendar operations use `America/New_York` (Florida)
- **Email target**: All forms email to `contact@techtrustautosolutions.com`
- **Calendar event color**: Red (colorId: 11) for easy visual identification

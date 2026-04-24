const { Resend } = require('resend');
const { google } = require('googleapis');

async function readJson(req){
  // If body already exists (Vercel may parse automatically), use it
  if (req.body) {
    if (typeof req.body === 'string') {
      try { return JSON.parse(req.body); } catch { return {}; }
    }
    return req.body;
  }
  // Fallback: read raw stream and parse
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8');
  if (!raw) return {};
  try { return JSON.parse(raw); } catch { return {}; }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.statusCode = 405;
    return res.end('Method Not Allowed');
  }
  try {
    const body = await readJson(req);
    // Basic normalization
    const payload = {
      type: body.type || 'contact',
      status: body.status || 'confirmed',
      name: body.name || '',
      email: body.email || 'contact@techtrustautosolutions.com',
      phone: body.phone || '',
      vehicle: body.vehicle || '',
      vin: body.vin || '',
      fuel_type: body.fuel_type || '',
      service: body.service || '',
      address: body.address || '',
      summary: body.summary || body.message || '',
      datetime: body.datetime || '',
      company: body.company || '',
      fleet_size: body.fleet_size || '',
      createdAt: new Date().toISOString()
    };

    let sent = false;
    const apiKey = process.env.RESEND_API_KEY || '';
    if(apiKey){
      try{
        const resend = new Resend(apiKey);
        const to = 'contact@techtrustautosolutions.com';
        const subject = payload.type === 'schedule'
          ? `[${payload.status === 'pending' ? 'PENDING' : 'CONFIRMED'}] New service booking — ${payload.service || 'General'}`
          : (payload.type === 'mobile' ? 'New mobile mechanic request' : 'New website inquiry');
        const html = `
          <h2>${subject}</h2>
          ${payload.status === 'pending' ? '<div style="background:#fef3c7;border:1px solid #f59e0b;padding:12px 16px;border-radius:8px;margin-bottom:16px"><strong>⚠️ PENDING APPROVAL</strong> — This booking requires your confirmation. Please review the details below and confirm or contact the customer.</div>' : ''}
          <p><b>Type:</b> ${payload.type}</p>
          <p><b>Status:</b> ${payload.status === 'pending' ? '⏳ Pending Approval' : '✅ Confirmed'}</p>
          <p><b>Name:</b> ${payload.name}</p>
          ${payload.email ? `<p><b>Email:</b> ${payload.email}</p>` : ''}
          ${payload.phone ? `<p><b>Phone:</b> ${payload.phone}</p>` : ''}
          ${payload.vehicle ? `<p><b>Vehicle:</b> ${payload.vehicle}</p>` : ''}
          ${payload.vin ? `<p><b>VIN:</b> ${payload.vin}</p>` : ''}
          ${payload.fuel_type ? `<p><b>Fuel Type:</b> ${payload.fuel_type}</p>` : ''}
          ${payload.service ? `<p><b>Service Requested:</b> ${payload.service}</p>` : ''}
          ${payload.address ? `<p><b>Address:</b> ${payload.address}</p>` : ''}
          ${payload.datetime ? `<p><b>Date/Time:</b> ${payload.datetime}</p>` : ''}
          ${payload.company ? `<p><b>Company:</b> ${payload.company}</p>` : ''}
          ${payload.fleet_size ? `<p><b>Fleet size:</b> ${payload.fleet_size}</p>` : ''}
          ${payload.summary ? `<p><b>Notes:</b> ${payload.summary}</p>` : ''}
          <hr/>
          <small>Submitted at ${payload.createdAt}</small>
        `;
        await resend.emails.send({
          from: 'TechTrust <no-reply@techtrustautosolutions.com>',
          to,
          subject,
          html
        });
        sent = true;
      }catch(err){
        console.error('[api/contact] email error', err);
      }
    }

    if(!sent){
      console.log('[api/contact] incoming request (no-email fallback)', payload);
    }

    // Create Google Calendar event for schedule type
    if(payload.type === 'schedule' && payload.datetime){
      const CALENDAR_ID = process.env.GOOGLE_CALENDAR_ID || process.env.GOOGLE_CALENDAR || '';
      const CLIENT_EMAIL = process.env.GOOGLE_CLIENT_EMAIL || '';
      const PRIVATE_KEY = (process.env.GOOGLE_PRIVATE_KEY || '').replace(/\\n/g, '\n');

      if(CALENDAR_ID && CLIENT_EMAIL && PRIVATE_KEY){
        try{
          const auth = new google.auth.JWT({
            email: CLIENT_EMAIL,
            key: PRIVATE_KEY,
            scopes: ['https://www.googleapis.com/auth/calendar']
          });
          const calendar = google.calendar({ version: 'v3', auth });

          const start = new Date(payload.datetime);
          const end = new Date(start.getTime() + 60*60*1000); // 1 hour

          const isPending = payload.status === 'pending';

          await calendar.events.insert({
            calendarId: CALENDAR_ID,
            requestBody: {
              summary: `${isPending ? '[PENDING] ' : ''}Service: ${payload.service || 'General'} — ${payload.vehicle}`,
              description: `Status: ${isPending ? 'PENDING APPROVAL' : 'CONFIRMED'}\nCustomer: ${payload.name}\nEmail: ${payload.email}\nPhone: ${payload.phone}\nVehicle: ${payload.vehicle}\nVIN: ${payload.vin}\nFuel: ${payload.fuel_type}\nService: ${payload.service}\nNotes: ${payload.summary}\n\nBooked via website`,
              start: { dateTime: start.toISOString(), timeZone: 'America/New_York' },
              end: { dateTime: end.toISOString(), timeZone: 'America/New_York' },
              colorId: isPending ? '5' : '11', // Yellow=pending, Red=confirmed
              status: isPending ? 'tentative' : 'confirmed',
              reminders: {
                useDefault: false,
                overrides: [
                  { method: 'email', minutes: 24 * 60 }, // 1 day before
                  { method: 'popup', minutes: 60 } // 1 hour before
                ]
              }
            }
          });
          console.log('[api/contact] Calendar event created for', payload.datetime);
        }catch(err){
          console.error('[api/contact] Calendar event creation failed', err.message);
        }
      }
    }

    res.setHeader('Content-Type', 'application/json');
    return res.status(200).end(JSON.stringify({ ok: true }));
  } catch (err) {
    console.error('[api/contact] error', err);
    return res.status(500).end(JSON.stringify({ ok: false }));
  }
};

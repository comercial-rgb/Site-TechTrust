const { google } = require('googleapis');

function json(res, code, obj){
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(obj));
}

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
  if (!raw) return {};
  try { return JSON.parse(raw); } catch { return {}; }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return json(res, 405, { ok:false, error:'Method Not Allowed' });
  try{
    const body = await readJson(req);
    const { datetime } = body || {};
    if(!datetime) return json(res, 400, { ok:false, error:'Missing datetime' });

    const CALENDAR_ID = process.env.GOOGLE_CALENDAR_ID || process.env.GOOGLE_CALENDAR || '';
    const CLIENT_EMAIL = process.env.GOOGLE_CLIENT_EMAIL || '';
    const PRIVATE_KEY = (process.env.GOOGLE_PRIVATE_KEY || '').replace(/\\n/g, '\n');

    // If not configured, assume available
    if(!CALENDAR_ID || !CLIENT_EMAIL || !PRIVATE_KEY){
      return json(res, 200, { ok:true, available:true, note:'calendar-not-configured' });
    }

    const auth = new google.auth.JWT({
      email: CLIENT_EMAIL,
      key: PRIVATE_KEY,
      scopes: ['https://www.googleapis.com/auth/calendar']
    });
    const calendar = google.calendar({ version: 'v3', auth });

    // Interpret datetime as local and block 1h
    const start = new Date(datetime);
    const end = new Date(start.getTime() + 60*60*1000);

    const isoStart = start.toISOString();
    const isoEnd = end.toISOString();

    const events = await calendar.events.list({
      calendarId: CALENDAR_ID,
      timeMin: isoStart,
      timeMax: isoEnd,
      maxResults: 1,
      singleEvents: true,
      orderBy: 'startTime'
    });

    const hasConflict = (events.data.items || []).length > 0;
    return json(res, 200, { ok:true, available: !hasConflict });
  }catch(err){
    console.error('[api/availability] error', err);
    return json(res, 200, { ok:true, available:true, note:'calendar-error-assuming-available' });
  }
};

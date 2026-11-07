// SAY WHO — Book Us · Google Calendar API (Cloudflare Pages Function)
//
//   GET  /api/availability?who=paris&month=2026-11  → free 15-min slots (Europe/Paris)
//   POST /api/book                                  → creates the event + Google Meet link
//
// Configuration: see V2/README.md and V2/.dev.vars.example.

const TZ = 'Europe/Paris';
const CONSULTANTS = ['paris', 'usa', 'italy'];
const DEFAULTS = {
  CALL_MINUTES: 15,
  SLOT_STEP_MINUTES: 30,
  MIN_NOTICE_HOURS: 12,
  MAX_MONTHS_AHEAD: 6,
  WORK_DAYS: '1,2,3,4,5', // 1 = Monday … 7 = Sunday
  WORK_HOURS: '09:00-13:00,14:00-18:00', // Paris time
};
const SCOPES = 'https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar.freebusy';

export async function onRequest(context) {
  const { request, env, params } = context;
  const route = (params.route || []).join('/');
  try {
    const cors = corsHeaders(request, env);
    if (cors === null) return json({ error: 'forbidden_origin' }, 403);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    let res;
    if (route === 'availability' && request.method === 'GET') res = await availability(request, env);
    else if (route === 'book' && request.method === 'POST') res = await book(request, env);
    else res = json({ error: 'not_found' }, 404);
    for (const [k, v] of Object.entries(cors)) res.headers.set(k, v);
    return res;
  } catch (err) {
    console.error(err && err.stack || err);
    return json({ error: err.publicCode || 'server_error' }, err.status || 500);
  }
}

/* ---------------- Routes ---------------- */

async function availability(request, env) {
  const url = new URL(request.url);
  const who = url.searchParams.get('who');
  const month = url.searchParams.get('month') || '';
  if (!CONSULTANTS.includes(who)) return json({ error: 'unknown_consultant' }, 400);
  if (!/^\d{4}-\d{2}$/.test(month)) return json({ error: 'bad_month' }, 400);

  const [y, m] = month.split('-').map(Number);
  const daysInMonth = new Date(Date.UTC(y, m, 0)).getUTCDate();
  const from = parisToUtc(y, m, 1, 0, 0);
  const to = parisToUtc(y, m, daysInMonth, 23, 59) + 60000;
  const cfg = config(env, who);
  if (to < Date.now() || from > maxDate(cfg)) return json({ timezone: TZ, month, days: {} }, 200, 60);

  const busy = isDemo(env) ? demoBusy(y, m, daysInMonth) : await freeBusy(env, who, from, to);
  const days = {};
  for (let d = 1; d <= daysInMonth; d++) {
    const slots = daySlots(cfg, y, m, d, busy);
    if (slots.length) days[`${month}-${pad(d)}`] = slots;
  }
  return json({ timezone: TZ, month, callMinutes: cfg.callMinutes, days, demo: isDemo(env) }, 200, 60);
}

async function book(request, env) {
  let body;
  try { body = await request.json(); } catch { return json({ error: 'bad_json' }, 400); }
  const who = body.who;
  const date = String(body.date || '');
  const time = String(body.time || '');
  const name = clean(body.name, 120);
  const company = clean(body.company, 120);
  const email = clean(body.email, 200).toLowerCase();
  const brief = clean(body.brief, 6000, true);
  if (body.website) return json({ error: 'bad_request' }, 400); // honeypot
  if (!CONSULTANTS.includes(who)) return json({ error: 'unknown_consultant' }, 400);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) return json({ error: 'bad_slot' }, 400);
  if (!name) return json({ error: 'missing_name' }, 400);
  if (!/^[^\s@<>()",;]+@[^\s@<>()",;]+\.[a-z]{2,}$/i.test(email)) return json({ error: 'bad_email' }, 400);

  const cfg = config(env, who);
  const [y, m, d] = date.split('-').map(Number);
  const [hh, mm] = time.split(':').map(Number);
  const start = parisToUtc(y, m, d, hh, mm);
  const end = start + cfg.callMinutes * 60000;

  if (isDemo(env)) {
    // Demo mode: no Google call, nothing is created.
    if (!daySlots(cfg, y, m, d, demoBusy(y, m, new Date(Date.UTC(y, m, 0)).getUTCDate())).includes(time)) return json({ error: 'slot_unavailable' }, 409);
    return json({ ok: true, demo: true, start: new Date(start).toISOString(), end: new Date(end).toISOString(), meetLink: null }, 201);
  }

  // Re-check against the live calendar right before booking.
  const busy = await freeBusy(env, who, parisToUtc(y, m, d, 0, 0), parisToUtc(y, m, d, 23, 59) + 60000);
  if (!daySlots(cfg, y, m, d, busy).includes(time)) return json({ error: 'slot_unavailable' }, 409);

  const calendarId = calendarFor(env, who);
  const token = await accessToken(env, who);
  const event = {
    summary: `SAY WHO — Discovery call · ${name}${company ? ' (' + company + ')' : ''}`,
    description: brief || `Contact: ${name}\nCompany: ${company || 'Not provided'}\nEmail: ${email}`,
    start: { dateTime: new Date(start).toISOString(), timeZone: TZ },
    end: { dateTime: new Date(end).toISOString(), timeZone: TZ },
    attendees: [{ email, displayName: name }],
    guestsCanModify: false,
    conferenceData: { createRequest: { requestId: crypto.randomUUID(), conferenceSolutionKey: { type: 'hangoutsMeet' } } },
    extendedProperties: { private: { source: 'saywho-book-us', consultant: who } },
  };
  const res = await fetch(
    `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events?conferenceDataVersion=1&sendUpdates=all`,
    { method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, body: JSON.stringify(event) },
  );
  if (!res.ok) throw googleError('events.insert', res.status, await res.text());
  const created = await res.json();
  return json({
    ok: true,
    start: created.start?.dateTime,
    end: created.end?.dateTime,
    meetLink: created.hangoutLink || created.conferenceData?.entryPoints?.find(e => e.entryPointType === 'video')?.uri || null,
  }, 201);
}

/* ---------------- Slots ---------------- */

function config(env, who) {
  const k = who.toUpperCase();
  const pick = (name) => env[`${name}_${k}`] ?? env[name] ?? DEFAULTS[name];
  return {
    callMinutes: Number(pick('CALL_MINUTES')),
    step: Number(pick('SLOT_STEP_MINUTES')),
    noticeMs: Number(pick('MIN_NOTICE_HOURS')) * 3600000,
    maxMonths: Number(pick('MAX_MONTHS_AHEAD')),
    workDays: String(pick('WORK_DAYS')).split(',').map(Number),
    windows: String(pick('WORK_HOURS')).split(',').map(w => w.trim().split('-').map(toMinutes)),
  };
}

function maxDate(cfg) {
  const now = new Date();
  return Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + cfg.maxMonths + 1, 1);
}

function daySlots(cfg, y, m, d, busy) {
  const isoDay = new Date(Date.UTC(y, m - 1, d)).getUTCDay() || 7;
  if (!cfg.workDays.includes(isoDay)) return [];
  const earliest = Date.now() + cfg.noticeMs;
  const latest = maxDate(cfg);
  const out = [];
  for (const [ws, we] of cfg.windows) {
    for (let t = ws; t + cfg.callMinutes <= we; t += cfg.step) {
      const start = parisToUtc(y, m, d, Math.floor(t / 60), t % 60);
      const end = start + cfg.callMinutes * 60000;
      if (start < earliest || start > latest) continue;
      if (busy.some(b => start < b.end && end > b.start)) continue;
      out.push(`${pad(Math.floor(t / 60))}:${pad(t % 60)}`);
    }
  }
  return out;
}

async function freeBusy(env, who, from, to) {
  const calendarId = calendarFor(env, who);
  const token = await accessToken(env, who);
  const res = await fetch('https://www.googleapis.com/calendar/v3/freeBusy', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ timeMin: new Date(from).toISOString(), timeMax: new Date(to).toISOString(), timeZone: TZ, items: [{ id: calendarId }] }),
  });
  if (!res.ok) throw googleError('freeBusy', res.status, await res.text());
  const data = await res.json();
  const cal = data.calendars?.[calendarId];
  if (!cal || cal.errors?.length) throw googleError('freeBusy', 502, JSON.stringify(cal?.errors || data));
  return (cal.busy || []).map(b => ({ start: Date.parse(b.start), end: Date.parse(b.end) }));
}

/* ---------------- Demo mode ---------------- */

// DEMO_MODE = "true" (wrangler.toml): plausible fake busy times, no Google access needed.
function isDemo(env) { return String(env.DEMO_MODE || '').toLowerCase() === 'true'; }
function demoBusy(y, m, daysInMonth) {
  const busy = [];
  for (let d = 1; d <= daysInMonth; d++) {
    for (let h = 9; h < 18; h++) {
      for (const mi of [0, 30]) {
        const x = Math.sin((y * 372 + m * 31 + d) * 9301 + (h * 2 + mi / 30) * 49297) * 233280;
        if (x - Math.floor(x) < 0.4) {
          const s = parisToUtc(y, m, d, h, mi);
          busy.push({ start: s, end: s + 30 * 60000 });
        }
      }
    }
  }
  return busy;
}

/* ---------------- Google auth ---------------- */

const tokenCache = new Map();

async function accessToken(env, who) {
  const cached = tokenCache.get(who);
  if (cached && cached.exp > Date.now() + 60000) return cached.token;
  let body;
  const refresh = env[`GOOGLE_REFRESH_TOKEN_${who.toUpperCase()}`];
  if (env.GOOGLE_SA_EMAIL && env.GOOGLE_SA_PRIVATE_KEY) {
    // Service account + domain-wide delegation: act as the consultant.
    body = new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: await signJwt(env, calendarFor(env, who)),
    });
  } else if (refresh && env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET) {
    // OAuth refresh token authorised once by the consultant.
    body = new URLSearchParams({ grant_type: 'refresh_token', refresh_token: refresh, client_id: env.GOOGLE_CLIENT_ID, client_secret: env.GOOGLE_CLIENT_SECRET });
  } else {
    throw Object.assign(new Error(`No Google credentials configured for "${who}"`), { status: 503, publicCode: 'calendar_not_configured' });
  }
  const res = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', body });
  if (!res.ok) throw googleError('token', res.status, await res.text());
  const data = await res.json();
  tokenCache.set(who, { token: data.access_token, exp: Date.now() + data.expires_in * 1000 });
  return data.access_token;
}

async function signJwt(env, subject) {
  const now = Math.floor(Date.now() / 1000);
  const enc = (o) => b64url(new TextEncoder().encode(JSON.stringify(o)));
  const unsigned = `${enc({ alg: 'RS256', typ: 'JWT' })}.${enc({
    iss: env.GOOGLE_SA_EMAIL, sub: subject, scope: SCOPES,
    aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600,
  })}`;
  const pem = env.GOOGLE_SA_PRIVATE_KEY.replace(/\\n/g, '\n').replace(/-----[^-]+-----/g, '').replace(/\s+/g, '');
  const der = Uint8Array.from(atob(pem), c => c.charCodeAt(0));
  const key = await crypto.subtle.importKey('pkcs8', der, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(unsigned));
  return `${unsigned}.${b64url(new Uint8Array(sig))}`;
}

function calendarFor(env, who) {
  const id = env[`CALENDAR_${who.toUpperCase()}`];
  if (!id) throw Object.assign(new Error(`CALENDAR_${who.toUpperCase()} is not set`), { status: 503, publicCode: 'calendar_not_configured' });
  return id;
}

/* ---------------- Helpers ---------------- */

// Paris wall-clock time → UTC timestamp (handles summer/winter time).
function parisToUtc(y, m, d, h, min) {
  const guess = Date.UTC(y, m - 1, d, h, min);
  let t = guess - parisOffset(guess);
  const off2 = parisOffset(t);
  if (guess - off2 !== t) t = guess - off2;
  return t;
}
const parisFmt = new Intl.DateTimeFormat('en-US', { timeZone: TZ, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' });
function parisOffset(utc) {
  const p = Object.fromEntries(parisFmt.formatToParts(new Date(utc)).map(x => [x.type, x.value]));
  return Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second) - Math.floor(utc / 1000) * 1000;
}

function corsHeaders(request, env) {
  const origin = request.headers.get('Origin');
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  if (!origin || !allowed.length) return {};
  if (origin === new URL(request.url).origin) return {};
  if (!allowed.includes(origin)) return null;
  return { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', Vary: 'Origin' };
}

function googleError(where, status, text) {
  return Object.assign(new Error(`Google ${where} failed (${status}): ${text}`), { status: 502, publicCode: 'calendar_error' });
}
function json(data, status = 200, maxAge = 0) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': maxAge ? `public, max-age=${maxAge}` : 'no-store' },
  });
}
function clean(v, max, multiline = false) {
  let s = String(v ?? '').trim();
  s = multiline ? s.replace(/[^\S\n]+/g, ' ') : s.replace(/\s+/g, ' ');
  return s.replace(/[\u0000-\u0009\u000B-\u001F\u007F]/g, '').slice(0, max);
}
function toMinutes(hhmm) { const [h, m] = hhmm.split(':').map(Number); return h * 60 + (m || 0); }
function pad(n) { return String(n).padStart(2, '0'); }
function b64url(bytes) {
  let s = ''; for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

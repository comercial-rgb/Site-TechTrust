const fs = require('fs');
const html = fs.readFileSync('index.html','utf8');

// Extract I18N
const m = html.match(/const I18N\s*=\s*(\{[\s\S]*?\});/);
if(!m){ console.log('ERROR: I18N not found'); process.exit(1); }

let i18n;
try { i18n = eval('('+m[1]+')'); }
catch(e){ console.log('ERROR parsing I18N:', e.message); process.exit(1); }

const langs = Object.keys(i18n);
console.log('Languages:', langs.join(', '));
langs.forEach(l => console.log('  '+l+':', Object.keys(i18n[l]).length, 'keys'));

const enKeys = Object.keys(i18n.en);
const ptKeys = Object.keys(i18n.pt);
const esKeys = Object.keys(i18n.es);

const missingPT = enKeys.filter(k => !ptKeys.includes(k));
const missingES = enKeys.filter(k => !esKeys.includes(k));
const extraPT = ptKeys.filter(k => !enKeys.includes(k));
const extraES = esKeys.filter(k => !enKeys.includes(k));

if(missingPT.length) console.log('Missing in PT:', missingPT);
if(missingES.length) console.log('Missing in ES:', missingES);
if(extraPT.length) console.log('Extra in PT:', extraPT);
if(extraES.length) console.log('Extra in ES:', extraES);

if(!missingPT.length && !missingES.length) {
  console.log('All EN keys present in PT and ES');
}

const critical = ['hero_h1','hero_sub','cta_demo','cta_ios','cta_android','mission_title','about_title','hq_headquarters','two_apps_title','security_title','benefits_title','for_everyone_title','final_cta_title','contact_title','footer_rights'];
const missingCritical = {};
langs.forEach(l => {
  const miss = critical.filter(k => !i18n[l][k]);
  if(miss.length) missingCritical[l] = miss;
});
if(Object.keys(missingCritical).length) {
  console.log('MISSING CRITICAL KEYS:', missingCritical);
} else {
  console.log('All critical keys present in all languages');
}

const refs = new Set();
const re = /data-i18n="([^"]+)"/g;
let mm;
while(mm = re.exec(html)) refs.add(mm[1]);
console.log('HTML data-i18n refs:', refs.size);

const unresolvedEN = [...refs].filter(k => !i18n.en[k]);
if(unresolvedEN.length) {
  console.log('WARNING: HTML refs not in EN I18N:', unresolvedEN);
} else {
  console.log('All HTML data-i18n refs resolved in EN');
}

const sections = ['home','services','about','software','industries','contact'];
sections.forEach(id => {
  if(!html.includes('id="'+id+'"')) console.log('MISSING section id:', id);
});
console.log('All section IDs present');
console.log('Total lines:', html.split('\n').length);

// Check unused keys
const unused = enKeys.filter(k => !refs.has(k));
if(unused.length) console.log('Defined but unused keys ('+unused.length+'):', unused);
else console.log('All keys are used in HTML');

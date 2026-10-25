// Usage: node .claude/skills/niche-guide/check.js [slug] [file.html]
// Checks niche guides in index.html (or file.html) against the roofing guide's depth. No slug = report on all.
const fs = require('fs'), path = require('path');
const args = process.argv.slice(2), file = args.find(a => a.endsWith('.html'));
const html = fs.readFileSync(file || path.join(__dirname, '../../../index.html'), 'utf8');
const data = html.slice(html.indexOf('var CONTACT='), html.indexOf('function extra('));
const { T, FULL, CATS, STEPS } = new Function(data + ';return {T,FULL,CATS,STEPS}')();

const LISTS = ['lic', 'cost', 'plan', 'mistakes', 'obj', 'faq', 'tools'];
const bar = Object.fromEntries(LISTS.map(k => [k, FULL.roofing[k].length]));
const str = x => typeof x === 'string' && x.trim().length > 0;

function problems(s) {
  const t = T.find(x => x.s === s), f = FULL[s], p = [];
  if (!t) return ['no entry in T'];
  if (!f) return ['no entry in FULL'];
  if (!CATS[t.c]) p.push('bad category index ' + t.c);
  for (const k of ['n', 'cost', 'season', 'fit', 'spend']) if (!str(t[k])) p.push('T.' + k + ' empty');
  if (!t.tips || t.tips.length !== STEPS.length || !t.tips.every(str)) p.push('tips must be ' + STEPS.length + ' strings');
  for (const k of LISTS) {
    const n = (f[k] || []).length;
    if (n < bar[k]) p.push(k + ' ' + n + '/' + bar[k]);
  }
  for (const k of ['cost', 'plan', 'obj', 'faq'])
    if (!(f[k] || []).every(r => Array.isArray(r) && r.length === 2 && r.every(str))) p.push(k + ' rows must be [text, text]');
  if (!str(f.costnote)) p.push('costnote empty');
  if (!/\$\d/.test(f.price || '')) p.push('price has no worked numbers');
  const text = JSON.stringify([t, f]);
  if (text.includes('—')) p.push('em dash used (site style has none)');
  if (/[<>]/.test(text)) p.push('< or > in text (strings are injected as HTML)');
  return p;
}

const slug = args.find(a => !a.endsWith('.html'));
const slugs = slug ? [slug] : T.map(t => t.s);
let bad = 0;
for (const s of slugs) {
  const p = problems(s);
  if (p.length) bad++;
  console.log(s.padEnd(24) + (p.length ? p.join(', ') : 'OK'));
}
for (const s of Object.keys(FULL)) if (!T.find(t => t.s === s)) { bad++; console.log(s.padEnd(24) + 'in FULL but not in T'); }
const words = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split(' ');
if (!html.includes('for ' + (words[T.length] || T.length) + ' trades')) { bad++; console.log('home page trade count does not say "for ' + (words[T.length] || T.length) + ' trades"'); }
process.exit(bad ? 1 : 0);

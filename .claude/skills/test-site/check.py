# Usage: python3 .claude/skills/test-site/check.py [base-url] [path ...]
# Opens each page in headless Chrome, clicks every link on every hash page, and checks that each
# one lands on a real page with no JavaScript errors. Also fetches every server path, external link
# and resource the page loads. Default: http://127.0.0.1:8000, paths / and /v2. Exit 1 on any failure.
import json, os, re, subprocess, sys, tempfile, urllib.error, urllib.parse, urllib.request

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
args = sys.argv[1:]
base = args[0].rstrip('/') if args and args[0].startswith('http') else 'http://127.0.0.1:8000'
paths = [a for a in args if a.startswith('/')] or ['/', '/v2']

# Runs before the page's own script: collects JavaScript errors.
SPY = '''<script>window.__ftErr=[];window.addEventListener("error",function(e){__ftErr.push(String(e.message))});
var __ce=console.error;console.error=function(){__ftErr.push([].join.call(arguments," "));__ce.apply(console,arguments)}</script>'''

# Runs after it: walks every hash page, clicks each link on it, and records what the click led to.
CRAWL = r'''<script>(function(){
var known={home:1,guides:1,"home-contact":1};T.forEach(function(t){known[t.s]=1});Object.keys(LEGAL).forEach(function(k){known[k]=1});
function title(id){var t=T.find(function(x){return x.s===id});return (t?t.n+" start-up guide":LEGAL[id]?LEGAL[id][0]:"FollowThrough")+" | FollowThrough"}
function errs(){return __ftErr.splice(0)}
var out={load:errs(),pages:{},clicks:[],other:[]},queue=["#home"],seen={"#home":1};
function visit(h){go(h);return {title:document.title,text:document.getElementById("app").innerText.trim().length,errors:errs()}}
while(queue.length){var h=queue.shift();out.pages[h]=visit(h);
  var n=document.querySelectorAll("a").length;
  for(var i=0;i<n;i++){go(h);errs();var a=document.querySelectorAll("a")[i];if(!a)break;
    var href=a.getAttribute("href")||"",text=(a.innerText||a.getAttribute("aria-label")||"").trim().slice(0,60);
    if(href.charAt(0)!=="#"){out.other.push({page:h,href:href,text:text});continue}
    var id=href.slice(1),r={page:h,href:href,text:text,problems:[]};
    try{a.click()}catch(x){r.problems.push("click threw: "+x.message)}
    var e=errs();if(e.length)r.problems.push("JavaScript error: "+e.join("; "));
    if(!known[id])r.problems.push("no page called \""+id+"\": the click re-renders the home page and jumps to the top"+(document.getElementById(id)?" instead of scrolling to the #"+id+" section":""));
    else{var want=title(id==="home-contact"?"home":id);
      if(document.title!==want)r.problems.push("title is \""+document.title+"\", expected \""+want+"\"");
      if(document.getElementById("app").innerText.trim().length<200)r.problems.push("page is nearly empty");
      if(id==="home-contact"&&!document.getElementById("signup"))r.problems.push("signup form missing");
      if(!seen[href]){seen[href]=1;queue.push(href)}}
    out.clicks.push(r)}}
var s=document.createElement("script");s.type="application/json";s.id="ft-result";s.textContent=JSON.stringify(out).replace(/</g,"\\u003c");document.body.appendChild(s)})()</script>'''


def fetch(url, method='GET'):
    req = urllib.request.Request(url, method=method, headers={'User-Agent': 'Mozilla/5.0 FollowThrough link check'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return None, str(e)


def crawl(html):
    html = html.replace('<head>', '<head>' + SPY, 1).replace('</body>', CRAWL + '</body>', 1)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, 'page.html')
        open(page, 'w').write(html)
        dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                              '--user-data-dir=' + os.path.join(tmp, 'profile'), '--virtual-time-budget=5000',
                              '--dump-dom', 'file://' + page], capture_output=True, text=True, timeout=120).stdout
    m = re.search(r'<script type="application/json" id="ft-result">(.*?)</script>', dom, re.S)
    return json.loads(m.group(1)) if m else None


fails, warns, external = [], [], {}
if not os.path.exists(CHROME):
    sys.exit('Google Chrome not found at ' + CHROME)
for path in paths:
    url = base + path
    status, html = fetch(url)
    if status != 200:
        fails.append('%s does not load (%s)' % (url, status or html))
        continue
    for tag in re.findall(r'<(?:link|script|img)\b[^>]*>', html):
        src = re.search(r'(?:href|src)="([^"]+)"', tag)
        if not src or re.search(r'rel="(preconnect|dns-prefetch)"', tag):
            continue
        external.setdefault(urllib.parse.urljoin(url, src.group(1)), set()).add(path + ' (resource)')
    r = crawl(html)
    if r is None:
        fails.append('%s: page script crashed before the crawl ran (open it in a browser and check the console)' % url)
        continue
    for e in r['load']:
        fails.append('%s: JavaScript error on load: %s' % (url, e))
    for h, p in r['pages'].items():
        if p['errors']:
            fails.append('%s%s: JavaScript error: %s' % (url, h, '; '.join(p['errors'])))
    broken = {}
    for c in r['clicks']:
        for p in c['problems']:
            broken.setdefault((c['href'], c['text'], p), []).append(c['page'])
    for (href, text, p), on in broken.items():
        fails.append('%s link "%s" (%s), on %d page(s) e.g. %s: %s' % (path, text, href, len(set(on)), on[0], p))
    for o in r['other']:
        href = o['href']
        if href.startswith('mailto:'):
            addr = href[7:].split('?')[0]
            if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-z]{2,}', addr):
                fails.append('%s%s: mailto link "%s" has a bad address: %s' % (path, o['page'], o['text'], addr))
            elif 'yourdomain' in addr:
                warns.append('%s: mailto link "%s" still uses the placeholder %s' % (path, o['text'], addr))
        elif href.startswith(('tel:', 'javascript:')) or not href:
            warns.append('%s%s: link "%s" has href "%s"' % (path, o['page'], o['text'], href))
        else:
            external.setdefault(urllib.parse.urljoin(url, href), set()).add(path + o['page'])
    print('%s: %d pages, %d link clicks' % (url, len(r['pages']), len(r['clicks'])))

for link, where in sorted(external.items()):
    status, err = fetch(link)
    if status is None or status >= 400:
        fails.append('%s does not load (%s), linked from %s' % (link, status or err, ', '.join(sorted(where))))
print('%d other links and resources fetched' % len(external))

for w in warns:
    print('WARN  ' + w)
for f in fails:
    print('FAIL  ' + f)
print('OK, nothing broken' if not fails else '%d problem(s)' % len(fails))
sys.exit(1 if fails else 0)

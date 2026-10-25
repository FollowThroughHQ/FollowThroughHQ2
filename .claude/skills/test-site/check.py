# Usage: python3 .claude/skills/test-site/check.py [base-url] [path ...] [--compare]
# Opens each page in headless Chrome at phone width (375px) and, on every page (/, /roofing...): clicks every link and
# checks it lands on a real page with no JavaScript errors; checks nothing runs off the side, text is readable
# in light and dark mode, no placeholder text is left, and each page has a title and a main heading. Tests the
# objection tabs, a step checkmark across a reload, and the signup form (a real test signup goes only to a
# private copy of the app that logs emails instead of sending them). Fetches every server path, external
# link and resource, takes a screenshot of each page, and for a site that isn't on this computer (or with
# --compare) names the parts that differ from resources/views/home.blade.php here.
# Default: http://127.0.0.1:8000, path /. Exit 1 on any failure.
import concurrent.futures, difflib, json, os, re, shutil, socket, subprocess, sys, tempfile, time
import urllib.error, urllib.parse, urllib.request

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SHOTS = os.path.join(ROOT, 'storage', 'app', 'site-check')
# The list in docs/02-website.md.
PLACEHOLDERS = ['[Your Name]', '[Your Name / Company]', '[address]', '[country]', '[country/state]', '[date]',
                '[X years]', '[industries / roles]', '[One sentence', 'Add a photo', 'hello@yourdomain.com']
args = sys.argv[1:]
base = args[0].rstrip('/') if args and args[0].startswith('http') else 'http://127.0.0.1:8000'
paths = [a for a in args if a.startswith('/')] or ['/']
local = urllib.parse.urlparse(base).hostname in ('127.0.0.1', 'localhost')
compare = '--compare' in args or not local

# Runs before the page's own script: collects JavaScript errors.
SPY = '''<script>window.__ftErr=[];window.addEventListener("error",function(e){__ftErr.push(String(e.message))});
var __ce=console.error;console.error=function(){__ftErr.push([].join.call(arguments," "));__ce.apply(console,arguments)};var __ftCfg=%s</script>'''

# Runs after it: walks every page, clicks each link on it and records what the click led to, measures each
# page, tests the objection tabs, ticks a step and reloads the page, then (after the reload) tests the signup form.
CRAWL = r'''<script>(function(){
var S=sessionStorage,saved=S.getItem("__ft"),app=document.getElementById("app"),root=document.documentElement;
var known={home:1,guides:1,calculator:1},jump={"home-contact":"signup",signup:"signup",demo:"demo"};T.forEach(function(t){known[t.s]=1});Object.keys(LEGAL).forEach(function(k){known[k]=1});
function title(id){var t=T.find(function(x){return x.s===id});return t?t.n+" start-up guide | FollowThrough":LEGAL[id]?LEGAL[id][0]+" | FollowThrough":id==="guides"?"Start-up guides | FollowThrough":id==="calculator"?"Lost quotes calculator | FollowThrough":"FollowThrough: start and sell a service business"}
function errs(){return __ftErr.splice(0)}
function done(e){return /\bdone\b/.test(e.className)}
function finish(out){out.errors2=errs();parent.postMessage(JSON.stringify(out).replace(/</g,"\\u003c"),"*")}
function desc(e){return e.tagName.toLowerCase()+(e.id?"#"+e.id:e.classList[0]?"."+e.classList[0]:"")+' "'+e.textContent.trim().replace(/\s+/g," ").slice(0,40)+'"'}
function clipped(e){for(var p=e.parentElement;p&&p!==document.body;p=p.parentElement)if(getComputedStyle(p).overflowX!=="visible")return true}
function wide(){var w=root.clientWidth,bad=[];if(root.scrollWidth<=w)return bad;
  document.querySelectorAll("body *").forEach(function(e){var r=e.getBoundingClientRect();if(r.width&&r.right>w+1&&e.parentElement.getBoundingClientRect().right<=w+1&&!clipped(e))bad.push(desc(e)+" sticks out "+Math.round(r.right-w)+"px")});
  return bad.length?bad:["the page is "+(root.scrollWidth-w)+"px wider than the screen"]}
function rgba(s){var m=(s.match(/[\d.]+/g)||[]).map(Number);if(m.length<3)return [0,0,0,0];if(m.length<4)m[3]=1;return m}
function mix(c,b){return [0,1,2].map(function(i){return c[i]*c[3]+b[i]*(1-c[3])})}
function back(e){var l=[],b=[255,255,255];for(;e;e=e.parentElement){var c=rgba(getComputedStyle(e).backgroundColor);if(c[3]>0){l.push(c);if(c[3]>=1)break}}for(var i=l.length-1;i>=0;i--)b=mix(l[i],b);return b}
function lum(c){c=c.map(function(v){v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*c[0]+.7152*c[1]+.0722*c[2]}
function hex(c){return "#"+c.map(function(v){return ("0"+Math.round(v).toString(16)).slice(-2)}).join("")}
function faint(){var bad=[];document.querySelectorAll("body *").forEach(function(e){
  if(/^(SCRIPT|STYLE)$/.test(e.tagName)||![].some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim()}))return;
  var r=e.getBoundingClientRect(),s=getComputedStyle(e);if(!r.width||!r.height||s.visibility==="hidden")return;
  var b=back(e),c=mix(rgba(s.color),b),x=lum(c),y=lum(b),k=(Math.max(x,y)+.05)/(Math.min(x,y)+.05),z=parseFloat(s.fontSize),need=z>=24||z>=18.66&&+s.fontWeight>=700?3:4.5;
  if(k<need)bad.push({text:desc(e),colors:hex(c)+" on "+hex(b),ratio:Math.floor(k*10)/10,need:need})});return bad}
function measure(){var p={title:document.title,h1:app.querySelectorAll("h1").length,height:root.scrollHeight,wide:wide(),faint:{},
  text:[].map.call(document.body.children,function(e){return e.tagName==="SCRIPT"?"":e.textContent}).concat([].map.call(document.querySelectorAll("[href]"),function(e){return e.getAttribute("href")})).join(" "),
  noalt:[].filter.call(document.querySelectorAll("img"),function(i){return !i.hasAttribute("alt")}).map(function(i){return i.getAttribute("src")})};
  ["light","dark"].forEach(function(m){root.setAttribute("data-theme",m);p.faint[m]=faint()});root.removeAttribute("data-theme");return p}
function visit(h){go(h);var p=measure();p.errors=errs();return p}
function tabs(out){var p=out.tabs=[],b;go("/");b=document.querySelectorAll("#tabs button");out.tabn=b.length;
  if(!b.length||b.length!==OBJ.length)p.push("found "+b.length+" objection tabs, expected "+OBJ.length);
  for(var i=b.length-1;i>=0;i--){b[i].click();var on=[].filter.call(b,function(y){return y.getAttribute("aria-selected")==="true"});
    if(on.length!==1||on[0]!==b[i])p.push("clicking the \""+b[i].textContent+"\" tab doesn't select it");
    if(document.getElementById("q").textContent!==OBJ[i][1]||document.getElementById("a").textContent!==OBJ[i][2])p.push("clicking the \""+b[i].textContent+"\" tab doesn't show its objection")}
  var e=errs();if(e.length)p.push("JavaScript error: "+e.join("; "))}
function signup(out){var p=out.signup=[];go("/#signup");
  var f=document.getElementById("f"),em=document.getElementById("em"),ok=document.getElementById("ok"),st=document.getElementById("fs"),b=f&&f.querySelector("button");
  if(!b||!em||!ok){p.push("the signup form is missing");return finish(out)}
  var sent=0,of=window.fetch;window.fetch=function(){sent++;return of.apply(window,arguments)};
  em.value="site-check@example.com";ok.checked=false;b.click();if(sent)p.push("it sends with the consent box unticked");
  em.value="not-an-email";ok.checked=true;sent=0;b.click();if(sent)p.push("it sends with a bad email address");sent=0;
  if(!__ftCfg.send||p.length){out.unsent=1;return finish(out)}
  em.value="site-check@example.com";b.click();if(!sent){p.push("a good email with the box ticked isn't sent");return finish(out)}
  var n=0;(function wait(){if(/^Thanks!/.test(st.textContent)&&f.style.display==="none")return finish(out);
    if(++n>50){p.push("after sending, the visitor sees \""+st.textContent+"\" instead of the thank-you message");return finish(out)}setTimeout(wait,100)})()}
if(saved){var out=JSON.parse(saved),s0=document.getElementById("st0");S.removeItem("__ft");out.load=out.load.concat(errs());
  if(document.title!==title(out.step)||!s0)out.steps.push("after a reload the /"+out.step+" guide doesn't open");
  else if(!done(s0)||!/^1 of /.test(document.getElementById("prog").textContent))out.steps.push("step 1 on /"+out.step+" is no longer ticked after reloading the page");
  else{s0.querySelector(".chk").click();if(done(s0)||get(out.step).length)out.steps.push("unticking step 1 on /"+out.step+" doesn't clear it")}
  return signup(out)}
// Chrome ignores address changes after about 200 in 10 seconds, so the site's click handler doesn't get to make them.
var rs=history.replaceState;history.replaceState=history.pushState=function(){};
var out={load:errs(),pages:{},clicks:[],other:[],steps:[]},queue=["/"],seen={"/":1};
while(queue.length){var h=queue.shift();out.pages[h]=visit(h);
  var n=document.querySelectorAll("a").length;
  for(var i=0;i<n;i++){go(h);errs();var a=document.querySelectorAll("a")[i];if(!a)break;
    var href=a.getAttribute("href")||"",text=(a.innerText||a.getAttribute("aria-label")||"").trim().slice(0,60);
    if(href.charAt(0)!=="/"&&href.charAt(0)!=="#"||/^\/(\/|api\/)/.test(href)){out.other.push({page:h,href:href,text:text});continue}
    var u=href.split("#"),id=u[0].slice(1)||"home",j=u[1],to=j&&jump[j],r={page:h,href:href,text:text,problems:[]};
    if(href.charAt(0)==="#"){r.problems.push("it uses an old #address; link to /"+(u[1]||"")+" instead");out.clicks.push(r);continue}
    if(j&&!to)r.problems.push("there is no #"+j+" section to jump to");
    if(a.target){if(!known[id])r.problems.push("it opens a new tab on \""+id+"\", which isn't a page");out.clicks.push(r);continue}
    try{a.click()}catch(x){r.problems.push("click threw: "+x.message)}
    var e=errs();if(e.length)r.problems.push("JavaScript error: "+e.join("; "));
    if(!known[id])r.problems.push("no page called \""+id+"\": the click shows the home page instead");
    else{var want=title(id);
      if(document.title!==want)r.problems.push("title is \""+document.title+"\", expected \""+want+"\"");
      if(app.innerText.trim().length<200)r.problems.push("page is nearly empty");
      var e2=to&&document.getElementById(to);
      if(to&&!e2)r.problems.push("the #"+to+" section is missing");
      else if(e2&&Math.abs(e2.getBoundingClientRect().top)>2&&scrollY+innerHeight<root.scrollHeight-2)r.problems.push("it doesn't scroll to the #"+to+" section (it stays "+Math.round(e2.getBoundingClientRect().top)+"px down the page)");
      if(!seen[u[0]]){seen[u[0]]=1;queue.push(u[0])}}
    out.clicks.push(r)}}
tabs(out);
var t=T[0],c;out.step=t.s;go("/"+t.s);c=document.querySelector('.chk[data-i="0"]');
if(!c)out.steps.push("no step checkmark on /"+t.s);
else{c.click();if(!done(document.getElementById("st0"))||!/^1 of /.test(document.getElementById("prog").textContent))out.steps.push("ticking step 1 on /"+t.s+" doesn't mark it done")}
out.steps=out.steps.concat(errs().map(function(x){return "JavaScript error: "+x}));
rs.call(history,null,"","#"+t.s);S.setItem("__ft",JSON.stringify(out));location.reload()})()</script>'''

# Chrome's window is at least 500px wide, so the page runs in a 375px frame: a phone screen in the middle of
# a 525px window, which is where sips crops the screenshots (it ignores --cropOffset).
FRAME = '''<!DOCTYPE html><html><body style="margin:0"><iframe src="page.html%s" style="display:block;border:0;margin:0 75px;width:375px;height:%dpx"></iframe>
<script>addEventListener("message",function(e){var s=document.createElement("script");s.type="application/json";s.id="ft-result";s.textContent=e.data;document.body.appendChild(s)})</script></body></html>'''
BROWSER = [CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--hide-scrollbars']


def fetch(url, method='GET', data=None):
    headers = {'User-Agent': 'Mozilla/5.0 FollowThrough link check'}
    if data is not None:
        data, method = json.dumps(data).encode(), 'POST'
        headers.update({'Content-Type': 'application/json', 'Accept': 'application/json'})
    req = urllib.request.Request(url, data, headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return None, str(e)


def start_app():
    # A private copy of the app on a free port that writes emails to its own log instead of sending them.
    php = shutil.which('php') or os.path.expanduser('~/.config/herd-lite/bin/php')
    if os.path.exists(os.path.join(ROOT, 'bootstrap', 'cache', 'config.php')) or not os.path.exists(php):
        return None, 'php not found, or the settings are cached (php artisan config:clear) so a test email could go out for real'
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    url = 'http://127.0.0.1:%d' % s.getsockname()[1]
    s.close()
    env = dict(os.environ, MAIL_MAILER='log', MAIL_LOG_CHANNEL='stderr', MAIL_TO='site-check@example.com', CACHE_STORE='array')
    app = subprocess.Popen([php, '-S', url[7:], os.path.join(ROOT, 'vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php')],
                           cwd=os.path.join(ROOT, 'public'), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    for _ in range(50):
        if fetch(url + '/')[0] == 200:
            return app, url
        time.sleep(0.2)
    app.kill()
    return None, 'the test copy of the app did not start'


def chrome(tmp, h, height, *flags):
    frame = os.path.join(tmp, 'frame%s.html' % h.replace('#', '-'))
    open(frame, 'w').write(FRAME % (h, height))
    return subprocess.run(BROWSER + ['--user-data-dir=' + os.path.join(tmp, 'profile' + h.replace('#', '-')), '--window-size=525,%d' % height]
                          + list(flags) + ['file://' + frame], capture_output=True, text=True, timeout=120).stdout


def crawl(html, form):
    html = re.sub(r'FORM_URL="([^"]*)"', lambda m: 'FORM_URL="%s"' % urllib.parse.urljoin(form, m.group(1)), html, 1)
    html = html.replace('<head>', '<head>' + SPY % json.dumps({'send': bool(app)}), 1).replace('</body>', CRAWL + '</body>', 1)
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, 'page.html'), 'w').write(html)
        dom = chrome(tmp, '', 812, '--virtual-time-budget=10000', '--dump-dom')
    m = re.search(r'<script type="application/json" id="ft-result">(.*?)</script>', dom, re.S)
    return json.loads(m.group(1)) if m else None


def screenshots(html, pages, prefix):
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, 'page.html'), 'w').write(html)

        def shot(h):
            # The page runs from a file, so it opens a page from its old #address.
            name = h.strip('/') or 'home'
            png, height = os.path.join(SHOTS, prefix + name + '.png'), min(pages[h]['height'], 16000)
            chrome(tmp, '#' + name, height, '--virtual-time-budget=3000', '--screenshot=' + png)
            subprocess.run(['sips', '-c', str(height), '375', png], capture_output=True)
        with concurrent.futures.ThreadPoolExecutor(4) as pool:
            list(pool.map(shot, [h for h in pages if 'height' in pages[h]]))


def part(mine, theirs):
    # What a changed line of the view is, for naming differences: variables, a function, a guide or the styles.
    def values(line):
        return dict(re.findall(r'(?:^var\s+|,)([A-Za-z_$][\w$]*)=("(?:[^"\\]|\\.)*"|[^,;]*)', line)) if line.startswith('var ') else {}
    line = mine or theirs
    m = re.match(r'(?:function\s+([\w$]+))|([A-Z]\w*(?:\.\w+)*)\s*=|\'?([\w-]+)\'?:\{lic:', line)
    if values(line):
        a, b = values(mine), values(theirs)
        return ', '.join(k for k in list(a) + [k for k in b if k not in a] if a.get(k) != b.get(k)) or 'var ' + ', '.join(a or b)
    if m:
        return m.group(1) and 'function ' + m.group(1) or m.group(2) or 'FULL.' + m.group(3)
    return 'styles' if re.match(r'[.:@a-z*][^=]*\{', line) else line[:60]


def differences(html):
    mine, theirs = open(os.path.join(ROOT, 'resources', 'views', 'home.blade.php')).read().splitlines(), html.splitlines()
    parts = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, mine, theirs, autojunk=False).get_opcodes():
        for k in range(max(a2 - a1, b2 - b1)) if op != 'equal' else []:
            name = part(mine[a1 + k] if a1 + k < a2 else '', theirs[b1 + k] if b1 + k < b2 else '')
            if name not in parts:
                parts.append(name)
    return parts


def spread(on):
    on = sorted(set(on), key=on.index)
    return on[0] if len(on) == 1 else '%d pages e.g. %s' % (len(on), on[0])


fails, warns, external, sent = [], [], {}, 0
if not os.path.exists(CHROME):
    sys.exit('Google Chrome not found at ' + CHROME)
app, form = start_app() if local else (None, base + '/')
if local and not app:
    fails.append('signup form not tested: ' + form)
    form = base + '/'
try:
    # The server must turn bad signups away, not only the browser.
    for data, what in (({'email': 'not-an-email', 'guide': 'trade', 'consent': True}, 'a bad email address'),
                       ({'email': 'site-check@example.com', 'guide': 'trade', 'consent': False}, 'the consent box unticked')):
        status, err = fetch(urllib.parse.urljoin(form, '/api/playbook'), data=data)
        if status and status != 422:
            fails.append('signup: the server doesn\'t turn away a signup with %s (status %s, expected 422)' % (what, status))
    os.makedirs(SHOTS, exist_ok=True)
    for f in os.listdir(SHOTS):
        if f.endswith('.png'):
            os.remove(os.path.join(SHOTS, f))
    for path in paths:
        url, at = base + path, path.rstrip('/')
        status, html = fetch(url)
        if status != 200:
            fails.append('%s does not load (%s)' % (url, status or html))
            continue
        for tag in re.findall(r'<(?:link|script|img)\b[^>]*>', html):
            src = re.search(r'(?:href|src)="([^"]+)"', tag)
            if not src or re.search(r'rel="(preconnect|dns-prefetch)"', tag):
                continue
            external.setdefault(urllib.parse.urljoin(url, src.group(1)), set()).add(path + ' (resource)')
        if compare and path == '/':
            parts = differences(html)
            print('%s is %s' % (url, 'the same as this computer\'s copy' if not parts else 'different from this computer\'s copy'))
            if parts:
                warns.append('%s differs from resources/views/home.blade.php on this computer in: %s' % (url, '; '.join(parts)))
        if not re.search(r'<meta name="description" content="[^"]+"', html):
            warns.append('%s: no description for search results (<meta name="description">)' % path)
        r = crawl(html, form)
        if r is None:
            fails.append('%s: page script crashed before the crawl ran (open it in a browser and check the console)' % url)
            continue
        for e in r['load'] + r['errors2']:
            fails.append('%s: JavaScript error on load: %s' % (url, e))
        pages = r['pages']
        titles, wide, faint, left, noalt = {}, {}, {}, {}, {}
        for h, p in pages.items():
            if p['errors']:
                fails.append('%s%s: JavaScript error: %s' % (url.rstrip('/'), h, '; '.join(p['errors'])))
            if 'title' not in p:
                continue
            titles.setdefault(p['title'], []).append(h)
            if p['h1'] != 1:
                warns.append('%s%s: %s main heading (h1), expected 1' % (at, h, p['h1'] or 'no'))
            for src in p['noalt']:
                noalt.setdefault(src, []).append(h)
            for w in p['wide']:
                wide.setdefault(w, []).append(h)
            for mode, bad in p['faint'].items():
                for b in bad:
                    faint.setdefault((mode, b['colors'], b['ratio'], b['need']), []).append((h, b['text']))
            for ph in PLACEHOLDERS:
                if ph in p['text']:
                    left.setdefault(ph, []).append(h)
        for t, on in titles.items():
            if len(on) > 1:
                warns.append('%s pages %s share the title "%s"' % (path, ', '.join(on), t))
        for src, on in noalt.items():
            warns.append('%s image %s has no alt text, on %s' % (path, src, spread(on)))
        for w, on in wide.items():
            fails.append('%s at phone width (375px), on %s: %s' % (path, spread(on), w))
        for (mode, colors, ratio, need), on in faint.items():
            warns.append('%s %s mode: hard-to-read text, %s (contrast %s, needs %s), on %s: %s' % (path, mode, colors, ratio, need, spread([h for h, _ in on]), on[0][1]))
        for ph, on in left.items():
            fails.append('%s placeholder %s still on %s' % (path, ph, ', '.join(on)))
        broken = {}
        for c in r['clicks']:
            # A page that opens when clicked must also open when its address is typed in or shared.
            if c['href'].startswith('/'):
                external.setdefault(urllib.parse.urljoin(url, c['href'].split('#')[0]), set()).add(at + c['page'])
            for p in c['problems']:
                broken.setdefault((c['href'], c['text'], p), []).append(c['page'])
        for (href, text, p), on in broken.items():
            fails.append('%s link "%s" (%s), on %d page(s) e.g. %s: %s' % (path, text, href, len(set(on)), on[0], p))
        for p in r['tabs']:
            fails.append('%s objection tabs on the home page: %s' % (path, p))
        for p in r['steps']:
            fails.append('%s step checkmarks: %s' % (path, p))
        for p in r['signup']:
            fails.append('%s signup form: %s' % (path, p))
        for o in r['other']:
            href = o['href']
            if href.startswith('mailto:'):
                addr = href[7:].split('?')[0]
                if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-z]{2,}', addr):
                    fails.append('%s%s: mailto link "%s" has a bad address: %s' % (at, o['page'], o['text'], addr))
            elif href.startswith(('tel:', 'javascript:')) or not href:
                warns.append('%s%s: link "%s" has href "%s"' % (at, o['page'], o['text'], href))
            else:
                external.setdefault(urllib.parse.urljoin(url, href), set()).add(at + o['page'])
        screenshots(html, pages, path.strip('/').replace('/', '-') + '-' if path != '/' else '')
        sent += not r.get('unsent') and not r['signup']
        print('%s: %d pages, %d link clicks, %d objection tabs, test signup %s' % (url, len(pages), len(r['clicks']), r['tabn'],
              'not sent (only sent on this computer)' if r.get('unsent') else 'sent to a test copy of the app'))
finally:
    if app:
        app.terminate()
        log = app.communicate()[1]
if sent and log.count('Subject: Free playbook:') < sent:
    fails.append('signup: the thank-you message showed, but no email was written to the test copy\'s log')
print('Screenshots at phone width: ' + os.path.relpath(SHOTS))

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

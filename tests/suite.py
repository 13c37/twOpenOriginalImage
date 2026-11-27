"""Release checks for twOpenOriginalImage.

Runs the userscript on a simulated x.com page in headless Chromium and checks the viewer, downloads,
scrolling, settings and fonts. Photos are served locally with an artificial delay; one photo exists
only as PNG to exercise the format fallback.

    pip install -r tests/requirements.txt && python -m playwright install chromium
    python tests/suite.py                # tests ../twOpenOriginalImage.user.js
    python tests/suite.py path/to/other.user.js
"""
import asyncio, base64, json, os, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BASE = Path(__file__).resolve().parent
CACHE = BASE / '.cache'
SCRIPT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else BASE.parent / 'twOpenOriginalImage.user.js'
DELAY = 0.4                 # simulated download time per full-size photo
PNG_ONLY = {'111_5'}        # photo 5 of the 20-photo post exists only as png
R = []

def check(name, ok, info=''):
    R.append((name, bool(ok)))
    print(('PASS ' if ok else 'FAIL ') + name + (('  [' + str(info) + ']') if info != '' else ''), flush=True)

async def make_images(img):
    """Draw the 20 test photos (jpg + png) with the browser's canvas: no image library needed."""
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
        pg = await b.new_page()
        files = await pg.evaluate("""() => {
            const out = {};
            for (let i = 0; i < 20; i++) {
                const c = document.createElement('canvas');
                c.width = 1600; c.height = (i % 3) ? 1200 : 2000;
                const g = c.getContext('2d');
                g.fillStyle = `hsl(${i * 18}, 60%, 55%)`; g.fillRect(0, 0, c.width, c.height);
                g.fillStyle = '#fff'; g.font = '48px sans-serif'; g.fillText('photo ' + (i + 1), 40, 80);
                out[`p${i + 1}.jpg`] = c.toDataURL('image/jpeg', 0.85).split(',')[1];
                out[`p${i + 1}.png`] = c.toDataURL('image/png').split(',')[1];
            }
            return out;
        }""")
        await b.close()
    for name, data in files.items():
        (img / name).write_bytes(base64.b64decode(data))

def prepare():
    """Test photos + the GM_config build pinned in the script's @require."""
    img = CACHE / 'img'
    img.mkdir(parents=True, exist_ok=True)
    if not (img / 'p20.png').exists():
        asyncio.run(make_images(img))
    url = re.search(r'@require\s+(\S+gm_config\.js)', SCRIPT.read_text(encoding='utf-8')).group(1)
    gm = CACHE / ('gm_config_' + re.sub(r'\W', '_', url)[-60:] + '.js')
    if not gm.exists():
        gm.write_bytes(urllib.request.urlopen(url, timeout=60).read())
    return img, gm

OV = "[id$=_image_overlay_container]"; LD = "[id$=_image_overlay_loading]"; HD = "[id$=_image_overlay_header]"

async def setup(p, query='', locale='en-US', fixture='fixture.html', path='/home'):
    b = await p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    ctx = await b.new_context(viewport={'width': 1280, 'height': 720}, locale=locale)
    st = {'errs': [], 'reqs': [], 't0': time.time()}
    async def x(r): await r.fulfill(path=BASE / fixture, content_type='text/html')
    async def local(r):
        f = r.request.url.split('/')[-1]
        await r.fulfill(path=SCRIPT if f == 'script.user.js' else GM_CONFIG, content_type='application/javascript')
    async def pbs(r):
        u = r.request.url; m = re.search(r'/media/(\d+)_(\d+)', u); fm = re.search(r'format=(\w+)', u) or re.search(r'\.(jpg|png)', u)
        key = f'{m.group(1)}_{m.group(2)}'; fm = fm.group(1) if fm else 'jpg'; orig = 'name=orig' in u
        st['reqs'].append((time.time() - st['t0'], key, fm, orig))
        if (key in PNG_ONLY and fm != 'png') or fm not in ('jpg', 'png'):
            await r.fulfill(status=404, body=''); return
        if orig: await asyncio.sleep(DELAY)
        n = (int(m.group(2)) - 1) % 20 + 1
        await r.fulfill(path=IMG / f'p{n}.{fm}', content_type='image/' + ('jpeg' if fm == 'jpg' else 'png'))
    await ctx.route('https://x.com/**', x); await ctx.route('https://local.test/**', local); await ctx.route('https://pbs.twimg.com/**', pbs)
    pg = await ctx.new_page()
    pg.on('pageerror', lambda e: st['errs'].append(str(e)))
    await pg.goto('https://x.com' + path + query); await pg.wait_for_timeout(1500)
    return b, ctx, pg, st
async def ev(pg,js): return await pg.evaluate(js)
async def ready(pg,t=20000):
    await pg.wait_for_function(f"()=>{{const l=document.querySelector('{LD}');return l&&getComputedStyle(l).display=='none'}}",timeout=t)
async def status(pg): return (await ev(pg,"()=>document.querySelector('[class$=_status_overlay]').textContent")).strip()
async def shown(pg, n, t=12000):
    """Media ids of the photos in the viewer, in order (None: not loaded yet). Waits for n loaded ones; returns what is there on timeout."""
    js = f"[...document.querySelectorAll('{OV} img.original-image')].map(i=>(i.src.match(/media\\/([^?.:]+)/)||[])[1])"
    try:
        await pg.wait_for_function(f"n=>{js}.filter(Boolean).length>=n", arg=n, timeout=t)
    except PlaywrightTimeoutError:
        pass
    await pg.wait_for_timeout(400)
    return await ev(pg, f"()=>{js}")
async def viewer_open(pg):
    return await ev(pg, f"()=>{{const c=document.querySelector('{OV}');return !!c&&getComputedStyle(c).display!='none'}}")
async def viewer_post(pg):
    """[post url, display name, user name] the open viewer works with."""
    return await ev(pg, "()=>{const a=document.querySelector('a[class$=_close_overlay]');return a?[a.href,a.getAttribute('data-fullname'),a.getAttribute('data-username')]:null}")
async def close_viewer(pg):
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
async def buttons(pg):
    """[article id, sits in an action bar] for every post button."""
    return await ev(pg, """()=>[...document.querySelectorAll('.twOpenOriginalImageButton')].map(c=>{const g=c.closest('[role=group]');
        return [c.closest('article')?.id, !!g && !!g.querySelector('[data-engagement-action="reply"]')]}).sort()""")
def ids(post, n): return [f'{post}_{i}' for i in range(1, n + 1)]
def cfg_query(**options): return '?cfg=' + urllib.parse.quote(json.dumps(options))

async def new_client(p):
    """x's redesigned web client: no #react-root, data-testid or <time> (fixture_new.html)."""
    new = {'fixture': 'fixture_new.html'}
    photo = lambda path: f'a[href="{path}"]'
    # ---- F: timeline ----
    b,ctx,pg,st=await setup(p,**new)
    st['reqs'].clear()
    await pg.click(photo('/nasa/status/111/photo/2')); await pg.wait_for_timeout(400)
    check('F1 new client: clicking a photo opens the viewer', await viewer_open(pg))
    nav=await ev(pg,'__nav')
    check('F2 new client: x does not also get the click', await viewer_open(pg) and nav==[], nav)
    got=await shown(pg,20)
    check('F3 new client: all 20 photos, though only 4 are on the page', got==ids('111',20), (len(got),got[:5]))
    orig=[r[1] for r in st['reqs'] if r[3]]
    check('F4 new client: clicked photo requested first', orig[:1]==['111_2'], orig[:3])
    info=await viewer_post(pg)
    check('F5 new client: viewer has the post url and author', info==['https://x.com/nasa/status/111','NASA Artemis','nasa'], info)
    link=await ev(pg,f"()=>document.querySelector('{OV} a.image-link')?.href")
    check('F6 new client: viewer photo links point to the post', link=='https://x.com/nasa/status/111/photo/1', link)
    await close_viewer(pg)
    await pg.click(photo('/carol/status/666/photo/1')); got=await shown(pg,6)
    check('F7 new client: full list from tweet.media_entities2, video skipped', got==ids('666',6), got)
    await close_viewer(pg)
    await ev(pg,'()=>{__nav.length=0}')
    await pg.click('#t555 img[src*="/media/"]'); await pg.wait_for_timeout(500)
    nav=await ev(pg,'__nav')
    check('F8 new client: video post is left to x', not await viewer_open(pg) and nav==['/vic/status/555'], nav)
    await close_viewer(pg)
    await ev(pg,'()=>{__nav.length=0}')
    await pg.click(photo('/spacex/status/222/photo/1'),modifiers=['Control']); await pg.wait_for_timeout(500)
    nav=await ev(pg,'__nav')
    check('F9 new client: ctrl+click is left to x', not await viewer_open(pg) and '/spacex/status/222/photo/1' in nav, nav)
    await close_viewer(pg)
    await ev(pg,'()=>{__nav.length=0;__xhr.length=0}')
    await pg.click(photo('/spacex/status/222/photo/1'),modifiers=['Shift']); await pg.wait_for_timeout(1500)
    xhr,nav=await ev(pg,'[__xhr,__nav]')
    check('F10 new client: shift+click downloads that photo in original size', len(xhr)==1 and '/media/222_1' in xhr[0] and 'name=orig' in xhr[0] and nav==[], (xhr,nav))
    await pg.click(photo('/spacex/status/222/photo/1')); got=await shown(pg,1)
    check('F11 new client: photo with its own alt text', got==['222_1'], got)
    await close_viewer(pg)
    await ev(pg,'()=>{scrollTo(0,0);__addPost()}'); await pg.wait_for_timeout(600)
    await pg.click(photo('/late/status/1234/photo/2')); got=await shown(pg,2)
    check('F12 new client: post rendered later works too', got==ids('1234',2), got)
    check('F13 new client: no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- G: quote posts ----
    b,ctx,pg,st=await setup(p,**new)
    await pg.click(photo('/alice/status/333/photo/1')); got=await shown(pg,3)
    check('G1 new client: quote post shows own photos, then quoted ones', got==['333_1','444_1','444_2'], got)
    await b.close()
    b,ctx,pg,st=await setup(p,**new)
    st['reqs'].clear()
    await pg.click(photo('/bob/status/444/photo/2')); got=await shown(pg,3)
    orig=[r[1] for r in st['reqs'] if r[3]]; info=await viewer_post(pg)
    check('G2 new client: quoted photo opens first, under the outer post', orig[:1]==['444_2'] and info==['https://x.com/alice/status/333','Alice','alice'], (orig[:2],info))
    await close_viewer(pg)
    await pg.click(photo('/erin/status/888/photo/1')); got=await shown(pg,1); info=await viewer_post(pg)
    check('G3 new client: quote of a photo, outer post has none', got==['888_1'] and info==['https://x.com/dave/status/777','Dave','dave'], (got,info))
    nav=await ev(pg,'__nav')
    check('G4 new client: quoted photo clicks do not reach x', got==['888_1'] and nav==[], nav)
    check('G5 new client: no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- I: post button and keyboard shortcut ----
    b,ctx,pg,st=await setup(p,cfg_query(DISPLAY_ORIGINAL_BUTTONS=True),**new)
    await pg.wait_for_timeout(500)
    got=await buttons(pg)
    check('I1 new client: one button per photo post, in its action bar', got==[[a,True] for a in ['t111','t222','t333','t666','t777']], got)
    if got:
        await pg.click('#t666 .twOpenOriginalImageButton button')
    shots=await shown(pg,6)
    check('I2 new client: post button opens that post', shots==ids('666',6), shots)
    await close_viewer(pg)
    await ev(pg,"()=>document.querySelector('[data-href=\"/alice/status/333\"]').focus()")
    await pg.keyboard.press('v'); shots=await shown(pg,3)
    check('I3 new client: key v opens the focused post', shots==['333_1','444_1','444_2'], shots)
    check('I4 new client: no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- J: opened post, light theme ----
    b,ctx,pg,st=await setup(p,'?light=1',path='/spacex/status/222',**new)
    await pg.keyboard.press('v'); got=await shown(pg,1); info=await viewer_post(pg)
    check('J1 status page: key v opens the opened post', got==['222_1'] and info==['https://x.com/spacex/status/222','SpaceX','spacex'], (got,info))
    bg=await ev(pg,f"()=>{{const h=document.querySelector('{HD}');return h&&getComputedStyle(h).backgroundColor}}")
    check('J2 status page: light mode bar is white', got==['222_1'] and bg=='rgb(255, 255, 255)', bg)
    check('J3 status page: no page errors', not st['errs'], st['errs'][:2])
    await b.close()
    b,ctx,pg,st=await setup(p,path='/dave/status/777',**new)
    await pg.click(photo('/erin/status/888/photo/1')); got=await shown(pg,1); info=await viewer_post(pg)
    check('J4 status page: post url when only the quote has photos', got==['888_1'] and info==['https://x.com/dave/status/777','Dave','dave'], (got,info))
    check('J5 status page: no page errors', not st['errs'], st['errs'][:2])
    await b.close()

async def main():
  async with async_playwright() as p:
    # ---- A: 20-photo post, dark ----
    b,ctx,pg,st=await setup(p)
    st['reqs'].clear(); st['t0']=time.time()
    await pg.click('[id="111"] a[href$="/photo/1"] img'); await pg.wait_for_timeout(300)
    v=await ev(pg,f"()=>{{const c=document.querySelector('{OV}'),l=document.querySelector('{LD}');return [getComputedStyle(c).display,getComputedStyle(l).display,l.innerText.trim()]}}")
    check('A1 viewer visible right after click', v[0]=='block', v[0])
    check('A2 spinner with progress text', v[1]=='block' and '0 / 20' in v[2], v[2])
    await ready(pg); t=time.time()-st['t0']
    check('A3 first photo shown fast (0.4s per photo; all-at-once took ~8s)', t<2.0, '%.2fs'%t)
    await pg.wait_for_timeout(6000)
    imgs=await ev(pg,f"()=>[...document.querySelectorAll('{OV} img.original-image')].map(i=>i.naturalWidth>0)")
    check('A4 all 20 photos loaded', len(imgs)==20 and all(imgs), sum(imgs))
    orig=[r for r in st['reqs'] if r[3]]
    check('A5 clicked photo requested first and alone', orig and orig[0][1]=='111_1' and (len(orig)<2 or orig[1][0]-orig[0][0]>0.3), [o[1] for o in orig[:4]])
    dl=await ev(pg,f"()=>{{const a=[...document.querySelectorAll('{OV} .download-link')];return [a.length,a[4]&&a[4].href,a[4]&&a[4].download,a[0]&&a[0].href]}}")
    check('A6 png-only photo: download link switched to png', dl[1] and 'format=png' in dl[1] and dl[2].endswith('.png'), dl[2])
    check('A7 normal photo: download link stays jpg orig', dl[3] and 'format=jpg' in dl[3] and 'name=orig' in dl[3])
    hdr=await ev(pg,f"()=>{{const h=document.querySelector('{HD}');return [h.innerText, h.getBoundingClientRect().height]}}")
    check('A8 bar: old compact style, 26px', hdr[1]==26, hdr[1])
    check('A9 bar text all lowercase', hdr[0]==hdr[0].lower() and '[j]next' in hdr[0] and 'close [esc]' in hdr[0], hdr[0].replace('\n',' | '))
    fonts=await ev(pg,f"()=>[...new Set(['{HD} .help-item','[class$=_status_overlay]','[class$=_close_overlay]','[class$=_loading_text]','{OV} .download-link'].map(s=>{{const e=document.querySelector(s);return e?getComputedStyle(e).fontFamily.split(',')[0].trim():'missing'}}))]")
    check('A10 one font (Chirp) across bar/loading/download buttons', fonts==['TwitterChirp'], fonts)
    # keys
    await pg.keyboard.press('j'); await pg.wait_for_timeout(700); s1=await status(pg)
    await pg.keyboard.press('j'); await pg.wait_for_timeout(700); s2=await status(pg)
    await pg.keyboard.press('k'); await pg.wait_for_timeout(700); s3=await status(pg)
    check('A11 keys j/j/k navigate 2,3,2', (s1,s2,s3)==('2 / 20','3 / 20','2 / 20'), (s1,s2,s3))
    size0=await ev(pg,"()=>document.querySelector('.help-item:nth-child(5)')?.textContent")
    await pg.keyboard.press('s'); await pg.wait_for_timeout(400)
    size1=await ev(pg,f"()=>[...document.querySelectorAll('{HD} .help-item')].map(e=>e.textContent).find(t=>t.startsWith('[s]'))")
    check('A12 key s changes size mode (lowercase)', size1 and size1!=size0 and size1==size1.lower(), size1)
    await pg.keyboard.press('b'); await pg.wait_for_timeout(400)
    bg=await ev(pg,f"()=>[...document.querySelectorAll('{HD} .help-item')].map(e=>e.textContent).find(t=>t.startsWith('[b]'))")
    check('A13 key b toggles background', bg=='[b]bgcolor:white', bg)
    await pg.keyboard.press('s'); await pg.keyboard.press('s'); await pg.keyboard.press('s'); await pg.keyboard.press('b'); await pg.wait_for_timeout(500)
    # wheel
    y0=await ev(pg,'scrollY')
    await pg.mouse.move(640,12)
    for _ in range(5): await pg.mouse.wheel(0,400)
    await pg.wait_for_timeout(300)
    check('A14 wheel on top bar does not scroll X', await ev(pg,'scrollY')==y0)
    await pg.mouse.move(1200,500)
    for _ in range(80): await pg.mouse.wheel(0,700)
    await pg.wait_for_timeout(700)
    bot=await ev(pg,f"()=>{{const c=document.querySelector('{OV}');return c.scrollTop+c.clientHeight>=c.scrollHeight-2}}")
    check('A15 viewer scrolls to the last photo', bot)
    check('A16 scrolling past the end does not scroll X', await ev(pg,'scrollY')==y0)
    for _ in range(80): await pg.mouse.wheel(0,-700)
    await pg.wait_for_timeout(700)
    check('A17 scrolling above the first photo does not scroll X', await ev(pg,'scrollY')==y0)
    # ZIP
    await pg.keyboard.press('z'); await pg.wait_for_timeout(2500)
    xhr=await ev(pg,"()=>__xhr.filter(u=>u.includes('pbs.twimg.com'))")
    p5=[u for u in xhr if '111_5' in u]
    check('A18 ZIP requests all 20 photos', len(set(re.sub(r'\?.*','',u) for u in xhr))==20, len(xhr))
    check('A19 ZIP uses the working format for the png-only photo', p5 and all('format=png' in u for u in p5), p5[:1])
    # duplicate click while open + esc
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(400)
    closed=await ev(pg,f"()=>[getComputedStyle(document.querySelector('{OV}')).display, getComputedStyle(document.querySelector('{HD}')).display, document.documentElement.style.overflowY]")
    check('A20 esc closes viewer and restores page scrolling', closed[0]=='none' and closed[1]=='none' and closed[2] in ('','auto','visible'), closed)
    check('A21 no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- B: single photo, light mode ----
    b,ctx,pg,st=await setup(p,'?light=1')
    await pg.evaluate('scrollTo(0,300)'); await pg.wait_for_timeout(200)
    await pg.click('[id="222"] a[href$="/photo/1"] img'); await ready(pg); await pg.wait_for_timeout(300)
    hl=await ev(pg,f"()=>{{const h=document.querySelector('{HD}');return [getComputedStyle(h).backgroundColor,h.innerText]}}")
    check('B1 light mode bar is white', hl[0]=='rgb(255, 255, 255)', hl[0])
    check('B2 1-photo post: no next/previous items', '[j]' not in hl[1], hl[1].replace('\n',' | '))
    y0=await ev(pg,'scrollY')
    for pos in [(1200,650),(640,12),(100,400),(640,700)]:
        await pg.mouse.move(*pos)
        for _ in range(6): await pg.mouse.wheel(0,500)
        for _ in range(6): await pg.mouse.wheel(0,-500)
    await pg.wait_for_timeout(400)
    check('B3 1-photo post: wheel anywhere never scrolls X', await ev(pg,'scrollY')==y0, y0)
    check('B4 no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- C: new-tab mode (overlay off); window.open backed by a same-page frame so requests are routed ----
    cfg=urllib.parse.quote(json.dumps({'DISPLAY_OVERLAY':False}))
    b,ctx,pg,st=await setup(p,'?iframeopen=1&cfg='+cfg)
    await pg.click('[id="111"] a[href$="/photo/2"] img'); await pg.wait_for_timeout(2500)
    f=[f for f in pg.frames if f!=pg.main_frame][-1]
    c=await f.evaluate("()=>[...document.querySelectorAll('img.original-image')].map(i=>[i.naturalWidth,i.src.split('/').pop()])")
    check('C1 new-tab mode shows the clicked photo in original size', len(c)==1 and c[0][0]==1600 and '111_2' in c[1-1][1] and 'name=orig' in c[0][1], c)
    check('C2 no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- D: Japanese UI ----
    b,ctx,pg,st=await setup(p,'',locale='ja-JP')
    await pg.click('[id="111"] a[href$="/photo/1"] img'); await ready(pg); await pg.wait_for_timeout(300)
    jt=await ev(pg,f"()=>document.querySelector('{HD}').innerText")
    check('D1 Japanese UI opens viewer', '1 / 20' in jt, jt.replace('\n',' | ')[:80])
    check('D2 no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- E: settings window ----
    b,ctx,pg,st=await setup(p)
    menu=await ev(pg,"()=>__menu.map(m=>m.n)")
    check('E1 menu entry lowercase', menu==['settings'], menu)
    await ev(pg,"()=>__menu[0].f()"); await pg.wait_for_timeout(800)
    fr=[f for f in pg.frames if f!=pg.main_frame][0]
    for theme in ['dark','light']:
        r=await fr.evaluate(f"""()=>{{const _v=document.querySelector('.tooi-version');if(_v&&_v.textContent=='vTEST')_v.remove();const t=document.querySelector('[id$=Config_field_UI_THEME]');t.value='{theme}';t.dispatchEvent(new Event('change',{{bubbles:true}}));
          const s=document.querySelector('.tooi-scroll');s.scrollTop=s.scrollHeight;
          const h=document.querySelector('.config_header').getBoundingClientRect(),c=document.querySelector('.tooi-credits').getBoundingClientRect(),f=document.querySelector('[id$=Config_buttons_holder]').getBoundingClientRect(),sr=s.getBoundingClientRect();
          const txt=document.body.innerText+[...document.querySelectorAll('option')].map(o=>o.textContent).join('')+[...document.querySelectorAll('[title],[placeholder]')].map(e=>(e.title||'')+(e.placeholder||'')).join('');
          return {{noOverlap: sr.top>=h.bottom-0.5 && sr.bottom<=c.top+0.5 && c.bottom<=f.top+0.5, lower: txt===txt.toLowerCase(), font:getComputedStyle(document.querySelector('.field_label')).fontFamily.split(',')[0]}}}}""")
        check(f'E2 settings {theme}: list never under header/credits/buttons', r['noOverlap'])
        check(f'E3 settings {theme}: all text lowercase', r['lower'])
        check(f'E4 settings {theme}: Chirp font', r['font']=='TwitterChirp', r['font'])
    check('E5 no page errors', not st['errs'], st['errs'][:2])
    await b.close()

    # ---- F to J: x's redesigned web client ----
    await new_client(p)
  n=sum(ok for _,ok in R); print(f'\n{n}/{len(R)} passed')
  return n==len(R)

if __name__ == '__main__':
    IMG, GM_CONFIG = prepare()
    print('testing', SCRIPT.name, re.search(r'@version\s+(\S+)', SCRIPT.read_text(encoding='utf-8')).group(1))
    sys.exit(0 if asyncio.run(main()) else 1)

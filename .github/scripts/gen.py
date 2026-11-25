import json, subprocess, random, math, os
os.makedirs("assets", exist_ok=True)
random.seed(3)
U = "shinmentakezo07"

def gh(*a):
    return json.loads(subprocess.check_output(["gh", "api", *a]))

# ---------- live data ----------
repos = json.loads(subprocess.check_output(["gh", "repo", "list", U, "--limit", "300", "--json",
                                            "name,isFork,stargazerCount,pushedAt"]))
own = [r for r in repos if not r["isFork"]]
langs = {}
for r in own:
    try:
        for k, v in gh(f"repos/{U}/{r['name']}/languages").items():
            langs[k] = langs.get(k, 0) + v
    except Exception:
        pass
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda x: -x[1])[:5]
stars = sum(r["stargazerCount"] for r in repos)
nrepos = len(repos)

INK, PAPER, RED, GOLD = "#0b0b0d", "#f1e9d6", "#e63946", "#d4a017"
FONT_BRUSH = "'Yuji Syuku','Shippori Mincho','Noto Serif JP',serif"
FONT_MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"

HALFTONE = f'''<pattern id="ht" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<circle cx="4" cy="4" r="1.6" fill="{INK}" opacity=".18"/></pattern>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="3" seed="4"/>
<feDisplacementMap in="SourceGraphic" scale="6"/></filter>
<filter id="paper"><feTurbulence baseFrequency=".9" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .08 0"/>
<feComposite in2="SourceGraphic" operator="in"/></filter>'''

def panel_frame(w, h):
    return (f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="{INK}" stroke-width="7" filter="url(#rough)"/>'
            f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="url(#ht)" opacity=".0"/>')

def speedlines(cx, cy, n, r1, r2, color, op=".55"):
    s = ""
    for i in range(n):
        a = i / n * 2 * math.pi + random.uniform(-.02, .02)
        w = random.uniform(1, 5)
        x1, y1 = cx + math.cos(a) * r1, cy + math.sin(a) * r1
        x2, y2 = cx + math.cos(a) * r2, cy + math.sin(a) * r2
        s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w:.1f}" opacity="{op}"/>'
    return s

# ================= 1. HERO (manga splash page) =================
W, H = 1200, 520
hero = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{HALFTONE}
<clipPath id="c"><rect x="6" y="6" width="{W-12}" height="{H-12}"/></clipPath>
<linearGradient id="sunG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a5f"/><stop offset="1" stop-color="{RED}"/></linearGradient>
</defs>
<style>
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes ink{{from{{stroke-dashoffset:3000}}to{{stroke-dashoffset:0}}}}
@keyframes stamp{{0%{{opacity:0;transform:scale(3) rotate(-25deg)}}60%{{opacity:1;transform:scale(.9) rotate(-8deg)}}100%{{opacity:1;transform:scale(1) rotate(-8deg)}}}}
@keyframes cut{{0%,70%{{transform:translateX(-1400px)}}78%,100%{{transform:translateX(1400px)}}}}
@keyframes split{{0%,72%{{transform:none}}76%{{transform:translate(6px,-4px)}}82%,100%{{transform:none}}}}
@keyframes jitter{{0%,100%{{transform:translate(0,0)}}25%{{transform:translate(1px,-1px)}}50%{{transform:translate(-1px,1px)}}75%{{transform:translate(1px,1px)}}}}
@keyframes fade{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.brush{{font:900 150px {FONT_BRUSH};fill:{INK}}}
.en{{font:900 64px Impact,'Bebas Neue','Arial Black',sans-serif;letter-spacing:6px;fill:{INK}}}
.tag{{font:700 18px {FONT_MONO};letter-spacing:4px}}
</style>
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<rect width="{W}" height="{H}" filter="url(#paper)" fill="{PAPER}"/>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="url(#ht)"/>
  <g style="transform-origin:860px 250px;animation:spin 120s linear infinite">{speedlines(860, 250, 90, 190, 900, INK, ".35")}</g>
  <circle cx="860" cy="250" r="175" fill="url(#sunG)"/>
  <circle cx="860" cy="250" r="175" fill="url(#ht)"/>
  <!-- ronin silhouette -->
  <g style="animation:split 5s ease-in-out infinite" fill="{INK}">
    <path d="M800 470 L812 330 Q790 300 815 268 Q805 240 830 222 Q860 205 885 225 Q905 245 895 272 Q925 300 905 335 L925 470Z"/>
    <path d="M770 228 Q860 175 950 228 L940 236 Q860 200 780 236Z"/>
    <path d="M905 300 L1060 150 L1066 156 L915 312Z"/>
    <rect x="1055" y="142" width="18" height="6" transform="rotate(-44 1064 145)"/>
  </g>
  <!-- slash -->
  <g style="animation:cut 5s cubic-bezier(.8,0,.2,1) infinite">
    <path d="M-200 520 L1400 -40 L1400 -30 L-200 530Z" fill="#fff"/>
    <path d="M-200 524 L1400 -36" stroke="{RED}" stroke-width="2"/>
  </g>
  <!-- title -->
  <text x="60" y="190" class="brush" style="paint-order:stroke;stroke:{PAPER};stroke-width:10">新免</text>
  <text x="60" y="350" class="brush" style="paint-order:stroke;stroke:{PAPER};stroke-width:10;fill:{RED}">武蔵</text>
  <rect x="60" y="378" width="520" height="62" fill="{INK}"/>
  <text x="76" y="425" class="en" style="fill:{PAPER};font-size:46px">SHINMEN TAKEZO</text>
  <text x="62" y="478" class="tag" style="fill:{INK};animation:fade .8s .6s both">// FULL STACK · BACKEND · AI / LLM ENGINEER</text>
  <!-- seal -->
  <g transform="translate(1090 430)"><g style="animation:stamp .7s .3s cubic-bezier(.3,1.6,.5,1) both">
    <rect x="-52" y="-52" width="104" height="104" rx="10" fill="none" stroke="{RED}" stroke-width="7" filter="url(#rough)"/>
    <text x="0" y="-6" text-anchor="middle" style="font:900 40px {FONT_BRUSH};fill:{RED}">二天</text>
    <text x="0" y="36" text-anchor="middle" style="font:900 40px {FONT_BRUSH};fill:{RED}">一流</text>
  </g></g>
  <!-- SFX -->
  <text x="610" y="110" style="font:900 italic 54px Impact,sans-serif;fill:{INK};animation:jitter .15s infinite" transform="rotate(-12 610 110)">ZAN!!</text>
  <text x="1010" y="80" style="font:900 30px {FONT_BRUSH};fill:{INK}" writing-mode="tb">斬</text>
</g>
{panel_frame(W, H)}
</svg>'''
open("assets/hero.svg", "w").write(hero)

# ================= 2. CHARACTER SHEET (live stats) =================
W, H = 1200, 380
bars = ""
for i, (k, v) in enumerate(top):
    pct = v / total
    y = 120 + i * 46
    lw = 520 * pct
    lv = max(1, round(pct * 99))
    bars += f'''<g style="animation:fade .5s {0.3+i*0.2:.1f}s both">
<text x="560" y="{y}" class="lbl">{k.upper()}</text>
<text x="1140" y="{y}" class="lbl" text-anchor="end">LV.{lv:02d}</text>
<rect x="560" y="{y+10}" width="580" height="16" fill="none" stroke="{INK}" stroke-width="3"/>
<rect x="563" y="{y+13}" width="{574*pct:.0f}" height="10" fill="{RED if i==0 else INK}" style="transform-origin:563px 0;animation:grow 1.2s {0.5+i*0.2:.1f}s cubic-bezier(.2,.9,.2,1) both"/>
</g>'''
stat = lambda x, y, n, l: f'''<g transform="translate({x} {y})"><rect width="130" height="96" fill="{INK}"/>
<text x="65" y="56" text-anchor="middle" style="font:900 44px Impact,sans-serif;fill:{PAPER}">{n}</text>
<text x="65" y="82" text-anchor="middle" class="lbl" style="fill:{GOLD};font-size:13px">{l}</text></g>'''
sheet = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{HALFTONE}</defs>
<style>
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes fade{{from{{opacity:0;transform:translateX(-10px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{50%{{opacity:0}}}}
.lbl{{font:800 16px {FONT_MONO};letter-spacing:3px;fill:{INK}}}
.h{{font:900 30px Impact,sans-serif;letter-spacing:4px;fill:{INK}}}
</style>
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<rect x="6" y="6" width="500" height="{H-12}" fill="url(#ht)"/>
<text x="40" y="70" class="h">参 · CHARACTER SHEET</text>
<text x="40" y="110" class="lbl">ROLE ......... FULL STACK DEVELOPER</text>
<text x="40" y="140" class="lbl">CORE ......... BACKEND ENGINEER</text>
<text x="40" y="170" class="lbl">PATH ......... AI / LLM ENGINEER</text>
<text x="40" y="200" class="lbl">STACK ........ TS · PYTHON · GO</text>
<text x="40" y="230" class="lbl">STATUS ....... <tspan fill="{RED}">● TRAINING</tspan><tspan style="animation:blink 1s step-end infinite">_</tspan></text>
{stat(40, 260, nrepos, "REPOS")}{stat(184, 260, stars, "STARS")}{stat(328, 260, len(langs), "BLADES")}
<line x1="520" y1="20" x2="520" y2="{H-20}" stroke="{INK}" stroke-width="7"/>
<text x="560" y="70" class="h">技 · <tspan fill="{RED}">MASTERY</tspan></text>
{bars}
<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="{INK}" stroke-width="7"/>
</svg>'''
open("assets/sheet.svg", "w").write(sheet)

# ================= 3. WANTED POSTERS =================
posters = [
 ("opencode2api", "Go", "OpenCode Zen proxy", "OpenAI + Anthropic\nkey pools · WebUI", "壱"),
 ("DeepAICode2API", "Go", "DeepAI Code gateway", "dual protocol\nembedded console", "弐"),
 ("magpie-aws-quick", "JS", "AWS Quick in Magpie", "bring your own\nQuick account", "参"),
 ("workbuddy2api-hub", "Python", "WorkBuddy hub", "Codex · Claude Code\nmulti-account", "四"),
]
for name, lang, l1, l2, num in posters:
    W, H = 290, 400
    a, b = l2.split("\n")
    bounty = random.randint(120, 990) * 1000000
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{HALFTONE}</defs>
<style>
@keyframes sway{{0%,100%{{transform:rotate(-1.2deg)}}50%{{transform:rotate(1.2deg)}}}}
@keyframes stamp{{0%,40%{{opacity:0;transform:scale(2.5) rotate(-30deg)}}55%{{opacity:1;transform:scale(.9) rotate(-14deg)}}65%,100%{{opacity:1;transform:scale(1) rotate(-14deg)}}}}
.w{{font:900 56px Impact,'Bebas Neue',sans-serif;letter-spacing:6px;fill:{INK}}}
.m{{font:700 13px {FONT_MONO};fill:{INK};letter-spacing:1px}}
</style>
<g style="transform-origin:145px 0;animation:sway 6s ease-in-out infinite">
<rect x="10" y="10" width="270" height="380" fill="#e8d9b5" stroke="{INK}" stroke-width="4"/>
<rect x="10" y="10" width="270" height="380" fill="url(#ht)" opacity=".6"/>
<text x="145" y="72" text-anchor="middle" class="w">WANTED</text>
<rect x="34" y="88" width="222" height="150" fill="{INK}"/>
<text x="145" y="195" text-anchor="middle" style="font:900 110px {FONT_BRUSH};fill:{RED}">{num}</text>
<text x="145" y="230" text-anchor="middle" class="m" style="fill:{PAPER}">[{lang}]</text>
<text x="145" y="268" text-anchor="middle" style="font:900 19px Impact,sans-serif;fill:{INK};letter-spacing:1px">{name.upper()}</text>
<text x="145" y="292" text-anchor="middle" class="m">{l1}</text>
<text x="145" y="312" text-anchor="middle" class="m" style="opacity:.7">{a}</text>
<text x="145" y="330" text-anchor="middle" class="m" style="opacity:.7">{b}</text>
<line x1="34" y1="344" x2="256" y2="344" stroke="{INK}" stroke-width="2"/>
<text x="145" y="372" text-anchor="middle" style="font:900 22px Impact,sans-serif;fill:{INK}">฿ {bounty:,}</text>
<g transform="translate(225 250)"><g style="animation:stamp 4s infinite">
<rect x="-34" y="-20" width="68" height="40" fill="none" stroke="{RED}" stroke-width="4"/>
<text x="0" y="8" text-anchor="middle" style="font:900 22px Impact,sans-serif;fill:{RED}">LIVE</text></g></g>
</g></svg>'''
    open(f"assets/{name}.svg", "w").write(svg)

# ================= 4. HANKO SEAL TECH STACK =================
stack = [("GO", "囲"), ("PY", "蛇"), ("TS", "型"), ("JS", "脚"), ("RS", "錆"), ("DK", "鯨"), ("LX", "企"), ("AI", "智")]
W, H = 1200, 200
seals = ""
for i, (en, jp) in enumerate(stack):
    x = 85 + i * 147
    rot = random.choice([-8, -4, 3, 6, 9])
    seals += f'''<g transform="translate({x} 100)"><g style="animation:stamp .5s {0.15*i:.2f}s cubic-bezier(.3,1.7,.5,1) both;--r:{rot}deg">
<circle r="52" fill="none" stroke="{RED}" stroke-width="6" filter="url(#rough)"/>
<text y="10" text-anchor="middle" style="font:900 46px {FONT_BRUSH};fill:{RED}">{jp}</text>
<text y="40" text-anchor="middle" style="font:800 13px {FONT_MONO};fill:{RED};letter-spacing:2px">{en}</text>
</g></g>'''
hanko = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{HALFTONE}</defs>
<style>@keyframes stamp{{0%{{opacity:0;transform:scale(2.4) rotate(-40deg)}}100%{{opacity:1;transform:scale(1) rotate(var(--r))}}}}</style>
<rect width="{W}" height="{H}" fill="{PAPER}"/>
{seals}
<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="{INK}" stroke-width="7"/>
</svg>'''
open("assets/hanko.svg", "w").write(hanko)

# ================= section headers =================
for fn, jp, en in [("h1", "壱", "THE BOUNTY BOARD"), ("h2", "弐", "WEAPONS OF CHOICE")]:
    open(f"assets/{fn}.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="90" viewBox="0 0 1200 90">
<style>@keyframes ink{{from{{stroke-dashoffset:1200}}to{{stroke-dashoffset:0}}}}</style>
<rect width="1200" height="90" fill="{INK}"/>
<text x="40" y="66" style="font:900 56px {FONT_BRUSH};fill:{RED}">{jp}</text>
<text x="120" y="60" style="font:900 38px Impact,sans-serif;letter-spacing:8px;fill:{PAPER}">{en}</text>
<path d="M700 45 H1160" stroke="{PAPER}" stroke-width="3" stroke-dasharray="1200" style="animation:ink 2s ease-out both"/>
<circle cx="1160" cy="45" r="7" fill="{RED}"/></svg>''')

# ================= footer =================
open("assets/footer.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="160" viewBox="0 0 1200 160">
<defs>{HALFTONE}</defs>
<style>@keyframes t{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}</style>
<rect width="1200" height="160" fill="{INK}"/>
<rect width="1200" height="160" fill="url(#ht)" opacity=".5"/>
<text x="600" y="72" text-anchor="middle" style="font:900 40px {FONT_BRUSH};fill:{PAPER};letter-spacing:12px">千日の稽古を鍛とし</text>
<text x="600" y="110" text-anchor="middle" style="font:700 15px {FONT_MONO};fill:{GOLD};letter-spacing:5px">"A THOUSAND DAYS OF PRACTICE TO FORGE — TEN THOUSAND TO POLISH."</text>
<text x="600" y="140" text-anchor="middle" style="font:700 12px {FONT_MONO};fill:{RED};letter-spacing:4px;animation:t 2.5s infinite">— TO BE CONTINUED —</text>
</svg>''')
print("langs:", top, "repos:", nrepos, "stars:", stars)

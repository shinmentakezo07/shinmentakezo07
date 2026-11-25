import json, subprocess, os, glob
U = "shinmentakezo07"
INK, PAPER, RED, GOLD = "#0b0b0d", "#f1e9d6", "#e63946", "#d4a017"
BR = "'Yuji Syuku','Shippori Mincho','Noto Serif JP',serif"
MO = "'JetBrains Mono','Fira Code',Consolas,monospace"
IM = "Impact,'Bebas Neue','Arial Black',sans-serif"
HT = f'<pattern id="ht" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="4" cy="4" r="1.6" fill="{INK}" opacity=".18"/></pattern>'

def sh(*a): return subprocess.check_output(a, text=True)

# ---- data ----
q = '{user(login:"%s"){createdAt followers{totalCount} contributionsCollection{totalCommitContributions restrictedContributionsCount totalPullRequestContributions totalIssueContributions totalRepositoriesWithContributedCommits contributionCalendar{totalContributions weeks{contributionDays{contributionCount date weekday}}}}}}' % U
u = json.loads(sh("gh", "api", "graphql", "-f", "query=" + q))["data"]["user"]
cc = u["contributionsCollection"]; cal = cc["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]
# streaks
cur = best = run = 0
for d in days:
    run = run + 1 if d["contributionCount"] > 0 else 0
    best = max(best, run)
for d in reversed(days):
    if d["contributionCount"] > 0: cur += 1
    elif d is days[-1]: continue
    else: break
active = sum(1 for d in days if d["contributionCount"] > 0)
peak = max(days, key=lambda d: d["contributionCount"])
wd = [0]*7
for d in days: wd[d["weekday"]] += d["contributionCount"]
bestday = ["SUN","MON","TUE","WED","THU","FRI","SAT"][wd.index(max(wd))]

w = json.loads(sh("gh", "repo", "view", f"{U}/wiwia", "--json", "stargazerCount,forkCount,createdAt,pushedAt,languages"))
link = sh("gh", "api", "-i", f"repos/{U}/wiwia/commits?per_page=1")
wcommits = int(link.split('page=')[-1].split('>')[0]) if 'rel="last"' in link else 1
wl = sorted(((l["node"]["name"], l["size"]) for l in w["languages"]), key=lambda x: -x[1])
wt = sum(s for _, s in wl)

# ================= WIWIA SHOWCASE =================
W, H = 1200, 560
pal = {"Python": "#3776AB", "TypeScript": "#3178C6", "Go": "#00ADD8", "CSS": "#c1121f", "Shell": "#4EAA25"}
x = 640; seg = ""; leg = ""
for i, (n, s) in enumerate(wl[:5]):
    ww = 500 * s / wt
    seg += f'<rect x="{x:.1f}" y="420" width="{ww:.1f}" height="22" fill="{pal.get(n, INK)}" style="transform-origin:640px 0;animation:grow 1.4s .4s cubic-bezier(.2,.9,.2,1) both"/>'
    x += ww
    leg += f'<g transform="translate({640 + (i % 3) * 170} {470 + (i // 3) * 26})"><rect width="12" height="12" fill="{pal.get(n, INK)}"/><text x="20" y="11" class="m">{n} {100*s/wt:.1f}%</text></g>'
flow_in = ["OpenAI Chat", "OpenAI Responses", "Anthropic Messages"]
flow_out = ["OpenAI", "Anthropic", "Gemini", "OpenRouter", "NVIDIA NIM", "+8 more"]
fin = "".join(f'<g style="animation:fade .5s {0.2+i*.15:.2f}s both"><rect x="640" y="{120+i*44}" width="170" height="32" fill="{INK}"/><text x="725" y="{141+i*44}" text-anchor="middle" class="m" style="fill:{PAPER}">{t}</text><path d="M810 {136+i*44} L900 {196}" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5" style="animation:flow 1s linear infinite"/></g>' for i, t in enumerate(flow_in))
fout = "".join(f'<g style="animation:fade .5s {0.8+i*.12:.2f}s both"><path d="M980 196 L1030 {110+i*34}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5" style="animation:flow 1s linear infinite"/><rect x="1030" y="{96+i*34}" width="130" height="26" fill="none" stroke="{INK}" stroke-width="3"/><text x="1095" y="{114+i*34}" text-anchor="middle" class="m">{t}</text></g>' for i, t in enumerate(flow_out))
box = lambda x, y, n, l: f'<g transform="translate({x} {y})"><rect width="128" height="84" fill="{INK}"/><text x="64" y="50" text-anchor="middle" style="font:900 40px {IM};fill:{PAPER}">{n}</text><text x="64" y="72" text-anchor="middle" class="m" style="fill:{GOLD};font-size:11px">{l}</text></g>'
wiwia = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{HT}</defs>
<style>
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes flow{{to{{stroke-dashoffset:-22}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes pulse{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
.m{{font:700 13px {MO};fill:{INK};letter-spacing:1px}}
.h{{font:900 30px {IM};letter-spacing:4px;fill:{INK}}}
</style>
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<rect x="6" y="6" width="590" height="{H-12}" fill="url(#ht)"/>
<text x="40" y="150" style="font:900 140px {BR};fill:{RED}">渦</text>
<text x="200" y="110" style="font:900 72px {IM};letter-spacing:8px;fill:{INK}">WIWIA</text>
<text x="200" y="146" class="m" style="font-size:15px">ONE GATEWAY · EVERY DIALECT</text>
<text x="200" y="168" class="m" style="font-size:15px">ANY PROVIDER</text>
<text x="40" y="215" class="m">› No pairwise converters — one canonical IR</text>
<text x="40" y="240" class="m">› Two backends, one contract: Python/FastAPI + Go/Gin</text>
<text x="40" y="265" class="m">› React 19 console · SQLite / Postgres state</text>
<text x="40" y="290" class="m">› Point Claude Code or Codex CLI at any model</text>
{box(40, 320, 3, "DIALECTS IN")}{box(178, 320, 13, "PROVIDERS")}{box(316, 320, 39, "PAIRINGS")}{box(454, 320, 2, "BACKENDS")}
{box(40, 420, wcommits, "COMMITS")}{box(178, 420, w["stargazerCount"], "STARS")}{box(316, 420, w["forkCount"], "FORKS")}{box(454, 420, len(wl), "LANGUAGES")}
<line x1="610" y1="20" x2="610" y2="{H-20}" stroke="{INK}" stroke-width="7"/>
<text x="640" y="70" class="h">流 · <tspan fill="{RED}">REQUEST FLOW</tspan></text>
{fin}
<g transform="translate(940 196)"><circle r="44" fill="{RED}"/><g style="animation:spin 6s linear infinite"><circle r="54" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8"/></g><text y="6" text-anchor="middle" style="font:900 18px {IM};fill:{PAPER};letter-spacing:2px">IR</text></g>
{fout}
<text x="640" y="400" class="h" style="font-size:22px">技 · CODEBASE</text>
<rect x="640" y="420" width="500" height="22" fill="none" stroke="{INK}" stroke-width="3"/>
{seg}{leg}
<a href="https://github.com/{U}/wiwia"><rect x="960" y="510" width="180" height="34" fill="{RED}" style="animation:pulse 2s infinite"/><text x="1050" y="533" text-anchor="middle" style="font:900 17px {IM};fill:{PAPER};letter-spacing:3px">VIEW REPO →</text></a>
<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="{INK}" stroke-width="7"/>
</svg>'''
open("assets/wiwia.svg", "w").write(wiwia)

# ================= BATTLE LOG (contribution stats + heatmap) =================
W, H = 1200, 400
weeks = cal["weeks"][-52:]
mx = max(d["contributionCount"] for d in days) or 1
cells = ""
for i, wk in enumerate(weeks):
    for d in wk["contributionDays"]:
        c = d["contributionCount"]
        if c == 0: fill, op = INK, ".08"
        else:
            r = c / mx; fill = RED if r > .5 else INK; op = f"{.35 + .65 * min(1, r * 2):.2f}"
        cells += f'<rect x="{40 + i*21.5:.1f}" y="{210 + d["weekday"]*22}" width="18" height="18" fill="{fill}" opacity="{op}" style="animation:pop .3s {i*0.025:.2f}s both"/>'
stat = lambda x, n, l: f'<g transform="translate({x} 60)" style="animation:fade .5s both"><text style="font:900 54px {IM};fill:{INK}">{n}</text><text y="26" class="m" style="fill:{RED}">{l}</text></g>'
yrs = 2026 - int(u["createdAt"][:4])
log = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
@keyframes pop{{from{{opacity:0;transform:scale(0)}}}}
@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}}}
.m{{font:700 12px {MO};fill:{INK};letter-spacing:2px}}
</style>
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<rect width="{W}" height="40" fill="{INK}"/>
<text x="40" y="28" style="font:900 22px {IM};letter-spacing:6px;fill:{PAPER}">戦 · BATTLE LOG — LAST 365 DAYS</text>
{stat(40, cal["totalContributions"], "CONTRIBUTIONS")}{stat(230, cc["totalCommitContributions"] + cc["restrictedContributionsCount"], "COMMITS")}{stat(400, cur, "DAY STREAK")}{stat(560, best, "BEST STREAK")}{stat(730, active, "ACTIVE DAYS")}{stat(900, peak["contributionCount"], "PEAK " + peak["date"][5:])}{stat(1080, cc["totalPullRequestContributions"], "PRS")}
<text x="40" y="160" class="m">STRONGEST DAY: <tspan fill="{RED}">{bestday}</tspan>   ·   ON THE ROAD SINCE {u["createdAt"][:7]}   ·   REPOS TOUCHED: {cc["totalRepositoriesWithContributedCommits"]}</text>
<line x1="40" y1="180" x2="1160" y2="180" stroke="{INK}" stroke-width="3"/>
{cells}
<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="{INK}" stroke-width="7"/>
</svg>'''
open("assets/battlelog.svg", "w").write(log)

# headers
for fn, jp, en in [("h1", "壱", "THE MAIN QUEST"), ("h2", "弐", "WEAPONS OF CHOICE"), ("h3", "参", "TRAINING RECORD")]:
    open(f"assets/{fn}.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="90" viewBox="0 0 1200 90">
<style>@keyframes ink{{from{{stroke-dashoffset:1200}}to{{stroke-dashoffset:0}}}}</style>
<rect width="1200" height="90" fill="{INK}"/><text x="40" y="66" style="font:900 56px {BR};fill:{RED}">{jp}</text>
<text x="120" y="60" style="font:900 38px {IM};letter-spacing:8px;fill:{PAPER}">{en}</text>
<path d="M720 45 H1160" stroke="{PAPER}" stroke-width="3" stroke-dasharray="1200" style="animation:ink 2s ease-out both"/><circle cx="1160" cy="45" r="7" fill="{RED}"/></svg>''')
print("ok", cal["totalContributions"], cur, best, wcommits)

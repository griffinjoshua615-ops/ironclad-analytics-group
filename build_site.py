"""Generate the static Dokimos site (Tailwind CDN + Google Fonts). Run: python3 build_site.py"""
import os, html, json

OUT = os.path.dirname(os.path.abspath(__file__))
EMAIL = "griffinjoshua615@gmail.com"
FORM = f"https://formsubmit.co/{EMAIL}"
SITE = "https://dokimos.co"   # placeholder canonical; swap when the domain is bought

MARK = '''<svg aria-hidden="true" viewBox="0 0 40 40" class="h-9 w-9"><rect x="2" y="2" width="36" height="36" rx="7" fill="#121212"/><path d="M11 29 L29 11" stroke="#D4A017" stroke-width="5" stroke-linecap="round"/></svg>'''

TAILWIND = '''<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{ink:'#121212',paper:'#F6F3EC',gold:'#D4A017',goldDeep:'#A67C0F',stone:'#2A2A2A',slate2:'#5B5B5B',line:'#E4DED2'},fontFamily:{display:['Fraunces','Georgia','serif'],body:['Inter','system-ui','sans-serif']}}}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  html{scroll-behavior:smooth}
  .streak{position:relative;overflow:hidden}
  .streak:before{content:"";position:absolute;left:-10%;top:55%;width:120%;height:14px;background:linear-gradient(90deg,rgba(212,160,23,0) 0%,rgba(212,160,23,.9) 35%,rgba(212,160,23,.9) 65%,rgba(212,160,23,0) 100%);transform:rotate(-14deg);opacity:.35;pointer-events:none}
  .num{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 144}
  .rule{height:4px;width:56px;background:#D4A017;border-radius:2px}
  a.navlink{position:relative}
  a.navlink.active:after{content:"";position:absolute;left:0;right:0;bottom:-6px;height:2px;background:#D4A017}
  details summary{cursor:pointer;list-style:none}
  details summary::-webkit-details-marker{display:none}
</style>'''

NAV = [("index.html", "Home"), ("environments.html", "Environments"), ("engine.html", "Engine"),
       ("course.html", "Course"), ("index.html#founder", "Founder"), ("contact.html", "Contact")]

def head(title, desc, path):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#121212">
<link rel="canonical" href="{SITE}/{path}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:image" content="{SITE}/og-image.png"><meta property="og:url" content="{SITE}/{path}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"Organization","@id":"{SITE}/#org","name":"Dokimos","alternateName":"Dokimos LLC","url":"{SITE}/","logo":"{SITE}/og-image.png","slogan":"Judgment, proven.","description":"Dokimos writes down the judgment that is not in the manual, as tests with exact answers, and proves it. Verified expert judgment for AI labs, Army units and fleets.","email":"{EMAIL}","address":{{"@type":"PostalAddress","addressLocality":"Port Wentworth","addressRegion":"GA","addressCountry":"US"}},"founder":{{"@type":"Person","name":"Joshua Griffin"}},"knowsAbout":["expert-authored AI evaluation tasks","reinforcement learning environments","Class IX parts management","Army sustainment","PLL and shop stock judgment","deadline and NMC recovery"]}},{{"@type":"Service","name":"Dokimos Environments","provider":{{"@id":"{SITE}/#org"}},"serviceType":"Expert-authored tasks and environments for AI labs in tacit sustainment domains","url":"{SITE}/environments.html","areaServed":"US"}},{{"@type":"Service","name":"Dokimos Engine","provider":{{"@id":"{SITE}/#org"}},"serviceType":"Unit-level Class IX decision support gated by expert-authored tests","url":"{SITE}/engine.html","areaServed":"US"}},{{"@type":"Course","name":"Dokimos Course: PLL and Class IX readiness judgment","provider":{{"@id":"{SITE}/#org"}},"description":"A public, scheduled two-day class on PLL and Class IX readiness judgment for clerks, maintenance sergeants and leaders.","url":"{SITE}/course.html","offers":{{"@type":"Offer","price":"1250","priceCurrency":"USD","description":"per seat, eight seats per class"}}}}]}}</script>
{TAILWIND}
</head>
<body class="bg-paper font-body text-stone antialiased">'''

def header(active):
    links = "".join(
        f'<a class="navlink {"active text-ink" if href == active else "text-slate2 hover:text-ink"}" href="{href}">{label}</a>'
        for href, label in NAV)
    return f'''<header class="sticky top-0 z-50 border-b border-line bg-paper/95 backdrop-blur">
  <nav class="mx-auto flex max-w-6xl items-center justify-between px-5 py-4" aria-label="Main">
    <a href="index.html" class="flex items-center gap-3">{MARK}<span class="font-display text-2xl font-semibold tracking-tight text-ink">Dokimos</span></a>
    <div class="hidden items-center gap-7 text-sm font-medium md:flex">{links}</div>
    <a href="contact.html" class="hidden rounded-md bg-ink px-4 py-2 text-sm font-semibold text-paper hover:bg-stone md:inline-flex">Talk to Dokimos</a>
    <details class="md:hidden"><summary class="rounded-md border border-line px-3 py-2 text-sm">Menu</summary>
      <div class="absolute left-0 right-0 top-full flex flex-col gap-4 border-b border-line bg-paper px-5 py-5 text-base">{links}<a href="contact.html" class="font-semibold text-ink">Talk to Dokimos</a></div></details>
  </nav>
</header>'''

FOOTER = f'''<footer class="border-t border-line bg-ink text-paper">
  <div class="mx-auto grid max-w-6xl gap-10 px-5 py-14 md:grid-cols-3">
    <div><div class="flex items-center gap-3">{MARK}<span class="font-display text-2xl font-semibold">Dokimos</span></div>
      <p class="mt-4 text-sm leading-6 text-paper/70">Judgment, proven. Verified expert judgment from the people who lived the job.</p>
      <p class="mt-4 text-xs text-paper/50">Say it DOCK-ee-moss. Ancient Greek for a coin that passed the test on the touchstone. Spell it with a K.</p></div>
    <div class="text-sm"><p class="font-semibold text-gold">Lines</p>
      <ul class="mt-3 space-y-2 text-paper/80"><li><a class="hover:text-paper" href="environments.html">Dokimos Environments</a></li><li><a class="hover:text-paper" href="engine.html">Dokimos Engine</a></li><li><a class="hover:text-paper" href="course.html">Dokimos Course</a></li><li><a class="hover:text-paper" href="assets/Dokimos_Capability_Sheet_2026-10.pdf">Capability sheet (PDF)</a></li></ul></div>
    <div class="text-sm"><p class="font-semibold text-gold">Contact</p>
      <ul class="mt-3 space-y-2 text-paper/80"><li>Port Wentworth, Georgia</li><li><a class="hover:text-paper" href="mailto:{EMAIL}">{EMAIL}</a></li><li><a class="hover:text-paper" href="contact.html">Contact form</a></li><li><a class="hover:text-paper" href="faq.html">FAQ</a></li><li><a class="hover:text-paper" href="privacy.html">Privacy</a></li></ul>
      <p class="mt-6 text-xs text-paper/50">A service-disabled veteran-owned business. SBA VetCert in progress. Not affiliated with the U.S. Army.</p></div>
  </div>
  <div class="border-t border-paper/10"><div class="mx-auto max-w-6xl px-5 py-5 text-xs text-paper/50">&copy; 2026 Dokimos. All rights reserved.</div></div>
</footer>
</body></html>'''

def page(fname, title, desc, body, active):
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(head(title, desc, fname) + header(active) + body + FOOTER)

def cta(text, href, dark=False):
    cls = "bg-gold text-ink hover:bg-goldDeep hover:text-paper" if dark else "bg-ink text-paper hover:bg-stone"
    return f'<a href="{href}" class="inline-flex items-center justify-center rounded-md px-6 py-3 text-sm font-semibold {cls}">{text}</a>'

# --------------------------------------------------------------------- index
index_body = f'''
<main>
<section class="streak bg-ink text-paper">
  <div class="mx-auto max-w-6xl px-5 py-24 md:py-32">
    <p class="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Verified expert judgment</p>
    <h1 class="mt-6 font-display text-6xl font-semibold leading-[0.95] tracking-tight md:text-8xl">Judgment,<br>proven.</h1>
    <p class="mt-8 max-w-2xl text-lg leading-8 text-paper/80">Dokimos writes down the judgment that is not in the manual, as tests with exact answers, and proves it. For AI labs that need ground truth in the domains their models fail. For units and fleets that lose their best people's judgment every time someone rotates out.</p>
    <div class="mt-10 flex flex-col gap-4 sm:flex-row">{cta("Talk to Dokimos", "contact.html", dark=True)}<a href="#proof" class="inline-flex items-center justify-center rounded-md border border-paper/30 px-6 py-3 text-sm font-semibold text-paper hover:bg-paper/10">See the proof</a></div>
  </div>
</section>

<section class="mx-auto max-w-6xl px-5 py-20">
  <div class="rule"></div>
  <h2 class="mt-6 font-display text-4xl font-semibold text-ink md:text-5xl">Three lines. One library.</h2>
  <p class="mt-4 max-w-2xl text-lg leading-8 text-slate2">Every test Dokimos writes earns three times: as ground truth for a model, as a release gate for a decision tool, and as a case in a classroom. The library compounds; nothing is written once.</p>
  <div class="mt-12 grid gap-10 md:grid-cols-3">
    <a href="environments.html" class="group border-t-2 border-ink pt-6"><p class="num text-5xl text-gold">01</p><h3 class="mt-3 font-display text-2xl font-semibold text-ink group-hover:underline">Dokimos Environments</h3><p class="mt-3 text-sm leading-7 text-slate2">Expert-authored tasks and full environments in tacit sustainment domains: Class IX parts judgment, dispatch and 5988-E fault flow, deadline recovery, warehouse operations. Shared or exclusive. Every item ships with one exact answer and a blind-solver record.</p><p class="mt-4 text-sm font-semibold text-ink">For AI labs and expert-data vendors &rarr;</p></a>
    <a href="engine.html" class="group border-t-2 border-ink pt-6"><p class="num text-5xl text-gold">02</p><h3 class="mt-3 font-display text-2xl font-semibold text-ink group-hover:underline">Dokimos Engine</h3><p class="mt-3 text-sm leading-7 text-slate2">Decision support for the motor pool. A laptop-level tool that turns GCSS-Army exports into a verified action list before the Monday maintenance meeting, gated by tests the clerks and maintenance sergeants wrote.</p><p class="mt-4 text-sm font-semibold text-ink">For Army units, then fleets and depots &rarr;</p></a>
    <a href="course.html" class="group border-t-2 border-ink pt-6"><p class="num text-5xl text-gold">03</p><h3 class="mt-3 font-display text-2xl font-semibold text-ink group-hover:underline">Dokimos Course</h3><p class="mt-3 text-sm leading-7 text-slate2">A public, scheduled class on PLL and Class IX readiness judgment, taught by people who ran the shop. Priced per seat, so a unit can buy it on a purchase card without a solicitation.</p><p class="mt-4 text-sm font-semibold text-ink">For leaders with a training budget &rarr;</p></a>
  </div>
</section>

<section id="proof" class="border-y border-line bg-white">
  <div class="mx-auto grid max-w-6xl gap-12 px-5 py-20 md:grid-cols-[0.9fr_1.1fr] md:items-center">
    <div><p class="num text-[9rem] leading-none text-ink md:text-[12rem]">0<span class="text-gold">/</span>5</p><p class="mt-2 text-sm font-semibold uppercase tracking-[0.2em] text-slate2">trials solved by frontier models</p></div>
    <div><div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink md:text-4xl">Models solve written rules. They fail unwritten judgment.</h2>
      <p class="mt-5 text-base leading-8 text-slate2">On an independent benchmark program (September 24 to October 3, 2026), frontier AI models solved a written-rule accrual task in every automated trial and failed the founder's Class IX stockage judgment task in zero of five. Same author, same grader, same format. The difference was whether the answer lived in a policy or in a clerk's head.</p>
      <p class="mt-4 text-base leading-8 text-slate2">That gap is what Dokimos sells: the judgment that is not written down anywhere a model can read, written down and proven.</p></div>
  </div>
</section>

<section class="mx-auto max-w-6xl px-5 py-20">
  <div class="rule"></div>
  <h2 class="mt-6 font-display text-4xl font-semibold text-ink">How a test earns the streak</h2>
  <p class="mt-4 max-w-2xl text-lg leading-8 text-slate2">The gold streak on a touchstone is the mark that the metal was tested. Every Dokimos deliverable carries it, and it means the same four things happened.</p>
  <ol class="mt-12 grid gap-8 md:grid-cols-4">
    <li class="border-l-2 border-gold pl-5"><p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate2">Step 1</p><h3 class="mt-2 font-display text-2xl font-semibold text-ink">Elicit</h3><p class="mt-2 text-sm leading-7 text-slate2">Sit with the people who carry the judgment and pull the cases out of their heads, one decision at a time.</p></li>
    <li class="border-l-2 border-gold pl-5"><p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate2">Step 2</p><h3 class="mt-2 font-display text-2xl font-semibold text-ink">Author</h3><p class="mt-2 text-sm leading-7 text-slate2">Write each case as a task with one exact answer and a verifier that checks it without a human in the loop.</p></li>
    <li class="border-l-2 border-gold pl-5"><p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate2">Step 3</p><h3 class="mt-2 font-display text-2xl font-semibold text-ink">Probe</h3><p class="mt-2 text-sm leading-7 text-slate2">Run blind solvers against it. Anything a model clears on rules alone goes back to the bench; that is a rule, not judgment.</p></li>
    <li class="border-l-2 border-gold pl-5"><p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate2">Step 4</p><h3 class="mt-2 font-display text-2xl font-semibold text-ink">Prove</h3><p class="mt-2 text-sm leading-7 text-slate2">Grade exactly, record the pass rate and the probe log, and deliver with the streak. Field outcomes become the next tests.</p></li>
  </ol>
</section>

<section class="bg-ink text-paper">
  <div class="mx-auto max-w-6xl px-5 py-20">
    <div class="rule"></div>
    <h2 class="mt-6 font-display text-4xl font-semibold">Who it is for</h2>
    <div class="mt-10 grid gap-8 md:grid-cols-4 text-sm leading-7 text-paper/80">
      <div><p class="font-semibold text-gold">AI labs and expert-data vendors</p><p class="mt-2">You need ground truth in domains your models fail, from authors whose tasks survive a strict grader.</p></div>
      <div><p class="font-semibold text-gold">Army sustainment units</p><p class="mt-2">Your parts judgment leaves with every PCS. You want it captured, tested, and on a laptop at the company level.</p></div>
      <div><p class="font-semibold text-gold">Fleets, depots and ports</p><p class="mt-2">Same problem, different uniform: the senior planner retires and the rules of thumb retire with them.</p></div>
      <div><p class="font-semibold text-gold">Leaders with a training budget</p><p class="mt-2">You want your clerks taught by people who made the mistakes already, at a public price you can put on a card.</p></div>
    </div>
  </div>
</section>

<section id="founder" class="mx-auto max-w-6xl px-5 py-20">
  <div class="grid gap-10 md:grid-cols-[1fr_1.4fr] md:items-start">
    <div><div class="rule"></div><h2 class="mt-6 font-display text-4xl font-semibold text-ink">Founder</h2><p class="mt-3 font-display text-2xl text-ink">Joshua Griffin</p><p class="mt-1 text-sm text-slate2">Port Wentworth, Georgia</p></div>
    <div class="space-y-5 text-base leading-8 text-slate2">
      <p>Six years in the U.S. Army as a motor transport sergeant, with the duties that never show up in a job title: PLL clerk ordering Class IX and managing shop stock, dispatch and the 5988-E fault flow, tracking deadlines and NMC status for a maintenance leader, and a parts surge during a major training rotation.</p>
      <p>Then area manager at an Amazon sort and delivery center, running a day shift of about 160 associates on live metrics. B.S. in Business Analytics with an accounting minor. MBA, University of Florida, December 2026.</p>
      <p>He authored the Class IX benchmark task that frontier models failed in every trial, and he built the pass protocol that keeps Dokimos tasks honest. Dokimos is a service-disabled veteran-owned business.</p>
    </div>
  </div>
</section>

<section class="border-t border-line bg-white">
  <div class="mx-auto max-w-6xl px-5 py-20 text-center">
    <h2 class="font-display text-4xl font-semibold text-ink md:text-5xl">Tell us the judgment you are losing.</h2>
    <p class="mx-auto mt-4 max-w-xl text-lg leading-8 text-slate2">Or the domain you need ground truth in. One message, a plain answer within two business days.</p>
    <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">{cta("Talk to Dokimos", "contact.html")}<a href="assets/Dokimos_Capability_Sheet_2026-10.pdf" class="inline-flex items-center justify-center rounded-md border border-ink px-6 py-3 text-sm font-semibold text-ink hover:bg-paper">Capability sheet (PDF)</a></div>
  </div>
</section>
</main>'''
page("index.html", "Dokimos | Judgment, proven.", "Dokimos writes down the judgment that is not in the manual, as tests with exact answers, and proves it. Verified expert judgment for AI labs, Army units and fleets.", index_body, "index.html")

# --------------------------------------------------------------------- environments
env_body = f'''
<main>
<section class="streak bg-ink text-paper"><div class="mx-auto max-w-6xl px-5 py-20 md:py-24">
  <p class="text-xs font-semibold uppercase tracking-[0.28em] text-gold">01 &middot; Dokimos Environments</p>
  <h1 class="mt-5 font-display text-5xl font-semibold leading-tight md:text-7xl">Ground truth from people who lived the job.</h1>
  <p class="mt-6 max-w-2xl text-lg leading-8 text-paper/80">Expert-authored tasks and full environments in tacit sustainment domains, built under a protocol that frontier models have already failed. Shared or exclusive. Delivered with the probe log.</p>
  <div class="mt-8 flex flex-col gap-4 sm:flex-row">{cta("Request a sample task", "contact.html", dark=True)}<a href="assets/Dokimos_Capability_Sheet_2026-10.pdf" class="inline-flex items-center justify-center rounded-md border border-paper/30 px-6 py-3 text-sm font-semibold text-paper hover:bg-paper/10">Capability sheet (PDF)</a></div>
</div></section>

<section class="mx-auto max-w-6xl px-5 py-20">
  <div class="grid gap-12 md:grid-cols-2">
    <div><div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">What you get</h2>
      <ul class="mt-6 space-y-4 text-base leading-7 text-slate2">
        <li><span class="font-semibold text-ink">Tasks.</span> Single-crux problems with one exact answer, a verifier, and a written reason the crux is judgment rather than a rule. Priced per task.</li>
        <li><span class="font-semibold text-ink">Environments.</span> A working setting (files, exports, records, tools) plus a suite of tasks and verifiers, so an agent can be trained and scored end to end. Priced per environment.</li>
        <li><span class="font-semibold text-ink">Exclusivity.</span> Shared items are sold to more than one buyer. Exclusive items are yours alone, at a multiple of the shared rate.</li>
        <li><span class="font-semibold text-ink">The probe log.</span> Every item ships with the record of which blind solvers were run and what they returned. You see the gap before you pay for it.</li>
      </ul></div>
    <div><div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">Domains</h2>
      <ul class="mt-6 grid gap-3 text-base leading-7 text-slate2 sm:grid-cols-2">
        <li class="border border-line bg-white p-4">Class IX parts judgment: dead, duplicate and superseded requisitions; shop stock; turn-ins</li>
        <li class="border border-line bg-white p-4">Dispatch and 5988-E fault flow</li>
        <li class="border border-line bg-white p-4">Deadline and NMC recovery under parts and funds constraints</li>
        <li class="border border-line bg-white p-4">Forward maintenance and expeditionary supply</li>
        <li class="border border-line bg-white p-4">Warehouse and sort operations: staffing, flow, bottlenecks</li>
        <li class="border border-line bg-white p-4">Month-end accrual and reconciliation with written policy (the control case)</li>
      </ul>
      <p class="mt-5 text-sm leading-7 text-slate2">New domains are added through a bench of veteran and industrial co-authors who work under the same protocol. Ask about a domain that is not listed.</p></div>
  </div>
</section>

<section class="border-y border-line bg-white"><div class="mx-auto max-w-6xl px-5 py-20">
  <div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">Why the protocol matters to your rejection rate</h2>
  <div class="mt-8 grid gap-8 md:grid-cols-3 text-base leading-7 text-slate2">
    <div><p class="num text-4xl text-gold">1</p><p class="mt-2"><span class="font-semibold text-ink">Ambiguity is not difficulty.</span> A task fails if two experts could reasonably give different answers. Each Dokimos task has one.</p></div>
    <div><p class="num text-4xl text-gold">2</p><p class="mt-2"><span class="font-semibold text-ink">Rules are not judgment.</span> If a blind solver clears the task on written policy alone, it is sent back. The library holds only what the models could not do.</p></div>
    <div><p class="num text-4xl text-gold">3</p><p class="mt-2"><span class="font-semibold text-ink">Exact grading or nothing.</span> Verifiers are deterministic. No rubric drift, no grader opinion, no argument after delivery.</p></div>
  </div>
  <p class="mt-10 text-base leading-8 text-slate2">Proof point: on an independent benchmark program in late 2026, the founder's Class IX judgment task went zero for five against frontier models while his written-rule accrual task was solved in every trial. Same author, same protocol. The protocol is what separates the two.</p>
</div></section>

<section class="mx-auto max-w-6xl px-5 py-20 text-center">
  <h2 class="font-display text-4xl font-semibold text-ink">Start with one task.</h2>
  <p class="mx-auto mt-4 max-w-xl text-lg leading-8 text-slate2">Name the domain and the behavior you want tested. We send a sample task with its probe log, and a quote for a shared or exclusive set.</p>
  <div class="mt-8">{cta("Request a sample task", "contact.html")}</div>
</section>
</main>'''
page("environments.html", "Dokimos Environments | Expert tasks and environments in tacit domains", "Expert-authored tasks and environments in tacit sustainment domains for AI labs and data vendors, built under a protocol frontier models have failed. Shared or exclusive.", env_body, "environments.html")

# --------------------------------------------------------------------- engine
eng_body = f'''
<main>
<section class="streak bg-ink text-paper"><div class="mx-auto max-w-6xl px-5 py-20 md:py-24">
  <p class="text-xs font-semibold uppercase tracking-[0.28em] text-gold">02 &middot; Dokimos Engine</p>
  <h1 class="mt-5 font-display text-5xl font-semibold leading-tight md:text-7xl">The motor pool's judgment, on a laptop, before Monday.</h1>
  <p class="mt-6 max-w-2xl text-lg leading-8 text-paper/80">The Motor Pool Judgment Engine turns a unit's GCSS-Army exports into a verified action list: which requisitions are dead, duplicated or already filled under a superseding part number; which vehicles are truly supply-down; which parts to expedite or cross-level to get the most mission-essential trucks back. Every rule in it passed a test a clerk wrote.</p>
  <div class="mt-8">{cta("Ask about a pilot", "contact.html", dark=True)}</div>
</div></section>

<section class="mx-auto max-w-6xl px-5 py-20">
  <div class="grid gap-12 md:grid-cols-2">
    <div><div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">The problem it fixes</h2>
      <p class="mt-5 text-base leading-8 text-slate2">The best PLL clerk in the battalion knows which open requisition is never coming, which deadline is really a receipt problem, and which part to walk across the motor pool instead of ordering again. None of that is in a manual. It leaves with the clerk, and the unit relearns it the expensive way: trucks down for parts that were on the shelf, money spent twice, readiness reports that are wrong in both directions.</p></div>
    <div><div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">What it does</h2>
      <ul class="mt-5 space-y-4 text-base leading-7 text-slate2">
        <li><span class="font-semibold text-ink">Reads what the unit already has.</span> Equipment status, due-ins, demand history, receipts. Offline, company level, no new system of record.</li>
        <li><span class="font-semibold text-ink">Applies the judgment layer.</span> Elicited expert rules for the patterns (status codes, supersession, part-number receipt posting) plus a model to normalize the free text, so the clerk does not have to guess.</li>
        <li><span class="font-semibold text-ink">Gates every release with the clerk's tests.</span> Hundreds of adjudicated cases with exact expected outputs. A change that breaks one does not ship.</li>
        <li><span class="font-semibold text-ink">Returns an action list, not a dashboard.</span> Parts, funds and priority, ready for the maintenance meeting. Outcomes feed back in as new tests, so the engine gets stricter, not looser.</li>
      </ul></div>
  </div>
</section>

<section class="border-y border-line bg-white"><div class="mx-auto max-w-6xl px-5 py-20">
  <div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">Where it stands</h2>
  <div class="mt-8 grid gap-8 md:grid-cols-3 text-base leading-7 text-slate2">
    <div><p class="font-semibold text-ink">Stage</p><p class="mt-2">Concept with a working expert test harness that has been run against frontier models. Built for the Army's Adaptive Sustainment priority (forward maintenance, expeditionary supply).</p></div>
    <div><p class="font-semibold text-ink">Pilot offer</p><p class="mt-2">Two Army pilots in 2027 and one commercial fleet pilot in the Savannah port corridor. A pilot is priced per site per year, deliberately under the federal micro-purchase threshold.</p></div>
    <div><p class="font-semibold text-ink">Research thread</p><p class="mt-2">Stockage and distribution optimization under constraints is explored with IBM Qiskit as labeled research. No quantum-advantage claims are made.</p></div>
  </div>
</div></section>

<section class="mx-auto max-w-6xl px-5 py-20 text-center">
  <h2 class="font-display text-4xl font-semibold text-ink">Bring one unit's exports.</h2>
  <p class="mx-auto mt-4 max-w-xl text-lg leading-8 text-slate2">A pilot starts with a single company's data and the clerk who knows it best. We come back with the first adjudicated cases and what the engine would have caught.</p>
  <div class="mt-8">{cta("Ask about a pilot", "contact.html")}</div>
</section>
</main>'''
page("engine.html", "Dokimos Engine | Motor Pool Judgment Engine", "Unit-level Class IX decision support that encodes the clerk's judgment and gates every release with expert-authored tests. Army first, then fleets and depots.", eng_body, "engine.html")

# --------------------------------------------------------------------- course
course_body = f'''
<main>
<section class="streak bg-ink text-paper"><div class="mx-auto max-w-6xl px-5 py-20 md:py-24">
  <p class="text-xs font-semibold uppercase tracking-[0.28em] text-gold">03 &middot; Dokimos Course</p>
  <h1 class="mt-5 font-display text-5xl font-semibold leading-tight md:text-7xl">PLL and Class IX readiness judgment.</h1>
  <p class="mt-6 max-w-2xl text-lg leading-8 text-paper/80">A public, scheduled, two-day class for PLL clerks, maintenance sergeants and the leaders who sign for the readiness report. Taught by people who ran the shop, from the mistakes they already made. Not a GCSS-Army buttons class.</p>
  <div class="mt-8">{cta("Join the schedule list", "contact.html", dark=True)}</div>
</div></section>

<section class="mx-auto max-w-6xl px-5 py-20">
  <div class="grid gap-12 md:grid-cols-[1.2fr_0.8fr]">
    <div><div class="rule"></div><h2 class="mt-6 font-display text-3xl font-semibold text-ink">What is taught</h2>
      <ol class="mt-6 space-y-4 text-base leading-7 text-slate2">
        <li><span class="font-semibold text-ink">Reading the open requisition list like a clerk with five years in.</span> Dead, duplicate, superseded, and the status codes that lie.</li>
        <li><span class="font-semibold text-ink">Supply-down or sitting on the shelf.</span> Receipt posting, part-number supersession, and the cases where the truck is down for a paperwork reason.</li>
        <li><span class="font-semibold text-ink">Expedite, cross-level or wait.</span> Parts, funds and mission priority in one decision, with the cases that make it hard.</li>
        <li><span class="font-semibold text-ink">Shop stock that earns its space.</span> Demand history, the lines that never move, and what to turn in.</li>
        <li><span class="font-semibold text-ink">The Monday meeting.</span> Turning all of it into an action list the commander can act on in ten minutes.</li>
      </ol>
      <p class="mt-6 text-base leading-8 text-slate2">Every lesson is built from adjudicated cases in the Dokimos library, with the answer and the reason. Students leave with the case book.</p></div>
    <div class="border border-line bg-white p-8">
      <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate2">Public price</p>
      <p class="num mt-3 text-6xl text-ink">$1,250</p><p class="text-sm text-slate2">per seat, two days, materials included</p>
      <ul class="mt-6 space-y-3 text-sm leading-7 text-slate2">
        <li>Eight seats per class. A unit sending eight pays $10,000.</li>
        <li>Regularly scheduled and open to the public, priced the same for everyone.</li>
        <li>Structured so a unit can pay with a Government Purchase Card using an SF-182. Confirm with your resource manager and GPC billing official.</li>
        <li>Delivered at or near Fort Stewart and Hunter Army Airfield first; other posts by request.</li>
      </ul>
      <p class="mt-6 text-xs text-slate2">Next public dates are announced to the schedule list first.</p>
      <div class="mt-6">{cta("Join the schedule list", "contact.html")}</div>
    </div>
  </div>
</section>
</main>'''
page("course.html", "Dokimos Course | PLL and Class IX readiness judgment", "A public, scheduled class on PLL and Class IX readiness judgment taught by people who ran the shop. $1,250 per seat, eight seats per class, structured for purchase-card buying.", course_body, "course.html")

# --------------------------------------------------------------------- contact
contact_body = f'''
<main>
<section class="mx-auto max-w-6xl px-5 py-20">
  <div class="grid gap-12 md:grid-cols-[0.9fr_1.1fr]">
    <div><div class="rule"></div><h1 class="mt-6 font-display text-5xl font-semibold text-ink">Talk to Dokimos</h1>
      <p class="mt-5 text-base leading-8 text-slate2">Tell us the judgment you are losing, the domain you need ground truth in, or the class you want to send people to. A plain answer within two business days.</p>
      <p class="mt-6 text-sm leading-7 text-slate2">Email works too: <a class="font-semibold text-ink underline" href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="mt-2 text-sm leading-7 text-slate2">Port Wentworth, Georgia. Eastern time.</p></div>
    <form action="{FORM}" method="POST" class="border border-line bg-white p-8">
      <input type="hidden" name="_subject" value="Dokimos website inquiry">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="{SITE}/thanks.html">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <div class="grid gap-5 sm:grid-cols-2">
        <label class="block text-sm font-medium text-ink">Name<input required name="name" class="mt-2 w-full rounded-md border border-line px-3 py-2 text-base" type="text"></label>
        <label class="block text-sm font-medium text-ink">Organization<input name="organization" class="mt-2 w-full rounded-md border border-line px-3 py-2 text-base" type="text"></label>
      </div>
      <label class="mt-5 block text-sm font-medium text-ink">Email<input required name="email" class="mt-2 w-full rounded-md border border-line px-3 py-2 text-base" type="email"></label>
      <label class="mt-5 block text-sm font-medium text-ink">What is this about?
        <select name="line" class="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-base">
          <option>Environments (AI lab or data vendor)</option><option>Engine (Army unit, fleet, depot)</option><option>Course (training seats)</option><option>Something else</option></select></label>
      <label class="mt-5 block text-sm font-medium text-ink">Message<textarea required name="message" rows="6" class="mt-2 w-full rounded-md border border-line px-3 py-2 text-base"></textarea></label>
      <button type="submit" class="mt-6 inline-flex rounded-md bg-ink px-6 py-3 text-sm font-semibold text-paper hover:bg-stone">Send</button>
      <p class="mt-4 text-xs leading-6 text-slate2">Submissions are delivered by FormSubmit to the Dokimos inbox. Nothing is stored on this site. See <a class="underline" href="privacy.html">privacy</a>.</p>
    </form>
  </div>
</section>
</main>'''
page("contact.html", "Contact | Dokimos", "Talk to Dokimos about environments, the engine, or course seats. A plain answer within two business days.", contact_body, "contact.html")

thanks_body = f'''<main><section class="mx-auto max-w-3xl px-5 py-32 text-center"><div class="rule mx-auto"></div><h1 class="mt-6 font-display text-5xl font-semibold text-ink">Received.</h1><p class="mt-5 text-lg leading-8 text-slate2">Thank you. You will hear back within two business days.</p><div class="mt-8">{cta("Back to Dokimos", "index.html")}</div></section></main>'''
page("thanks.html", "Thank you | Dokimos", "Your message was received.", thanks_body, "")

privacy_body = '''<main><section class="mx-auto max-w-3xl px-5 py-20"><div class="rule"></div><h1 class="mt-6 font-display text-4xl font-semibold text-ink">Privacy</h1>
<div class="mt-6 space-y-4 text-base leading-8 text-slate2">
<p>This site does not use cookies and does not run analytics scripts. It loads fonts from Google Fonts and styling from the Tailwind CDN, which receive your browser's standard requests.</p>
<p>The contact form is delivered by FormSubmit (formsubmit.co) to the Dokimos inbox. What you type in the form is used to reply to you and for nothing else. It is not sold or shared.</p>
<p>To have your message deleted, email the address in the footer.</p>
<p class="text-sm">Last updated October 9, 2026.</p></div></section></main>'''
page("privacy.html", "Privacy | Dokimos", "How the Dokimos site handles your information.", privacy_body, "")


# --------------------------------------------------------------------- faq
FAQ = [
 ("What does Dokimos do?", "Dokimos writes down the judgment that is not in the manual, as tests with exact answers, and proves it. The output is three things: expert-authored tasks and environments for AI labs (Dokimos Environments), a decision tool for Army motor pools and fleets (Dokimos Engine), and a public class for PLL clerks and maintenance sergeants (Dokimos Course)."),
 ("What is a judgment task?", "A single decision an experienced person makes that no written policy fully covers, written as a problem with one exact answer, a verifier that checks it automatically, and a short reason the crux is judgment rather than a rule. Example: deciding that an open requisition is dead because the part was superseded and received under a new number."),
 ("Why do AI labs buy this?", "Frontier models now solve most tasks that have a written rule. They still fail tasks whose answer lives in an expert's head. Labs pay for ground truth in exactly those domains, and they pay more when the tasks survive a strict grader. On an independent benchmark program in late 2026, frontier models solved the founder's written-rule task in every trial and his Class IX judgment task in zero of five."),
 ("What is the probe log?", "The record of which blind solvers were run against a task before delivery and what they returned. If a model clears a task on written rules alone, the task goes back to the bench. Buyers see the gap before they pay for it."),
 ("What domains do you cover?", "Class IX parts judgment (dead, duplicate and superseded requisitions, shop stock, turn-ins), dispatch and 5988-E fault flow, deadline and NMC recovery under parts and funds constraints, forward maintenance and expeditionary supply, and warehouse and sort operations. New domains are added through veteran and industrial co-authors under the same protocol."),
 ("Do you use real Army data?", "No. Environments are built from synthetic and sanitized records that reproduce the judgment. The Engine runs offline on a unit's own laptop; nothing is uploaded, and Dokimos never asks a unit to send its exports."),
 ("How is Dokimos different from a data labeling vendor?", "Labeling vendors recruit people to annotate what a lab already has. Dokimos authors the cases, writes the exact answers and the verifiers, runs the probes, and delivers the proof. The product is verified judgment, not labor."),
 ("What does the Engine actually produce?", "An action list for the Monday maintenance meeting: which requisitions are dead, duplicated or already filled under a superseding part number; which vehicles are truly supply-down; which parts to expedite or cross-level. Every rule in it passed a test a clerk wrote."),
 ("How can a unit buy the course?", "The course is public, regularly scheduled and priced the same for everyone, $1,250 per seat, eight seats per class. That structure is meant for Government Purchase Card buying with an SF-182. Confirm with your resource manager and GPC billing official."),
 ("Who is behind Dokimos?", "Joshua Griffin, six years U.S. Army motor transport (PLL clerk, dispatch and 5988-E, deadline and NMC tracking), then area manager at an Amazon sort and delivery center. B.S. Business Analytics, accounting minor; MBA, University of Florida, December 2026. Dokimos is a service-disabled veteran-owned business in Port Wentworth, Georgia."),
 ("How do I get a sample task?", "Use the contact form and name the domain. A sample task with its probe log goes out within 48 hours, with a quote for a shared or exclusive set."),
 ("How do you say Dokimos?", "DOCK-ee-moss. Ancient Greek for a coin that passed the test on the touchstone. Spell it with a K."),
]
faq_items = "".join(f'<details class="border-b border-line py-5"><summary class="flex items-center justify-between font-display text-xl font-semibold text-ink">{html.escape(q)}<span class="ml-4 text-gold">+</span></summary><p class="mt-3 max-w-3xl text-base leading-8 text-slate2">{html.escape(a)}</p></details>' for q, a in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
faq_body = f"""
<main><section class="mx-auto max-w-6xl px-5 py-20"><div class="rule"></div><h1 class="mt-6 font-display text-5xl font-semibold text-ink">Questions, answered plainly</h1>
<p class="mt-4 max-w-2xl text-lg leading-8 text-slate2">What buyers ask before the first call. If yours is not here, <a class="underline" href="contact.html">ask it</a>.</p>
<div class="mt-10">{faq_items}</div></section></main>
<script type="application/ld+json">{faq_ld}</script>"""
page("faq.html", "FAQ | Dokimos", "Plain answers to what AI labs, Army units and training buyers ask Dokimos before the first call.", faq_body, "")

# --------------------------------------------------------------------- assets
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect x="2" y="2" width="36" height="36" rx="7" fill="#121212"/><path d="M11 29 L29 11" stroke="#D4A017" stroke-width="5" stroke-linecap="round"/></svg>')
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    urls = "".join(f"<url><loc>{SITE}/{p}</loc></url>" for p in ["index.html", "environments.html", "engine.html", "course.html", "faq.html", "contact.html", "privacy.html"])
    f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(head("Not found | Dokimos", "Page not found.", "404.html") + header("") + f'<main><section class="mx-auto max-w-3xl px-5 py-32 text-center"><p class="num text-8xl text-gold">404</p><h1 class="mt-4 font-display text-4xl font-semibold text-ink">That page did not pass.</h1><p class="mt-4 text-lg text-slate2">It is not here. Try the home page.</p><div class="mt-8">{cta("Home", "index.html")}</div></section></main>' + FOOTER)
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write("# Dokimos site\n\nStatic site for Dokimos (Judgment, proven). Pages are generated by `build_site.py`; edit the Python, run it, commit the output.\n\nContact form posts to FormSubmit; the first submission triggers a one-time activation email to the inbox.\n")
print("built", sorted(p for p in os.listdir(OUT) if p.endswith((".html", ".svg", ".txt", ".xml"))))

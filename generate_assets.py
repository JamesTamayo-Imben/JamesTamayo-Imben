import random
import re
import textwrap
from math import ceil
from html import escape as e
from xml.etree import ElementTree as ET
BG="#040A1C"; PANEL="#0A1633"; LINE="#16295A"; ACC="#3B82F6"; LIGHT="#93C5FD"; CY="#22D3EE"; TXT="#E6EEFF"; MUT="#8FA3C7"
LOCATION="Dasmariñas, Cavite, PH"
MONO="'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SERIF="Georgia,'Palatino Linotype','Times New Roman',serif"
TYPE_SCALE={"micro":10,"caption":12,"label":14,"body":16,"lead":20,"subhead":24,
            "heading":32,"display":48,"hero":64,"index":96}
TYPE_STEPS=tuple(TYPE_SCALE.values())
_id=[0]
def uid(): _id[0]+=1; return f"u{_id[0]}"

def type_size(size):
    return min(TYPE_STEPS,key=lambda step:abs(step-size))

STYLE="""<style>
.f{opacity:0;animation:f .9s ease forwards}
@keyframes f{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.tw{animation:tw 3.2s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.1}50%{opacity:.9}}
.bl{animation:bl 1s steps(1) infinite}
@keyframes bl{50%{opacity:0}}
.fl{stroke-dasharray:5 7;animation:fl 1s linear infinite}
@keyframes fl{to{stroke-dashoffset:-12}}
.pu{animation:pu 2.8s ease-in-out infinite}
@keyframes pu{0%,100%{opacity:.45}50%{opacity:1}}
.r{opacity:0;animation:r .6s ease forwards}
@keyframes r{to{opacity:1}}
@media (prefers-reduced-motion:reduce){.f,.r{opacity:1;animation:none}}
</style>"""
STYLE_CSS=STYLE.removeprefix("<style>").removesuffix("</style>")

def wrap(name,w,h,body,orbs=True,big=False,background=True,corner_radius=18):
    o=''
    if orbs:
        o=(f'<circle cx="{w*0.15}" cy="{h*0.2}" r="{h*0.55 if big else h*0.7}" fill="#2563EB" opacity="{.38 if big else .16}" filter="url(#blur)">'
           f'<animate attributeName="cx" values="{w*0.15};{w*0.28};{w*0.15}" dur="12s" repeatCount="indefinite"/></circle>'
           f'<circle cx="{w*0.88}" cy="{h*0.9}" r="{h*0.5 if big else h*0.6}" fill="{CY}" opacity="{.22 if big else .08}" filter="url(#blur)">'
           f'<animate attributeName="cy" values="{h*0.9};{h*0.7};{h*0.9}" dur="10s" repeatCount="indefinite"/></circle>')
    surface=f'<rect width="{w}" height="{h}" fill="url(#bg)"/>{o}<rect width="{w}" height="{h}" fill="url(#grid)"/>' if background else ""
    frame=f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{corner_radius}" fill="none" stroke="{LINE}"/>' if background else ""
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
{STYLE}
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050E2B"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{CY}"/></linearGradient>
<linearGradient id="tx" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="{LIGHT}"/><stop offset="1" stop-color="{CY}"/></linearGradient>
<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-20%" y="-30%" width="140%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="55"/></filter>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1B3170" stroke-opacity=".38"/></pattern>
<clipPath id="rc"><rect width="{w}" height="{h}" rx="{corner_radius}"/></clipPath>
</defs>
<g clip-path="url(#rc)">
{surface}
{body}
</g>
{frame}
</svg>'''
    with open(f"assets/{name}.svg","w",encoding="utf-8") as asset:
        asset.write(s)

def t(x,y,s,size=TYPE_SCALE["body"],fill=TXT,font=MONO,weight="400",style="normal",anchor="start",ls=0,extra=""):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{type_size(size)}" fill="{fill}" font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{e(s)}</text>\n'

def ft(x,y,s,delay=0,**k):
    return t(x,y,s,extra=f'class="f" style="animation-delay:{delay}s"',**k)

def typed(x,y,s,size,fill,begin,weight="400"):
    size=type_size(size)
    cw=size*0.6; n=len(s); i=uid()
    vals=";".join(str(round(j*cw)) for j in range(n+2))
    dur=max(0.4,n*0.03)
    return (f'<clipPath id="{i}"><rect x="{x}" y="{y-size}" width="0" height="{size*1.5}"><animate attributeName="width" values="{vals}" calcMode="discrete" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
            + t(x,y,s,size,fill,weight=weight,extra=f'clip-path="url(#{i})"'))

def stars(w,h,n,seed):
    r=random.Random(seed); o=''
    for _ in range(n):
        o+=f'<circle class="tw" cx="{r.randint(10,w-10)}" cy="{r.randint(10,h-10)}" r="{r.choice([1,1,1.5,2])}" fill="{LIGHT}" style="animation-delay:{r.random()*3:.2f}s"/>'
    return o

def pill(x,y,s,size=13,delay=0,stroke=ACC,fill=PANEL):
    size=type_size(size)
    w=len(s)*size*0.6+24; h=size+16
    return (f'<g class="f" style="animation-delay:{delay}s"><rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}" stroke-opacity=".8"/>'
            + t(x+w/2,y+h/2+size*0.35,s,size,TXT,anchor="middle")+'</g>'), w

def sheen(x,y,w,h,r,delay=0):
    i=uid()
    return (f'<clipPath id="{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
            f'<g clip-path="url(#{i})"><rect x="{x-120}" y="{y}" width="90" height="{h}" fill="url(#sheen)">'
            f'<animate attributeName="x" values="{x-120};{x+w+60};{x+w+60}" keyTimes="0;.45;1" dur="5.5s" begin="{delay}s" repeatCount="indefinite"/></rect></g>')

# ---------- HERO ----------
def hero():
    w,h=1000,440; b=''
    b+=typed(40,104,"> whoami",16,CY,0.3)
    b+=f'<text x="40" y="184" font-family="{MONO}" font-size="{TYPE_SCALE["hero"]}" font-weight="800" fill="url(#tx)" filter="url(#glow)" class="f" style="animation-delay:1.2s">JAMES TAMAYO</text>'
    b+=f'<rect x="42" y="204" width="0" height="4" rx="2" fill="url(#a)"><animate attributeName="width" from="0" to="280" begin="1.6s" dur="1s" fill="freeze"/></rect>'
    b+=ft(40,254,"Full-stack developer",1.8,size=25,fill=LIGHT,weight="600",ls=1)
    b+=ft(40,292,"I design in Figma and build web apps with React and Laravel.",2.1,size=19,fill=MUT,font=SERIF,style="italic")
    x=40
    for i,c in enumerate(["React","Laravel","Inertia.js","TypeScript","Supabase","MySQL"]):
        p,pw=pill(x,322,c,13,2.4+i*0.15); b+=p; x+=pw+10
    b+=f'<circle class="pu" cx="48" cy="404" r="5" fill="{CY}"/>'+ft(62,409,f"BSIS student  ·  {LOCATION}",2.9,size=13,fill=MUT)
    b+=t(672,112,"STEP22  /  TRUST TRACE",11,CY,weight="800",ls=2)
    b+='<path d="M682 158v176" fill="none" stroke="#1B3170" stroke-width="2"/>'
    trace=[
        (174,"01","ROLE CHECK","Six roles. One scoped view.","role"),
        (250,"02","LEDGER ENTRY","Financial records, linked by hash.","entry"),
        (326,"03","PROOF CHAIN","SHA-256 makes changes visible.","proof")
    ]
    trace_icons={
        "role":'<path d="M12 2.8 20 6v5.2c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6z"/><circle cx="12" cy="9" r="2"/><path d="M8.5 16a3.5 3.5 0 0 1 7 0"/>',
        "entry":'<path d="M7 3.5h7l4 4V20H7z"/><path d="M14 3.5v4h4M10 12h5M10 15h5"/>',
        "proof":'<path d="M8.5 8.5 6 6a3 3 0 0 0-4 4l4 4a3 3 0 0 0 4 0l2-2"/><path d="m15.5 15.5 2.5 2.5a3 3 0 0 0 4-4l-4-4a3 3 0 0 0-4 0l-2 2"/><path d="m9 15 6-6"/>'
    }
    for y,num,title,detail,kind in trace:
        b+=f'<circle cx="682" cy="{y}" r="16" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".7"/>'
        b+=f'<g transform="translate(670 {y-12})" fill="none" stroke="{CY}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{trace_icons[kind]}</g>'
        b+=t(716,y-5,num,10,CY,weight="700")+t(746,y-5,title,15,TXT,weight="700")
        b+=t(746,y+18,detail,12,MUT,font=SERIF,style="italic")
        if y != 326:
            b+=f'<line x1="716" y1="{y+34}" x2="960" y2="{y+34}" stroke="{LINE}" stroke-dasharray="2 6"/>'
    b+=t(816,374,"RBAC  /  SHA-256 CHAIN",10,MUT,ls=1,anchor="middle")
    b+=f'<rect x="0" y="{h-4}" width="{w}" height="4" fill="url(#a)" opacity=".8"/>'
    wrap("james-hero-banner",w,h,b,big=True)

def about_copy():
    paragraph=("I'm a full-stack developer and BS Information Systems student based in Dasmariñas, Cavite. "
               "I design interfaces in Figma and build web apps with React, Laravel, and Supabase. "
               "My projects include a school transparency platform, a local-first focus app, and a birthday-sharing app.")
    lines=textwrap.wrap(paragraph,width=100)
    w,h=1000,len(lines)*24+32
    b=f'<rect x="0" y="0" width="7" height="{h}" fill="url(#a)"/>'
    for i,line in enumerate(lines):
        b+=t(34,28+i*24,line,15,TXT)
    wrap("about-copy",w,h,b,orbs=False)


# ---------- ASCII PORTRAIT ----------
def portrait():
    rows=open("ascii.txt",encoding="utf-8").read().split("\n")
    cols=max(len(r) for r in rows); AW=480; cw=AW/cols; fs=cw/0.6; lh=cw*2.0
    ax,ay=30,64; H=int(ay+len(rows)*lh+36); w=1000
    cls={";":"#1E40AF",":":"#1E40AF","+":"#2563EB","x":"#3B82F6","X":"#60A5FA","$":"#93C5FD","&":"#EAF2FF"}
    b=stars(w,H,30,21)
    # frame for ascii
    b+=f'<rect x="{ax-14}" y="22" width="{AW+28}" height="{H-44}" rx="14" fill="#030817" stroke="{LINE}"/>'
    b+=f'<rect x="{ax-14}" y="22" width="{AW+28}" height="30" rx="14" fill="{PANEL}"/><rect x="{ax-14}" y="40" width="{AW+28}" height="12" fill="{PANEL}"/>'
    for i,c in enumerate(["#1E3A8A",ACC,CY]): b+=f'<circle cx="{ax+4+i*18}" cy="37" r="5" fill="{c}"/>'
    b+=t(ax+AW/2,41,"~/james/portrait.ascii",11,MUT,anchor="middle")
    b+=f'<g filter="url(#glow)" opacity=".95">'
    for i,row in enumerate(rows):
        runs=[]; 
        for ch in row:
            k=cls.get(ch,"sp")
            if runs and runs[-1][0]==k: runs[-1][1]+=ch
            else: runs.append([k,ch])
        tsp="".join((f'<tspan fill="{k}">{e(txt)}</tspan>' if k!="sp" else f'<tspan>{e(txt)}</tspan>') for k,txt in runs)
        b+=(f'<text class="r" xml:space="preserve" x="{ax}" y="{ay+(i+1)*lh:.2f}" font-family="{MONO}" font-size="{fs:.2f}" '
            f'textLength="{AW}" lengthAdjust="spacing" style="animation-delay:{i*0.035:.2f}s">{tsp}</text>\n')
    b+='</g>'
    # scan line
    b+=(f'<rect x="{ax-8}" y="{ay}" width="{AW+16}" height="2" fill="{CY}" opacity=".55" filter="url(#glow)">'
        f'<animate attributeName="y" values="{ay};{ay+len(rows)*lh:.0f};{ay}" dur="7s" repeatCount="indefinite"/></rect>')
    # ID card
    X=560; Wd=410
    b+=f'<g class="f" style="animation-delay:.4s"><rect x="{X}" y="22" width="{Wd}" height="430" rx="16" fill="{PANEL}" fill-opacity=".92" stroke="{ACC}" stroke-opacity=".5"/></g>'
    b+=ft(X+26,62,"ID.CARD",.6,size=12,fill=CY,weight="800",ls=5)
    b+=ft(X+26,106,"James Tamayo",.8,size=36,fill=TXT,font=SERIF,weight="700",style="italic")
    b+=ft(X+26,134,"Full-stack developer",1.0,size=15,fill=LIGHT,weight="600")
    b+=f'<rect x="{X+26}" y="148" width="0" height="3" rx="1.5" fill="url(#a)"><animate attributeName="width" from="0" to="120" begin="1.2s" dur=".9s" fill="freeze"/></rect>'
    F=[("EDUCATION","BS in Information Systems"),("SCHOOL","Kolehiyo ng Lungsod ng Dasmariñas"),("YEARS","2023 to 2026 (Student)"),
       ("LOCATION",LOCATION),("BUILDS WITH","React · Laravel · Supabase · Node.js"),("DESIGNS IN","Figma  (UI / UX)")]
    for i,(k,v) in enumerate(F):
        y=190+i*44
        b+=ft(X+26,y,k,1.2+i*.12,size=11,fill=MUT,weight="700",ls=3)+ft(X+26,y+21,v,1.3+i*.12,size=14,fill=TXT)
    # design card
    b+=f'<g class="f" style="animation-delay:1.8s"><rect x="{X}" y="470" width="{Wd}" height="144" rx="16" fill="#06102A" stroke="{LINE}"/></g>'
    b+=ft(X+28,508,"DESIGN  ×  CODE",2.0,size=12,fill=CY,weight="800",ls=4)
    b+=ft(X+28,544,"Sketch it in Figma.",2.1,size=22,fill=TXT,font=SERIF,weight="700",style="italic")
    b+=ft(X+28,574,"Ship it in code.",2.2,size=22,fill=LIGHT,font=SERIF,weight="700",style="italic")
    # stat tiles
    for i,(v,l) in enumerate([("5","projects"),("4","certs"),("2026","grad year")]):
        x=X+i*140; y=634
        b+=f'<g class="f" style="animation-delay:{2.3+i*.15}s"><rect x="{x}" y="{y}" width="130" height="78" rx="12" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".5"/>'+t(x+16,y+38,v,26,LIGHT,weight="800")+t(x+16,y+60,l,12,MUT)+'</g>'
        b+=sheen(x,y,130,78,12,3+i*.4)
    wrap("ascii-portrait",w,H,b)

# ---------- TITLES ----------
def titles():
    D={"about":("01","ABOUT","Hello, I'm James."),"recognition":("02","RECOGNITION","Proof, on the record."),
       "work":("03","SELECTED WORK","Products, not assignments."),"toolkit":("04","TOOLKIT","The tools I reach for."),
       "commits":("05","COMMIT LOG","A year of building."),"certifications":("06","CERTIFICATIONS","Credentials, verified."),
       "connect":("07","CONNECT","Let's build something worth explaining.")}
    for n,(num,lab,head) in D.items():
        b=t(28,98,num,96,"none",weight="800",extra=f'stroke="{ACC}" stroke-width="1.4" stroke-opacity=".55"')
        b+=ft(170,46,lab,0.1,size=13,fill=CY,weight="700",ls=5)
        b+=ft(170,88,head,0.3,size=34,fill=TXT,font=SERIF,weight="700",style="italic")
        b+=f'<rect x="172" y="102" width="0" height="3" rx="1.5" fill="url(#a)"><animate attributeName="width" from="0" to="130" begin=".6s" dur=".9s" fill="freeze"/></rect>'
        b+=f'<line x1="850" y1="62" x2="975" y2="62" stroke="{ACC}" stroke-opacity=".5" class="fl"/><circle cx="975" cy="62" r="5" fill="{CY}" filter="url(#glow)" class="pu"/>'
        b+=f'<circle r="3" fill="#fff"><animateMotion path="M850 62 H975" dur="2.2s" repeatCount="indefinite"/></circle>'
        wrap(f"title-{n}",1000,125,b)

# ---------- ACHIEVEMENTS ----------
def achievement_icon(x,y,kind):
    paths={
        "projects":'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 7h.01M11 7h.01M8 13h8M8 16h5"/>',
        "roles":'<circle cx="9" cy="8" r="3"/><path d="M3.5 19v-1.5a5.5 5.5 0 0 1 11 0V19zM16 5.5a3 3 0 0 1 0 5.8M17 14a4.5 4.5 0 0 1 3.5 4.4V19h-3"/>',
        "ledger":'<path d="M6 3.5h8l4 4V14"/><path d="M14 3.5v4h4M6 3.5v17h6"/><path d="M9 11h6M9 14h4"/><path d="m14 18 2 2 4-4"/>',
        "certificate":'<circle cx="12" cy="10" r="7"/><path d="m8 16-1 5 5-2 5 2-1-5M9 10l2 2 4-4"/>',
        "local":'<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 9h8M8 13h5M9 19v2m6-2v2"/>',
        "stars":'<path d="m12 3 2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>'
    }
    return (f'<g transform="translate({x-12} {y-12})" fill="none" stroke="{CY}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>')

def achievements():
    A=[("5","Featured projects","projects",100),("6","User roles in STEP22","roles",100),
       ("SHA-256","Tamper-evident ledger","ledger",100),("4","Online certifications","certificate",100),
       ("0","Accounts needed: Pomonote, Batify","local",100),("4","GitHub stars earned","stars",100)]
    b=stars(1000,340,16,5)
    for i,(v,l,ic,p) in enumerate(A):
        x=30+(i%3)*320; y=30+(i//3)*150; d=0.15*i
        b+=f'<g class="f" style="animation-delay:{d}s"><rect x="{x}" y="{y}" width="300" height="130" rx="14" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".45"/>'
        b+=f'<circle cx="{x+40}" cy="{y+42}" r="20" fill="none" stroke="{CY}" stroke-opacity=".7" class="pu" style="animation-delay:{d}s"/>'+achievement_icon(x+40,y+42,ic)
        b+=t(x+76,y+50,v,28,LIGHT,weight="800")+t(x+24,y+90,l,15,MUT,SERIF,style="italic")
        b+=f'<rect x="{x+24}" y="{y+106}" width="252" height="5" rx="2.5" fill="#0D1F4D"/><rect x="{x+24}" y="{y+106}" width="0" height="5" rx="2.5" fill="url(#a)"><animate attributeName="width" from="0" to="{252*p/100:.0f}" begin="{1+d}s" dur="1.2s" fill="freeze"/></rect></g>'
        b+=sheen(x,y,300,130,14,d+1)
    wrap("achievements",1000,340,b)

# ---------- PROJECTS ----------
def projects():
    P=[("01","STEP22: School Transparency Portal","Role-based governance and a tamper-evident financial ledger for KLD.",[("6","user roles"),("SHA-256","ledger chain"),("2-layer","access control")],["Laravel 12","React 18","Inertia.js","MySQL","Supabase Auth"],["Role-scoped UI","Laravel + RBAC","SHA-256 ledger"]),
       ("02","Pomonote: Focus Timer + Tasks","Keyboard-first, local-first focus timer + tasks + notes. No account.",[("0","accounts needed"),("0","dependencies"),("MIT","licensed")],["JavaScript","Local-first","Keyboard-first"],["Timer","Tasks","Notes"]),
       ("03","Batify: Letters, Wishes & Gifts","Birthday letters, wishes and gifts in one link. No signup.",[("1","link to share"),("0","signups"),("3","Supabase services")],["React","Supabase","Postgres","Edge Functions"],["React SPA","Edge Functions","Postgres+Storage"]),
       ("04","FolioOS: Desktop Portfolio","A desktop-style portfolio with case studies and recruiter details.",[("Next.js","App Router"),("TypeScript","built with"),("Supabase","backend")],["Next.js","React","TypeScript","Supabase","Zustand"],["Desktop portfolio","Case studies","Recruiter profile"]),
       ("05","Tagthr22: 3D Design Element","A React and TypeScript code bundle based on a Figma design.",[("TypeScript","built with"),("Vite","build tool"),("Public","repository")],["React","TypeScript","Vite","MUI"],["Figma design","React code bundle","Vite preview"])]
    for n,(num,title,desc,m,chips,flow) in enumerate(P,1):
        w,h=1000,290; b=stars(w,h,10,n)
        b+=f'<rect x="0" y="0" width="7" height="{h}" fill="url(#a)"/>'
        b+=ft(34,46,f"PROJECT {num}",0.1,size=12,fill=CY,weight="700",ls=4)
        b+=ft(34,82,title,0.3,size=23,fill=TXT,weight="800")
        b+=ft(34,110,desc,0.5,size=16,fill=MUT,font=SERIF,style="italic")
        for i,(v,l) in enumerate(m):
            x=34+i*200; y=134
            b+=f'<g class="f" style="animation-delay:{0.7+i*0.15}s"><rect x="{x}" y="{y}" width="186" height="68" rx="12" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".5"/>'+t(x+16,y+33,v,22,LIGHT,weight="800")+t(x+16,y+54,l,12,MUT)+'</g>'
            b+=sheen(x,y,186,68,12,1+i*0.4)
        x=34
        for i,c in enumerate(chips):
            p,pw=pill(x,226,c,13,1.3+i*0.12,stroke=CY); b+=p; x+=pw+10
        # flow panel
        b+=f'<rect x="660" y="26" width="310" height="238" rx="14" fill="#06102A" stroke="{LINE}"/>'+t(682,52,"SYSTEM FLOW",11,MUT,ls=3)
        ys=[70,132,194]
        for i,(yy,lab) in enumerate(zip(ys,flow)):
            b+=f'<g class="f" style="animation-delay:{0.8+i*0.25}s"><rect x="745" y="{yy}" width="140" height="42" rx="11" fill="{PANEL}" stroke="url(#a)" stroke-width="1.6" filter="url(#glow)"/>'+t(815,yy+26,lab,13,TXT,weight="700",anchor="middle")+'</g>'
        for a,c in ((ys[0]+42,ys[1]),(ys[1]+42,ys[2])):
            b+=f'<line class="fl" x1="815" y1="{a}" x2="815" y2="{c}" stroke="{CY}" stroke-width="2"/><circle r="3.5" fill="#fff"><animateMotion path="M815 {a} V{c}" dur="1.6s" repeatCount="indefinite"/></circle>'
        wrap(f"project-{n}",w,h,b)

# ---------- TOOLKIT ----------
def toolkit_icon(x,y,kind):
    paths={
        "languages":'<path d="m8 5-6 7 6 7M16 5l6 7-6 7M14 4l-4 16"/>',
        "ai":'<path d="m12 2.8 1.9 6.3 6.3 1.9-6.3 1.9-1.9 6.3-1.9-6.3-6.3-1.9 6.3-1.9z"/><path d="M19 3v3m-1.5-1.5h3M4 17v4m-2-2h4"/>',
        "frontend":'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 9v11"/>',
        "backend":'<rect x="4" y="3" width="16" height="8" rx="1.5"/><rect x="4" y="13" width="16" height="8" rx="1.5"/><path d="M8 7h.01M8 17h.01M12 7h4M12 17h4"/>',
        "data":'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
        "design":'<path d="m4 20 4.5-1 10-10L15 5.5 5 15.5 4 20Z"/><path d="m13.5 7 3.5 3.5M4 20l4-1"/>'
    }
    return (f'<g transform="translate({x-11} {y-11})" fill="none" stroke="{CY}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>')

def toolkit():
    T=[("LANGUAGES","languages",["JavaScript","TypeScript","PHP","SQL","HTML / CSS"]),
       ("AI TOOLS","ai",["AI-assisted dev","Prompt engineering","LLM APIs"]),
       ("FRONTEND","frontend",["React","Inertia.js","Tailwind","Vite"]),
       ("BACKEND","backend",["Laravel","Node.js","Express","REST APIs"]),
       ("DATA / INFRA","data",["MySQL","PostgreSQL","SQLite","Supabase","GitHub Pages"]),
       ("DESIGN / TOOLS","design",["Figma","UI Design","Git","GitHub","Composer"])]
    w,h=1000,470; b=stars(w,h,24,9)
    # constellation links
    for r in range(2):
        yy=125+r*210; b+=f'<line class="fl" x1="180" y1="{yy}" x2="820" y2="{yy}" stroke="{CY}" stroke-opacity=".35"/>'
    for c in range(3):
        xx=180+c*320; b+=f'<line class="fl" x1="{xx}" y1="125" x2="{xx}" y2="335" stroke="{CY}" stroke-opacity=".35"/>'
    for i,(cat,icon,items) in enumerate(T):
        px=30+(i%3)*320; py=30+(i//3)*210; d=0.12*i
        b+=f'<g class="f" style="animation-delay:{d}s"><rect x="{px}" y="{py}" width="300" height="190" rx="16" fill="{PANEL}" fill-opacity=".92" stroke="{ACC}" stroke-opacity=".45"/>'
        b+=toolkit_icon(px+26,py+30,icon)+t(px+48,py+35,cat,13,CY,weight="800",ls=3)
        b+=f'<line x1="{px+20}" y1="{py+52}" x2="{px+280}" y2="{py+52}" stroke="{LINE}"/></g>'
        x,y=px+20,py+68
        for j,it in enumerate(items):
            pw=len(it)*7.2+24
            if x+pw>px+285: x=px+20; y+=40
            p,pw=pill(x,y,it,13,0.4+d+j*0.08); b+=p; x+=pw+8
        b+=sheen(px,py,300,190,16,d+1.5)
    wrap("toolkit",w,h,b)

# ---------- CERTS ----------
def certs():
    C=[f"[Online Certification {i}]" for i in range(1,5)]
    w,h=1000,190; b=stars(w,h,10,4)
    for i,c in enumerate(C):
        x=30+(i%2)*480; y=30+(i//2)*68; d=0.1*i
        b+=f'<g class="f" style="animation-delay:{d}s"><rect x="{x}" y="{y}" width="450" height="54" rx="12" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".4"/>'
        b+=f'<circle cx="{x+30}" cy="{y+27}" r="13" fill="none" stroke="{CY}" stroke-width="1.6"/><path d="M{x+23} {y+27} l5 5 l9 -10" fill="none" stroke="{CY}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        b+=t(x+58,y+32,c,16,TXT,weight="600")+t(x+430,y+32,"VERIFIED",10,MUT,anchor="end",ls=2)+'</g>'
        b+=sheen(x,y,450,54,12,d+1.2)
    wrap("certifications",w,h,b)


def certificate_cards():
    cards=[
        ("Certificate details","See linked document"),
        ("IEEE-CS-PH 2025 Talk Series: Talk 3","Certificate of Participation · IEEE CS Philippines"),
        ("Oceans: Hour of Code","Code.org · course: oceans"),
        ("Certificate details","Ref: AAR-TOD-2025-ZAM-387-015"),
    ]
    w,h=490,156
    for i,(title,detail) in enumerate(cards,1):
        delay=(i-1)*0.5
        b=stars(w,h,6,i+10)
        b+=t(464,126,f"{i:02}",96,"none",weight="800",anchor="end",
             extra=f'stroke="{ACC}" stroke-width="1.2" stroke-opacity=".35"')
        b+=f'<rect x="10" y="10" width="470" height="136" rx="16" fill="{PANEL}" fill-opacity=".92" stroke="url(#a)" stroke-opacity=".7"/>'
        b+='<polygon points="50,80 60,110 66,102 72,110 82,80" fill="#1D4ED8" opacity=".9"/>'
        b+=f'<circle cx="66" cy="58" r="36" fill="none" stroke="{CY}" stroke-opacity=".7" stroke-dasharray="3 7"><animateTransform attributeName="transform" type="rotate" from="0 66 58" to="360 66 58" dur="18s" repeatCount="indefinite"/></circle>'
        b+=f'<circle cx="66" cy="58" r="27" fill="{BG}" stroke="url(#a)" stroke-width="2.4" filter="url(#glow)"/>'
        b+=f'<path d="M55 58 l8 8 l15 -17" fill="none" stroke="{CY}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        b+=t(124,38,f"CERTIFICATE  {i:02} / 04",10,CY,weight="800",ls=3)
        b+=t(124,64,title,16,TXT,weight="800")
        b+=t(124,84,detail,12,MUT,font=SERIF,style="italic")
        b+=f'<rect x="124" y="104" width="176" height="28" rx="14" fill="url(#a)" filter="url(#glow)" class="pu"/>'
        b+=t(138,122,"VIEW CERTIFICATE",10,BG,weight="800",ls=1.5)
        b+=t(284,123,"↗",17,BG,weight="700",anchor="middle")
        b+=sheen(10,10,470,136,16,delay)
        wrap(f"cert-{i}",w,h,b,orbs=False)


# ---------- FOOTER ----------
def footer():
    w,h=1000,230; b=stars(w,h,22,2)
    for k,(yy,amp,op,dur,col) in enumerate([(160,18,.35,7,ACC),(178,14,.28,9,CY),(194,10,.4,11,"#1D4ED8")]):
        seg=" t125 0"*12
        b+=(f'<path d="M0 {yy} q62.5 -{amp} 125 0{seg} V{h} H0Z" fill="{col}" opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-250 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    b+=f'<text x="500" y="92" text-anchor="middle" font-family="{SERIF}" font-size="{TYPE_SCALE["display"]}" font-weight="700" font-style="italic" fill="url(#tx)" filter="url(#glow)">James Tamayo</text>'
    b+=t(500,128,"Building systems that can explain themselves.",16,LIGHT,anchor="middle",ls=1)
    b+=f'<rect class="bl" x="{500+len("Building systems that can explain themselves.")*4.8+8:.0f}" y="114" width="9" height="16" fill="{CY}"/>'
    wrap("footer-signature",w,h,b)

def readme_link_assets():
    actions=[
        ("button-case-study","Private case study"),
        ("button-live-site","Live Pomonote"),
        ("button-repository","View repository"),
        ("button-certificate","View certificate"),
    ]
    for name,label in actions:
        w=ceil(len(label)*7.2+48); h=40
        b=f'<rect x="1" y="1" width="{w-2}" height="38" rx="10" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".7"/>'
        b+=t(14,25,label,12,TXT,weight="600")
        x=w-25
        b+=f'<path d="M{x} 12h10v10 M{x+10} 12l-10 10" fill="none" stroke="{CY}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        wrap(name,w,h,b,orbs=False,corner_radius=10)

    account_icons={
        "github":'<path d="M7 7 6 3l4 2a8 8 0 0 1 4 0l4-2-1 4a8 8 0 0 1 2 5c0 4-2.5 6-7 6s-7-2-7-6a8 8 0 0 1 2-5z"/><path d="M9 18v2m6-2v2"/>',
        "facebook":'<path d="M13 20v-8h3l.5-3H13V7.5c0-1 .4-1.5 1.6-1.5H16V3.3c-.6-.1-1.5-.3-2.7-.3C10.7 3 9 4.7 9 7.7V9H6v3h3v8z"/>',
        "leetcode":'<path d="m8 6-5 6 5 6m8-12 5 6-5 6m-2-14-4 16"/>',
        "email":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    }
    accounts=[
        ("account-github","JamesTamayo-Imben","github"),
        ("account-facebook","James_Tamayo","facebook"),
        ("account-leetcode","James__Tamayo0604","leetcode"),
        ("account-email","jamesttamayo0604@gmail.com","email"),
    ]
    for name,label,kind in accounts:
        w,h=360,40
        b=f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".7"/>'
        b+=(f'<g transform="translate(10 8)" fill="none" stroke="{CY}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{account_icons[kind]}</g>')
        b+=t(44,25,label,12,TXT)
        wrap(name,w,h,b,orbs=False,corner_radius=10)

    w,h=495,195
    b=f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
    b+=t(24,42,"GitHub at a glance",18,TXT,weight="600")
    b+=f'<line x1="24" y1="62" x2="471" y2="62" stroke="{LINE}"/>'
    b+=t(24,106,"4",30,LIGHT,weight="600")
    b+=t(66,106,"GitHub stars earned",14,TXT)
    b+=t(24,142,"Across my featured projects",13,MUT)
    wrap("github-summary",w,h,b,orbs=False)


def full_readme():
    ns="http://www.w3.org/2000/svg"
    xlink="http://www.w3.org/1999/xlink"
    ET.register_namespace("",ns)
    ET.register_namespace("xlink",xlink)
    q=lambda tag: f"{{{ns}}}{tag}"
    root=ET.Element(q("svg"),{
        "viewBox":"0 0 1000 0",
        "width":"1000",
        "height":"0",
        "role":"img",
        "aria-labelledby":"readme-title readme-description",
    })
    ET.SubElement(root,q("title"),{"id":"readme-title"}).text="James Tamayo — Developer portfolio"
    ET.SubElement(root,q("desc"),{"id":"readme-description"}).text=(
        "Full-stack developer and BS Information Systems student in Dasmariñas, Cavite. "
        "Portfolio featuring selected projects, skills, certifications, GitHub activity, and contact links."
    )
    style=ET.SubElement(root,q("style"))
    style.text=STYLE_CSS
    defs=ET.SubElement(root,q("defs"))
    content=ET.SubElement(root,q("g"))
    ET.SubElement(content,q("rect"),{"width":"1000","height":"1","fill":BG})

    y=0
    asset_index=0
    style_texts={STYLE_CSS}

    def embed(name,x,y,width=1000,href=None):
        nonlocal asset_index
        path=f"assets/{name}.svg"
        source=ET.parse(path).getroot()
        vx,vy,vw,vh=map(float,source.attrib["viewBox"].split())
        scale=width/vw
        height=vh*scale
        asset_index+=1
        prefix=f"asset{asset_index}_"
        id_map={node.attrib["id"]:prefix+node.attrib["id"] for node in source.iter() if "id" in node.attrib}

        def rewrite(value):
            value=re.sub(r"url\(#([^)]+)\)",lambda m:f"url(#{id_map.get(m.group(1),m.group(1))})",value)
            if value.startswith("#") and value[1:] in id_map:
                value="#"+id_map[value[1:]]
            return value

        for node in source.iter():
            for key,value in list(node.attrib.items()):
                if key=="id":
                    node.set(key,id_map[value])
                else:
                    node.set(key,rewrite(value))
            if node.tag==q("style") and node.text:
                style_texts.add(rewrite(node.text))

        transform=f"translate({x-vx*scale:g} {y-vy*scale:g}) scale({scale:g})"
        holder=ET.SubElement(content,q("a"),{"href":href}) if href else content
        group=ET.SubElement(holder,q("g"),{"transform":transform})
        for child in list(source):
            if child.tag==q("style"):
                continue
            if child.tag==q("defs"):
                defs.extend(list(child))
            else:
                group.append(child)
        return ceil(height)

    def section(name):
        nonlocal y
        y+=24
        y+=embed(f"title-{name}",0,y)
        y+=16

    def text_line(parent,x,y,value,size=14,fill=TXT,weight="400",anchor="start"):
        ET.SubElement(parent,q("text"),{
            "x":str(x),"y":str(y),"font-family":MONO,"font-size":str(size),
            "fill":fill,"font-weight":weight,"text-anchor":anchor,
        }).text=value

    def account_icon(parent,x,y,kind):
        paths={
            "github":'<path d="M7 7 6 3l4 2a8 8 0 0 1 4 0l4-2-1 4a8 8 0 0 1 2 5c0 4-2.5 6-7 6s-7-2-7-6a8 8 0 0 1 2-5z"/><path d="M9 18v2m6-2v2"/>',
            "facebook":'<path d="M13 20v-8h3l.5-3H13V7.5c0-1 .4-1.5 1.6-1.5H16V3.3c-.6-.1-1.5-.3-2.7-.3C10.7 3 9 4.7 9 7.7V9H6v3h3v8z"/>',
            "leetcode":'<path d="m8 6-5 6 5 6m8-12 5 6-5 6m-2-14-4 16"/>',
            "email":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
        }
        icon=ET.SubElement(parent,q("g"),{
            "transform":f"translate({x} {y})",
            "fill":"none","stroke":CY,"stroke-width":"1.5",
            "stroke-linecap":"round","stroke-linejoin":"round",
        })
        icon.append(ET.fromstring(f'<g xmlns="{ns}">{paths[kind]}</g>'))

    def badge(x,y,width,label,href=None,icon=None):
        if width is None:
            width=ceil(len(label)*12*0.6+32)
        holder=ET.SubElement(content,q("a"),{"href":href}) if href else content
        group=ET.SubElement(holder,q("g"))
        ET.SubElement(group,q("rect"),{
            "x":str(x),"y":str(y),"width":str(width),"height":"32","rx":"8",
            "fill":PANEL,"stroke":ACC,"stroke-opacity":".65",
        })
        if icon:
            account_icon(group,x+14,y+8,icon)
            text_line(group,x+42,y+21,label,12,TXT)
        else:
            text_line(group,x+width/2,y+21,label,12,TXT,anchor="middle")
        return width

    y+=embed("james-hero-banner",0,y)

    section("about")
    y+=embed("about-copy",0,y)
    y+=16
    y+=embed("ascii-portrait",0,y)

    section("recognition")
    y+=embed("achievements",0,y)

    section("work")
    project_links=[
        None,
        "https://github.com/JamesTamayo-Imben/pomonote",
        "https://github.com/JamesTamayo-Imben/Batify",
        "https://github.com/JamesTamayo-Imben/folio-os",
        "https://github.com/JamesTamayo-Imben/Tagthr22",
    ]
    for i,href in enumerate(project_links,1):
        y+=embed(f"project-{i}",0,y,href=href)
        y+=12
        if i==1:
            badge(34,y,None,"Private case study","https://github.com/JamesTamayo-Imben")
        elif i==2:
            live_width=badge(34,y,None,"Live Pomonote","https://jamestamayo-imben.github.io/pomonote/")
            badge(34+live_width+12,y,None,"Pomonote repository",project_links[i-1])
        else:
            project_names={3:"Batify",4:"FolioOS",5:"Tagthr22"}
            badge(34,y,None,f"{project_names[i]} repository",href)
        y+=44

    section("toolkit")
    y+=embed("toolkit",0,y)

    section("commits")
    y+=embed("readme-snake",0,y)
    y+=16
    activity_y=y
    streak_height=embed("readme-streak",0,activity_y,495)
    summary_height=embed("github-summary",505,activity_y,495)
    y=activity_y+max(streak_height,summary_height)

    section("certifications")
    certificate_links=[
        "https://drive.google.com/file/d/1rm0vM_M6UXmaVhQ5w7uSMMP9n35cL7JJ/view?usp=drive_link",
        "https://drive.google.com/file/d/14iAMh-NrXXQ3_TS15LdLmEnbz_9R8KCS/view?usp=sharing",
        "https://drive.google.com/file/d/14lQeYoOjECjDDWqUz4OuEDYWL66cR0go/view?usp=sharing",
        "https://drive.google.com/file/d/1abepLXUSFUCco-Y-RyXOihvMdXzwyzvr/view?usp=sharing",
    ]
    cert_y=y
    for i,href in enumerate(certificate_links):
        col=i%2; row=i//2
        embed(f"cert-{i+1}",col*510,cert_y+row*176,490,href)
    y=cert_y+((len(certificate_links)+1)//2)*176

    section("connect")
    contact_links=[
        ("JamesTamayo-Imben","https://github.com/JamesTamayo-Imben","github"),
        ("James_Tamayo","https://www.facebook.com/jam.es.968621","facebook"),
        ("James__Tamayo0604","https://leetcode.com/u/James_Tamayo0604/","leetcode"),
        ("jamesttamayo0604@gmail.com","mailto:jamesttamayo0604@gmail.com","email"),
    ]
    for i,(label,href,icon) in enumerate(contact_links):
        x=34+(i%2)*482
        yy=y+(i//2)*48
        badge(x,yy,450,label,href,icon)
    y+=96
    y+=embed("footer-signature",0,y,href="https://github.com/JamesTamayo-Imben")
    y+=24

    style.text="\n".join(sorted(style_texts))
    root.set("viewBox",f"0 0 1000 {y}")
    root.set("height",str(y))
    content[0].set("height",str(y))
    ET.ElementTree(root).write("assets/full-readme.svg",encoding="utf-8",xml_declaration=True)

if __name__ == "__main__":
    hero(); about_copy(); portrait(); titles(); achievements(); projects(); toolkit(); certs(); certificate_cards(); footer()
    readme_link_assets(); full_readme()

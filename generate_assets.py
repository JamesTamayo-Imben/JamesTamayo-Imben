import random
from html import escape as e
BG="#040A1C"; PANEL="#0A1633"; LINE="#16295A"; ACC="#3B82F6"; LIGHT="#93C5FD"; CY="#22D3EE"; TXT="#E6EEFF"; MUT="#8FA3C7"
MONO="'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SERIF="Georgia,'Palatino Linotype','Times New Roman',serif"
_id=[0]
def uid(): _id[0]+=1; return f"u{_id[0]}"

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

def wrap(name,w,h,body,orbs=True,big=False):
    o=''
    if orbs:
        o=(f'<circle cx="{w*0.15}" cy="{h*0.2}" r="{h*0.55 if big else h*0.7}" fill="#2563EB" opacity="{.38 if big else .16}" filter="url(#blur)">'
           f'<animate attributeName="cx" values="{w*0.15};{w*0.28};{w*0.15}" dur="12s" repeatCount="indefinite"/></circle>'
           f'<circle cx="{w*0.88}" cy="{h*0.9}" r="{h*0.5 if big else h*0.6}" fill="{CY}" opacity="{.22 if big else .08}" filter="url(#blur)">'
           f'<animate attributeName="cy" values="{h*0.9};{h*0.7};{h*0.9}" dur="10s" repeatCount="indefinite"/></circle>')
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
<clipPath id="rc"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#rc)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>{o}<rect width="{w}" height="{h}" fill="url(#grid)"/>
{body}
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>'''
    open(f"assets/{name}.svg","w").write(s)

def t(x,y,s,size=16,fill=TXT,font=MONO,weight="400",style="normal",anchor="start",ls=0,extra=""):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{e(s)}</text>\n'

def ft(x,y,s,delay=0,**k):
    return t(x,y,s,extra=f'class="f" style="animation-delay:{delay}s"',**k)

def typed(x,y,s,size,fill,begin,weight="400"):
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
    w,h=1000,440; b=stars(w,h,34,7)
    for i,c in enumerate(["#1E3A8A",ACC,CY]): b+=f'<circle cx="{40+i*22}" cy="38" r="6" fill="{c}"/>'
    b+=typed(40,104,"> npm run build --intelligence",16,CY,0.3)
    b+=f'<text x="40" y="184" font-family="{MONO}" font-size="66" font-weight="800" fill="url(#tx)" filter="url(#glow)" class="f" style="animation-delay:1.2s">JAMES TAMAYO</text>'
    b+=f'<rect x="42" y="204" width="0" height="4" rx="2" fill="url(#a)"><animate attributeName="width" from="0" to="280" begin="1.6s" dur="1s" fill="freeze"/></rect>'
    b+=ft(40,254,"AI-Enabled Full-Stack Developer",1.8,size=25,fill=LIGHT,weight="600",ls=1)
    b+=ft(40,292,"I design in Figma. I build with AI-assisted code. I ship.",2.1,size=19,fill=MUT,font=SERIF,style="italic")
    x=40
    for i,c in enumerate(["AI-assisted","React","Laravel","Figma","Supabase","MySQL"]):
        p,pw=pill(x,322,c,13,2.4+i*0.15); b+=p; x+=pw+10
    b+=f'<circle class="pu" cx="48" cy="404" r="5" fill="{CY}"/>'+ft(62,409,"BSIS student  ·  Dasmariñas, Cavite, PH",2.9,size=13,fill=MUT)
    # neural net
    layers=[(690,3),(775,5),(860,5),(945,3)]; pts=[]
    for lx,n in layers: pts.append([(lx,220+(k-(n-1)/2)*54) for k in range(n)])
    r=random.Random(3); k=0
    for a,bb in zip(pts,pts[1:]):
        for p in a:
            for q in bb:
                k+=1
                if k%3==0: b+=f'<line class="fl" x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{CY}" stroke-opacity=".7" style="animation-delay:{r.random():.2f}s"/>'
                else: b+=f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{ACC}" stroke-opacity=".22"/>'
    for L in pts:
        for p in L:
            b+=f'<circle class="pu" cx="{p[0]}" cy="{p[1]}" r="8" fill="{PANEL}" stroke="{CY}" stroke-width="2" style="animation-delay:{r.random()*2:.2f}s" filter="url(#glow)"/>'
    b+=t(690,372,"INPUT",11,MUT,ls=3,anchor="middle")+t(945,372,"OUTPUT",11,MUT,ls=3,anchor="middle")+t(817,372,"HIDDEN LAYERS",11,MUT,ls=3,anchor="middle")
    b+=f'<rect x="0" y="{h-4}" width="{w}" height="4" fill="url(#a)" opacity=".8"/>'
    wrap("james-hero-banner",w,h,b,big=True)


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
    b+=ft(X+26,134,"AI-Enabled Full-Stack Developer",1.0,size=15,fill=LIGHT,weight="600")
    b+=f'<rect x="{X+26}" y="148" width="0" height="3" rx="1.5" fill="url(#a)"><animate attributeName="width" from="0" to="120" begin="1.2s" dur=".9s" fill="freeze"/></rect>'
    F=[("EDUCATION","BS in Information System"),("SCHOOL","Kolehiyo ng Lungsod ng Dasmariñas"),("YEARS","2023 to 2026 (Student)"),
       ("LOCATION","Dasmariñas, Cavite, PH"),("BUILDS WITH","React · Laravel · Supabase · Node.js"),("DESIGNS IN","Figma  (UI / UX)")]
    for i,(k,v) in enumerate(F):
        y=190+i*44
        b+=ft(X+26,y,k,1.2+i*.12,size=11,fill=MUT,weight="700",ls=3)+ft(X+26,y+21,v,1.3+i*.12,size=14,fill=TXT)
    # design card
    b+=f'<g class="f" style="animation-delay:1.8s"><rect x="{X}" y="470" width="{Wd}" height="120" rx="16" fill="#06102A" stroke="{LINE}"/>'
    b+=f'<rect x="{X}" y="470" width="6" height="120" fill="url(#a)"/></g>'
    b+=ft(X+28,508,"DESIGN  ×  CODE",2.0,size=12,fill=CY,weight="800",ls=4)
    b+=ft(X+28,544,"Sketch it in Figma.",2.1,size=22,fill=TXT,font=SERIF,weight="700",style="italic")
    b+=ft(X+28,574,"Ship it in code.",2.2,size=22,fill=LIGHT,font=SERIF,weight="700",style="italic")
    # stat tiles
    for i,(v,l) in enumerate([("5","projects"),("4","certs"),("2026","grad year")]):
        x=X+i*140; y=610
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

# ---------- ABOUT ----------
def about():
    w,h=1000,420; b=stars(w,h,18,11)
    b+=f'<rect x="30" y="24" width="640" height="372" rx="14" fill="#06102A" stroke="{LINE}"/><rect x="30" y="24" width="640" height="38" rx="14" fill="{PANEL}"/><rect x="30" y="48" width="640" height="14" fill="{PANEL}"/>'
    for i,c in enumerate(["#1E3A8A",ACC,CY]): b+=f'<circle cx="{54+i*20}" cy="43" r="5.5" fill="{c}"/>'
    b+=t(350,48,"~/james/about.sh",12,MUT,anchor="middle")
    L=[("$ whoami",1),("> James Tamayo, AI-enabled Full-Stack Developer",0),("$ cat education.md",1),("> BS in Information System, Kolehiyo ng Lungsod ng Dasmariñas",0),
       ("$ cat now.md",1),("> Student, 2023 to 2026  ·  Dasmariñas, Cavite, PH",0),("$ cat design.md",1),("> UI design in Figma, then built in React and Laravel",0),
       ("$ ls shipped/",1),("> step22  pomonote  batify  folio-os  tagthr22",0),("$ echo $FOCUS",1),("> full-stack web, local-first apps, AI-assisted dev",0)]
    for i,(s,c) in enumerate(L):
        b+=typed(54,98+i*24.5,s,14,CY if c else (TXT if i==1 else MUT),0.4+i*0.75,weight="700" if c else "400")
    b+=f'<rect class="bl" x="{54+len(L[-1][0])*8.4+4:.0f}" y="{98+(len(L)-1)*24.5-12:.0f}" width="9" height="16" fill="{CY}"/>'
    cx,cy=830,190
    b+=f'<circle cx="{cx}" cy="{cy}" r="104" fill="none" stroke="{ACC}" stroke-opacity=".6" stroke-dasharray="3 9"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="30s" repeatCount="indefinite"/></circle>'
    b+=f'<circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="{CY}" stroke-opacity=".5" stroke-dasharray="40 14"><animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="22s" repeatCount="indefinite"/></circle>'
    b+=f'<circle cx="{cx}" cy="{cy}" r="68" fill="{PANEL}" stroke="url(#a)" stroke-width="2" filter="url(#glow)"/>'
    b+=f'<text x="{cx}" y="{cy+19}" text-anchor="middle" font-family="{MONO}" font-size="54" font-weight="800" fill="url(#tx)">JT</text>'
    b+=t(cx,cy+142,"AI  ×  FULL-STACK",13,LIGHT,weight="700",anchor="middle",ls=3)+t(cx,cy+164,"[Your City, Country]",12,MUT,anchor="middle")
    wrap("about-intro",w,h,b)

# ---------- ACHIEVEMENTS ----------
def achievements():
    A=[("5","Featured projects","★",100),("6","User roles in STEP22","◆",100),("SHA-256","Tamper-evident ledger","▲",100),
       ("4","Online certifications","●",100),("0","Accounts needed: Pomonote, Batify","■",100),("4","GitHub stars earned","✦",100)]
    b=stars(1000,340,16,5)
    for i,(v,l,ic,p) in enumerate(A):
        x=30+(i%3)*320; y=30+(i//3)*150; d=0.15*i
        b+=f'<g class="f" style="animation-delay:{d}s"><rect x="{x}" y="{y}" width="300" height="130" rx="14" fill="{PANEL}" stroke="{ACC}" stroke-opacity=".45"/>'
        b+=f'<circle cx="{x+40}" cy="{y+42}" r="20" fill="none" stroke="{CY}" stroke-opacity=".7" class="pu" style="animation-delay:{d}s"/>'+t(x+40,y+50,ic,18,CY,anchor="middle")
        b+=t(x+76,y+50,v,28,LIGHT,weight="800")+t(x+24,y+90,l,15,MUT,SERIF,style="italic")
        b+=f'<rect x="{x+24}" y="{y+106}" width="252" height="5" rx="2.5" fill="#0D1F4D"/><rect x="{x+24}" y="{y+106}" width="0" height="5" rx="2.5" fill="url(#a)"><animate attributeName="width" from="0" to="{252*p/100:.0f}" begin="{1+d}s" dur="1.2s" fill="freeze"/></rect></g>'
        b+=sheen(x,y,300,130,14,d+1)
    wrap("achievements",1000,340,b)

# ---------- PROJECTS ----------
def projects():
    P=[("01","STEP22: School Transparency Portal","Role-based governance and a tamper-evident financial ledger for KLD.",[("6","user roles"),("SHA-256","ledger chain"),("2-layer","access control")],["Laravel 12","React 18","Inertia.js","MySQL","Supabase Auth"],["Role-scoped UI","Laravel + RBAC","SHA-256 ledger"]),
       ("02","Pomonote: Focus Timer + Tasks","Keyboard-first, local-first focus timer + tasks + notes. No account.",[("0","accounts needed"),("0","dependencies"),("MIT","licensed")],["JavaScript","Local-first","Keyboard-first"],["Timer","Tasks","Notes"]),
       ("03","Batify: Letters, Wishes & Gifts","Birthday letters, wishes and gifts in one link. No signup.",[("1","link to share"),("0","signups"),("3","Supabase services")],["React","Supabase","Postgres","Edge Functions"],["React SPA","Edge Functions","Postgres+Storage"]),
       ("04","folio-os","[One-line description of folio-os]",[("TypeScript","built with"),("1","GitHub star"),("Public","repository")],["TypeScript","[Add stack]"],["[Step 1]","[Step 2]","[Step 3]"]),
       ("05","Tagthr22","[One-line description of Tagthr22]",[("TypeScript","built with"),("1","GitHub star"),("Public","repository")],["TypeScript","[Add stack]"],["[Step 1]","[Step 2]","[Step 3]"])]
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
def toolkit():
    T=[("LANGUAGES",["JavaScript","TypeScript","PHP","SQL","HTML / CSS"]),("AI-ENABLED",["AI-assisted dev","Prompt Eng.","LLM APIs"]),
       ("FRONTEND",["React","Inertia.js","Tailwind","Vite"]),("BACKEND",["Laravel","Node.js","Express","REST APIs"]),
       ("DATA / INFRA",["MySQL","PostgreSQL","SQLite","Supabase","GitHub Pages"]),("DESIGN / TOOLS",["Figma","UI Design","Git","GitHub","Composer"])]
    w,h=1000,470; b=stars(w,h,24,9)
    # constellation links
    for r in range(2):
        yy=125+r*210; b+=f'<line class="fl" x1="180" y1="{yy}" x2="820" y2="{yy}" stroke="{CY}" stroke-opacity=".35"/>'
    for c in range(3):
        xx=180+c*320; b+=f'<line class="fl" x1="{xx}" y1="125" x2="{xx}" y2="335" stroke="{CY}" stroke-opacity=".35"/>'
    for i,(cat,items) in enumerate(T):
        px=30+(i%3)*320; py=30+(i//3)*210; d=0.12*i
        b+=f'<g class="f" style="animation-delay:{d}s"><rect x="{px}" y="{py}" width="300" height="190" rx="16" fill="{PANEL}" fill-opacity=".92" stroke="{ACC}" stroke-opacity=".45"/>'
        b+=f'<circle class="pu" cx="{px+26}" cy="{py+30}" r="5" fill="{CY}" style="animation-delay:{d}s"/>'+t(px+42,py+35,cat,13,CY,weight="800",ls=3)
        b+=f'<line x1="{px+20}" y1="{py+52}" x2="{px+280}" y2="{py+52}" stroke="{LINE}"/></g>'
        x,y=px+20,py+68
        for j,it in enumerate(items):
            pw=len(it)*8.2+24
            if x+pw>px+285: x=px+20; y+=44
            p,_=pill(x,y,it,13,0.4+d+j*0.08); b+=p; x+=pw+8
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

# ---------- FOOTER ----------
def footer():
    w,h=1000,230; b=stars(w,h,22,2)
    for k,(yy,amp,op,dur,col) in enumerate([(160,18,.35,7,ACC),(178,14,.28,9,CY),(194,10,.4,11,"#1D4ED8")]):
        seg=" t125 0"*12
        b+=(f'<path d="M0 {yy} q62.5 -{amp} 125 0{seg} V{h} H0Z" fill="{col}" opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-250 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    b+=f'<text x="500" y="92" text-anchor="middle" font-family="{SERIF}" font-size="46" font-weight="700" font-style="italic" fill="url(#tx)" filter="url(#glow)">James Tamayo</text>'
    b+=t(500,128,"Building systems that can explain themselves.",16,LIGHT,anchor="middle",ls=1)
    b+=f'<rect class="bl" x="{500+len("Building systems that can explain themselves.")*4.8+8:.0f}" y="114" width="9" height="16" fill="{CY}"/>'
    wrap("footer-signature",w,h,b)

hero(); portrait(); titles(); about(); achievements(); projects(); toolkit(); certs(); footer()

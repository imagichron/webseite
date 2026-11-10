"""Zeichnet sechs fotoähnliche Illustrationen (SVG) für die Beispiel-Zeitreise „Anna & Paul“."""
import random
import sys
from pathlib import Path

ziel = Path(sys.argv[1])
ziel.mkdir(parents=True, exist_ok=True)
random.seed(7)
W, H = 1200, 900


def svg(name, body, defs=""):
    (ziel / (name + ".svg")).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{defs}'
        '<filter id="korn"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .10 0"/></filter>'
        '<radialGradient id="vign" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>'
        f'{body}<rect width="{W}" height="{H}" filter="url(#korn)"/><rect width="{W}" height="{H}" fill="url(#vign)"/></svg>',
        encoding="utf-8")


def farbe(*f):
    return random.choice(f)


# 1) Hochzeit: Kirche mit Zwiebelturm, Brautpaar, Konfetti
konf = "".join(
    f'<rect x="{random.randint(0, W)}" y="{random.randint(0, 620)}" width="10" height="16" rx="2" '
    f'fill="{farbe("#ff8fa3", "#ffd36e", "#8fd3ff", "#ffffff", "#c9a7ff")}" '
    f'transform="rotate({random.randint(0, 180)} {random.randint(0, W)} {random.randint(0, H)})" opacity=".9"/>'
    for _ in range(120))
svg("hochzeit", f'''
<rect width="1200" height="900" fill="url(#himmel)"/>
<path d="M0 640 Q300 600 600 630 T1200 620 V900 H0z" fill="#7fae6a"/>
<path d="M0 700 Q400 660 800 700 T1200 690 V900 H0z" fill="#6a9a58"/>
<g transform="translate(700 210)">
 <rect x="0" y="180" width="300" height="260" fill="#f4ede0"/><polygon points="-20,185 150,90 320,185" fill="#9c4a3a"/>
 <rect x="110" y="300" width="80" height="140" rx="40" fill="#6b4a3a"/>
 <rect x="230" y="60" width="90" height="380" fill="#f7f0e4"/>
 <ellipse cx="275" cy="40" rx="52" ry="58" fill="#3d6b4f"/><rect x="270" y="-40" width="10" height="40" fill="#3d6b4f"/><circle cx="275" cy="-46" r="9" fill="#d9b44a"/>
 <circle cx="275" cy="130" r="22" fill="#fff" stroke="#9a8f80" stroke-width="4"/><path d="M275 130 v-14 M275 130 h10" stroke="#555" stroke-width="3"/>
 <rect x="30" y="230" width="40" height="60" rx="20" fill="#7aa0c4"/><rect x="230" y="200" width="40" height="60" rx="20" fill="#7aa0c4"/>
</g>
<g transform="translate(330 470)">
 <circle cx="0" cy="0" r="34" fill="#e8c4a0"/><path d="M-36 -8 Q0 -60 36 -8 Q30 -40 0 -42 Q-30 -40 -36 -8z" fill="#6b3f2a"/>
 <path d="M-60 40 Q0 20 60 40 L110 300 H-110z" fill="#fffaf2"/><path d="M-40 -30 Q-80 60 -70 160 L-40 40z" fill="#fff" opacity=".7"/>
 <circle cx="40" cy="120" r="18" fill="#ff8fa3"/><circle cx="58" cy="132" r="12" fill="#ffd36e"/>
</g>
<g transform="translate(470 450)">
 <circle cx="0" cy="0" r="36" fill="#e2b892"/><path d="M-36 -6 Q0 -50 36 -6 Q20 -34 0 -34 Q-20 -34 -36 -6z" fill="#2f2a26"/>
 <path d="M-55 45 H55 L70 320 H-70z" fill="#2c3445"/><path d="M-12 45 L0 120 L12 45z" fill="#fff"/><path d="M-6 48 h12 l-6 10z" fill="#b2283a"/>
</g>
{konf}''', '<linearGradient id="himmel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ec5ec"/><stop offset="1" stop-color="#e6f2fa"/></linearGradient>')

# 2) Hochzeitstorte
svg("torte", '''
<rect width="1200" height="900" fill="url(#raum)"/>
<rect y="640" width="1200" height="260" fill="#efe3cf"/><rect y="640" width="1200" height="14" fill="#e2d2b8"/>
<g transform="translate(600 0)">
 <ellipse cx="0" cy="650" rx="330" ry="40" fill="#d8cbb4"/>
 <rect x="-260" y="470" width="520" height="170" rx="18" fill="#fff8ee"/><rect x="-200" y="330" width="400" height="150" rx="16" fill="#fffaf3"/><rect x="-140" y="210" width="280" height="130" rx="14" fill="#fffdf8"/>
 <path d="M-260 520 q26 30 52 0 t52 0 t52 0 t52 0 t52 0 t52 0 t52 0 t52 0 t52 0 t52 0" stroke="#f0d9c0" stroke-width="10" fill="none"/>
 <path d="M-200 380 q25 26 50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0" stroke="#f0d9c0" stroke-width="9" fill="none"/>
 <circle cx="-120" cy="470" r="22" fill="#f4a6b4"/><circle cx="-90" cy="480" r="16" fill="#ffc9d2"/><circle cx="130" cy="330" r="20" fill="#f4a6b4"/><circle cx="104" cy="338" r="14" fill="#ffc9d2"/><circle cx="-60" cy="210" r="18" fill="#f4a6b4"/>
 <path d="M-20 210 v-70 M20 210 v-70" stroke="#c9a24a" stroke-width="6"/><circle cx="-20" cy="128" r="16" fill="#e8c4a0"/><circle cx="20" cy="128" r="16" fill="#e2b892"/>
 <path d="M-34 150 h28 l6 60 h-40z" fill="#fff"/><path d="M6 150 h28 l4 60 h-36z" fill="#2c3445"/>
</g>
<g opacity=".5"><circle cx="160" cy="180" r="70" fill="#ffd9a0"/><circle cx="1040" cy="150" r="90" fill="#ffd9a0"/></g>
<path d="M120 640 v-120 h40 v120" fill="#c9b79c"/><path d="M1020 640 c0 -80 70 -80 70 0" fill="#9cc48a"/>''',
    '<linearGradient id="raum" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7e7cf"/><stop offset="1" stop-color="#f2dcc0"/></linearGradient>')

# 3) Chiemsee bei Sonnenuntergang
reflex = "".join(
    f'<rect x="{560 + random.randint(-90, 90)}" y="{560 + i * 12}" width="{random.randint(40, 160)}" height="5" rx="2" '
    f'fill="#ffd7a0" opacity="{max(.1, .8 - i * .04):.2f}"/>' for i in range(24))
svg("see", f'''
<rect width="1200" height="560" fill="url(#abend)"/>
<circle cx="640" cy="470" r="70" fill="#fff1c9"/><circle cx="640" cy="470" r="140" fill="#ffe0a8" opacity=".35"/>
<path d="M0 500 L120 430 L220 470 L360 380 L470 450 L560 420 L700 470 L820 400 L960 460 L1080 410 L1200 450 V560 H0z" fill="#6a5a7a" opacity=".85"/>
<path d="M0 540 L180 500 L300 530 L480 490 L640 535 L820 495 L1000 530 L1200 500 V560 H0z" fill="#4c4462"/>
<rect y="560" width="1200" height="340" fill="url(#wasser)"/>{reflex}
<g transform="translate(330 610)"><path d="M0 60 h120 l-20 26 h-80z" fill="#2a2433"/><path d="M58 60 V-60 L120 50z" fill="#fff4e4"/><path d="M52 60 V-40 L0 50z" fill="#ffd7b5"/></g>
<path d="M0 860 Q200 820 420 900 H0z" fill="#3b3a2a"/><path d="M60 870 q10 -80 14 -120 M90 880 q4 -70 -6 -110" stroke="#3b3a2a" stroke-width="6" fill="none"/>''',
    '<linearGradient id="abend" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b4b8a"/><stop offset=".45" stop-color="#e88a6a"/><stop offset="1" stop-color="#ffcf8f"/></linearGradient>'
    '<linearGradient id="wasser" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d98a72"/><stop offset=".35" stop-color="#6b5a86"/><stop offset="1" stop-color="#2b2f4f"/></linearGradient>')

# 4) Alpen mit Almwiese
blumen = "".join(
    f'<circle cx="{random.randint(0, W)}" cy="{random.randint(700, 890)}" r="{random.randint(4, 8)}" '
    f'fill="{farbe("#fff", "#ffd36e", "#e86a8a", "#a98be8")}"/>' for _ in range(160))
baeume = "".join(f'<polygon points="{x},{y} {x - 26},{y + 80} {x + 26},{y + 80}"/>'
                 for x, y in [(90, 600), (140, 620), (1110, 590), (1150, 615)])
svg("berge", f'''
<rect width="1200" height="900" fill="url(#tag)"/>
<g fill="#fff" opacity=".85"><ellipse cx="220" cy="140" rx="90" ry="28"/><ellipse cx="280" cy="125" rx="60" ry="30"/><ellipse cx="900" cy="110" rx="110" ry="30"/></g>
<path d="M0 560 L180 300 L270 380 L420 180 L560 420 L700 250 L860 470 L1000 260 L1200 520 V900 H0z" fill="#7d8fa8"/>
<path d="M420 180 L470 260 L440 250 L410 290 L380 245 L360 260z M700 250 L740 310 L710 300 L690 330 L670 300z M1000 260 L1050 330 L1020 320 L995 350 L970 320z" fill="#fff"/>
<path d="M0 640 Q300 560 600 620 T1200 600 V900 H0z" fill="#8fbf6a"/>
<path d="M0 720 Q350 650 700 720 T1200 700 V900 H0z" fill="#7aad58"/>
<g transform="translate(820 560)"><rect x="0" y="40" width="170" height="100" fill="#a0693f"/><polygon points="-20,48 85,-10 190,48" fill="#5b3a26"/><rect x="30" y="70" width="34" height="30" fill="#f6e2b0"/><rect x="110" y="70" width="34" height="30" fill="#f6e2b0"/><rect x="0" y="100" width="170" height="10" fill="#e86a6a" opacity=".8"/></g>
<g fill="#3e6b3a">{baeume}</g>
{blumen}''', '<linearGradient id="tag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb3e8"/><stop offset="1" stop-color="#d8ecf8"/></linearGradient>')

# 5) Erstes gemeinsames Auto vor dem Haus
svg("auto", '''
<rect width="1200" height="900" fill="url(#mittag)"/>
<rect x="120" y="230" width="520" height="420" fill="#f2e6d0"/><polygon points="90,240 380,80 670,240" fill="#a5513f"/>
<rect x="190" y="320" width="110" height="110" fill="#bcd8ec" stroke="#fff" stroke-width="10"/><rect x="460" y="320" width="110" height="110" fill="#bcd8ec" stroke="#fff" stroke-width="10"/>
<rect x="330" y="470" width="100" height="180" fill="#7a5238"/><path d="M190 430 h110 v20 h-110z M460 430 h110 v20 h-110z" fill="#e86a6a"/>
<rect y="650" width="1200" height="250" fill="#9a9a94"/><rect y="640" width="1200" height="16" fill="#cfcac0"/>
<g transform="translate(620 520)">
 <path d="M0 150 Q10 90 80 80 L170 20 Q200 4 300 4 Q380 4 420 40 L480 85 Q540 95 545 150 Z" fill="#d94b3d"/>
 <path d="M185 30 Q205 18 290 18 L290 82 L120 82z" fill="#cfe4f2"/><path d="M305 18 Q370 18 405 46 L440 82 L305 82z" fill="#cfe4f2"/>
 <rect x="0" y="140" width="545" height="26" rx="10" fill="#5a5a5a"/>
 <circle cx="120" cy="168" r="48" fill="#262626"/><circle cx="120" cy="168" r="20" fill="#bbb"/><circle cx="440" cy="168" r="48" fill="#262626"/><circle cx="440" cy="168" r="20" fill="#bbb"/>
 <rect x="510" y="100" width="30" height="16" rx="4" fill="#fff3b0"/>
 <path d="M60 60 q40 -60 90 -30" stroke="#fff" stroke-width="6" fill="none" opacity=".6"/>
</g>
<g transform="translate(830 270)"><circle r="70" fill="#7aad58"/><circle cx="60" cy="30" r="60" fill="#6a9a4c"/><rect x="20" y="60" width="22" height="120" fill="#7a5238"/></g>''',
    '<linearGradient id="mittag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc8f0"/><stop offset="1" stop-color="#eaf5fb"/></linearGradient>')

# 6) Gartenfest mit Lampions am Abend
farben = ["#ffb36b", "#ff6a8a", "#ffd36e", "#8fd3ff", "#c9a7ff"] * 2
lamp = "".join(
    f'<g transform="translate({x} {130 + int(60 * ((x - 80) / 1040 - .5) ** 2 * 4)})"><line y1="-20" y2="0" stroke="#333" stroke-width="2"/>'
    f'<ellipse cy="26" rx="26" ry="30" fill="{c}"/><ellipse cy="26" rx="44" ry="48" fill="{c}" opacity=".25"/></g>'
    for x, c in zip(range(80, 1180, 110), farben))
gaeste = "".join(f'<g transform="translate({x} 440)"><circle r="34"/><path d="M-50 40 h100 l18 180 h-136z"/></g>' for x in (210, 1000))
funken = "".join(f'<circle cx="{random.randint(0, W)}" cy="{random.randint(250, 600)}" r="{farbe(2, 3, 4)}"/>' for _ in range(60))
svg("gartenfest", f'''
<rect width="1200" height="900" fill="url(#nacht)"/>
<path d="M0 130 Q600 260 1200 130" stroke="#222" stroke-width="3" fill="none"/>{lamp}
<rect y="620" width="1200" height="280" fill="#2f4a33"/>
<rect x="300" y="560" width="600" height="20" rx="6" fill="#8a5a3a"/><rect x="330" y="580" width="16" height="130" fill="#6a4228"/><rect x="854" y="580" width="16" height="130" fill="#6a4228"/>
<g fill="#fff8ee"><rect x="360" y="530" width="60" height="30" rx="6"/><circle cx="520" cy="540" r="22"/><rect x="600" y="520" width="20" height="40"/><rect x="760" y="530" width="70" height="30" rx="6"/></g>
<g fill="#1b2230">{gaeste}</g>
<g fill="#ffd36e" opacity=".9">{funken}</g>''',
    '<linearGradient id="nacht" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2140"/><stop offset=".7" stop-color="#3b3560"/><stop offset="1" stop-color="#5a4570"/></linearGradient>')
print("6 SVG gezeichnet in", ziel)

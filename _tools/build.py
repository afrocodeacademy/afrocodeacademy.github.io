#!/usr/bin/env python3
"""Generates the Afro Code Academy static pages (EN + DE).

Usage (from the repo root):  python3 _tools/build.py
Requires Pillow (pip install pillow) to read image sizes. Edit the content in this file,
re-run it, and commit the regenerated .html files together with this script.
"""
import html, os, sys
from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "images", "web")
YEAR = 2026
SITE = "https://afrocodeacademy.com"
EMAIL = "afrocodeacademy(at)gmail.com"
LOCATIONS = "Hamburg &amp; Göttingen"
# Legal notice (Impressum) details
LEGAL_NAME = "Abdul Qadir Ibrahim"
LEGAL_ADDRESS = ["c/o ARCA e.V.", "Bodenstedtstraße 16", "22765 Hamburg", "Deutschland"]
IG = "https://www.instagram.com/afrocodeacademy"
TW = "https://twitter.com/afrocodeacademy"

PAGES = {
    "home": ("index_en.html", "index.html"),
    "about": ("about.html", "about_de.html"),
    "curriculum": ("curriculum.html", "curriculum_de.html"),
    "gallery": ("gallery.html", "gallery_de.html"),
    "volunteer": ("volunteer.html", "volunteer_de.html"),
    "partners": ("partners.html", "partners_de.html"),
    "contact": ("contact.html", "contact_de.html"),
    "impressum": ("impressum.html", "impressum.html"),
}
L = {"en": 0, "de": 1}
NAV = ["home", "about", "curriculum", "gallery", "volunteer", "partners", "contact"]
NAV_LABEL = {
    "en": {"home": "Home", "about": "About", "curriculum": "Curriculum", "gallery": "Gallery",
           "volunteer": "Volunteer", "partners": "Partners", "contact": "Contact"},
    "de": {"home": "Start", "about": "Über uns", "curriculum": "Lehrplan", "gallery": "Galerie",
           "volunteer": "Mitmachen", "partners": "Partner", "contact": "Kontakt"},
}

def url(page, lang):
    return PAGES[page][L[lang]]

def abs_url(fname):
    return f"{SITE}/" if fname == "index.html" else f"{SITE}/{fname}"

# ---------- email registration ----------
MAIL = {
    "kids": {
        "en": ("Course registration: Kids & teens",
               "Hello Afro Code Academy team,\n\nI would like to register my child for a coding course.\n\n"
               "Child's name:\nAge:\nPreferred language (German / English):\nParent or guardian's name:\nPhone number:\n\nThank you!"),
        "de": ("Kursanmeldung: Kinder & Jugendliche",
               "Hallo Afro Code Academy Team,\n\nich möchte mein Kind für einen Programmierkurs anmelden.\n\n"
               "Name des Kindes:\nAlter:\nBevorzugte Sprache (Deutsch / Englisch):\nName des Elternteils:\nTelefonnummer:\n\nVielen Dank!"),
    },
    "robotics": {
        "en": ("Robotics workshop: please keep me updated",
               "Hello Afro Code Academy team,\n\nPlease let me know when registration for the robotics workshop for kids opens.\n\n"
               "Parent or guardian's name:\nChild's age:\nCity (Hamburg / Göttingen):\n\nThank you!"),
        "de": ("Robotik-Workshop: Bitte haltet mich auf dem Laufenden",
               "Hallo Afro Code Academy Team,\n\nbitte gebt mir Bescheid, sobald die Anmeldung für den Robotik-Workshop für Kinder startet.\n\n"
               "Name des Elternteils:\nAlter des Kindes:\nStadt (Hamburg / Göttingen):\n\nVielen Dank!"),
    },
    "adults": {
        "en": ("Course registration: Adults (18+)",
               "Hello Afro Code Academy team,\n\nI would like to register for the adult course.\n\n"
               "Name:\nTrack (Web Development / Data Analytics):\nPrevious programming experience:\n\nThank you!"),
        "de": ("Kursanmeldung: Erwachsene (18+)",
               "Hallo Afro Code Academy Team,\n\nich möchte mich für den Erwachsenenkurs anmelden.\n\n"
               "Name:\nTrack (Webentwicklung / Datenanalyse):\nBisherige Programmiererfahrung:\n\nVielen Dank!"),
    },
}

def mail_attrs(kind, lang, fallback="#register"):
    subject, body = MAIL[kind][lang]
    esc = lambda t: html.escape(t, quote=True).replace("\n", "&#10;")
    return f'href="{fallback}" data-mail="{EMAIL}" data-subject="{esc(subject)}" data-body="{esc(body)}"'

def dims(name):
    with Image.open(os.path.join(WEB, name)) as im:
        return im.size

def pic(name, alt, cls="", eager=False, sizes=None):
    w, h = dims(name)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="images/web/{name}" alt="{alt}" width="{w}" height="{h}" {load} decoding="async"{c}>'

def photo(n, size="sm"):
    return f"photo-{n}-{size}.webp"

# ---------- icons ----------
def svg(d, fill=False, sw="2"):
    if fill:
        return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{d}</svg>'
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

I = {
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "download": svg('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>'),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7l8 6 8-6"/>'),
    "insta": svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>'),
    "x": svg('<path d="M17.8 3h3.1l-6.8 7.8L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.3-8.3L2 3h6.4l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/>', fill=True),
    "pin": svg('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "calendar": svg('<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
    "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "gift": svg('<path d="M20 12v9H4v-9M2 7h20v5H2zM12 21V7M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7z"/>'),
    "globe": svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
    "laptop": svg('<rect x="4" y="5" width="16" height="11" rx="2"/><path d="M2 20h20"/>'),
    "lang": svg('<path d="M4 5h9M8.5 3v2M6 5c0 4 3 7 6 8M11 5c-1 4-4 7-7 8M13 21l4-9 4 9M14.5 18h5"/>'),
    "teach": svg('<path d="M3 5h18v11H3zM8 21l4-5 4 5M7 9h6M7 12h4"/>'),
    "heart": svg('<path d="M12 20s-7-4.4-9-8.6C1.6 8.3 3.6 5 6.9 5c2 0 3.4 1.1 5.1 3 1.7-1.9 3.1-3 5.1-3 3.3 0 5.3 3.3 3.9 6.4C19 15.6 12 20 12 20z"/>'),
    "admin": svg('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
    "blocks": svg('<rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/><rect x="8" y="3" width="8" height="8" rx="1.5"/>'),
    "gamepad": svg('<path d="M6.5 7h11A4.5 4.5 0 0 1 22 11.5v1a4.5 4.5 0 0 1-8 2.8l-.3-.3h-3.4l-.3.3a4.5 4.5 0 0 1-8-2.8v-1A4.5 4.5 0 0 1 6.5 7z"/><path d="M7 10v4M5 12h4M15.5 11h.01M18 13h.01"/>'),
    "terminal": svg('<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M7 9l3 3-3 3M12.5 15H17"/>'),
    "chart": svg('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M7 12l3-3 2 2 4-4M8 20h8M12 16v4"/>'),
    "zoom": svg('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/>'),
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": svg('<path d="M6 6l12 12M18 6L6 18"/>'),
    "ext": svg('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
}
I["menu"] = I["menu"].replace("<svg ", '<svg class="i-menu" ')
I["close"] = I["close"].replace("<svg ", '<svg class="i-close" ')

# ---------- gallery data ----------
GALLERY = [
    ("4", "Hands-on help during a Saturday coding class", "Praktische Hilfe im Programmierkurs am Samstag"),
    ("23", "Group photo with students and volunteers", "Gruppenfoto mit Schülern und Freiwilligen"),
    ("13", "Two young learners exploring a coding app on a tablet", "Zwei junge Lernende entdecken eine Programmier-App auf dem Tablet"),
    ("3", "A mentor guides a student through an exercise", "Ein Mentor begleitet einen Schüler bei einer Übung"),
    ("11", "Celebrating at the end of class", "Freude am Ende des Kurses"),
    ("22", "Showing off a game built in Scratch", "Ein selbst gebautes Scratch-Spiel wird präsentiert"),
    ("1", "A volunteer teaching in front of the class", "Ein Freiwilliger unterrichtet vor der Klasse"),
    ("0340", "Girls getting started at their laptops", "Mädchen starten an ihren Laptops"),
    ("12", "Our team and students outside the workshop", "Unser Team und Schüler vor dem Workshop"),
    ("2", "Volunteers helping children at their laptops", "Freiwillige helfen Kindern an ihren Laptops"),
    ("21", "Students and volunteers gathered around a project", "Schüler und Freiwillige rund um ein Projekt"),
    ("0335", "Young learners with laptops and tablets", "Junge Lernende mit Laptops und Tablets"),
    ("7", "Children coding together in a bright classroom", "Kinder programmieren gemeinsam in einem hellen Klassenraum"),
    ("16", "One-on-one support from a volunteer", "Individuelle Unterstützung durch einen Freiwilligen"),
    ("19", "Building a game on a tablet", "Ein Spiel auf dem Tablet bauen"),
    ("5", "Students and volunteers after a workshop", "Schüler und Freiwillige nach einem Workshop"),
    ("15", "A full classroom of young coders", "Ein voller Klassenraum junger Programmierer"),
    ("8", "Volunteers supporting young coders", "Freiwillige unterstützen junge Programmierer"),
    ("17", "The workshop room during class", "Der Workshop-Raum während des Kurses"),
    ("10", "Students focused on their projects", "Schüler konzentriert bei ihren Projekten"),
    ("9", "Working through a coding challenge as a team", "Gemeinsam eine Programmieraufgabe lösen"),
    ("18", "A small-group session", "Eine Sitzung in kleiner Gruppe"),
    ("14", "Mentors helping students at their laptops", "Mentoren helfen Schülern an den Laptops"),
    ("24", "Coding in the break room", "Programmieren im Aufenthaltsraum"),
]
ALT = {n: (en, de) for n, en, de in GALLERY}

def alt(n, lang):
    return ALT[n][L[lang]]

def gallery_link(n, lang, figure=True):
    cap = alt(n, lang)
    fig = f'<span class="cap" aria-hidden="true">{cap}</span>' if figure else ""
    return (f'<a href="images/web/{photo(n, "lg")}" data-lightbox data-caption="{cap}">'
            f'{pic(photo(n), cap)}<span class="zoom-icon">{I["zoom"]}</span>{fig}</a>')

# ---------- layout ----------
FONTS = ('<link rel="preload" href="fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>'
         '<link rel="preload" href="fonts/plus-jakarta-sans-latin.woff2" as="font" type="font/woff2" crossorigin>'
         '<link rel="stylesheet" href="fonts/fonts.css">')

UI = {
    "en": {"skip": "Skip to content", "register": "Register", "menu": "Open menu",
           "tagline": "Free coding classes that help children from underprivileged groups, especially those with migration backgrounds, succeed in the digital world.",
           "explore": "Explore", "contact": "Get in touch", "follow": "Follow us", "rights": "All rights reserved.",
           "made": "Run entirely by volunteers.", "impressum": "Legal notice (Impressum)"},
    "de": {"skip": "Zum Inhalt springen", "register": "Anmelden", "menu": "Menü öffnen",
           "tagline": "Kostenlose Programmierkurse, die Kindern aus unterprivilegierten Gruppen, insbesondere mit Migrationshintergrund, den Weg in die digitale Welt ebnen.",
           "explore": "Entdecken", "contact": "Kontakt", "follow": "Folge uns", "rights": "Alle Rechte vorbehalten.",
           "made": "Ausschließlich von Freiwilligen getragen.", "impressum": "Impressum"},
}

def brand(href):
    return (f'<a class="brand" href="{href}"><span class="brand-mark" aria-hidden="true">&lt;/&gt;</span>'
            f'<span class="brand-text">Afro Code<small>Academy</small></span></a>')

def header(page, lang):
    u = UI[lang]
    other = "de" if lang == "en" else "en"
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{url(p, lang)}"{cur if p == page else ""}>{NAV_LABEL[lang][p]}</a></li>'
        for p in NAV)
    counterpart = url(page, other)
    if lang == "en":
        lang_sw = f'<span>EN</span><a href="{counterpart}" hreflang="de" lang="de" aria-label="Deutsch">DE</a>'
    else:
        lang_sw = f'<a href="{counterpart}" hreflang="en" lang="en" aria-label="English">EN</a><span>DE</span>'
    reg = url("curriculum", lang) + "#register"
    return f'''<a class="skip" href="#main">{u["skip"]}</a>
<div class="kente" aria-hidden="true"></div>
<header class="site-header">
  <div class="container header-inner">
    {brand(url("home", lang))}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{u["menu"]}">{I["menu"]}{I["close"]}</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav-links">{links}</ul>
      <div class="nav-actions">
        <div class="lang" role="group" aria-label="Language">{lang_sw}</div>
        <a class="btn btn--primary" href="{reg}">{u["register"]}</a>
      </div>
    </nav>
  </div>
</header>'''

def footer(lang):
    u = UI[lang]
    col1 = "".join(f'<li><a href="{url(p, lang)}">{NAV_LABEL[lang][p]}</a></li>' for p in NAV[:4])
    col2 = "".join(f'<li><a href="{url(p, lang)}">{NAV_LABEL[lang][p]}</a></li>' for p in NAV[4:])
    col2 += f'<li><a href="{url("curriculum", lang)}#register">{u["register"]}</a></li>'
    return f'''<footer class="site-footer">
  <div class="kente" aria-hidden="true"></div>
  <div class="container">
    <div class="footer-grid">
      <div>{brand(url("home", lang))}<p class="footer-about">{u["tagline"]}</p></div>
      <div><h4>{u["explore"]}</h4><ul>{col1}</ul></div>
      <div><h4>{u["contact"]}</h4><ul>{col2}</ul></div>
      <div><h4>{u["follow"]}</h4>
        <div class="socials">
          <a href="{IG}" aria-label="Instagram" rel="noopener">{I["insta"]}</a>
          <a href="{TW}" aria-label="X (Twitter)" rel="noopener">{I["x"]}</a>
          <a href="#" data-mail="{EMAIL}" aria-label="Email">{I["mail"]}</a>
        </div>
        <p style="margin-top:16px;font-size:.92rem">{EMAIL}</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {YEAR} Afro Code Academy. {u["rights"]} {u["made"]}</span>
      <a href="impressum.html">{u["impressum"]}</a>
    </div>
  </div>
</footer>'''

def layout(page, lang, title, desc, body, og_img="og-image.jpg", extra_head=""):
    en, de = PAGES[page]
    alt_links = (f'<link rel="alternate" hreflang="en" href="{abs_url(en)}">'
                 f'<link rel="alternate" hreflang="de" href="{abs_url(de)}">'
                 f'<link rel="alternate" hreflang="x-default" href="{abs_url(de)}">')
    canon = abs_url(PAGES[page][L[lang]])
    full_title = f"{title} · Afro Code Academy" if page != "home" else f"Afro Code Academy · {title}"
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  {alt_links}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Afro Code Academy">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE}/images/web/{og_img}">
  <meta property="og:url" content="{canon}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#fbf6ee">
  <link rel="icon" href="images/web/favicon.svg" type="image/svg+xml">
  {FONTS}
  <link rel="stylesheet" href="css/site.css">
  {extra_head}
</head>
<body>
{header(page, lang)}
<main id="main">
{body}
</main>
{footer(lang)}
<script src="js/site.js" defer></script>
</body>
</html>
'''

def page_hero(eyebrow, title, lead, img=None, img_alt=""):
    if img:
        return f'''<section class="page-hero">
  {pic(img, img_alt, eager=True)}
  <div class="container"><span class="eyebrow">{eyebrow}</span><h1>{title}</h1><p class="lead">{lead}</p></div>
</section>'''
    return f'''<section class="page-hero page-hero--plain">
  <div class="container"><span class="eyebrow">{eyebrow}</span><h1>{title}</h1><p class="lead">{lead}</p></div>
</section>'''

# ---------- shared content ----------
COURSES = {
    "en": [
        ("4–7", "Little explorers", "Logic & sequence",
         "Our main focus in this age group is teaching logic and sequence through games, robots, apps, and simple coding challenges.",
         ["Games", "Robots", "Apps", "ScratchJr"]),
        ("7–12", "Young makers", "Programming concepts",
         "We transition students to programming concepts like conditionals, Booleans, variables, loops, and functions: making games and animations in Scratch, text-based games in Python, graphics-based games using Pygame, Arduino, and Minecraft playing and modding.",
         ["Scratch", "Python", "Pygame", "Arduino", "Minecraft"]),
        ("13–18", "Teen developers", "Advanced platforms",
         "As they become teenagers, students develop more maturity and are usually ready to move on to more advanced learning platforms.",
         ["Python", "Arduino (C)", "Raspberry Pi", "GameMaker Studio", "Minecraft modding", "HTML / CSS / JS"]),
        ("18+", "Adults", "Complete beginners",
         "A comprehensive curriculum for complete beginners, with two tracks: build your very own website from scratch, or dive into data analytics with Python.",
         ["Web development", "Data analytics", "Online"]),
    ],
    "de": [
        ("4–7", "Kleine Entdecker", "Logik & Abläufe",
         "Unser Hauptaugenmerk in dieser Altersgruppe liegt auf der Vermittlung von Logik und Abläufen durch Spiele, Roboter, Apps und einfache Programmieraufgaben.",
         ["Spiele", "Roboter", "Apps", "ScratchJr"]),
        ("7–12", "Junge Macher", "Programmierkonzepte",
         "Wir führen die Kinder an Programmierkonzepte wie Bedingungen, Boolesche Werte, Variablen, Schleifen und Funktionen heran: Spiele und Animationen in Scratch, textbasierte Spiele in Python, grafische Spiele mit Pygame, Arduino sowie Minecraft spielen und modden.",
         ["Scratch", "Python", "Pygame", "Arduino", "Minecraft"]),
        ("13–18", "Teen-Entwickler", "Fortgeschrittene Plattformen",
         "Als Teenager entwickeln die Schüler mehr Reife und sind in der Regel bereit, sich fortgeschritteneren Lernplattformen zuzuwenden – spielerisch und verständlich vermittelt.",
         ["Python", "Arduino (C)", "Raspberry Pi", "GameMaker Studio", "Minecraft-Modding", "HTML / CSS / JS"]),
        ("18+", "Erwachsene", "Absolute Anfänger",
         "Ein umfassender Lehrplan für absolute Programmieranfänger mit zwei Tracks: Baue deine eigene Website von Grund auf oder tauche mit Python in die Datenanalyse ein.",
         ["Webentwicklung", "Datenanalyse", "Online"]),
    ],
}

COURSE_ICONS = ["blocks", "gamepad", "terminal", "chart"]
COURSE_SHORT = {
    "en": ["Logic and sequence through games, robots, apps and simple coding challenges.",
           "Conditionals, loops, variables and functions, learned by building games and animations.",
           "Real tools and platforms: Python, Arduino, Raspberry Pi, game making and web development.",
           "Two online beginner tracks: build your own website, or analyse data with Python."],
    "de": ["Logik und Abläufe mit Spielen, Robotern, Apps und einfachen Programmieraufgaben.",
           "Bedingungen, Schleifen, Variablen und Funktionen – beim Bauen von Spielen und Animationen.",
           "Echte Werkzeuge: Python, Arduino, Raspberry Pi, Spieleentwicklung und Webentwicklung.",
           "Zwei Online-Einsteiger-Tracks: eigene Website bauen oder Daten mit Python analysieren."],
}

def course_cards(lang, short=False):
    out = []
    for i, ((age, label, title, text, tags), ic) in enumerate(zip(COURSES[lang], COURSE_ICONS)):
        if short:
            text, tags = COURSE_SHORT[lang][i], tags[:4]
        t = "".join(f"<span>{x}</span>" for x in tags)
        out.append(f'''<article class="course reveal"><div class="course-icon">{I[ic]}</div><div>
<div class="course-top"><span class="course-age">{age}</span><span class="course-label">{label}</span></div>
<h3>{title}</h3><p>{text}</p><div class="tags">{t}</div></div></article>''')
    return '<div class="courses">' + "".join(out) + "</div>"

PARTNERS = [
    ("plea", "https://www.plea-ev.de/", "PLEA e.V.", "Göttingen",
     "P.L.E.A. e.V. is a non-profit, non-denominational association from Göttingen that does not belong to any political party. It was founded in 2007 by African diaspora academics and former development workers. Their approach is to work together and on an equal footing with partners in Africa to develop solution strategies for existing development problems. In cooperation with motivated development agencies in Africa, they promote incomplete and neglected development dynamics, so their support covers all areas of life for which it is requested or needed.",
     "P.L.E.A. e.V. ist ein gemeinnütziger, überkonfessioneller und zu keiner politischen Partei gehörender Verein aus Göttingen, der 2007 von afrikanischen Diaspora-Akademikern und ehemaligen Entwicklungshelfern gegründet wurde. Der Ansatz ist, gemeinsam und auf gleicher Augenhöhe mit Partner/innen in Afrika Lösungsstrategien für bestehende Entwicklungsprobleme zu erarbeiten. In Zusammenarbeit mit motivierten Entwicklungsträgern in Afrika werden so unvollständige und vernachlässigte Entwicklungsdynamiken gefördert. Daher umfasst die Entwicklungsförderung alle Bereiche des Lebens, für die Unterstützung angefordert und/oder benötigt wird."),
    ("migrationszentrum", "https://migrationszentrum-goettingen.wir-e.de/aktuelles", "Migrationszentrum für Stadt und Landkreis Göttingen", "Göttingen",
     "The Migration Center is a counselling, education and meeting centre under the auspices of the Diakonieverband of the Protestant-Lutheran church district of Göttingen. Its goals are the social and professional integration of migrants and support for their self-help potential. Social pedagogues, lawyers, language course instructors, interpreters and an administrator make up the team, supported by interns and volunteers. The international team is committed to the humanitarian values of the Protestant Church and works according to the integration plan of Lower Saxony and the principles for refugee social work of the Lutheran Church of Hanover.",
     "Das Migrationszentrum ist ein Beratungs-, Bildungs- und Begegnungszentrum in der Trägerschaft des Diakonieverbandes des Ev.-luth. Kirchenkreises Göttingen. Die soziale und berufliche Integration von Migrant/innen und die Unterstützung des Selbsthilfepotentials sind Ziele der Angebote. Sozialpädagog/innen, Jurist/innen, Sprachkursdozent/innen, Dolmetscher/innen und eine Verwaltungskraft bilden das Team, unterstützt von Praktikant/innen und Ehrenamtlichen. Das internationale Team ist den humanitären Werten der Evangelischen Kirche verbunden und arbeitet nach dem Integrationsplan des Landes Niedersachsen und den Grundsätzen für Flüchtlingssozialarbeit der Ev.-luth. Landeskirche Hannovers."),
    ("arca", "https://arca-ev.de", "ARCA e.V.", "Hamburg",
     "ARCA are people from Hamburg who have come together to positively change the living situation of African, Black German and Afrodiasporic residents. With their work they strive for more diversity in society, so that everyone's voice is heard, not just those who have money or power.",
     "ARCA sind Menschen aus Hamburg, die sich zusammengeschlossen haben, um die Lebenssituation afrikanischer, schwarzer deutscher und afrodiasporischer Einwohner/innen positiv zu verändern. Mit ihrer Arbeit streben sie nach mehr Vielfalt in der Gesellschaft, damit jeder mit seiner Stimme gehört wird und nicht nur die, die Geld oder Macht haben."),
]

def logo_strip():
    return '<div class="logo-strip">' + "".join(
        f'<a href="{href}" rel="noopener" aria-label="{name}">{pic("partner-" + k + ".png", name)}</a>'
        for k, href, name, *_ in PARTNERS) + "</div>"

# ---------- pages ----------
def home(lang):
    en = lang == "en"
    facts = ([("100%", "Free, always"), ("Sat", "Classes every Saturday"), ("4–18+", "Ages we teach"), ("DE · EN", "Languages of instruction")]
             if en else
             [("100 %", "Immer kostenlos"), ("Sa", "Kurse jeden Samstag"), ("4–18+", "Altersgruppen"), ("DE · EN", "Unterrichtssprachen")])
    facts_html = "".join(f'<div class="fact"><b>{a}</b><span>{b}</span></div>' for a, b in facts)
    mosaic = "".join(gallery_link(n, lang, figure=False) for n in ["23", "3", "13", "22", "1"])
    T = {
        "eyebrow": "Free coding classes for kids, teens &amp; adults" if en else "Kostenlose Programmierkurse für Kinder, Jugendliche &amp; Erwachsene",
        "h1": 'Coding skills for a <span class="hl">brighter future</span>.' if en else 'Programmieren für eine <span class="hl">bessere Zukunft</span>.',
        "lead": ('Our vision for Afro Code Academy is to empower children in underprivileged groups, specifically children with migration backgrounds, with the skills and knowledge to succeed in the digital world. By teaching them how to code, we help them unlock new opportunities and pave the way for a brighter future.'
                 if en else
                 'Unsere Vision für die Afro Code Academy ist es, Kindern aus unterprivilegierten Gruppen, insbesondere Kindern mit Migrationshintergrund, die Fähigkeiten und das Wissen zu vermitteln, um in der digitalen Welt erfolgreich zu sein. Durch Programmierkenntnisse helfen wir ihnen, neue Möglichkeiten zu erschließen und den Weg in eine bessere Zukunft zu ebnen.'),
        "cta1": "Explore courses" if en else "Kurse entdecken",
        "cta2": "Register now" if en else "Jetzt anmelden",
        "note": ('<strong>New:</strong> we also offer FREE courses for adults in web development and data analytics.'
                 if en else '<strong>Neu:</strong> Wir bieten auch KOSTENLOSE Kurse für Erwachsene in Webentwicklung und Datenanalyse an.'),
        "free": "100%<b>free</b>" if en else "100 %<b>gratis</b>",
        "where": "Classes in" if en else "Kurse in",
    }
    about_t = ("About our project", "Run entirely by dedicated volunteers",
               'Our project, Afro Code Academy, is run entirely by dedicated volunteers who are passionate about empowering children with the skills and knowledge to succeed in the digital world. We believe that by teaching these children how to code, we can help them unlock new opportunities and pave the way for a brighter future.',
               "Read our story") if en else (
               "Über unser Projekt", "Ausschließlich von engagierten Freiwilligen getragen",
               'Unser Projekt Afro Code Academy wird ausschließlich von engagierten Freiwilligen geleitet, denen es am Herzen liegt, Kindern die Fähigkeiten und das Wissen zu vermitteln, um in der digitalen Welt erfolgreich zu sein. Wir glauben, dass wir diesen Kindern durch Programmierkenntnisse helfen können, neue Möglichkeiten zu erschließen und den Weg in eine bessere Zukunft zu ebnen.',
               "Mehr über uns")
    robo = ({"soon": "Coming soon", "title": 'Robotics workshop <span class="hl">for kids</span>',
             "text": "Build it, wire it, code it, and watch it move! In our new hands-on robotics workshop, kids assemble simple robots, connect motors and sensors, and program them to drive, light up and react to the world around them.",
             "points": [("blocks", "Build your own robot"), ("terminal", "Program motors &amp; sensors"), ("gamepad", "Team challenges &amp; races")],
             "cta": "Notify me", "cta2": "See current courses", "note": "Free, like all our courses", "alt": "Illustration of a friendly waving robot"} if en else
            {"soon": "Demnächst", "title": 'Robotik-Workshop <span class="hl">für Kinder</span>',
             "text": "Bauen, verkabeln, programmieren – und zusehen, wie es sich bewegt! In unserem neuen Robotik-Workshop bauen Kinder einfache Roboter, schließen Motoren und Sensoren an und programmieren sie so, dass sie fahren, leuchten und auf ihre Umgebung reagieren.",
             "points": [("blocks", "Eigenen Roboter bauen"), ("terminal", "Motoren &amp; Sensoren programmieren"), ("gamepad", "Team-Challenges &amp; Rennen")],
             "cta": "Benachrichtige mich", "cta2": "Aktuelle Kurse ansehen", "note": "Kostenlos, wie alle unsere Kurse", "alt": "Illustration eines freundlich winkenden Roboters"})
    robo_points = "".join(f'<li>{I[ic]}<span>{t}</span></li>' for ic, t in robo["points"])
    hl = ([("gift", "Free, always", "No fees, and no plans to change that."),
           ("calendar", "A month of Saturdays", "Each course runs every Saturday for one month."),
           ("laptop", "All levels welcome", "From first steps to experienced young coders.")] if en else
          [("gift", "Immer kostenlos", "Keine Gebühren – und das bleibt so."),
           ("calendar", "Einen Monat lang samstags", "Jeder Kurs läuft einen Monat lang jeden Samstag."),
           ("laptop", "Alle Niveaus willkommen", "Von den ersten Schritten bis zu erfahrenen jungen Programmierern.")])
    highlights = "".join(f'<li><span class="hl-icon">{I[ic]}</span><span><strong>{a}</strong>{b}</span></li>' for ic, a, b in hl)
    courses_h = ("What courses do we offer?", "We have courses for different age groups, and these groups are subdivided into smaller groups.", "Full curriculum") if en else (
                 "Welche Kurse bieten wir an?", "Wir haben Kurse für verschiedene Altersgruppen, welche jeweils in weitere Untergruppen unterteilt werden.", "Zum Lehrplan")
    gal_h = ("Workshop gallery", "Moments from our classrooms", "View all photos") if en else ("Workshop-Galerie", "Momente aus unseren Kursen", "Alle Fotos ansehen")
    band = ("Want to volunteer?", "Help us empower the next generation of coders.",
            "Teach classes and workshops, mentor students or help with program administration. Whatever your skills, there is a role for you.",
            "Join the team", "Contact us") if en else (
            "Mitmachen?", "Hilf uns, die nächste Generation von Programmierern zu fördern.",
            "Unterrichte Kurse und Workshops, betreue Schüler oder hilf bei der Programmverwaltung. Egal welche Fähigkeiten du hast – wir haben eine passende Aufgabe.",
            "Mitmachen", "Kontakt")
    partners_h = "Supported by our partners" if en else "Unterstützt von unseren Partnern"

    body = f'''<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">{T["eyebrow"]}</span>
      <h1>{T["h1"]}</h1>
      <p class="lead">{T["lead"]}</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="{url("curriculum", lang)}">{T["cta1"]} {I["arrow"]}</a>
        <a class="btn btn--ghost" href="{url("curriculum", lang)}#register">{T["cta2"]}</a>
      </div>
      <p class="hero-note"><span class="dot" aria-hidden="true"></span><span>{T["note"]} <a href="{url("curriculum", lang)}#adults">{"Details" if not en else "Learn more"}</a></span></p>
    </div>
    <div class="collage">
      <figure class="c1">{pic(photo("4", "lg"), alt("4", lang), eager=True)}</figure>
      <figure class="c2">{pic(photo("13"), alt("13", lang), eager=True)}</figure>
      <figure class="c3">{pic(photo("11"), alt("11", lang), eager=True)}</figure>
      <div class="badge-free" aria-hidden="true"><span>{T["free"]}</span></div>
      <div class="badge-place">{I["pin"]}<span><small>{T["where"]}</small>{LOCATIONS}</span></div>
    </div>
  </div>
</section>

<section class="facts" aria-label="{"Key facts" if en else "Auf einen Blick"}">
  <div class="container facts-grid">{facts_html}</div>
</section>

<section class="section section--robotics" id="robotics">
  <div class="container">
    <div class="robotics reveal">
      <div class="robotics-copy">
        <span class="soon-pill"><span class="soon-dot" aria-hidden="true"></span>{robo["soon"]}</span>
        <h2>{robo["title"]}</h2>
        <p>{robo["text"]}</p>
        <ul class="robo-points">{robo_points}</ul>
        <div class="btn-row">
          <a class="btn btn--primary" {mail_attrs("robotics", lang, "#robotics")}>{I["mail"]} {robo["cta"]}</a>
          <a class="btn btn--ghost" href="{url("curriculum", lang)}">{robo["cta2"]} {I["arrow"]}</a>
        </div>
        <p class="robo-note">{I["gift"]} {robo["note"]}</p>
      </div>
      <div class="robotics-art">
        <img src="images/web/robot.svg" alt="{robo["alt"]}" width="480" height="400" loading="lazy">
        <div class="soon-sticker" aria-hidden="true"><span>{robo["soon"]}</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split reveal">
      <figure class="split-media photo photo--leaf photo--left">{pic(photo("21"), alt("21", lang))}</figure>
      <div>
        <span class="eyebrow">{about_t[0]}</span>
        <h2>{about_t[1]}</h2>
        <p>{about_t[2]}</p>
        <ul class="highlights">{highlights}</ul>
        <div class="btn-row"><a class="btn btn--ghost" href="{url("about", lang)}">{about_t[3]} {I["arrow"]}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">{"Courses" if en else "Kurse"}</span>
      <h2>{courses_h[0]}</h2>
      <p class="lead">{courses_h[1]}</p>
    </div>
    {course_cards(lang, short=True)}
    <div class="btn-row" style="justify-content:center"><a class="btn btn--primary" href="{url("curriculum", lang)}">{courses_h[2]} {I["arrow"]}</a></div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">{gal_h[0]}</span>
      <h2>{gal_h[1]}</h2>
    </div>
    <div class="mosaic reveal">{mosaic}</div>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--light" href="{url("gallery", lang)}">{gal_h[2]} {I["arrow"]}</a></div>
  </div>
</section>

<section class="section section--tight section--tint">
  <div class="container">
    <p class="center eyebrow" style="display:flex;justify-content:center">{partners_h}</p>
    {logo_strip()}
  </div>
</section>

<section class="band">
  {pic(photo("12", "lg"), "")}
  <div class="container">
    <span class="eyebrow">{band[0]}</span>
    <h2>{band[1]}</h2>
    <p>{band[2]}</p>
    <div class="btn-row">
      <a class="btn btn--primary" href="{url("volunteer", lang)}">{band[3]} {I["arrow"]}</a>
      <a class="btn btn--outline-light" href="{url("contact", lang)}">{band[4]}</a>
    </div>
  </div>
</section>'''
    title = "Free coding classes for kids" if en else "Kostenlose Programmierkurse für Kinder"
    desc = ("Afro Code Academy offers free coding classes for children with migration backgrounds, taught by volunteers in German and English, plus free web development and data analytics courses for adults."
            if en else
            "Die Afro Code Academy bietet kostenlose Programmierkurse für Kinder mit Migrationshintergrund, geleitet von Freiwilligen auf Deutsch und Englisch, sowie kostenlose Kurse für Erwachsene.")
    return layout("home", lang, title, desc, body, extra_head=jsonld(lang))


def about(lang):
    en = lang == "en"
    if en:
        hero = page_hero("About us", "About our project",
                         "A volunteer-run initiative empowering children from underprivileged groups, specifically children with migration backgrounds, to succeed in the digital world.",
                         photo("23", "lg"), alt("23", "en"))
        p = [
            'Our project, Afro Code Academy, is run entirely by dedicated volunteers who are passionate about empowering children in underprivileged groups, specifically children with migration backgrounds, with the skills and knowledge to succeed in the digital world. We believe that by teaching these children how to code, we can help them unlock new opportunities and pave the way for a brighter future.',
            'Our team of volunteers includes experienced coders, educators, and mentors who are committed to providing high-quality instruction and support to every child who participates in our program. We offer a range of classes and workshops designed to suit learners of all ages and skill levels, and we strive to create a fun and engaging learning environment where students can thrive.',
            'In addition to teaching coding skills, we also work to promote diversity and inclusion in the tech industry. We believe that everyone should have the opportunity to pursue their passions and achieve their goals, regardless of their background or circumstances.',
            'Through our program, we hope to inspire a new generation of coders who will go on to make their mark in the world and drive positive change in their communities. If you share our vision and would like to support our efforts, please consider joining our team of volunteers.',
            'In addition to being free, our courses are also designed to be flexible and accommodate learners of all levels. Whether a child is just starting to learn about coding or is already an experienced programmer, we have classes and workshops that will suit their needs and help them achieve their goals.',
            'We are grateful for the support of our volunteers who make it possible for us to offer these free courses. Together, we can help these children unlock their potential and prepare for success in the digital world.',
        ]
        h = ["Who we are", "Diversity & inclusion in tech", "Flexible, free and for everyone"]
        quote = "Together, we can make a difference."
        vals = [("Free, always", "No fees, no plans to change that."), ("Volunteer-run", "Coders, educators and mentors."), ("All levels", "Beginners to experienced young coders.")]
        cta = ("Share our vision?", "Join our team of volunteers", "Become a volunteer")
    else:
        hero = page_hero("Über uns", "Über unser Projekt",
                         "Eine von Freiwilligen getragene Initiative, die Kindern aus unterprivilegierten Gruppen, insbesondere mit Migrationshintergrund, den Weg in die digitale Welt ebnet.",
                         photo("23", "lg"), alt("23", "de"))
        p = [
            'Unser Projekt Afro Code Academy wird ausschließlich von engagierten Freiwilligen geleitet, denen es am Herzen liegt, Kindern aus unterprivilegierten Gruppen, insbesondere Kindern mit Migrationshintergrund, die Fähigkeiten und das Wissen zu vermitteln, um in der digitalen Welt erfolgreich zu sein. Wir glauben, dass wir diesen Kindern durch die Vermittlung von Programmierkenntnissen helfen können, neue Möglichkeiten zu erschließen und ihnen den Weg in eine bessere Zukunft zu ebnen.',
            'Zu unserem Team von Freiwilligen gehören erfahrene Programmierer, Pädagogen und Mentoren, die sich dafür einsetzen, jedem Kind, das an unserem Programm teilnimmt, qualitativ hochwertigen Unterricht und Unterstützung zu bieten. Wir bieten eine Reihe von Kursen und Workshops an, die für Lernende aller Altersgruppen und Fähigkeitsstufen geeignet sind, und wir bemühen uns, eine unterhaltsame und ansprechende Lernumgebung zu schaffen, in der sich die Schüler entfalten können.',
            'Neben der Vermittlung von Programmierkenntnissen setzen wir uns auch für die Förderung von Vielfalt und Integration in der Tech-Branche ein. Wir glauben, dass jeder die Möglichkeit haben sollte, seinen Leidenschaften nachzugehen und seine Ziele zu erreichen, unabhängig von seinem Hintergrund oder seinen Lebensumständen.',
            'Wir hoffen, dass wir mit unserem Programm eine neue Generation von Programmierern inspirieren können, die sich in der Welt einen Namen machen und positive Veränderungen in ihren Communities bewirken werden. Wenn Sie unsere Vision teilen und das Projekt unterstützen möchten, melden Sie sich gerne bei uns. Wir würden uns sehr freuen, weitere Freiwillige in unserem Team willkommen zu heißen.',
            'Unsere Kurse sind nicht nur kostenlos, sondern auch so konzipiert, dass sie flexibel sind und sich an Lernende aller Niveaus richten. Ganz gleich, ob ein Kind gerade erst mit dem Programmieren anfängt oder bereits fortgeschritten ist: Wir haben Kurse und Workshops, die allen Bedürfnissen entsprechen und jedem Kind helfen sollen, seine individuellen Ziele zu erreichen.',
            'Wir sind dankbar für die Unterstützung durch unsere Freiwilligen, die es uns ermöglichen, diese kostenlosen Kurse für Kinder aus marginalisierten Gruppen anzubieten. Gemeinsam können wir diesen Kindern helfen, ihr Potenzial zu entfalten und sich auf den Erfolg in der digitalen Welt vorzubereiten.',
        ]
        h = ["Wer wir sind", "Vielfalt & Integration in der Tech-Branche", "Flexibel, kostenlos und für alle"]
        quote = "Gemeinsam können wir etwas bewirken."
        vals = [("Immer kostenlos", "Keine Gebühren – und das bleibt so."), ("Von Freiwilligen", "Programmierer, Pädagogen und Mentoren."), ("Alle Niveaus", "Von Anfängern bis zu erfahrenen jungen Programmierern.")]
        cta = ("Teilst du unsere Vision?", "Werde Teil unseres Teams", "Freiwillige/r werden")
    vals_html = "".join(f'<div class="role">{ic}<h3>{a}</h3><p>{b}</p></div>' for (a, b), ic in zip(vals, [I["gift"], I["heart"], I["laptop"]]))
    body = f'''{hero}
<section class="section">
  <div class="container">
    <div class="split reveal">
      <div>
        <span class="eyebrow">{h[0]}</span>
        <h2>{"Empowering children through code" if en else "Kinder durch Programmieren stärken"}</h2>
        <p class="lead">{p[0]}</p>
        <p>{p[1]}</p>
      </div>
      <figure class="split-media photo">{pic(photo("5"), alt("5", lang))}</figure>
    </div>
    <div class="roles reveal">{vals_html}</div>
    <p class="quote reveal">{quote}</p>
    <div class="split split--rev reveal">
      <div>
        <span class="eyebrow">{h[1]}</span>
        <h2>{h[1]}</h2>
        <p>{p[2]}</p>
        <p>{p[3]}</p>
      </div>
      <div class="split-media photo-pair">{pic(photo("8"), alt("8", lang))}{pic(photo("19"), alt("19", lang))}</div>
    </div>
    <div class="split reveal">
      <div>
        <span class="eyebrow">{"Our courses" if en else "Unsere Kurse"}</span>
        <h2>{h[2]}</h2>
        <p>{p[4]}</p>
        <p>{p[5]}</p>
        <div class="btn-row"><a class="btn btn--ghost" href="{url("curriculum", lang)}">{NAV_LABEL[lang]["curriculum"]} {I["arrow"]}</a></div>
      </div>
      <figure class="split-media photo photo--plum">{pic(photo("14"), alt("14", lang))}</figure>
    </div>
  </div>
</section>
<section class="band">
  {pic(photo("12", "lg"), "")}
  <div class="container">
    <span class="eyebrow">{cta[0]}</span>
    <h2>{cta[1]}</h2>
    <div class="btn-row"><a class="btn btn--primary" href="{url("volunteer", lang)}">{cta[2]} {I["arrow"]}</a></div>
  </div>
</section>'''
    desc = ("Afro Code Academy is run entirely by volunteers who teach coding to children from underprivileged groups, specifically children with migration backgrounds."
            if en else "Die Afro Code Academy wird ausschließlich von Freiwilligen getragen, die Kindern aus unterprivilegierten Gruppen das Programmieren beibringen.")
    return layout("about", lang, NAV_LABEL[lang]["about"], desc, body)


def curriculum(lang):
    en = lang == "en"
    kids_pdf = "CURRICULUM.pdf" if en else "CURRICULUM_de.pdf"
    if en:
        hero = page_hero("Curriculum", "Courses for every age",
                         "Simple, fun and exciting projects that give children a basic introduction to code, plus free beginner tracks for adults.",
                         photo("15", "lg"), alt("15", "en"))
        kids = ("Kids &amp; teens", "Kids curriculum",
                "Our curriculum focuses on simple, fun and exciting projects to give children a basic introduction to code. We also offer courses for teenagers and adults that prepare them for more complicated tasks in high school and college, and help them succeed in any profession they choose.",
                [("pin", LOCATIONS), ("calendar", "Every Saturday"), ("clock", "One month"), ("gift", "Free"), ("lang", "German &amp; English")],
                "Download curriculum (PDF)", "Register your child")
        ages = [("4–7", COURSES["en"][0][3]), ("7–12", COURSES["en"][1][3]),
                ("13–18", COURSES["en"][2][3] + " We teach Python, Arduino (C) and Raspberry Pi (Python), Game Maker Studio, Minecraft modding, and web development (HTML/CSS/JavaScript).")]
        adults = ("Adults 18+", "Adult curriculum",
                  "Our comprehensive curriculum is designed for complete beginners in programming! We offer two exciting tracks to kickstart your journey into the world of coding:",
                  [("Web Development Track", "Embark on a thrilling adventure to build your very own website from scratch.", "&lt;/&gt;"),
                   ("Data Analytics Track", "Unleash the power of Python and delve into the realm of data analytics! Uncover the secrets of data manipulation, analysis, and visualization using Python.", "Py")],
                  [("laptop", "Online"), ("clock", "2 hours / week"), ("calendar", "3 months"), ("gift", "Free")],
                  "Download curriculum (PDF)", "Register as an adult")
    else:
        hero = page_hero("Lehrplan", "Kurse für jedes Alter",
                         "Einfache, lustige und spannende Projekte, die Kindern eine grundlegende Einführung ins Programmieren geben – plus kostenlose Einsteiger-Tracks für Erwachsene.",
                         photo("15", "lg"), alt("15", "de"))
        kids = ("Kinder &amp; Jugendliche", "Lehrplan für Kinder",
                "Unser Lehrplan konzentriert sich auf einfache, lustige und spannende Projekte, um Kindern eine grundlegende Einführung in die Welt des Programmierens zu geben. Wir bieten auch Kurse für Jugendliche und Erwachsene an, die sie auf kompliziertere Aufgaben in der weiterführenden Schule und an der Universität vorbereiten und ihnen helfen, in jedem Beruf, den sie wählen, erfolgreich zu sein.",
                [("pin", LOCATIONS), ("calendar", "Jeden Samstag"), ("clock", "Ein Monat"), ("gift", "Kostenlos"), ("lang", "Deutsch &amp; Englisch")],
                "Lehrplan herunterladen (PDF)", "Kind anmelden")
        ages = [("4–7", COURSES["de"][0][3]), ("7–12", COURSES["de"][1][3]),
                ("13–18", COURSES["de"][2][3] + " Wir unterrichten Python, Arduino (C) und Raspberry Pi (Python), Game Maker Studio, Minecraft-Modding und Web-Entwicklung (HTML/CSS/JavaScript).")]
        adults = ("Erwachsene 18+", "Lehrplan für Erwachsene",
                  "Unser umfassender Lehrplan für absolute Programmieranfänger! Wir bieten zwei spannende Tracks, die deine Reise in die Welt des Programmierens ankurbeln:",
                  [("Web Development Track", "Begib dich auf ein spannendes Abenteuer und erstelle deine ganz eigene Website von Grund auf.", "&lt;/&gt;"),
                   ("Data Analytics Track", "Entfessle die Leistungsfähigkeit von Python und tauche ein in die Welt der Datenanalyse! Entdecke die Geheimnisse der Datenmanipulation, -analyse und -visualisierung mit Python.", "Py")],
                  [("laptop", "Online"), ("clock", "2 Stunden / Woche"), ("calendar", "3 Monate"), ("gift", "Kostenlos")],
                  "Lehrplan herunterladen (PDF)", "Als Erwachsene/r anmelden")
    meta = lambda items: '<div class="meta-row">' + "".join(f'<span class="meta">{I[i]}{t}</span>' for i, t in items) + "</div>"
    ages_html = "".join(f'<div class="age-item"><span class="age-icon">{I[ic]}</span><b>{a}</b><p>{t}</p></div>' for (a, t), ic in zip(ages, COURSE_ICONS))
    tracks_html = "".join(f'<div class="track"><h3><span>{ic}</span>{t}</h3><p>{d}</p></div>' for t, d, ic in adults[3])
    reg_h = ("Ready to start?", "Register by email", f"Registration is free and done by email. Pick a course below and your email app opens with a short template to fill in, or write to us directly at <strong>{EMAIL}</strong>.",
             "Kids &amp; teens (4–18)", "Saturday classes, one month", "Adults (18+)", "Online, 2 hours a week for 3 months") if en else (
            "Bereit?", "Anmeldung per E-Mail", f"Die Anmeldung ist kostenlos und erfolgt per E-Mail. Wähle unten einen Kurs – dein E-Mail-Programm öffnet sich mit einer kurzen Vorlage – oder schreib uns direkt an <strong>{EMAIL}</strong>.",
             "Kinder &amp; Jugendliche (4–18)", "Samstagskurse, ein Monat", "Erwachsene (18+)", "Online, 2 Stunden pro Woche über 3 Monate")
    body = f'''{hero}
<section class="section">
  <div class="container">
    <div class="split reveal" id="kids">
      <div>
        <span class="eyebrow">{kids[0]}</span>
        <h2>{kids[1]}</h2>
        <p>{kids[2]}</p>
        {meta(kids[3])}
        <div class="downloads">
          <a class="btn btn--primary" {mail_attrs("kids", lang)}>{I["mail"]} {kids[5]}</a>
          <a class="btn btn--ghost" href="{kids_pdf}" target="_blank" rel="noopener">{I["download"]} {kids[4]}</a>
        </div>
      </div>
      <div class="split-media photo-pair">{pic(photo("19"), alt("19", lang))}{pic(photo("0335"), alt("0335", lang))}</div>
    </div>
    <div class="age-list reveal">{ages_html}</div>
  </div>
</section>
<section class="section section--tint" id="adults">
  <div class="container">
    <div class="split split--rev reveal">
      <div>
        <span class="eyebrow">{adults[0]}</span>
        <h2>{adults[1]}</h2>
        <p>{adults[2]}</p>
        {meta(adults[4])}
        <div class="downloads">
          <a class="btn btn--primary" {mail_attrs("adults", lang)}>{I["mail"]} {adults[6]}</a>
          <a class="btn btn--ghost" href="Curriculum_adult.pdf" target="_blank" rel="noopener">{I["download"]} {adults[5]}</a>
        </div>
      </div>
      <figure class="split-media photo photo--leaf photo--left">{pic(photo("24"), alt("24", lang))}</figure>
    </div>
    <div class="tracks reveal">{tracks_html}</div>
  </div>
</section>
<section class="section" id="register">
  <div class="container">
    <div class="section-head center"><span class="eyebrow">{reg_h[0]}</span><h2>{reg_h[1]}</h2><p class="lead">{reg_h[2]}</p></div>
    <div class="tracks" style="max-width:880px;margin-inline:auto">
      <a class="contact-card" {mail_attrs("kids", lang)}><span class="ic">{I["teach"]}</span><span><strong>{reg_h[3]}</strong><small>{reg_h[4]}</small></span></a>
      <a class="contact-card" {mail_attrs("adults", lang)}><span class="ic">{I["laptop"]}</span><span><strong>{reg_h[5]}</strong><small>{reg_h[6]}</small></span></a>
    </div>
  </div>
</section>'''
    desc = ("Free coding courses for ages 4–18 every Saturday, plus free online web development and data analytics tracks for adult beginners."
            if en else "Kostenlose Programmierkurse für 4- bis 18-Jährige jeden Samstag sowie kostenlose Online-Kurse in Webentwicklung und Datenanalyse für Erwachsene.")
    return layout("curriculum", lang, NAV_LABEL[lang]["curriculum"], desc, body)


def gallery(lang):
    en = lang == "en"
    hero = page_hero("Gallery" if en else "Galerie",
                     "Workshop gallery" if en else "Workshop-Galerie",
                     "Saturdays full of laptops, tablets, games and big smiles. Tap any photo to see it larger." if en else
                     "Samstage voller Laptops, Tablets, Spiele und strahlender Gesichter. Tippe auf ein Foto, um es zu vergrößern.",
                     photo("17", "lg"), alt("17", lang))
    grid = "".join(gallery_link(n, lang) for n, *_ in GALLERY)
    cta = ("Want your child in the next class?", "Register now") if en else ("Soll dein Kind beim nächsten Kurs dabei sein?", "Jetzt anmelden")
    body = f'''{hero}
<section class="section">
  <div class="container">
    <div class="masonry">{grid}</div>
    <div class="center" style="margin-top:48px">
      <h3>{cta[0]}</h3>
      <div class="btn-row" style="justify-content:center"><a class="btn btn--primary" href="{url("curriculum", lang)}#register">{cta[1]} {I["arrow"]}</a></div>
    </div>
  </div>
</section>'''
    desc = ("Photos from Afro Code Academy's free coding workshops for children." if en
            else "Fotos aus den kostenlosen Programmier-Workshops der Afro Code Academy.")
    return layout("gallery", lang, NAV_LABEL[lang]["gallery"], desc, body, og_img="photo-23-lg.webp")


TEAM = [
    ("abdul-qadir", "Abdul Qadir", "Mathematician · Co-founder", "Mathematiker · Mitgründer",
     "I am a Ghanaian-Nigerian postdoctoral researcher in Mathematics with a focus on Machine Learning and Numerical Mathematics. I am passionate about understanding the nuances of programming and mathematics and their importance to the African community. My goal is to introduce programming to underprivileged communities through initiatives like teaching code. My vision is that every child has access to the opportunities coding has provided me."),
    ("halima", "Halima", "PhD candidate in Molecular Biology", "Doktorandin in Molekularbiologie",
     "I am a Nigerian PhD candidate in Oocyte Meiosis at the Max Planck Institute for Biophysical Chemistry. I am hoping that this project will encourage more African girls to learn to code."),
    ("souaybou", "Souaybou", "Data Scientist", "Data Scientist",
     "I am a Malian mathematician, data scientist, and AI enthusiast. I have a master's degree in data analysis with a background in applied mathematics and computer science. I have professional experience in the field of AI, both in research and production, and I strongly believe in sharing knowledge and providing solutions to people in need. We are at the beginning of a massive digital transformation, and no one should be left behind. Afro Code Academy offers an opportunity to bridge the digital divide for Africans."),
    ("thomas", "Thomas", "Full stack developer · Co-founder", "Full-Stack-Entwickler · Mitgründer",
     "I am a full stack developer from Ghana. I have a Master's degree in Applied Computer Science and have worked as a mobile app developer for Vodafone. I also enjoy volunteering my time to teach others how to code. I believe that by empowering the next generation of coders, we can help them unlock new opportunities and drive positive change in their communities."),
    ("aminata", "Aminata", "Political Scientist", "Politikwissenschaftlerin",
     "Since I already dealt with Critical Theories such as Postcolonialism and Intersectional Feminism in my studies, I am even more pleased to be able to support this project and thus contribute to changing structural inequalities in our society. Especially in an industry as promising as IT, we should ensure that the next generation of Data Scientists will be more diverse. I am more involved in matters concerning communication and organization."),
]

def volunteer(lang):
    en = lang == "en"
    if en:
        hero = page_hero("Volunteer", "Join us",
                         "Are you passionate about empowering children with the skills and knowledge to succeed in the digital world?",
                         photo("12", "lg"), alt("12", "en"))
        p = ['Do you have experience in coding or education, and are you looking for a meaningful way to make a difference in your community? If so, we encourage you to consider volunteering with our project, Afro Code Academy.',
             'Our team of volunteers is essential to the success of our program, and we are always looking for dedicated individuals who share our vision and are eager to help. As a volunteer, you will have the opportunity to work closely with children and provide them with the support and guidance they need to learn coding skills and build a strong foundation for the future.',
             'If you are interested in volunteering with us, please contact us for more information. We would be delighted to have you join our team and help us empower the next generation of coders. Together, we can make a difference.']
        roles_h = "We offer a range of volunteer opportunities. No matter what your skills and interests are, we have a role that will suit you."
        roles = [("teach", "Teaching", "Lead classes and workshops for our different age groups."),
                 ("heart", "Mentoring", "Support students one-on-one as they learn and build."),
                 ("admin", "Administration", "Help with organization, communication and running the program.")]
        team_h = ("Our volunteers", "Meet the team")
        join = ("This could be you", "We are always looking for dedicated people who share our vision.", "Get in touch")
        cta = "Contact us to volunteer"
    else:
        hero = page_hero("Mitmachen", "Werde Teil des Teams",
                         "Liegt es dir am Herzen, Kindern die Fähigkeiten und das Wissen zu vermitteln, um in der digitalen Welt erfolgreich zu sein?",
                         photo("12", "lg"), alt("12", "de"))
        p = ['Haben Sie Erfahrung im Bereich Programmierung oder Bildung und suchen Sie nach einer sinnvollen Möglichkeit, in Ihrer Gemeinde etwas zu bewirken? Dann möchten wir Sie ermutigen, eine freiwillige Mitarbeit in unserem Projekt Afro Code Academy in Betracht zu ziehen.',
             'Unser Team von Freiwilligen ist für den Erfolg unseres Programms unerlässlich, und wir sind immer auf der Suche nach engagierten Personen, die unsere Vision teilen und gerne helfen möchten. Als Freiwillige/r haben Sie die Möglichkeit, eng mit Kindern zusammenzuarbeiten und ihnen die Unterstützung und Anleitung zu geben, die sie brauchen, um Programmierkenntnisse zu erlernen und eine solide Grundlage für die Zukunft zu schaffen.',
             'Wenn Sie an einer ehrenamtlichen Tätigkeit interessiert sind, nehmen Sie bitte Kontakt mit uns auf, um weitere Informationen zu erhalten. Wir würden uns freuen, wenn Sie unserem Team beitreten und uns dabei helfen, die nächste Generation von Programmierern zu fördern. Gemeinsam können wir etwas bewirken.']
        roles_h = "Wir bieten eine Reihe von Freiwilligeneinsätzen an. Ganz gleich, welche Fähigkeiten und Interessen Sie haben – wir haben eine Aufgabe, die zu Ihnen passt."
        roles = [("teach", "Unterrichten", "Kurse und Workshops für unsere Altersgruppen leiten."),
                 ("heart", "Betreuen", "Schüler individuell beim Lernen und Bauen begleiten."),
                 ("admin", "Organisation", "Bei Organisation, Kommunikation und Programmverwaltung helfen.")]
        team_h = ("Unsere Freiwilligen", "Das Team")
        join = ("Das könntest du sein", "Wir suchen immer engagierte Menschen, die unsere Vision teilen.", "Kontakt aufnehmen")
        cta = "Jetzt Kontakt aufnehmen"
    bio_lang = "" if en else ' lang="en"'
    roles_html = "".join(f'<div class="role">{I[i]}<h3>{a}</h3><p>{b}</p></div>' for i, a, b in roles)
    team_html = "".join(
        f'<article class="member reveal"><div class="member-head">{pic("team-" + k + ".webp", name)}<div><h3>{name}</h3><div class="member-role">{re if en else rd}</div></div></div><p{bio_lang}>{bio}</p></article>'
        for k, name, re, rd, bio in TEAM)
    team_html += f'<article class="member member--join reveal"><div class="plus" aria-hidden="true">+</div><h3>{join[0]}</h3><p>{join[1]}</p><div class="btn-row"><a class="btn btn--primary" href="{url("contact", lang)}">{join[2]} {I["arrow"]}</a></div></article>'
    body = f'''{hero}
<section class="section">
  <div class="container">
    <div class="split reveal">
      <div>
        <span class="eyebrow">{"Volunteering" if en else "Ehrenamt"}</span>
        <h2>{"Make a difference in your community" if en else "Etwas in Ihrer Gemeinde bewirken"}</h2>
        <p class="lead">{p[0]}</p>
        <p>{p[1]}</p>
      </div>
      <div class="split-media photo-pair">{pic(photo("3"), alt("3", lang))}{pic(photo("1"), alt("1", lang))}</div>
    </div>
    <p style="margin-top:56px" class="lead reveal">{roles_h}</p>
    <div class="roles reveal">{roles_html}</div>
    <p style="margin-top:32px" class="reveal">{p[2]}</p>
    <div class="btn-row reveal"><a class="btn btn--primary" href="{url("contact", lang)}">{cta} {I["arrow"]}</a></div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head center"><span class="eyebrow">{team_h[0]}</span><h2>{team_h[1]}</h2></div>
    <div class="team">{team_html}</div>
  </div>
</section>'''
    desc = ("Volunteer with Afro Code Academy: teach, mentor or help run free coding classes for children." if en
            else "Werde Freiwillige/r bei der Afro Code Academy: unterrichten, betreuen oder organisieren.")
    return layout("volunteer", lang, NAV_LABEL[lang]["volunteer"], desc, body, og_img="photo-12-lg.webp")


def partners(lang):
    en = lang == "en"
    hero = page_hero("Partners" if en else "Partner",
                     "Our partners" if en else "Unsere Partner",
                     "The organisations that help make our free coding classes possible." if en else
                     "Die Organisationen, die unsere kostenlosen Programmierkurse möglich machen.",
                     photo("21", "lg"), alt("21", lang))
    cards = "".join(
        f'''<article class="partner reveal"><a class="partner-logo" href="{href}" rel="noopener" aria-label="{name}">{pic("partner-" + k + ".png", name)}</a>
<div><div class="partner-place">{place}</div><h3><a href="{href}" rel="noopener">{name}</a></h3><p>{den if en else dde}</p>
<a href="{href}" rel="noopener" class="btn btn--ghost" style="margin-top:6px">{"Visit website" if en else "Zur Website"} {I["ext"]}</a></div></article>'''
        for k, href, name, place, den, dde in PARTNERS)
    body = f'''{hero}
<section class="section"><div class="container"><div class="partners">{cards}</div></div></section>'''
    return layout("partners", lang, NAV_LABEL[lang]["partners"],
                  "Afro Code Academy partners: PLEA e.V., Migrationszentrum Göttingen and ARCA e.V." if en else
                  "Partner der Afro Code Academy: PLEA e.V., Migrationszentrum Göttingen und ARCA e.V.", body)


def contact(lang):
    en = lang == "en"
    hero = page_hero("Contact" if en else "Kontakt",
                     "Contact us" if en else "Kontakt",
                     "Questions about our courses, volunteering or partnerships? We would love to hear from you." if en else
                     "Fragen zu unseren Kursen, zum Mitmachen oder zu Partnerschaften? Wir freuen uns auf deine Nachricht.",
                     photo("11", "lg"), alt("11", lang))
    body = f'''{hero}
<section class="section">
  <div class="container contact-grid">
    <div class="reveal">
      <span class="eyebrow">{"Get in touch" if en else "Schreib uns"}</span>
      <h2>{"Say hello" if en else "Sag hallo"}</h2>
      <p class="lead">{"The quickest way to reach us is by email. You can also follow along with our classes on social media." if en else "Am schnellsten erreichst du uns per E-Mail. Auf Social Media kannst du unsere Kurse mitverfolgen."}</p>
      <div class="contact-cards" style="margin-top:28px">
        <a class="contact-card" href="#" data-mail="{EMAIL}"><span class="ic">{I["mail"]}</span><span><small>Email</small><strong>{EMAIL}</strong></span></a>
        <a class="contact-card" href="{IG}" rel="noopener"><span class="ic">{I["insta"]}</span><span><small>Instagram</small><strong>@afrocodeacademy</strong></span></a>
        <a class="contact-card" href="{TW}" rel="noopener"><span class="ic">{I["x"]}</span><span><small>X / Twitter</small><strong>@afrocodeacademy</strong></span></a>
      </div>
    </div>
    <figure class="photo photo--clay reveal" style="margin-top:8px">{pic(photo("7"), alt("7", lang))}</figure>
  </div>
</section>'''
    return layout("contact", lang, NAV_LABEL[lang]["contact"],
                  "Contact Afro Code Academy by email, Instagram or X." if en else
                  "Kontakt zur Afro Code Academy per E-Mail, Instagram oder X.", body)


def impressum():
    addr = "<br>".join(LEGAL_ADDRESS)
    body = f'''{page_hero("Rechtliches · Legal notice", "Impressum", "Angaben gemäß § 5 DDG")}
<section class="section section--tight">
  <div class="container prose">
    <h3>Afro Code Academy</h3>
    <p>Ehrenamtliches Bildungsprojekt<br>{LEGAL_NAME}<br>{addr}</p>
    <h3>Kontakt</h3>
    <p>E-Mail: <a href="#" data-mail="{EMAIL}">{EMAIL}</a></p>
    <h3>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h3>
    <p>{LEGAL_NAME}<br>{addr}</p>
    <h3>Haftung für Links</h3>
    <p>Unsere Website enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.</p>
  </div>
</section>'''
    return layout("impressum", "de", "Impressum", "Impressum der Afro Code Academy.", body)


def redirect(target):
    base = target.split("#")[0]
    js = f'location.replace("{target}")' if "#" in target else f'location.replace("{target}" + location.hash)'
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Afro Code Academy</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{abs_url(base)}">
<meta http-equiv="refresh" content="0; url={target}">
<script>{js};</script>
</head><body><a href="{target}">Afro Code Academy</a></body></html>
'''

def sitemap():
    rows = []
    for page, (en, de) in PAGES.items():
        links = (f'<xhtml:link rel="alternate" hreflang="en" href="{abs_url(en)}"/>'
                 f'<xhtml:link rel="alternate" hreflang="de" href="{abs_url(de)}"/>')
        for f in dict.fromkeys((de, en)):
            rows.append(f"  <url><loc>{abs_url(f)}</loc>{links}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")

def jsonld(lang):
    import json
    en = lang == "en"
    courses = []
    for age, label, title, text, tags in COURSES[lang]:
        courses.append({
            "@type": "Course",
            "name": f"{title} ({'ages' if en else 'Alter'} {age})",
            "description": text,
            "inLanguage": ["de", "en"],
            "isAccessibleForFree": True,
            "provider": {"@type": "EducationalOrganization", "name": "Afro Code Academy", "url": SITE + "/"},
        })
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "EducationalOrganization", "name": "Afro Code Academy", "url": SITE + "/",
             "logo": f"{SITE}/images/web/favicon.svg", "email": EMAIL.replace("(at)", "@"),
             "description": UI[lang]["tagline"], "sameAs": [IG, TW]},
            *courses,
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="4" y="4" width="56" height="56" rx="16" fill="#d4502a"/><text x="32" y="41" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#fff" text-anchor="middle">&lt;/&gt;</text></svg>'''

def write(name, s):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(s)
    print("wrote", name)

for lang in ("en", "de"):
    write(url("home", lang), home(lang))
    write(url("about", lang), about(lang))
    write(url("curriculum", lang), curriculum(lang))
    write(url("gallery", lang), gallery(lang))
    write(url("volunteer", lang), volunteer(lang))
    write(url("partners", lang), partners(lang))
    write(url("contact", lang), contact(lang))
write("impressum.html", impressum())
write("index_de.html", redirect("index.html"))
# Old Google Forms pages: registration is now by email
write("register.html", redirect("curriculum.html#register"))
write("register_adult.html", redirect("curriculum.html#register"))
write("sitemap.xml", sitemap())
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(WEB, "favicon.svg"), "w") as f:
    f.write(FAVICON)

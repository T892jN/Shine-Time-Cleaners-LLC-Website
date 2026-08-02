from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://shinetimecleanersllc.com"
BUSINESS = "Shine Time Cleaners"
EMAIL = "contact@shinetimecleanersllc.com"
MISSOURI_CITIES = ["St. Louis", "Kansas City", "Springfield", "Columbia", "Independence", "Lee's Summit", "St. Charles", "O'Fallon"]

nav = [
    ("Home", "/"),
    ("About", "/about/"),
    ("Why Choose Us", "/why-choose-us/"),
    ("Services", "/services/"),
    ("Service Areas", "/service-areas/"),
    ("Guides", "/standard-cleaning-guide/"),
    ("FAQ", "/frequently-asked-questions/"),
    ("Contact", "/contact/"),
]

footer_links = [
    ("Standard Cleaning Guide", "/standard-cleaning-guide/"),
    ("Deep Cleaning Guide", "/deep-cleaning-guide/"),
    ("Move-Out Cleaning Guide", "/move-out-cleaning-guide/"),
    ("Pet-Friendly Cleaning", "/pet-friendly-cleaning/"),
    ("Seasonal Cleaning Tips", "/seasonal-cleaning-tips/"),
    ("House Cleaning Checklist", "/house-cleaning-checklist/"),
    ("Apartment Cleaning Checklist", "/apartment-cleaning-checklist/"),
    ("Pricing", "/pricing/"),
    ("Privacy", "/privacy/"),
    ("Terms", "/terms-of-service/"),
]

service_cards = [
    ("Standard Cleaning", "/standard-cleaning-guide/", "Routine upkeep for kitchens, bathrooms, bedrooms, living areas, floors, and high-touch surfaces."),
    ("Deep Cleaning", "/deep-cleaning-guide/", "A more detailed reset for buildup, first visits, seasonal refreshes, and homes that need extra attention."),
    ("Move-Out Cleaning", "/move-out-cleaning-guide/", "A turnover-focused clean for empty or nearly empty homes before moving in, moving out, listing, or handing over keys."),
    ("Pet-Friendly Cleaning", "/pet-friendly-cleaning/", "Practical cleaning for homes with pets, including hair, tracked-in debris, odors, and surface care."),
]

faqs = [
    ("Do you bring cleaning supplies?", "Yes. Shine Time Cleaners brings cleaning supplies for typical residential appointments. Customers should mention delicate surfaces, product restrictions, allergies, or preferred products before service."),
    ("How long does a cleaning visit take?", "Time depends on home size, condition, room count, and service type. A small maintenance visit may take a few hours, while deep cleaning or move-out cleaning can take most of a day."),
    ("Can I choose priority rooms?", "Yes. Customers can prioritize kitchens, bathrooms, floors, dusting, guest areas, pet-heavy areas, or move-related details so the appointment focuses on the highest-value work first."),
    ("Do you clean apartments?", "Yes. Apartments, townhomes, condos, and houses can be cleaned when the scope is residential and access details are clear."),
    ("Are the testimonials real?", "The testimonials shown on this site are clearly marked as placeholder examples until verified customer reviews are available. They are included to show the type of feedback section the site will use."),
]

schema_org = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": BUSINESS,
    "url": DOMAIN,
    "logo": f"{DOMAIN}/favicon.svg",
    "email": EMAIL,
}

schema_local = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": BUSINESS,
    "url": DOMAIN,
    "image": f"{DOMAIN}/images/hero.svg",
    "email": EMAIL,
    "priceRange": "$$",
    "areaServed": [{"@type": "State", "name": "Missouri"}],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"},
    ],
    "description": "Residential cleaning services for Missouri homes, apartments, move-out cleanings, deep cleaning, standard cleaning, and custom cleaning plans.",
}

def rel(path, current):
    if current == "/":
        prefix = ""
    else:
        depth = len([p for p in current.strip("/").split("/") if p])
        prefix = "../" * depth
    if path == "/":
        return prefix or "./"
    return prefix + path.strip("/") + "/"

def jsonld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

def breadcrumb_schema(title, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": DOMAIN + path},
        ],
    }

def faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }

def header(current):
    links = "".join(f'<a href="{rel(href, current)}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for label, href in nav)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header" data-header>
    <nav class="nav container" aria-label="Primary navigation">
      <a class="brand" href="{rel("/", current)}" aria-label="{BUSINESS} home"><span class="brand-mark" aria-hidden="true">ST</span><span><strong>Shine Time</strong><small>Cleaners</small></span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-menu" data-nav-toggle><span></span><span></span><span></span><span class="sr-only">Menu</span></button>
      <div class="nav-menu" id="primary-menu" data-nav-menu>{links}<a class="nav-cta" href="{rel("/contact/", current)}">Request availability</a></div>
    </nav>
  </header>'''

def footer(current):
    main = "".join(f'<a href="{rel(href, current)}">{label}</a>' for label, href in nav[1:])
    guides = "".join(f'<a href="{rel(href, current)}">{label}</a>' for label, href in footer_links)
    return f'''<footer class="site-footer">
    <div class="container footer-grid">
      <div><a class="brand footer-brand" href="{rel("/", current)}"><span class="brand-mark" aria-hidden="true">ST</span><span><strong>Shine Time</strong><small>Cleaners</small></span></a><p>Residential cleaning guidance and house cleaning services for Missouri households. Supplies are provided, service scopes are explained clearly, and new customer requests are welcome.</p></div>
      <nav aria-label="Footer navigation">{main}{guides}</nav>
    </div>
    <div class="container footer-bottom"><p>&copy; <span data-year></span> Shine Time Cleaners. All rights reserved.</p></div>
  </footer>'''

def page(title, desc, path, hero_label, h1, intro, body, extra_schema=None, image="/images/hero.svg"):
    canonical = DOMAIN + path
    schemas = [schema_org, schema_local, breadcrumb_schema(title, path)]
    if extra_schema:
        schemas.extend(extra_schema)
    schema_html = "\n  ".join(jsonld(s) for s in schemas)
    css = rel("/style.css", path)[:-1] if path != "/" else "style.css"
    js = rel("/script.js", path)[:-1] if path != "/" else "script.js"
    favicon = rel("/favicon.svg", path)[:-1] if path != "/" else "favicon.svg"
    hero_html = "" if path == "/" else f'''<section class="page-hero"><div class="container reveal"><p class="eyebrow">{hero_label}</p><h1>{h1}</h1><p>{intro}</p><div class="page-actions"><a class="btn btn-primary" href="{rel("/contact/", path)}">Request availability</a><a class="btn btn-secondary" href="{rel("/services/", path)}">Compare services</a></div></div></section>'''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{DOMAIN}{image}">
  <link rel="icon" href="{favicon}" type="image/svg+xml">
  <link rel="stylesheet" href="{css}">
  {schema_html}
</head>
<body>
  {header(path)}
  <main id="main">
    {hero_html}
    {body}
  </main>
  {footer(path)}
  <script src="{js}"></script>
</body>
</html>
'''

def checklist(items):
    return '<ul class="check-list">' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>'

def faq_block(items):
    cards = ''.join(f'<article class="faq-card reveal"><h2>{q}</h2><p>{a}</p></article>' for q, a in items)
    return f'<section class="section-pad"><div class="container faq-list">{cards}</div></section>'

def service_grid(current="/"):
    cards = ''.join(f'<a class="service-card reveal" href="{rel(href, current)}"><h3>{title}</h3><p>{text}</p></a>' for title, href, text in service_cards)
    return f'<div class="service-card-grid">{cards}</div>'

def write(path, html):
    target = ROOT / "index.html" if path == "/" else ROOT / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")

home_body = f'''
<section class="hero section-pad">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy reveal">
      <p class="eyebrow">Residential cleaning in Missouri</p>
      <h1>Practical house cleaning help for busy Missouri homes.</h1>
      <p class="hero-text">Shine Time Cleaners helps homeowners and renters keep kitchens, bathrooms, bedrooms, floors, and shared living spaces under control. This site is built to help you understand cleaning options before you request service, with checklists, estimated times, preparation tips, and honest scope guidance.</p>
      <div class="hero-actions"><a class="btn btn-primary" href="contact/">Request availability</a><a class="btn btn-secondary" href="house-cleaning-checklist/">Use the checklist</a></div>
      <div class="trust-strip"><span>Supplies provided</span><span>Missouri service focus</span><span>Clear cleaning scopes</span></div>
    </div>
    <div class="hero-visual reveal delay-1"><img src="images/hero.svg" alt="Clean and bright residential living room after a Shine Time cleaning visit"></div>
  </div>
</section>
<section class="section-pad"><div class="container split"><div class="section-intro reveal"><p class="eyebrow">Useful before you book</p><h2>Know what you are asking for before a cleaner arrives.</h2></div><div class="rich-copy reveal delay-1"><p>A lot of cleaning websites only say that they clean homes. Shine Time Cleaners explains what that means room by room, how long different visits may take, which tasks belong in standard cleaning, and when deep cleaning or move-out cleaning makes more sense.</p><p>Use the guides to compare service levels, set priorities, and avoid surprises. If you are in Missouri and comparing cleaning options in cities such as {", ".join(MISSOURI_CITIES[:5])}, the service area page explains how home type, traffic, weather, pets, and commute patterns can influence cleaning needs.</p></div></div></section>
<section class="section-pad about-band"><div class="container"><div class="section-heading reveal"><p class="eyebrow">Services</p><h2>Start with the cleaning situation that matches your home.</h2><p>Each guide includes included tasks, estimated timing, best-fit customers, preparation notes, and frequently asked questions.</p></div>{service_grid("/")}</div></section>
<section class="section-pad"><div class="container content-grid">
<article class="info-card wide reveal"><h2>Meet the team</h2><p>Shine Time Cleaners is presented as a small residential cleaning company, which means the work depends on communication, consistency, and respect inside a customer's home. As the public team roster grows, this section should be updated with real names, roles, and photos. For now, the site is clear about service standards, cleaning scope, and how customers can prepare.</p></article>
<article class="info-card reveal delay-1"><h2>Mission</h2><p>Help Missouri households enjoy cleaner, calmer homes through organized residential cleaning and plain-language service expectations.</p></article>
<article class="info-card reveal delay-2"><h2>Core values</h2>{checklist(["Respect the home and the people who live there.", "Explain what is included before the appointment.", "Bring supplies for typical residential cleaning.", "Focus on details that change how a room feels."])}</article>
</div></section>
<section class="section-pad"><div class="container"><div class="section-heading reveal"><p class="eyebrow">Placeholders marked clearly</p><h2>Examples of trust content to replace with real customer proof.</h2><p>AdSense and visitors both reward honesty. The examples below should be replaced only when real testimonials and project photos are available.</p></div><div class="testimonial-grid"><article class="testimonial-card reveal"><p>"The kitchen and bathrooms felt reset without needing us to provide supplies."</p><strong>Placeholder testimonial example</strong></article><article class="testimonial-card reveal delay-1"><p>"The checklist helped us decide between standard and deep cleaning."</p><strong>Placeholder testimonial example</strong></article><article class="testimonial-card reveal delay-2"><p>"The move-out scope made it easier to prepare for handing over keys."</p><strong>Placeholder testimonial example</strong></article></div><div class="gallery-grid"><div class="gallery-placeholder">Before photo placeholder</div><div class="gallery-placeholder">After photo placeholder</div><div class="gallery-placeholder">Kitchen detail placeholder</div><div class="gallery-placeholder">Bathroom detail placeholder</div></div></div></section>
<section class="cta-section section-pad"><div class="container"><div class="cta-panel reveal"><div><p class="eyebrow">Next step</p><h2>Tell us what your home needs.</h2><p>Share your home size, service type, timing, and highest-priority rooms so the request can be reviewed with useful context.</p></div><a class="btn btn-light" href="contact/">Request availability</a></div></div></section>
'''

write("/", page("Shine Time Cleaners | Residential Cleaning Guides and Services in Missouri", "Residential cleaning services and detailed home cleaning guides from Shine Time Cleaners, serving Missouri homeowners and renters with practical cleaning information.", "/", "Home", "Practical house cleaning help for busy Missouri homes.", "Compare services, read cleaning guides, and request residential cleaning availability from Shine Time Cleaners.", home_body, [faq_schema(faqs[:3])]))

about_body = f'''
<section class="section-pad"><div class="container content-grid">
<article class="info-card wide reveal"><h2>Company story</h2><p>Shine Time Cleaners was created around a simple problem: homes are used every day, but most families do not have unlimited time to keep every surface, fixture, floor, and corner fresh. The company focuses on residential cleaning because household spaces need a different kind of care than offices or retail properties. Kitchens collect food residue and fingerprints. Bathrooms need routine sanitation and buildup control. Bedrooms benefit from dust reduction and floor care. Entryways and living rooms show the pace of everyday life almost immediately.</p><p>The site has also been shaped as a resource. A homeowner should be able to read the service guides and understand the difference between routine maintenance, a deep reset, a move-out clean, and a pet-friendly plan before requesting availability.</p></article>
<article class="info-card reveal delay-1"><h2>Mission statement</h2><p>Our mission is to provide practical residential cleaning support that makes Missouri homes easier to live in, easier to maintain, and easier to enjoy.</p></article>
<article class="info-card reveal delay-2"><h2>What we believe</h2>{checklist(["Cleaning should have a clear scope.", "Customers deserve honest preparation guidance.", "A good visit starts with the right priorities.", "Trust is built through details, consistency, and communication."])}</article>
<article class="info-card reveal"><h2>Meet the team</h2><p>As Shine Time Cleaners grows, this page should include verified staff profiles. Until those public profiles are ready, the company is keeping the focus on the service process, the rooms cleaned, and the information customers need to make a good decision.</p></article>
<article class="info-card wide reveal delay-1"><h2>How we approach a home</h2><p>A first cleaning request is reviewed by asking practical questions: How many bedrooms and bathrooms are there? Are the floors mostly carpet, hard surface, or a mix? Are pets in the home? Is the service routine upkeep or a reset after months of buildup? Are there delicate materials or rooms that should be skipped? That information helps prevent vague promises and supports a more realistic plan.</p></article>
</div></section>{faq_block(faqs[:3])}
'''
write("/about/", page("About Us | Shine Time Cleaners", "Learn about Shine Time Cleaners, a Missouri residential cleaning company focused on clear scopes, practical home care, and useful cleaning guidance.", "/about/", "About us", "A residential cleaning company built around useful guidance and careful home care.", "Shine Time Cleaners focuses on real household needs: clean kitchens, fresher bathrooms, maintained floors, reduced dust, and clear expectations.", about_body, [faq_schema(faqs[:3])]))

why_body = f'''
<section class="section-pad"><div class="container content-grid">
<article class="info-card wide reveal"><h2>Why homeowners choose a cleaner</h2><p>Most people do not hire a cleaner because they dislike their home. They hire help because work, family, pets, weather, errands, and moves all compete for the same time. Professional cleaning is useful when it removes friction: bathrooms are ready for guests, kitchen counters are easier to use, floors feel better underfoot, and dust does not keep creeping from one room to another.</p></article>
<article class="info-card reveal"><h2>Clear service scope</h2><p>Each service guide explains what is typically included, what may need extra time, and how to choose the right level of cleaning.</p></article>
<article class="info-card reveal delay-1"><h2>Supplies provided</h2><p>Shine Time Cleaners brings supplies for typical residential cleaning, which makes the appointment easier for customers to prepare for.</p></article>
<article class="info-card reveal delay-2"><h2>Room-by-room thinking</h2><p>Cleaning plans are organized around kitchens, bathrooms, bedrooms, living spaces, floors, dusting, and priority areas.</p></article>
<article class="info-card reveal"><h2>Missouri home awareness</h2><p>Missouri homes deal with seasonal pollen, muddy spring entryways, winter salt residue, humid bathrooms, pet hair, and heavy-use kitchens.</p></article>
<article class="info-card reveal delay-1"><h2>Honest trust content</h2><p>Testimonials and gallery examples are labeled until real reviews and project photos are available. That protects visitors from misleading claims.</p></article>
<article class="info-card reveal delay-2"><h2>Preparation help</h2><p>Checklists help customers clear clutter, identify fragile items, and share access notes before a visit.</p></article>
</div></section>
<section class="section-pad about-band"><div class="container"><div class="section-heading reveal"><p class="eyebrow">Example testimonials</p><h2>Replace these with verified customer reviews when available.</h2></div><div class="testimonial-grid"><article class="testimonial-card reveal"><p>"The service guide made it easy to understand what belonged in a deep cleaning request."</p><strong>Placeholder testimonial example</strong></article><article class="testimonial-card reveal delay-1"><p>"We liked having clear prep steps before asking for a quote."</p><strong>Placeholder testimonial example</strong></article><article class="testimonial-card reveal delay-2"><p>"The room checklist helped us focus on bathrooms and floors first."</p><strong>Placeholder testimonial example</strong></article></div></div></section>
'''
write("/why-choose-us/", page("Why Choose Shine Time Cleaners | Residential Cleaning Trust and Process", "See why Missouri homeowners may choose Shine Time Cleaners for clear residential cleaning scopes, supplied materials, room-by-room planning, and practical guidance.", "/why-choose-us/", "Why choose us", "Clear cleaning guidance, realistic expectations, and respect for the home.", "Choosing a cleaner is easier when the business explains how service works before asking you to book.", why_body))

services_body = f'''
<section class="section-pad"><div class="container"><div class="section-heading reveal"><p class="eyebrow">Service overview</p><h2>Residential cleaning options explained in plain language.</h2><p>This page summarizes each service and links to detailed guides with checklists, time estimates, and best-fit situations.</p></div>{service_grid("/services/")}</div></section>
<section class="section-pad about-band"><div class="container service-list">
<article class="service-detail reveal"><img src="../images/kitchen.svg" alt="Clean kitchen counters and sink after residential cleaning"><div><h2>Standard Cleaning</h2><p>Standard cleaning is routine upkeep for homes that are already reasonably maintained. It typically covers kitchens, bathrooms, bedrooms, living areas, dusting, vacuuming, and mopping. Estimated time is often 2 to 5 hours depending on home size and condition.</p>{checklist(["Kitchen counters, sinks, tables, and appliance exteriors.", "Bathroom mirrors, sinks, tubs, showers, toilets, and floors.", "Bedroom dusting, floor care, and light straightening.", "Living room dusting, touch points, vacuuming, and mopping."])}<a class="text-link" href="../standard-cleaning-guide/">Read the standard cleaning guide</a></div></article>
<article class="service-detail reveal"><img src="../images/supplies.svg" alt="Cleaning supplies prepared for a deep cleaning appointment"><div><h2>Deep Cleaning</h2><p>Deep cleaning is for homes that need a reset. It may include more detailed attention to buildup, edges, baseboards, fixtures, reachable cabinet fronts, and high-use rooms. Estimated time is often 4 to 8+ hours.</p>{checklist(["Best before recurring service begins.", "Useful after illness, hosting, renovations, or heavy use.", "Prioritizes kitchens, bathrooms, dust buildup, and floor edges.", "May require a larger time block than standard cleaning."])}<a class="text-link" href="../deep-cleaning-guide/">Read the deep cleaning guide</a></div></article>
<article class="service-detail reveal"><img src="../images/hero.svg" alt="Empty room prepared for move-out cleaning"><div><h2>Move-Out Cleaning</h2><p>Move-out cleaning helps prepare a home for turnover, listing, landlord walkthroughs, or new occupants. Estimated time can range from 4 hours to a full day depending on size, vacancy, and buildup.</p>{checklist(["Empty-room floor and surface cleaning.", "Kitchen and bathroom reset work.", "Attention to closets, cabinets, and appliance exteriors when included.", "Best scheduled after most belongings are removed."])}<a class="text-link" href="../move-out-cleaning-guide/">Read the move-out cleaning guide</a></div></article>
<article class="service-detail reveal"><img src="../images/bedroom.svg" alt="Bedroom cleaned with pet-friendly household care in mind"><div><h2>Pet-Friendly Cleaning</h2><p>Pet-friendly cleaning focuses on hair, paw prints, tracked-in dirt, odor-prone areas, and surfaces pets frequently touch. Estimated time depends on shedding, flooring, furniture access, and how many pet areas are included.</p>{checklist(["Vacuuming pet-heavy rooms and traffic paths.", "Wiping baseboards, door areas, and washable touch points.", "Focusing on entryways, couches nearby, and feeding zones.", "Discussing products, allergies, and pet safety needs in advance."])}<a class="text-link" href="../pet-friendly-cleaning/">Read the pet-friendly cleaning guide</a></div></article>
</div></section>{faq_block(faqs)}
'''
write("/services/", page("Residential Cleaning Services | Shine Time Cleaners", "Compare standard cleaning, deep cleaning, move-out cleaning, pet-friendly cleaning, room checklists, estimated times, and service fit from Shine Time Cleaners.", "/services/", "Services", "Residential cleaning services for the rooms you use every day.", "Use this page to choose the right service level before requesting availability.", services_body, [faq_schema(faqs)]))

service_area_body = '<section class="section-pad"><div class="container content-grid">'
city_text = {
    "St. Louis": "Older homes, apartments, and busy neighborhoods can create a mix of dust, entryway grit, and high-use kitchens. Cleaning plans often focus on bathrooms, floors, and surface dust before guests or workweeks.",
    "Kansas City": "Larger suburban homes and active family schedules often benefit from recurring standard cleaning, seasonal deep cleaning, and floor care after wet or snowy weather.",
    "Springfield": "Homes around Springfield may need practical upkeep for kitchens, bathrooms, bedrooms, and mudroom-style entry points after outdoor activity.",
    "Columbia": "Student rentals, apartments, and family homes can need move-out support, apartment cleaning, and flexible room priorities around changing schedules.",
    "Independence": "Residential cleaning requests often include bathrooms, kitchens, hard floors, and high-traffic family spaces that collect dust and tracked-in debris.",
    "Lee's Summit": "Larger homes may benefit from zone-based cleaning plans that rotate deep detail tasks while keeping kitchens and bathrooms on a regular rhythm.",
    "St. Charles": "Historic properties, townhomes, and family homes can require careful attention to floor transitions, dust-prone trim, and guest-ready common areas.",
    "O'Fallon": "Growing households often ask for recurring upkeep, pet-friendly cleaning, and seasonal resets for kitchens, baths, bedrooms, and open living areas.",
}
for city in MISSOURI_CITIES:
    service_area_body += f'<article class="info-card reveal"><h2>{city}</h2><p>{city_text[city]}</p><p>Availability depends on scheduling, travel time, and the service scope requested.</p></article>'
service_area_body += '</div></section><section class="cta-section section-pad"><div class="container"><div class="cta-panel reveal"><div><p class="eyebrow">Missouri service requests</p><h2>Ask about availability in your city.</h2><p>Include your city, ZIP code, home type, preferred timing, and priority rooms so service fit can be reviewed clearly.</p></div><a class="btn btn-light" href="../contact/">Contact Shine Time</a></div></div></section>'
write("/service-areas/", page("Service Areas in Missouri | Shine Time Cleaners", "Learn how Shine Time Cleaners approaches residential cleaning requests across Missouri cities including St. Louis, Kansas City, Springfield, Columbia, and nearby communities.", "/service-areas/", "Service areas", "Residential cleaning guidance for Missouri homes and apartments.", "Shine Time Cleaners focuses on Missouri residential cleaning requests. This page explains how local home types and seasonal conditions can shape cleaning needs.", service_area_body))

def guide_page(path, title, desc, label, h1, intro, sections, guide_faqs):
    body = '<section class="section-pad"><div class="container article-content reveal">'
    for h, paras, items in sections:
        body += f'<h2>{h}</h2>' + ''.join(f'<p>{p}</p>' for p in paras)
        if items:
            body += checklist(items)
    body += '</div></section>' + faq_block(guide_faqs)
    write(path, page(title, desc, path, label, h1, intro, body, [faq_schema(guide_faqs)]))

guide_page("/standard-cleaning-guide/", "Standard Cleaning Guide | Shine Time Cleaners", "A practical standard cleaning guide with included tasks, room-by-room checklist, estimated timing, best-fit homes, and FAQs.", "Standard cleaning guide", "What standard cleaning includes, how long it takes, and who it helps most.", "Standard cleaning is maintenance cleaning for homes that need a dependable refresh, not a full reset.", [
("Who standard cleaning is for", ["Standard cleaning is best for households that keep up with basic tidying but need help with recurring dust, bathroom use, kitchen mess, and floors. It suits weekly, biweekly, or monthly visits, especially when the home is not heavily cluttered and surfaces are accessible.", "A standard visit is not meant to remove months of buildup or handle every hidden detail. It works best when the customer chooses priorities and the home is ready enough for cleaners to reach surfaces."], ["Busy families needing recurring upkeep.", "Apartment residents who want bathrooms, kitchens, and floors refreshed.", "Homeowners preparing for a normal week, guests, or routine maintenance."]),
("Estimated cleaning time", ["A small apartment may take about 2 to 3 hours. A medium home may take 3 to 5 hours. Larger homes, extra bathrooms, pet hair, heavy kitchen use, or cluttered surfaces can add time. The first visit can take longer because dust and buildup are usually heavier before a recurring rhythm is established."], None),
("Room-by-room checklist", ["The checklist below describes common standard cleaning tasks. Final scope depends on access, time, home condition, and customer priorities."], ["Kitchen: wipe counters, sinks, faucets, tables, backsplashes, and appliance exteriors.", "Bathrooms: clean mirrors, vanities, sinks, toilets, tubs, showers, fixtures, and floors.", "Bedrooms: dust accessible furniture, vacuum or mop floors, and refresh visible touch points.", "Living areas: dust tables, shelves, ledges, and decor; vacuum rugs; mop hard floors.", "Entryways: remove tracked-in debris, wipe reachable surfaces, and clean floors."]),
("How to prepare", ["Pick up laundry, papers, toys, and dishes where possible. Secure valuables, note fragile items, and share rooms that should be skipped. Preparation helps more appointment time go toward cleaning rather than moving belongings."], None),
], [("Is standard cleaning enough for a first visit?", "Sometimes, but many first visits need deep cleaning if there is visible buildup, heavy dust, or neglected kitchen and bathroom details."), ("Can I rotate tasks?", "Yes. Recurring customers can rotate detail tasks such as baseboards, guest rooms, or extra dusting when time allows."), ("Are supplies included?", "Yes, supplies for typical residential cleaning are provided.")])

guide_page("/deep-cleaning-guide/", "Deep Cleaning Guide | Shine Time Cleaners", "Deep cleaning guide for Missouri homes with detailed checklists, estimated times, best-fit situations, preparation tips, and FAQs.", "Deep cleaning guide", "A deeper reset for buildup, busy seasons, and homes that need extra attention.", "Deep cleaning gives more time to the details that standard cleaning may not fully reach.", [
("Who deep cleaning is for", ["Deep cleaning is useful before starting recurring service, after a long gap between cleanings, before hosting, after illness, during seasonal resets, or when kitchens and bathrooms need more than a quick maintenance pass.", "It is also a good choice when dust has settled on baseboards, fixtures look dull, bathroom buildup is visible, or floors need extra edge attention."], ["First-time residential cleaning customers.", "Homes with heavy bathroom or kitchen use.", "Households preparing for guests, events, or seasonal changes."]),
("Estimated cleaning time", ["Deep cleaning often takes 4 to 8 hours or more. Large homes, multiple bathrooms, pet hair, clutter, or move-related tasks can require additional time. A realistic deep clean may need priorities: bathrooms and kitchen first, then floors, then detail dusting."], None),
("Deep cleaning checklist", ["A deep cleaning plan expands standard cleaning by adding more detailed attention where buildup is common."], ["Kitchen: cabinet fronts, appliance exteriors, sink detail, backsplash splashes, counter edges, and floor edges.", "Bathrooms: fixtures, shower buildup, tub edges, toilet bases, mirror polishing, vanity fronts, and floor corners.", "Bedrooms: lamps, nightstands, reachable decor, baseboards when included, and floor edges.", "Living spaces: deeper dusting, fingerprints, entryway buildup, furniture edges, and high-touch surfaces.", "Laundry and utility areas: exterior surfaces, dust-prone ledges, and hard floors when included."]),
("What deep cleaning does not automatically include", ["Interior ovens, interior refrigerators, window tracks, heavy mold remediation, hoarding cleanup, pest contamination, and biohazard cleanup require separate discussion or specialized providers. Clear boundaries help keep the appointment realistic and safe."], None),
], [("Should I book deep cleaning before recurring service?", "If the home has visible buildup, a deep first visit usually creates a better baseline for future standard cleaning."), ("Can deep cleaning be limited to certain rooms?", "Yes. Many customers prioritize kitchens, bathrooms, or floors first."), ("How should I prepare?", "Clear clutter from surfaces, move personal items from tubs and counters, and share any delicate-surface instructions.")])

guide_page("/move-out-cleaning-guide/", "Move-Out Cleaning Guide | Shine Time Cleaners", "Move-out cleaning guide with turnover checklist, best timing, estimated duration, room priorities, and FAQs for homes and apartments.", "Move-out cleaning guide", "A practical cleaning plan for handing over keys, listing a home, or moving in.", "Move-out cleaning works best after belongings are removed and utilities are still on.", [
("Who move-out cleaning is for", ["Move-out cleaning is intended for renters, homeowners, landlords, property managers, and sellers who need a home cleaned after most belongings are gone. It can also help before moving into a new place if the prior condition is unknown.", "The goal is not to repair damage or guarantee deposit outcomes. The goal is to clean reachable surfaces, rooms, fixtures, floors, and visible residue within an agreed scope."], ["Renters preparing for a walkthrough.", "Homeowners listing a property.", "Families moving into a home that needs a reset.", "Landlords preparing a residential unit for the next occupant."]),
("Estimated cleaning time", ["An apartment may take 3 to 6 hours. A house may take 5 hours to a full day or longer depending on size and condition. Empty homes can be easier to access, but heavy buildup, trash, adhesive residue, or appliance interiors can add time."], None),
("Move-out checklist", ["A useful move-out clean focuses on the rooms a new occupant will inspect first."], ["Kitchen: counters, sinks, faucets, cabinet exteriors, appliance exteriors, backsplash, and floors.", "Bathrooms: toilets, tubs, showers, vanities, mirrors, fixtures, shelves, and floors.", "Bedrooms and living areas: dusting, floors, closets when included, ledges, and touch points.", "Entryways and halls: baseboards when included, floor edges, doors, handles, and visible marks.", "Final pass: remove obvious dust, crumbs, and tracked-in debris from cleaned areas."]),
("Scheduling tips", ["Schedule cleaning after movers have removed most belongings but before utilities are turned off. Leave access instructions, parking notes, trash rules, and any landlord requirements. If carpets are being professionally cleaned, coordinate the order so floors are not dirtied afterward."], None),
], [("Do you guarantee a security deposit return?", "No cleaner can guarantee a landlord decision, but a thorough move-out clean can help address common walkthrough concerns."), ("Should the home be empty?", "Empty or nearly empty is best because cleaners can reach more surfaces and floors."), ("Can appliance interiors be included?", "They should be requested specifically because they can add significant time.")])

guide_page("/pet-friendly-cleaning/", "Pet-Friendly Cleaning Guide | Shine Time Cleaners", "Pet-friendly home cleaning guide covering hair, paw prints, odors, feeding zones, estimated timing, preparation, and FAQs.", "Pet-friendly cleaning", "Cleaning strategies for homes with dogs, cats, and everyday pet mess.", "Pet-friendly cleaning is about practical household care: hair, tracked-in dirt, washable surfaces, and odor-prone spaces.", [
("Who pet-friendly cleaning is for", ["This service focus is for homes where pets live indoors, shed on floors or furniture-adjacent spaces, track dirt through entryways, or create extra cleaning needs around feeding areas and litter zones.", "Customers should always share pet safety notes, product restrictions, allergies, and whether pets will be secured during the appointment."], ["Homes with shedding dogs or cats.", "Apartments with litter areas or compact pet zones.", "Families with muddy entryways or pet traffic paths."]),
("Estimated cleaning time", ["Pet-heavy homes often take longer than similar homes without pets. Add time for hair removal from floor edges, repeated vacuum passes, entryway cleanup, and baseboard wiping. A small home may add 30 to 60 minutes; larger homes or heavy shedding can add more."], None),
("Pet-focused checklist", ["The checklist prioritizes areas where pet mess usually affects daily comfort."], ["Vacuum carpets, rugs, furniture-adjacent floors, and traffic paths.", "Clean hard floors around doors, feeding areas, and litter zones.", "Wipe washable baseboards, door areas, and reachable marks when included.", "Dust surfaces where pet hair settles.", "Discuss odor-prone rooms, product limits, and pet containment before service."]),
("Preparation tips", ["Secure pets in a safe room, crate, or off-site location if needed. Pick up toys, bowls, and loose bedding unless they are part of the agreed cleaning area. Share whether a pet is nervous, reactive, likely to escape, or sensitive to sound."], None),
], [("Do you use pet-safe products?", "Share pet needs and product restrictions before service so product choices can be discussed."), ("Can you clean litter boxes?", "Litter box handling should be discussed separately and is not assumed in standard cleaning."), ("Should pets be home during cleaning?", "Pets should be secured if they may be stressed, escape, or interfere with cleaning.")])

guide_page("/seasonal-cleaning-tips/", "Seasonal Cleaning Tips for Missouri Homes | Shine Time Cleaners", "Seasonal Missouri cleaning tips for pollen, humidity, mud, winter residue, guest prep, and room-by-room maintenance.", "Seasonal tips", "How Missouri seasons change what your home needs cleaned.", "Missouri weather can change the cleaning priorities inside a home from month to month.", [
("Spring cleaning", ["Spring often brings pollen, rain, mud, and open windows. Entryways, window ledges, baseboards, and floors may need extra attention. Kitchens and bathrooms also benefit from a reset after winter routines."], ["Wipe window ledges and reachable dusty trim.", "Clean entry mats and hard floors.", "Prioritize bathrooms where humidity begins to rise.", "Dust bedrooms and living rooms after pollen-heavy weeks."]),
("Summer cleaning", ["Summer can mean guests, kids at home, humidity, and more frequent bathroom use. Focus on kitchens, bathrooms, trash areas, and floors that feel sticky or dull."], ["Clean appliance exteriors and counters more often.", "Keep bathroom surfaces dry and refreshed.", "Mop entryways and kitchens after outdoor activity.", "Rotate dusting around fans and vents when reachable."]),
("Fall cleaning", ["Fall is a good time to reset before holidays. Guest rooms, dining areas, kitchens, bathrooms, and entryways often become more important."], ["Refresh guest bedrooms.", "Deep clean bathrooms before hosting.", "Wipe dining surfaces and chairs.", "Clean floors before heavy indoor season."]),
("Winter cleaning", ["Winter brings salt, moisture, boots, and more time indoors. Entryways and hard floors often need extra care, while dust can collect quickly in closed-up rooms."], ["Protect entry floors from wet shoes.", "Vacuum rugs and traffic paths.", "Dust bedrooms and living spaces.", "Keep kitchens ready for holiday cooking."]),
], [("How often should seasonal cleaning happen?", "Many homes benefit from a deeper reset two to four times per year, with standard cleaning in between."), ("Is seasonal cleaning the same as deep cleaning?", "It can be, but seasonal cleaning usually targets weather-related and hosting-related priorities."), ("What season is hardest on Missouri homes?", "Spring and winter often create the most visible floor and entryway issues.")])

guide_page("/house-cleaning-checklist/", "House Cleaning Checklist | Shine Time Cleaners", "Room-by-room house cleaning checklist for homeowners comparing cleaning services, preparing for a visit, or maintaining a cleaner home.", "House checklist", "A room-by-room checklist for a cleaner, more manageable home.", "Use this checklist to prepare for service or organize your own cleaning priorities.", [
("Kitchen checklist", ["The kitchen usually has the highest mix of crumbs, grease, water spots, fingerprints, and traffic. Start here if the home needs to feel usable quickly."], ["Clear dishes and food items.", "Wipe counters, backsplashes, tables, cabinet fronts, and appliance exteriors.", "Clean sink, faucet, and visible splash areas.", "Vacuum or sweep, then mop hard floors."]),
("Bathroom checklist", ["Bathrooms need both surface cleaning and detail attention. Remove personal items from counters and tubs before a scheduled visit."], ["Clean mirror, sink, counter, toilet, tub, shower, and fixtures.", "Wipe reachable shelves, ledges, and cabinet fronts.", "Empty small trash cans when included.", "Vacuum and mop floors."]),
("Bedroom checklist", ["Bedrooms benefit from dust reduction and floor care. Laundry and personal clutter should be picked up before a professional visit."], ["Dust nightstands, dressers, lamps, and reachable decor.", "Vacuum carpet or mop hard floors.", "Wipe high-touch surfaces.", "Lightly straighten accessible areas when included."]),
("Living area checklist", ["Shared spaces collect daily evidence of meals, pets, guests, and family routines."], ["Dust tables, shelves, electronics-adjacent surfaces, and decor.", "Vacuum rugs, traffic paths, and furniture-adjacent floors.", "Mop hard floors.", "Clean fingerprints on reachable touch points."]),
], [("Should I clean before the cleaner comes?", "You do not need to clean, but picking up clutter helps the appointment focus on actual cleaning."), ("What should I prioritize?", "Kitchens, bathrooms, and floors usually create the biggest visible improvement."), ("Can this checklist be customized?", "Yes. Use it as a starting point and remove tasks that do not fit your home.")])

guide_page("/apartment-cleaning-checklist/", "Apartment Cleaning Checklist | Shine Time Cleaners", "Apartment cleaning checklist for renters, students, move-outs, small spaces, kitchens, bathrooms, floors, and recurring upkeep.", "Apartment checklist", "A compact-space checklist for apartments, condos, and townhomes.", "Apartments can be smaller than houses, but high-use rooms can get dirty just as quickly.", [
("Small-space strategy", ["In apartments, clutter and surface buildup are more visible because rooms are closer together. Cleaning works best when counters, floors, and bathrooms are prioritized first."], ["Clear counters, tabletops, and bathroom vanities.", "Start with kitchen and bathroom sanitation.", "Vacuum traffic paths and rugs.", "Mop kitchen, bathroom, and entry floors."]),
("Apartment kitchen checklist", ["Apartment kitchens often have compact counters and heavy appliance use. Even a quick reset can make the whole unit feel cleaner."], ["Wipe counters, sink, faucet, backsplash, and appliance exteriors.", "Clean cabinet fronts near handles.", "Remove crumbs around tables and prep areas.", "Sweep or vacuum and mop hard floors."]),
("Apartment bathroom checklist", ["A single apartment bathroom can see daily use from everyone in the household, so mirrors, sinks, toilets, tubs, and floors should stay high on the list."], ["Clean mirror, vanity, sink, faucet, toilet, tub, and shower.", "Wipe shelves and reachable ledges.", "Remove hair and buildup from visible areas.", "Mop floors and wipe base areas when included."]),
("Move-out apartment notes", ["For move-outs, ask what the lease or property manager expects. Interior appliances, cabinet interiors, balcony areas, or carpet cleaning may require separate scheduling."], None),
], [("How long does apartment cleaning take?", "A small apartment may take 2 to 3 hours for standard cleaning, while move-out or deep cleaning may take longer."), ("Can you clean before a lease inspection?", "Move-out cleaning can help prepare, but lease requirements should be shared in advance."), ("Do apartments need deep cleaning?", "Yes, especially before moving out, after a long gap, or when bathrooms and kitchens have buildup.")])

pricing_body = '''
<section class="section-pad"><div class="container"><div class="note-box reveal"><h2>Pricing depends on the work, not just square footage.</h2><p>Residential cleaning estimates should account for home size, room count, number of bathrooms, flooring, pets, clutter, condition, service frequency, and special instructions. A lightly used 1,500 square foot home can take less time than a smaller apartment with heavy kitchen buildup or a move-out deadline.</p></div><div class="price-grid price-guide"><article class="price-card reveal"><h3>Standard cleaning</h3><span class="price">2-5 hours typical</span><p>Best for routine upkeep when surfaces are reachable and buildup is moderate.</p></article><article class="price-card reveal delay-1"><h3>Deep cleaning</h3><span class="price">4-8+ hours typical</span><p>Best for first visits, seasonal resets, heavy dust, and detailed kitchen or bathroom needs.</p></article><article class="price-card reveal delay-2"><h3>Move-out cleaning</h3><span class="price">4 hours-full day</span><p>Best when a home or apartment is empty or nearly empty and needs turnover cleaning.</p></article></div></div></section>
<section class="section-pad about-band"><div class="container content-grid"><article class="info-card reveal"><h2>What lowers time</h2><p>Clear counters, picked-up floors, accessible bathrooms, regular maintenance, and a prioritized checklist can reduce the time needed.</p></article><article class="info-card reveal delay-1"><h2>What adds time</h2><p>Heavy buildup, pet hair, many bathrooms, delicate surfaces, cluttered rooms, and appliance interiors can increase time.</p></article><article class="info-card reveal delay-2"><h2>How to request an estimate</h2><p>Include city, home type, approximate square footage, bedrooms, bathrooms, service type, pets, and top priorities.</p></article></div></section>
'''
write("/pricing/", page("Residential Cleaning Pricing Guide | Shine Time Cleaners", "Understand residential cleaning pricing factors, estimated cleaning times, service scope, and how to request a useful estimate.", "/pricing/", "Pricing guide", "Cleaning prices make more sense when the scope is clear.", "Use this pricing guide to understand what affects a residential cleaning estimate before requesting availability.", pricing_body))

contact_body = f'''
<section class="section-pad"><div class="container split"><div class="contact-panel reveal"><span class="status-pill">Request availability</span><h2>Send a residential cleaning request</h2><p>Email is the current published contact method for Shine Time Cleaners. Replace this address with your preferred business mailbox if different before submitting for review.</p><a class="btn btn-primary" href="mailto:{EMAIL}?subject=Residential%20Cleaning%20Request">Email {EMAIL}</a><p class="fine-print">Suggested message details: name, city, ZIP code, home type, square footage, bedrooms, bathrooms, pets, service type, preferred timing, and priority rooms.</p></div><div class="info-card reveal delay-1"><h2>Business hours</h2>{checklist(["Monday-Friday: 8:00 AM-6:00 PM", "Saturday: 9:00 AM-2:00 PM", "Sunday: Closed", "Availability may vary by city, travel time, and service scope."])}<h2>Request form worksheet</h2><p>If your email client opens, paste the details below into your message.</p></div></div></section>
<section class="section-pad about-band"><div class="container"><form class="contact-form reveal" action="mailto:{EMAIL}" method="post" enctype="text/plain"><label>Name<input name="name" autocomplete="name"></label><label>Email<input name="email" type="email" autocomplete="email"></label><label>City and ZIP<input name="location"></label><label>Service type<select name="service"><option>Standard cleaning</option><option>Deep cleaning</option><option>Move-out cleaning</option><option>Pet-friendly cleaning</option><option>Custom plan</option></select></label><label>Home details<textarea name="details" rows="6" placeholder="Approximate square footage, bedrooms, bathrooms, pets, timing, and priority rooms"></textarea></label><button class="btn btn-primary" type="submit">Prepare email request</button></form></div></section>
'''
write("/contact/", page("Contact Shine Time Cleaners | Request Residential Cleaning in Missouri", "Contact Shine Time Cleaners to request residential cleaning availability. Include city, home size, service type, pets, schedule, and priority rooms.", "/contact/", "Contact", "Request residential cleaning availability with the details that matter.", "A clear request helps Shine Time Cleaners understand your home, priorities, and service fit.", contact_body))

faq_body = faq_block(faqs + [
("What is the difference between standard and deep cleaning?", "Standard cleaning maintains a home that is already in reasonable condition. Deep cleaning gives more time to buildup, edges, fixtures, baseboards when included, and heavily used rooms."),
("Do you serve all of Missouri?", "Service availability depends on scheduling, travel time, and the exact location. The service areas page explains Missouri cities and nearby communities that may be relevant to service requests."),
("Can I request only bathrooms and floors?", "Yes. Custom priorities can focus on the rooms that matter most, although the estimate should reflect the time and detail required."),
("Do you provide exact online prices?", "The site explains timing and pricing factors because exact pricing depends on home details, condition, and requested scope."),
("Do you clean interior appliances?", "Interior ovens and refrigerators should be requested specifically because they add time and may require special preparation."),
("How should I prepare for move-out cleaning?", "Remove belongings, keep utilities on, share access instructions, and provide any landlord or property manager checklist."),
("Can cleaning happen while I am away?", "Access arrangements should be discussed in advance. Customers should secure valuables, pets, alarms, and entry instructions."),
("What if I have allergies or product restrictions?", "Mention allergies, sensitivities, preferred products, and restricted surfaces before service so the plan can be reviewed."),
])
write("/frequently-asked-questions/", page("Frequently Asked Questions | Shine Time Cleaners", "Answers to residential cleaning questions about supplies, timing, deep cleaning, move-out cleaning, pets, service areas, preparation, and pricing.", "/frequently-asked-questions/", "FAQ", "Answers to common residential cleaning questions.", "Use these answers to understand services, timing, preparation, and expectations before requesting availability.", faq_body, [faq_schema(faqs)]))
write("/faq/", page("Residential Cleaning FAQ | Shine Time Cleaners", "Answers to common questions about Shine Time Cleaners residential cleaning services, supplies, pricing, timing, and preparation.", "/faq/", "FAQ", "Residential cleaning questions, answered clearly.", "This page is kept for visitors who use the shorter FAQ address.", faq_body, [faq_schema(faqs)]))

privacy_body = '''
<section class="section-pad"><div class="container policy-content reveal"><p><strong>Effective date:</strong> August 2, 2026</p><h2>Overview</h2><p>Shine Time Cleaners respects visitor privacy. This website provides residential cleaning information, service guides, contact options, and business details. The site may use hosting logs, analytics, cookies, security tools, and advertising services such as Google AdSense if enabled.</p><h2>Information collected automatically</h2><p>Technical data may include IP address, browser type, device type, pages viewed, referring page, approximate location derived from IP address, and dates or times of visits. This information helps operate, secure, and improve the website.</p><h2>Information visitors provide</h2><p>If a visitor sends an email or uses a mailto contact form, they may provide name, email address, city, home details, service interests, scheduling preferences, and notes about pets or surfaces. This information is used to respond to the request and evaluate service availability.</p><h2>Cookies and advertising</h2><p>If Google AdSense or analytics tools are enabled, third parties may use cookies or similar technologies to measure traffic, personalize or limit ads where allowed, and report performance. Visitors can manage cookies through browser settings and Google advertising controls.</p><h2>Sharing</h2><p>Information may be shared with providers that support hosting, email, analytics, security, advertising, or business operations. Information may also be disclosed if required by law or to protect rights and safety.</p><h2>Security and retention</h2><p>No website can guarantee perfect security. Information is kept only as long as reasonably useful for business, legal, security, and customer-service purposes.</p><h2>Contact</h2><p>Privacy questions can be sent to contact@shinetimecleanersllc.com.</p></div></section>
'''
write("/privacy/", page("Privacy Policy | Shine Time Cleaners", "Privacy Policy for Shine Time Cleaners covering website data, contact requests, cookies, analytics, advertising, retention, and user choices.", "/privacy/", "Privacy", "How this website handles privacy, cookies, analytics, and ads.", "This policy explains how visitor information may be collected and used when browsing or contacting Shine Time Cleaners.", privacy_body))

terms_body = '''
<section class="section-pad"><div class="container policy-content reveal"><p><strong>Effective date:</strong> August 2, 2026</p><h2>Use of this website</h2><p>This website provides general residential cleaning information, service descriptions, checklists, and contact options. The content is for informational purposes and does not create a service agreement by itself.</p><h2>Service requests</h2><p>Submitting an email or contact request does not guarantee availability, pricing, or appointment confirmation. Service details, timing, access, and scope must be reviewed and agreed before work begins.</p><h2>Cleaning scope</h2><p>Tasks described on this site are examples of common residential cleaning work. Final scope may vary based on home condition, safety, access, product restrictions, customer priorities, and time available.</p><h2>Customer responsibilities</h2><p>Customers should provide accurate home details, disclose fragile or restricted surfaces, secure valuables, provide safe access, manage pets, and identify areas that should not be cleaned.</p><h2>Limitations</h2><p>Shine Time Cleaners does not claim to provide restoration, remediation, pest cleanup, hazardous waste cleanup, medical cleaning, construction cleanup, or guaranteed stain removal unless separately agreed in writing.</p><h2>Website content</h2><p>All site content is owned by Shine Time Cleaners unless otherwise noted. Placeholder testimonials and gallery areas are clearly labeled and should be replaced only with verified customer content.</p><h2>Contact</h2><p>Questions about these terms can be sent to contact@shinetimecleanersllc.com.</p></div></section>
'''
write("/terms-of-service/", page("Terms of Service | Shine Time Cleaners", "Terms of Service for Shine Time Cleaners covering website use, service requests, cleaning scope, customer responsibilities, and limitations.", "/terms-of-service/", "Terms", "Terms for using this website and requesting cleaning services.", "These terms explain how website information and residential cleaning requests should be understood.", terms_body))

urls = ["/", "/about/", "/why-choose-us/", "/services/", "/service-areas/", "/standard-cleaning-guide/", "/deep-cleaning-guide/", "/move-out-cleaning-guide/", "/pet-friendly-cleaning/", "/seasonal-cleaning-tips/", "/house-cleaning-checklist/", "/apartment-cleaning-checklist/", "/pricing/", "/frequently-asked-questions/", "/faq/", "/contact/", "/privacy/", "/terms-of-service/"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}{u}</loc></url>\n' for u in urls) + '</urlset>\n', encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")

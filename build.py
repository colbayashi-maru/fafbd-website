#!/usr/bin/env python3
"""
Generates every page of firstassetfinancial.com into public/.

    python3 build.py

Nothing under public/ is hand-maintained except assets/ — the HTML is all
written from here, so there is no hand-kept page that can drift away from
the shell. Firm-wide facts are the constants directly below and are used by
the header, the footer, the page bodies and the JSON-LD; change the constant,
not the eight places it appears.

Regulatory facts (CRD, SEC number, state count, office) are taken from FINRA
BrokerCheck for CRD 139107, not from the previous website. Where the copy
makes a statement about how the firm operates, that statement is sourced to
the firm's own filed Form CRS. See content/COMPLIANCE.md.
"""

import hashlib
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'public')
CONTENT = os.path.join(HERE, 'content')

# --------------------------------------------------------------------------
# Firm-wide facts
# --------------------------------------------------------------------------

SITE = 'https://firstassetfinancial.com'

FIRM = 'First Asset Financial Inc.'
SHORT = 'First Asset Financial'

PHONE = '(800) 825-5511'
PHONE_URI = '+18008255511'
OFFICE_PHONE = '(785) 825-5050'          # BrokerCheck main office; Form CRS compliance line
OFFICE_PHONE_URI = '+17858255050'
FAX = '(785) 823-9207'
EMAIL = 'FAF@FirstAssetFinancial.com'

STREET = '110 E. Iron Ave.'
CITY = 'Salina'
STATE = 'KS'
ZIP = '67401'
PO_BOX = 'P.O. Box 1364'
PO_ZIP = '67402-1364'

CRD = '139107'
SEC_NO = '8-67191'
BROKERCHECK = 'https://brokercheck.finra.org/firm/summary/' + CRD
SEC_REGISTERED_SINCE = 'June 2006'
INCORPORATED = 'Kansas in 2005'
STATE_COUNT = '23'
CLEARING_FIRM = 'Hilltop Securities Inc.'
PRESIDENT = 'Bob Hamman'

# The firm restricted its securities business in 2026 to annuities, registered
# index-linked annuities and variable universal life. It no longer places
# mutual funds, ETFs or individual securities of any kind.
#
# "Full-service" was true of the old business and is not true of this one, so
# it appears nowhere. These two strings are what replaced it, and they are used
# in the footer, the hero, the JSON-LD and every meta description — change them
# here, not in the eight places they appear. See content/COMPLIANCE.md.
WHAT_WE_ARE = 'a broker-dealer specializing in annuities and variable life insurance'
WHAT_WE_PLACE = ('variable annuities, registered index-linked annuities and '
                 'variable universal life')

FORM_CRS_PDF = '/assets/docs/FAF-Form-CRS.pdf'


def _asset_version():
    """Cache-bust the stylesheet on content, so a deploy cannot serve a stale one."""
    css = os.path.join(ROOT, 'assets', 'faf.css')
    try:
        with open(css, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()[:8]
    except OSError:
        return '0'


ASSET_V = _asset_version()

# --------------------------------------------------------------------------
# Shell
# --------------------------------------------------------------------------

NAV = [
    ('/services/', 'What We Offer'),
    ('/disclosures/', 'Disclosures'),
    ('/forms/', 'Forms'),
    ('/resources/', 'Resources'),
    ('/brokers/', 'Representatives'),
    ('/contact/', 'Contact'),
]


def nav_html(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return '\n        '.join(out)


FOOTER = f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr-top">
      <div>
        <div class="ftr-logo">
          <img src="/assets/faf-lockup-reversed.svg" alt="{SHORT}" width="208" height="39">
        </div>
        <p>A broker-dealer in {CITY}, {STATE} placing annuities and variable
           life insurance through independent representatives.</p>
      </div>
      <div>
        <h2>Navigate</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/services/">What We Offer</a></li>
          <li><a href="/disclosures/">Disclosures</a></li>
          <li><a href="/forms/">Forms</a></li>
          <li><a href="/resources/">Resources</a></li>
          <li><a href="/brokers/">For Representatives</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{PHONE_URI}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{STREET}<br>{CITY}, {STATE} {ZIP}</li>
        </ul>
      </div>
      <div>
        <h2>Check us</h2>
        <ul>
          <li><a href="{BROKERCHECK}" rel="noopener">FINRA BrokerCheck</a></li>
          <li><a href="{FORM_CRS_PDF}">Form CRS</a></li>
          <li><a href="https://www.finra.org/" rel="noopener">FINRA</a></li>
          <li><a href="https://www.sipc.org/" rel="noopener">SIPC</a></li>
        </ul>
      </div>
    </div>
    <div class="ftr-legal">
      <p>{FIRM} is a broker-dealer registered with the U.S. Securities and
         Exchange Commission (SEC&nbsp;#{SEC_NO}, CRD&nbsp;#{CRD}) and a member of
         <a href="https://www.finra.org/" rel="noopener">FINRA</a> and
         <a href="https://www.sipc.org/" rel="noopener">SIPC</a>. Registration
         does not mean that any regulator has approved or endorsed the firm, its
         personnel or its services.</p>
      <p><strong>Securities products are not FDIC insured, carry no bank
         guarantee, and may lose value, including loss of the amount
         invested.</strong> SIPC protects the custody of securities and cash at
         a failed brokerage; it does not protect against a decline in the market
         value of an investment.</p>
      <p>{SHORT} is <strong>not</strong> a registered investment adviser and does
         not provide investment advisory, tax or legal advice. Some of our
         representatives are separately licensed as investment adviser
         representatives of an unaffiliated or affiliated advisory firm; that is
         a different relationship, with different costs and different
         obligations. Our
         <a href="{FORM_CRS_PDF}">Form CRS</a> describes both, along with the
         conflicts of interest that apply to us.</p>
      <p><strong>{SHORT} is a limited-scope broker-dealer.</strong> Our
         securities business is {WHAT_WE_PLACE}. We do not offer mutual funds,
         exchange-traded funds, stocks, bonds, municipal securities, options or
         any other individual security. The scope of our registration is on the
         public record at
         <a href="{BROKERCHECK}" rel="noopener">FINRA BrokerCheck</a>.</p>
      <p>This site is published for residents of the United States. {SHORT} and
         its representatives may transact business only in states in which they
         are registered or exempt from registration.</p>
      <p>&copy; {{year}} {FIRM} All rights reserved.</p>
    </div>
  </div>
</footer>"""

SCRIPT = """<script>
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
</script>"""

ORG_JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": FIRM,
    "description": (f"{FIRM} is {WHAT_WE_ARE} in {CITY}, {STATE}. Our securities "
                    f"business is {WHAT_WE_PLACE}."),
    "alternateName": SHORT,
    "url": SITE + "/",
    "logo": SITE + "/assets/faf-lockup-reversed.svg",
    "telephone": PHONE,
    "faxNumber": FAX,
    "email": EMAIL,
    "foundingDate": "2005",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": STREET,
        "addressLocality": CITY,
        "addressRegion": STATE,
        "postalCode": ZIP,
        "addressCountry": "US",
    },
    "identifier": [
        {"@type": "PropertyValue", "name": "CRD", "value": CRD},
        {"@type": "PropertyValue", "name": "SEC", "value": SEC_NO},
    ],
    "memberOf": [
        {"@type": "Organization", "name": "Financial Industry Regulatory Authority (FINRA)"},
        {"@type": "Organization", "name": "Securities Investor Protection Corporation (SIPC)"},
    ],
    "sameAs": [BROKERCHECK],
}, indent=2)


def shell(title, desc, body, canonical, current=''):
    year = '2026'
    footer = FOOTER.replace('{year}', year)
    full_title = title if SHORT in title else f'{title} | {SHORT}'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SHORT}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/assets/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/faf.css?v={ASSET_V}">
<script type="application/ld+json">
{ORG_JSONLD}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap">
    <a class="hdr-logo" href="/">
      <img src="/assets/faf-lockup-reversed.svg" alt="{SHORT} — home" width="240" height="45">
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
        {nav_html(current)}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
{footer}
{SCRIPT}
</body>
</html>
"""


# --------------------------------------------------------------------------
# Shared blocks
# --------------------------------------------------------------------------

def disclosure_band(extra=''):
    """
    FINRA Rule 2210(d)(1) requires that a communication be fair and balanced
    and provide a sound basis for evaluating the facts. Where a page describes
    what we offer, the material limitations go with it, at readable size,
    immediately after the copy they qualify — not in footer fine print.
    """
    return f"""<section class="band">
  <div class="wrap">
    <h2>What this page does not say</h2>
    <p><strong>Investing involves risk, including the possible loss of the
       amount you invest.</strong> No investment strategy assures a profit or
       protects against loss in a declining market, and nothing on this site is
       a recommendation to buy or sell any security.</p>
    <p>Securities products are <strong>not FDIC insured, carry no bank
       guarantee and may lose value</strong>. SIPC protects the custody of
       securities and cash if a brokerage fails; it does not protect against
       market loss.</p>
    <p>We are paid by commission when you buy or sell. <strong>We make more when
       there are more transactions</strong>, which is a conflict of interest
       between us and you. We do not monitor accounts on an ongoing basis
       unless we have separately agreed in writing to do so. Our
       <a href="{FORM_CRS_PDF}">Form CRS</a> sets out our services, our costs,
       our conflicts and our disciplinary history, and we encourage you to read
       it before you open an account.</p>
    <p><strong>Annuities and variable life policies are long-term contracts.</strong>
       They carry surrender charges for early withdrawal, ongoing contract and
       rider fees, and tax consequences on early distribution — and the
       guarantees in them depend on the claims-paying ability of the issuing
       insurance company, not on {SHORT} and not on SIPC. All are sold by
       prospectus; read it, including the charges and expenses, before you
       invest. {SHORT} does not provide tax or legal
       advice.{(' ' + extra) if extra else ''}</p>
  </div>
</section>"""


def closer(heading, text, buttons):
    return f"""<section class="sec sec-brand">
  <div class="wrap narrow">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="btns" style="margin-top:2rem">{buttons}</div>
  </div>
</section>"""


def phead(h1, lede, eyebrow=''):
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''
    return f"""<section class="phead">
  <div class="wrap">
    {eb}<h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


def photo(name):
    """
    The class and custom properties for a section that sits over a photograph,
    or empty strings if the file is not there.

    Emitting nothing when the file is absent is the point: the stylesheet draws
    the brand ground underneath either way, so a missing photograph degrades to
    a plain coloured band rather than to a broken image. Drop a correctly named
    pair into public/assets/photos/ and it appears on the next build.
    """
    base = os.path.join(ROOT, 'assets', 'photos', name)
    if not os.path.exists(base + '.jpg'):
        return '', ''
    style = (f"--hero-jpg:url('/assets/photos/{name}.jpg');"
             f"--hero-webp:url('/assets/photos/{name}.webp')")
    return ' hero-photo', f' style="{style}"'


def write(relpath, text):
    path = os.path.join(ROOT, relpath.lstrip('/'))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print('  ', relpath)


def load(name):
    with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
        return json.load(fh)


def doc_href(entry):
    if entry.get('kind') == 'link':
        return entry['url'], 'External', ' rel="noopener"'
    return '/assets/docs/' + entry['file'], 'PDF', ''


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def page_home():
    hero_class, hero_style = photo('home-hero')
    body = f"""<section class="hero{hero_class}"{hero_style}>
  <div class="wrap">
    <p class="eyebrow">Member FINRA &middot; Member SIPC &middot; Since 2005</p>
    <h1>Your partner in financial independence.</h1>
    <p class="lede">{FIRM} is {WHAT_WE_ARE}, in {CITY}, {STATE}, working through
       independent representatives in {STATE_COUNT} states.</p>
    <div class="btns">
      <a class="btn btn-gold" href="/services/">Explore our services</a>
      <a class="btn btn-ghost" href="/contact/">Contact a representative</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow eyebrow-light">What we offer</p>
    <h2>Three products, and we know them well</h2>
    <p>We are a limited-scope broker-dealer. That is a deliberate choice: a
       short list is a list your representative can actually know. What any
       individual representative can place depends on the securities and
       insurance licenses they hold.</p>
    <div class="tiles tiles-3">
      <div class="tile">
        <h3>Variable annuities</h3>
        <p>A long-term contract whose value moves with the subaccounts you
           choose. Income options and optional riders, each at a cost. Sold by
           prospectus.</p>
      </div>
      <div class="tile">
        <h3>Registered index-linked annuities</h3>
        <p>Crediting linked to an index, with a stated buffer or floor against
           loss — and a cap or participation rate that limits the gain in
           exchange. A security. Sold by prospectus.</p>
      </div>
      <div class="tile">
        <h3>Variable universal life</h3>
        <p>Permanent life insurance whose cash value is invested in
           subaccounts. A death benefit and an investment account in one
           contract, with the costs of both. Sold by prospectus.</p>
      </div>
    </div>
    <p class="note">These can be held inside an IRA — traditional, Roth,
       rollover, SEP or SIMPLE — or a 403(b), where the tax treatment comes
       from the account rather than from the contract. <strong>Buying an
       annuity inside an IRA does not add a tax benefit</strong>, because the
       account is already tax-deferred; ask your representative why a
       particular contract belongs there.</p>
    <div class="btns" style="margin-top:2.5rem">
      <a class="btn btn-outline" href="/services/">What each one costs you</a>
    </div>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap split">
    <div>
      <p class="eyebrow eyebrow-light">About us</p>
      <h2>A small firm, by choice</h2>
      <p>{FIRM} has been registered with the SEC since {SEC_REGISTERED_SINCE}
         and incorporated in {INCORPORATED}. The home office is on Iron Avenue
         in {CITY}, and you can reach it on one number.</p>
      <p>Our representatives are independent. They run their own practices and
         know their own clients, and the firm exists to support that rather than
         to manage it. Clearing, custody and execution run through
         {CLEARING_FIRM}, so the infrastructure behind your account is not the
         size of the firm in front of it.</p>
      <p>In 2026 we narrowed what the firm does to annuities and variable life
         insurance, and gave up the rest of the securities business. A smaller
         firm doing fewer things is easier to supervise and easier to be a
         customer of. If you are looking for mutual funds, ETFs or individual
         securities, we are not the right firm and we will tell you so.</p>
    </div>
    <div>
      <div class="orgs">
        <div class="org">
          <span class="org-mark">FINRA</span>
          <span class="org-name">Financial Industry Regulatory Authority</span>
          <span class="org-role">Member</span>
        </div>
        <div class="org">
          <span class="org-mark">SIPC</span>
          <span class="org-name">Securities Investor Protection Corporation</span>
          <span class="org-role">Member</span>
        </div>
      </div>
      <dl class="deflist deflist-tight">
        <div><dt>CRD</dt><dd>{CRD}</dd></div>
        <div><dt>SEC</dt><dd>{SEC_NO}</dd></div>
        <div><dt>Public record</dt><dd><a href="{BROKERCHECK}" rel="noopener">FINRA BrokerCheck</a></dd></div>
      </dl>
      <p class="note" style="margin-top:1.5rem">Registration is a filing
         requirement. It does not mean the SEC, FINRA or any other regulator has
         approved, endorsed or passed on the merits of this firm or anything it
         offers.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow eyebrow-light">How we are paid</p>
    <h2>Three things worth knowing before you call</h2>
    <p>Most brokerage websites leave these to a footnote. They decide whether we
       are the right firm for you, so they are on the front page instead.</p>
    <div class="cards cards-3">
      <div class="card">
        <span class="num">01</span>
        <h3>By commission, per transaction</h3>
        <p>You pay us when you buy or sell. Because of that, we make more when
           there are more transactions — which is a conflict of interest between
           us and you, and we would rather say so here than bury it.</p>
      </div>
      <div class="card">
        <span class="num">02</span>
        <h3>We do not monitor your account</h3>
        <p>We are a brokerage, not an investment adviser. You make the final
           decision on every purchase and sale, and we do not review your
           holdings on a continuing basis unless we agree in writing to.</p>
      </div>
      <div class="card">
        <span class="num">03</span>
        <h3>Nothing we are paid extra to sell</h3>
        <p>No proprietary products, no sales contests, and no limited menu —
           the same statement we make to the SEC in our Form CRS.</p>
      </div>
    </div>
    <p class="note">The specifics — the range our commissions fall in, the
       minimum on a brokered trade, the other costs you may incur, and the
       conflicts that come with all of it — are set out in
       <a href="{FORM_CRS_PDF}">our Form CRS</a>. It is two pages. Read it before
       you open an account, and ask us about anything in it.</p>
  </div>
</section>

{disclosure_band()}

{closer('Start with a conversation',
        'Call the home office and we will pair you with a representative licensed in '
        'your state. There is no form to fill in first.',
        f'<a class="btn btn-gold" href="tel:{PHONE_URI}">{PHONE}</a>'
        '<a class="btn btn-ghost" href="/contact/">All contact details</a>')}

<section class="sec sec-tight rule-top">
  <div class="wrap">
    <p class="aside">Are you a registered representative weighing a move?
       <a href="/brokers/">See what association with {SHORT} involves</a>.</p>
  </div>
</section>
"""
    return shell(
        f'{SHORT} — annuities and variable life insurance, {CITY}, {STATE}',
        f'{FIRM} is {WHAT_WE_ARE} in {CITY}, {STATE}, registered with the SEC '
        f'and a member of FINRA and SIPC. Our securities business is '
        f'{WHAT_WE_PLACE}.',
        body, '/', '')


def page_services():
    body = phead(
        'What we offer',
        'Three products. What each one is, what it costs you to hold, and what '
        'has to be true for it to be the right thing to own.',
        'What we offer') + f"""

<section class="sec">
  <div class="wrap narrow prose">
    <h2>A short list, on purpose</h2>
    <p>{SHORT} is a <strong>limited-scope broker-dealer</strong>. Our securities
       business is {WHAT_WE_PLACE} — and nothing else.</p>
    <p><strong>We do not offer mutual funds, exchange-traded funds, stocks,
       bonds, municipal securities, options, certificates of deposit or any
       other individual security.</strong> We placed most of those once and we
       no longer do. If that is what you are looking for, we are not the right
       firm, and the sooner we both know it the better.</p>
    <p>What is left is a family of contracts that are genuinely complicated —
       long-dated, layered with optional riders, and expensive to leave early.
       They suit some people well and other people not at all. A firm that
       places three products has no excuse for not knowing them thoroughly, and
       that is the trade we have made.</p>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap">
    <h2>The three</h2>
    <p>All three are securities, all three are sold by prospectus, and in all
       three the contract guarantees depend on the insurance company that issues
       them.</p>

    <div class="catalog">
      <div class="catgroup">
        <h3>Variable annuities</h3>
        <ul>
          <li>Value moves with the subaccounts you choose <span>You bear the investment risk</span></li>
          <li>Income and death-benefit riders <span>Each at an annual cost</span></li>
          <li>Surrender charges for early withdrawal <span>Often 5&ndash;7 years</span></li>
          <li>Mortality, expense and administrative charges <span>Annual, on top of subaccount fees</span></li>
        </ul>
      </div>

      <div class="catgroup">
        <h3>Registered index-linked annuities (RILAs)</h3>
        <ul>
          <li>Crediting linked to an index <span>You do not own the index</span></li>
          <li>A buffer or floor against loss <span>Partial protection, not full</span></li>
          <li>A cap or participation rate <span>The price of that protection</span></li>
          <li>Surrender charges, and a term you are expected to hold through</li>
        </ul>
      </div>

      <div class="catgroup">
        <h3>Variable universal life (VUL)</h3>
        <ul>
          <li>Permanent life insurance with an investment account inside</li>
          <li>Cash value invested in subaccounts <span>You bear the investment risk</span></li>
          <li>Cost of insurance, which rises with age <span>Deducted from cash value</span></li>
          <li>A policy can lapse if the cash value runs out <span>Premiums may need to increase</span></li>
        </ul>
      </div>

      <div class="catgroup">
        <h3>Where they can be held</h3>
        <ul>
          <li>A taxable account</li>
          <li>Traditional, Roth and rollover IRAs</li>
          <li>SEP and SIMPLE IRAs</li>
          <li>403(b) plans <span>Schools, hospitals</span></li>
        </ul>
      </div>
    </div>

    <p class="note"><strong>Buying an annuity inside an IRA or a 403(b) does not
       add a tax benefit.</strong> Those accounts are already tax-deferred, so
       the contract's own deferral is worth nothing there. That does not make it
       the wrong choice — the income guarantees or the death benefit may be the
       reason — but it does mean there has to be a reason, and you are entitled
       to hear it. Ask.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap narrow prose">
    <h2>Before you sign one</h2>
    <p>These are the questions that matter most in this particular corner of the
       business. They are not rhetorical; put them to your representative and
       write the answers down.</p>
    <ul class="linklist">
      <li>What am I paying, in total, every year — contract charges, rider charges and subaccount fees together?</li>
      <li>What does it cost me to get out, and for how many years?</li>
      <li>What exactly does the guarantee guarantee, and who is standing behind it?</li>
      <li>If this is going in an IRA or a 403(b), what am I getting that the account does not already give me?</li>
      <li>If this replaces a contract I already hold, what do I lose by leaving the old one?</li>
      <li>What are you paid on this, and would you be paid differently on something else?</li>
    </ul>
    <p class="note">The last two matter more than they look. A 1035 exchange —
       swapping one contract for another — restarts surrender charges and is the
       transaction FINRA scrutinizes most closely in this business, ours
       included. Read
       <a href="/disclosures/#education">FINRA's guidance on exchanges</a> before
       you agree to one.</p>
  </div>
</section>

{disclosure_band()}

<section class="sec sec-warm">
  <div class="wrap">
    <h2>Brokerage or advisory?</h2>
    <p>They are different relationships and they cost different things. It is
       worth being clear which one you are in.</p>
    <div class="cards">
      <div class="card">
        <span class="num">Brokerage</span>
        <h3>What {SHORT} does</h3>
        <p>You pay per transaction. We make a recommendation, you decide, and we
           execute. We are required to act in your best interest when we make a
           recommendation — and we do not monitor the account afterwards.</p>
      </div>
      <div class="card">
        <span class="num">Advisory</span>
        <h3>What we are not</h3>
        <p>{SHORT} is not a registered investment adviser. Some of our
           representatives are separately licensed as investment adviser
           representatives through an advisory firm. That relationship is
           typically paid by an ongoing fee and may include monitoring. If a
           representative offers you both, ask which one you are being offered
           and why. An adviser can place things we cannot.</p>
      </div>
    </div>
    <p class="note">A representative who can offer you either has a conflict of
       interest in the choice, because the two are paid differently. Our
       <a href="{FORM_CRS_PDF}">Form CRS</a> says so, and it is a fair question
       to put to them directly.</p>
  </div>
</section>

{closer('Ready to talk it through?',
        'The account forms are here, and a representative will tell you which of '
        'them apply. Nothing gets signed on a first call.',
        '<a class="btn btn-gold" href="/forms/">Account forms</a>'
        '<a class="btn btn-ghost" href="/contact/">Contact us</a>')}
"""
    return shell(
        'What we offer',
        f'{SHORT} places {WHAT_WE_PLACE} — what each one is, what it costs to '
        f'hold, and the questions to ask before you sign.',
        body, '/services/', '/services/')


def page_disclosures():
    data = load('disclosures.json')

    def doc_list(entries, start=1):
        rows = []
        for i, e in enumerate(entries, start):
            href, kind, rel = doc_href(e)
            rows.append(
                f'      <li><a class="doc" href="{href}"{rel}>'
                f'<span class="n">{i:02d}</span>'
                f'<span class="t">{e["title"]}<small>{e["note"]}</small></span>'
                f'<span class="k">{kind}</span></a></li>'
            )
        return '\n'.join(rows)

    body = phead(
        'Disclosures',
        'The documents that describe how this firm works, what it costs, and '
        'what can go wrong. They are hosted here, on our own domain, so a link '
        'to one keeps working.',
        'Important information') + f"""

<section class="sec">
  <div class="wrap">
    <h2 id="firm">Our documents</h2>
    <p>If you read only one, read the first.</p>
    <ul class="docs">
{doc_list(data['firm_documents'])}
    </ul>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap">
    <h2 id="education">Reading on what you may be sold</h2>
    <p>One of these is ours. The rest are published by FINRA and by the SEC's
       investor education office, and we link them because they are blunter
       about what these contracts cost than a firm's own literature usually
       is — including ours.</p>
    <ul class="docs">
{doc_list(data['education'])}
    </ul>
    <p class="note">Links marked <em>External</em> leave this site. We do not
       control those pages and are not responsible for their content; they were
       last checked on 25 September 2026.</p>
  </div>
</section>

{disclosure_band()}

{closer('Questions about any of this?',
        'The home office can answer them, or put you in touch with the person who '
        'can. Compliance questions go to the same number.',
        f'<a class="btn btn-gold" href="tel:{OFFICE_PHONE_URI}">{OFFICE_PHONE}</a>'
        '<a class="btn btn-ghost" href="/contact/">All contact details</a>')}
"""
    return shell(
        'Disclosures',
        f'Form CRS, the privacy policy, business continuity, account protection '
        f'and margin disclosures for {FIRM}, hosted on our own domain.',
        body, '/disclosures/', '/disclosures/')


def page_form_crs():
    body = phead(
        'Form CRS',
        'Our Customer Relationship Summary — two pages on what we offer, how we '
        'are paid, the conflicts that creates, and our disciplinary history.',
        'Customer Relationship Summary') + f"""

<section class="sec">
  <div class="wrap narrow prose">
    <h2>Why this document exists</h2>
    <p>The SEC requires every broker-dealer and every investment adviser to give
       retail investors a short summary of the relationship on offer, in a
       prescribed order, in plain language. It is the one document designed to
       be compared side by side with another firm's.</p>
    <p>Ours covers the services we provide, the fees you will pay, the legal
       standard that applies when we make a recommendation, how our
       representatives are compensated, the conflicts of interest that follow
       from all of that, and whether the firm or its people have a legal or
       disciplinary history.</p>
    <div class="btns" style="margin-top:2rem">
      <a class="btn btn-solid" href="{FORM_CRS_PDF}">Read our Form CRS (PDF)</a>
    </div>
    <p class="note">You can also request a paper copy at no charge by calling
       <a href="tel:{PHONE_URI}">{PHONE}</a>, and you can compare ours against
       any other firm's at
       <a href="https://www.investor.gov/CRS" rel="noopener">Investor.gov/CRS</a>.</p>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap narrow prose">
    <h2>Questions the form suggests you ask</h2>
    <p>These are the conversation starters the SEC puts in the form itself. Put
       them to any representative, ours or anyone else's.</p>
    <ul class="linklist">
      <li>Given my financial situation, should I choose a brokerage service? Why or why not?</li>
      <li>How will you choose investments to recommend to me?</li>
      <li>What is your relevant experience, including your licenses, education and other qualifications?</li>
      <li>If I give you $10,000 to invest, how much will go to fees and costs, and how much will be invested for me?</li>
      <li>How might your conflicts of interest affect me, and how will you address them?</li>
      <li>As a financial professional, do you have any disciplinary history? For what type of conduct?</li>
      <li>Who is my primary contact person, and is that person a representative of a broker-dealer or an investment adviser?</li>
      <li>Who can I talk to if I have concerns about how this person is treating me?</li>
    </ul>
  </div>
</section>

{disclosure_band()}
"""
    return shell(
        'Form CRS',
        f'The {FIRM} Customer Relationship Summary — services, fees, conflicts '
        f'and disciplinary history, in two pages.',
        body, '/form-crs/', '')


def page_forms():
    data = load('forms.json')
    groups = []
    for g in data['groups']:
        intro = f'    <p>{g["intro"]}</p>\n' if g.get('intro') else ''
        rows = []
        for f in g['forms']:
            rows.append(
                f'      <li><a class="doc" href="/assets/docs/{f["file"]}">'
                f'<span class="n">&#9670;</span>'
                f'<span class="t">{f["title"]}<small>{f["note"]}</small></span>'
                f'<span class="k">PDF</span></a></li>'
            )
        groups.append(
            f'  <div class="wrap">\n'
            f'    <h2>{g["title"]}</h2>\n{intro}'
            f'    <ul class="docs">\n' + '\n'.join(rows) + '\n    </ul>\n  </div>'
        )

    body = phead(
        'Account forms',
        'The forms most often needed, hosted here so the link keeps working. '
        'Your representative will tell you which ones apply — do not guess.',
        'Investor forms') + '\n\n' + '\n\n'.join(
        f'<section class="sec{" sec-warm" if i % 2 else ""}">\n{g}\n</section>'
        for i, g in enumerate(groups)) + f"""

<section class="sec sec-warm">
  <div class="wrap">
    <p class="note">These are the forms we are asked for most. If you need one
       that is not here, call <a href="tel:{PHONE_URI}">{PHONE}</a> and we will
       send it. The forms are PDFs; some are fillable and all can be printed.</p>
    <p class="note"><strong>The mutual fund forms are gone.</strong> {SHORT} no
       longer places mutual funds. If you hold a fund position that was bought
       through us, call the home office and we will tell you where it sits now
       and who services it.</p>
  </div>
</section>

{disclosure_band()}

<section class="sec sec-brand">
  <div class="wrap narrow">
    <h2>Why we ask for so much</h2>
    <p>The account form asks about your income, your net worth, your experience
       and what you are trying to achieve. That is not idle curiosity: federal
       law and FINRA rules require us to have a reasonable basis for any
       recommendation we make, and with contracts this long-dated and this hard
       to reverse, we cannot have one without knowing those things. A Customer
       Identification Program notice, required under the USA PATRIOT Act,
       explains the identity checks separately.</p>
    <div class="btns" style="margin-top:2rem">
      <a class="btn btn-gold" href="/disclosures/#firm">Read the CIP notice</a>
      <a class="btn btn-ghost" href="/contact/">Ask us</a>
    </div>
  </div>
</section>
"""
    return shell(
        'Account forms',
        f'New account and annuity forms for {FIRM}, hosted on our own domain.',
        body, '/forms/', '/forms/')


def page_resources():
    data = load('resources.json')
    groups = []
    for g in data['groups']:
        items = '\n'.join(
            f'        <li><a href="{l["url"]}" rel="noopener">{l["label"]}</a>'
            f'<span>{l["note"]}</span></li>'
            for l in g['links']
        )
        groups.append(
            f'      <div class="catgroup reslist">\n'
            f'        <h3>{g["title"]}</h3>\n'
            f'        <ul>\n{items}\n        </ul>\n      </div>'
        )

    body = phead(
        'Resources',
        'A short list of tools we are prepared to stand behind, all of them run '
        'by a regulator or a government agency.',
        'Investor resources') + f"""

<section class="sec">
  <div class="wrap">
    <div class="catalog">
{chr(10).join(groups)}
    </div>
    <p class="note">These links leave this site. We do not control those pages
       and are not responsible for their content or their availability. Every
       one was checked on 25 September 2026.</p>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap narrow prose">
    <h2>Why this list is short</h2>
    <p>The page this replaced carried seventy-eight links, assembled around
       2006 and never revised. When they were checked in September 2026, about a
       third no longer resolved at all, and a dozen more quietly landed on a
       different company than the one named in the link — a fund family that had
       been acquired, renamed or wound up in the twenty years since.</p>
    <p>A link that carries one firm's name and opens another firm's sales page is
       a communication we cannot stand behind, so the archive was retired rather
       than patched. What is left is regulators, government tools, and nothing
       that goes stale quietly.</p>
    <p>If you want a fund's own material, ask your representative for the
       prospectus. That is the document that governs, and it is the one we are
       required to give you.</p>
  </div>
</section>

{disclosure_band()}
"""
    return shell(
        'Resources',
        'Regulator-run tools for checking a firm, comparing fund costs, and '
        'looking up municipal securities disclosures.',
        body, '/resources/', '/resources/')


def page_brokers():
    body = phead(
        'For registered representatives',
        'A small firm that clears through a large one, for representatives who '
        'would rather deal with a home office that picks up the phone.',
        'For representatives') + f"""

<section class="sec">
  <div class="wrap">
    <h2>What we are</h2>
    <p>{FIRM} has been registered since {SEC_REGISTERED_SINCE} and is licensed
       in {STATE_COUNT} states. Our representatives are independent: they run
       their own practices, and the home office exists to support that rather
       than to manage it. Clearing, custody and execution run through
       {CLEARING_FIRM}</p>
    <p><strong>Read this part before anything else.</strong> We are a
       limited-scope broker-dealer. Our securities business is
       {WHAT_WE_PLACE} — we do not place mutual funds, ETFs or individual
       securities of any kind. If your book depends on those, this is not a
       firm you can move it to, and we would rather you knew that on the first
       call than the fourth.</p>

    <div class="cards">
      <div class="card">
        <span class="num">01</span>
        <h3>You stay independent</h3>
        <p>You run your practice. We are the broker-dealer behind it, not a
           branch manager above it.</p>
      </div>
      <div class="card">
        <span class="num">02</span>
        <h3>A home office you can reach</h3>
        <p>One number, staffed by people who know your business. Compliance and
           operations questions get a person, not a ticket.</p>
      </div>
      <div class="card">
        <span class="num">03</span>
        <h3>Small firm, institutional clearing</h3>
        <p>{CLEARING_FIRM} handles clearing and custody, so the platform behind
           you is not the size of the firm in front of you.</p>
      </div>
      <div class="card">
        <span class="num">04</span>
        <h3>No product pressure</h3>
        <p>No proprietary products, no sales contests and no limited menu — the
           same statement we make to customers in our Form CRS.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap narrow prose">
    <h2>What the first conversation covers</h2>
    <p>We would rather talk than publish numbers that turn out not to apply to
       your book. A first call goes through four things:</p>
    <dl class="deflist">
      <div><dt>Your book</dt><dd>What you hold, what you place, and how much of it fits inside our scope</dd></div>
      <div><dt>Licensing</dt><dd>Which registrations you hold, which states you need, and what has to be filed</dd></div>
      <div><dt>Compliance</dt><dd>Supervision, outside business activities, and what our written procedures will ask of you</dd></div>
      <div><dt>Economics</dt><dd>Payout, the costs that come out of it, and what the transition period looks like</dd></div>
    </dl>
    <p class="note">Nothing on this page is an offer of employment or of any
       particular compensation arrangement. Terms are individually negotiated
       and set out in a written agreement.</p>
  </div>
</section>

{closer('Start the conversation',
        f'Ask for {PRESIDENT} or the compliance department at the home office. '
        'Enquiries from representatives are handled directly and in confidence.',
        f'<a class="btn btn-gold" href="tel:{OFFICE_PHONE_URI}">{OFFICE_PHONE}</a>'
        f'<a class="btn btn-ghost" href="mailto:{EMAIL}">{EMAIL}</a>')}
"""
    return shell(
        'For registered representatives',
        f'{FIRM} is an independent, limited-scope broker-dealer in {CITY}, '
        f'{STATE} placing {WHAT_WE_PLACE}, for representatives who want to run '
        f'their own practice.',
        body, '/brokers/', '/brokers/')


def page_contact():
    body = phead(
        'Contact',
        'Call the home office and we will pair you with a representative '
        'licensed in your state. There is no form to fill in first.',
        'Contact') + f"""

<section class="sec">
  <div class="wrap">
    <div class="contact-grid">
      <div>
        <h3>Telephone</h3>
        <p><a class="big-link" href="tel:{PHONE_URI}">{PHONE}</a></p>
        <p style="color:var(--ink-faint);font-size:0.875rem">Toll free</p>
        <p style="margin-top:1rem"><a href="tel:{OFFICE_PHONE_URI}">{OFFICE_PHONE}</a></p>
        <p style="color:var(--ink-faint);font-size:0.875rem">Home office and compliance</p>
      </div>
      <div>
        <h3>Email</h3>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p style="color:var(--ink-faint);font-size:0.875rem;margin-top:1rem">
           Please do not send account numbers, Social Security numbers or trade
           instructions by email. Email is not a secure channel and we cannot
           accept orders through it.</p>
      </div>
      <div>
        <h3>Fax</h3>
        <p>{FAX}</p>
      </div>
      <div>
        <h3>Street and express delivery</h3>
        <p>{FIRM}<br>{STREET}<br>{CITY}, {STATE} {ZIP}</p>
      </div>
      <div>
        <h3>Mail</h3>
        <p>{FIRM}<br>{PO_BOX}<br>{CITY}, {STATE} {PO_ZIP}</p>
      </div>
      <div>
        <h3>President</h3>
        <p>{PRESIDENT}</p>
        <p style="color:var(--ink-faint);font-size:0.875rem">{FIRM}</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap narrow prose">
    <h2>If you have a complaint</h2>
    <p>Tell us first, in writing, at the address above, marked for the
       compliance department — or call {OFFICE_PHONE} and ask for compliance. We
       would rather hear it from you than read it in a filing.</p>
    <p>You can also take it to FINRA at any time, whatever we say.
       <a href="https://www.finra.org/investors/have-problem" rel="noopener">FINRA's
       investor complaint center</a> explains how, and
       <a href="{BROKERCHECK}" rel="noopener">BrokerCheck</a> shows our
       disciplinary history alongside the rest of our record.</p>
  </div>
</section>

{disclosure_band()}
"""
    return shell(
        'Contact',
        f'Reach the {FIRM} home office in {CITY}, {STATE} — telephone, email, '
        f'fax and mailing addresses.',
        body, '/contact/', '/contact/')


def page_404():
    body = f"""<section class="sec mid">
  <div class="wrap narrow">
    <p class="eyebrow" style="color:var(--gold-deep)">Error 404</p>
    <h1 style="font-family:var(--display);font-weight:500;font-size:clamp(2rem,4vw,2.75rem);line-height:1.15;margin:0 0 1rem;color:var(--brand)">
      That page is not here.</h1>
    <p>It may have moved when this site was rebuilt. Everything the old site
       published still exists somewhere below.</p>
    <ul class="linklist">
      <li><a href="/">Home</a></li>
      <li><a href="/services/">What we offer</a></li>
      <li><a href="/disclosures/">Disclosures</a></li>
      <li><a href="/forms/">Account forms</a></li>
      <li><a href="/resources/">Resources</a></li>
      <li><a href="/brokers/">For representatives</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="{FORM_CRS_PDF}">Form CRS</a></li>
    </ul>
    <p class="note">If you followed a link here from somewhere on this site,
       tell us at <a href="mailto:{EMAIL}">{EMAIL}</a> and we will fix it.</p>
  </div>
</section>"""
    return shell('Page not found', 'That page is not here.', body, '/404.html', '')


# --------------------------------------------------------------------------
# sitemap / robots
# --------------------------------------------------------------------------

PUBLIC_PAGES = ['/', '/services/', '/disclosures/', '/form-crs/', '/forms/',
                '/resources/', '/brokers/', '/contact/']


def sitemap():
    urls = '\n'.join(
        f'  <url><loc>{SITE}{p}</loc>'
        f'<changefreq>{"monthly" if p == "/" else "yearly"}</changefreq>'
        f'<priority>{"1.0" if p == "/" else "0.7"}</priority></url>'
        for p in PUBLIC_PAGES
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'{urls}\n</urlset>\n')


def robots():
    return (f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')


def webmanifest():
    return json.dumps({
        "name": FIRM,
        "short_name": SHORT,
        "icons": [
            {"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": "#2B3439",
        "background_color": "#F5F3EE",
        "display": "browser",
    }, indent=2) + '\n'


# --------------------------------------------------------------------------

def main():
    print('Building into', ROOT)
    write('index.html', page_home())
    write('services/index.html', page_services())
    write('disclosures/index.html', page_disclosures())
    write('form-crs/index.html', page_form_crs())
    write('forms/index.html', page_forms())
    write('resources/index.html', page_resources())
    write('brokers/index.html', page_brokers())
    write('contact/index.html', page_contact())
    write('404.html', page_404())
    write('sitemap.xml', sitemap())
    write('robots.txt', robots())
    write('assets/site.webmanifest', webmanifest())
    print('Done. Stylesheet version', ASSET_V)


if __name__ == '__main__':
    main()

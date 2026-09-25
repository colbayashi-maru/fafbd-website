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
          <img src="/assets/faf-logo-compact.svg" alt="{SHORT}" width="208" height="33">
        </div>
        <p>A full-service broker-dealer in {CITY}, {STATE}, working through
           independent representatives.</p>
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
          <li><a href="https://www.msrb.org/" rel="noopener">MSRB</a></li>
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
    "alternateName": SHORT,
    "url": SITE + "/",
    "logo": SITE + "/assets/faf-logo-whitetext.svg",
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
      <img src="/assets/faf-logo-compact.svg" alt="{SHORT} — home" width="240" height="38">
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
    <p>{SHORT} does not provide tax or legal advice. Mutual funds and variable
       annuities are sold by prospectus; read it, including the charges and
       expenses, before investing.{(' ' + extra) if extra else ''}</p>
  </div>
</section>"""


def closer(heading, text, buttons):
    return f"""<section class="sec sec-navy">
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
    body = f"""<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Broker-dealer &middot; {CITY}, Kansas &middot; Since 2005</p>
    <h1>Brokerage, in plain terms.</h1>
    <p class="lede">{FIRM} is a full-service broker-dealer in {CITY}, {STATE}.
       We have been registered with the SEC since {SEC_REGISTERED_SINCE} and we
       work through independent representatives in {STATE_COUNT} states.</p>
    <div class="btns">
      <a class="btn btn-gold" href="/services/">What we offer</a>
      <a class="btn btn-ghost" href="/contact/">Talk to someone</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2>Two ways in</h2>
    <p>Most of what a firm like ours publishes is written for one of two people.
       Pick the one you are.</p>
    <div class="doors">
      <div class="door">
        <h3>You are looking for a representative</h3>
        <p>Call the home office and we will put you with a representative who is
           licensed in your state. Before that conversation, it is worth knowing
           what we offer, how we are paid, and what our filings say about us.</p>
        <div class="btns">
          <a class="btn btn-navy" href="/services/">What we offer</a>
        </div>
      </div>
      <div class="door">
        <h3>You are a registered representative</h3>
        <p>We are a small firm that clears through a large one. Representatives
           keep their independence and deal directly with a home office that
           answers. If you are weighing a move, start here.</p>
        <div class="btns">
          <a class="btn btn-navy" href="/brokers/">For representatives</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-warm">
  <div class="wrap">
    <h2>How we are paid</h2>
    <p>This is the part most brokerage websites leave to a footnote. It decides
       whether we are the right firm for you, so it belongs near the top.</p>
    <div class="cards">
      <div class="card">
        <span class="num">01</span>
        <h3>By commission, per transaction</h3>
        <p>You pay us when you buy or sell — a commission, concession, or
           mark-up. There is no ongoing fee for having an account with us.</p>
      </div>
      <div class="card">
        <span class="num">02</span>
        <h3>Which creates a conflict</h3>
        <p>Because we are paid per transaction, we make more when there are more
           transactions. Our Form CRS names that conflict plainly, and so do we.</p>
      </div>
      <div class="card">
        <span class="num">03</span>
        <h3>We do not monitor your account</h3>
        <p>We are a brokerage, not an investment adviser. You make the final
           decision on every purchase and sale, and we do not review your
           holdings on a continuing basis unless we agree in writing to.</p>
      </div>
      <div class="card">
        <span class="num">04</span>
        <h3>No proprietary products</h3>
        <p>We do not manufacture investments, run sales contests, or work from a
           limited menu — as stated in our filed Form CRS.</p>
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

<section class="sec">
  <div class="wrap">
    <h2>How the firm is registered</h2>
    <p>These are identifiers and filings, not credentials. They tell you where
       to look us up, and they are the same numbers a regulator would use.</p>
    <dl class="deflist">
      <div><dt>Legal name</dt><dd>{FIRM}</dd></div>
      <div><dt>CRD number</dt><dd>{CRD}</dd></div>
      <div><dt>SEC number</dt><dd>{SEC_NO}</dd></div>
      <div><dt>Registered with</dt><dd>The U.S. Securities and Exchange Commission, since {SEC_REGISTERED_SINCE}</dd></div>
      <div><dt>Member of</dt><dd>FINRA and SIPC. Registered with the MSRB for municipal securities business</dd></div>
      <div><dt>Incorporated</dt><dd>{INCORPORATED}</dd></div>
      <div><dt>Home office</dt><dd>{STREET}, {CITY}, {STATE} {ZIP}</dd></div>
      <div><dt>Clearing firm</dt><dd>{CLEARING_FIRM}, which holds customer securities and cash</dd></div>
      <div><dt>Public record</dt><dd><a href="{BROKERCHECK}" rel="noopener">FINRA BrokerCheck</a> — our registrations, our representatives, and our disciplinary history</dd></div>
    </dl>
    <p class="note">Registration is a filing requirement. It does not mean the
       SEC, FINRA or any other regulator has approved, endorsed or passed on the
       merits of this firm or anything it offers.</p>
  </div>
</section>

{closer('Start with a conversation',
        'Call the home office and we will pair you with a representative licensed in '
        'your state. There is no form to fill in first.',
        f'<a class="btn btn-gold" href="tel:{PHONE_URI}">{PHONE}</a>'
        '<a class="btn btn-ghost" href="/contact/">All contact details</a>')}
"""
    return shell(
        f'{SHORT} — a full-service broker-dealer in {CITY}, {STATE}',
        f'{FIRM} is a full-service broker-dealer in {CITY}, {STATE}, registered '
        f'with the SEC and a member of FINRA and SIPC, working through '
        f'independent representatives in {STATE_COUNT} states.',
        body, '/', '')


def page_services():
    body = phead(
        'What we offer',
        'The products our representatives can place, what each one is, and what '
        'it costs you to hold it. Which of these any individual representative '
        'can offer depends on the securities licenses they hold.',
        'What we offer') + f"""

<section class="sec">
  <div class="wrap">
    <h2>The catalog</h2>
    <p>Availability varies by representative. A Series 6 license covers a
       narrower set than a Series 7; ask yours what they are licensed to place
       before you plan around anything on this list.</p>

    <div class="catalog">
      <div class="catgroup">
        <h3>Funds and pooled investments</h3>
        <ul>
          <li>Mutual funds <span>Sold by prospectus</span></li>
          <li>Exchange-traded funds (ETFs) <span>Sold by prospectus</span></li>
          <li>Real estate investment trusts (REITs) <span>Sold by prospectus</span></li>
        </ul>
      </div>

      <div class="catgroup">
        <h3>Individual securities</h3>
        <ul>
          <li>Corporate equity securities (stocks)</li>
          <li>Corporate debt securities (bonds)</li>
          <li>Municipal securities</li>
          <li>U.S. government securities</li>
          <li>Brokered certificates of deposit</li>
          <li>Put and call options</li>
        </ul>
      </div>

      <div class="catgroup">
        <h3>Retirement and education accounts</h3>
        <ul>
          <li>Traditional, Roth and Educational IRAs</li>
          <li>Rollovers, transfers and Roth conversions</li>
          <li>Self-directed IRAs</li>
          <li>SEP and SIMPLE IRAs</li>
          <li>401(k), pension and profit-sharing plans</li>
          <li>403(b) plans <span>Schools, hospitals</span></li>
          <li>Non-qualified deferred compensation plans</li>
          <li>529 college savings plans</li>
          <li>Health savings plans</li>
        </ul>
      </div>

      <div class="catgroup">
        <h3>Annuities and insurance products</h3>
        <ul>
          <li>Fixed annuities</li>
          <li>Variable annuities <span>Sold by prospectus</span></li>
          <li>Equity-indexed annuities</li>
          <li>Variable universal life <span>Sold by prospectus</span></li>
        </ul>
      </div>
    </div>

    <p class="note">Annuities are long-term contracts. They carry surrender
       charges, ongoing contract and rider fees, and tax consequences on early
       withdrawal, and the guarantees in them depend on the claims-paying
       ability of the issuing insurance company — not on {SHORT} and not on
       SIPC. Before you exchange one annuity for another, read
       <a href="/disclosures/#education">FINRA's guidance on 1035 exchanges</a>.</p>
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
           and why.</p>
      </div>
    </div>
    <p class="note">A representative who can offer you either has a conflict of
       interest in the choice, because the two are paid differently. Our
       <a href="{FORM_CRS_PDF}">Form CRS</a> says so, and it is a fair question
       to put to them directly.</p>
  </div>
</section>

{closer('Ready to open an account?',
        'The account forms are here, and a representative will tell you which of '
        'them apply to what you want to do.',
        '<a class="btn btn-gold" href="/forms/">Account forms</a>'
        '<a class="btn btn-ghost" href="/contact/">Contact us</a>')}
"""
    return shell(
        'What we offer',
        f'The products {SHORT} representatives can place — funds, individual '
        f'securities, retirement and education accounts, and annuities — and '
        f'what each one costs to hold.',
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
    <p>Two of these are ours. The rest are published by FINRA and by the SEC's
       investor education office, and we link them because they are blunter
       about product costs than a firm's own literature usually is.</p>
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
      <a class="btn btn-navy" href="{FORM_CRS_PDF}">Read our Form CRS (PDF)</a>
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
        'Investor forms') + f"""

<section class="sec">
{groups[0]}
</section>

<section class="sec sec-warm">
{groups[1]}
</section>

<section class="sec">
{groups[2]}
  <div class="wrap">
    <p class="note">These are the forms we are asked for most. If you need one
       that is not here, call <a href="tel:{PHONE_URI}">{PHONE}</a> and we will
       send it. The forms are PDFs; some are fillable and all can be printed.</p>
  </div>
</section>

{disclosure_band()}

<section class="sec sec-navy">
  <div class="wrap narrow">
    <h2>Why we ask for so much</h2>
    <p>The account form asks about your income, your net worth, your experience
       and what you are trying to achieve. That is not idle curiosity: federal
       law and FINRA rules require us to have a reasonable basis for any
       recommendation we make, and we cannot have one without knowing those
       things. A Customer Identification Program notice, required under the USA
       PATRIOT Act, explains the identity checks separately.</p>
    <div class="btns" style="margin-top:2rem">
      <a class="btn btn-gold" href="/disclosures/#firm">Read the CIP notice</a>
      <a class="btn btn-ghost" href="/contact/">Ask us</a>
    </div>
  </div>
</section>
"""
    return shell(
        'Account forms',
        f'New account, mutual fund and variable annuity forms for {FIRM}, '
        f'hosted on our own domain.',
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
      <div><dt>Your book</dt><dd>What you hold, what you place, and which of it transfers cleanly</dd></div>
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
        f'{FIRM} is an independent broker-dealer in {CITY}, {STATE}, clearing '
        f'through {CLEARING_FIRM}, for representatives who want to run their own '
        f'practice.',
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
    <h1 style="font-family:var(--display);font-weight:500;font-size:clamp(2rem,4vw,2.75rem);line-height:1.15;margin:0 0 1rem;color:var(--navy)">
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
        "theme_color": "#0B1F3A",
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

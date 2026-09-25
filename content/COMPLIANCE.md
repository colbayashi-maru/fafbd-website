# Communications review — firstassetfinancial.com

**Status: the specific problems listed below are corrected. Seven items remain
open, and all seven sit in the firm's own filings and records rather than in
website copy.** One of them — the address in the filed Form CRS — should be
looked at this week.

This records a rule-by-rule review of the site's copy and the changes made as a
result. It is not a legal opinion and it is not a substitute for review by the
firm's Chief Compliance Officer or outside counsel. **Nothing here is a
substitute for the registered-principal approval that Rule 2210(b)(1)(A)
requires before this site is used.**

Reviewed against the Base44 prototype at `first-asset-flow.base44.app` and the
live PHP site at `firstassetfinancial.com`, as of 25 September 2026.

---

## The regime is not the same one as Your IA's

Worth stating plainly, because the two projects look alike and are not.

Your IA is an SEC-registered **investment adviser**, so its website is governed
by the Advisers Act Marketing Rule, 206(4)-1. **First Asset Financial is a
broker-dealer and expressly not an investment adviser** — its own Form CRS says
so in the second sentence. The Marketing Rule does not apply to it at all.

What applies instead is **FINRA Rule 2210**, plus Regulation Best Interest and
the Form CRS rules. The obligations overlap in spirit and differ in detail: 2210
requires principal approval before first use, carries its own filing and
recordkeeping mechanics, and — unlike the Marketing Rule — flatly prohibits any
projection of performance rather than conditioning it.

| Rule | What it requires | Bearing on this site |
|---|---|---|
| **FINRA 2210(a)(5)** | Defines a "retail communication" — anything distributed to more than 25 retail investors in 30 days | The whole website is one. Every rule below applies to every page |
| **FINRA 2210(b)(1)(A)** | A registered principal must approve each retail communication **before first use** | **Firm obligation. Not yet satisfied.** See "Before cutover" |
| **FINRA 2210(b)(4)** | Retain communications for three years, with the name of the approving principal | Satisfied structurally — see "Recordkeeping" |
| **FINRA 2210(c)** | Filing with FINRA Advertising Regulation in defined cases | Not triggered as the site now stands. See "Do not add" |
| **FINRA 2210(d)(1)(A)** | Fair and balanced; must provide a **sound basis** for evaluating the facts | Drove the disclosure band and the removal of three claims |
| **FINRA 2210(d)(1)(B)** | No false, exaggerated, unwarranted, promissory or misleading statement; no material omission | The core constraint here. Drove items 1, 3, 4, 5, 8 below |
| **FINRA 2210(d)(1)(D)** | May not state or imply that FINRA, the SEC or any regulator endorses the firm | Drove item 2 |
| **FINRA 2210(d)(1)(F)** | **Prohibits** predicting or projecting performance | None on the site. See "Do not add" |
| **FINRA 2210(d)(3)** | References to FINRA membership must carry the member's name and not mislead | Satisfied — the lockup and the footer both name the firm |
| **FINRA 2210(d)(6)** | Testimonials carry disclosure obligations | **None on the site.** See "Do not add" |
| **FINRA 2266** | SIPC information must reach customers | The footer and the band both explain what SIPC does and does not cover |
| **Exchange Act Rule 17a-14** | Form CRS must be posted on the firm's **public website** | **Was broken. Fixed** — see item 7 |
| **Reg BI (Rule 15l-1)** | Best-interest standard for recommendations; disclosure of scope and conflicts | Drove the "How we are paid" section |
| **Exchange Act Rule 17a-4(b)(4)** | Retain communications relating to the business | Satisfied structurally |
| **Securities Act §5 / Rule 156** | Funds and variable annuities are sold by prospectus | Stated on every page that names one |

---

## Violations found and corrected

### 1. "Managed Portfolios — professionally managed portfolios tailored to your objectives" — 2210(d)(1)(B), and worse

**The most serious item on the prototype.** It appeared twice: as a headline
service card on the home page, and as "Professionally Managed Portfolios" at
the top of the product catalogue.

The firm's own filed Form CRS says the opposite, twice:

> "FAF is NOT a Registered Investment Advisor ("RIA")."

> "We do not monitor your portfolio or investment account on a continuous
> basis. Any voluntary review is not considered to be 'account monitoring'."

Advertising professionally managed, objective-tailored portfolios is a
description of **discretionary advisory management**. Offering that from an
entity that has told the Commission it is not an adviser and does not monitor
accounts is not merely an unwarranted statement under 2210(d)(1)(B); it is
holding the firm out as something its registration does not cover.

→ Removed from both places. `/services/` now carries an explicit
**"Brokerage or advisory?"** section that states what the firm does, states that
it is not an RIA, and explains that a representative separately licensed as an
investment adviser representative is offering a *different* relationship — which
is exactly how Form CRS frames it, and it names the conflict in that choice.

### 2. "Registered. Regulated. Trusted." — 2210(d)(1)(D)

A heading that set the firm's regulatory status out as a reason to trust it.
Registration is a filing requirement. Presenting it as a credential is the
implication 2210(d)(1)(D) exists to stop, and "Trusted" is not something a
regulator conferred.

→ Now **"How the firm is registered"**, a plain table of identifiers, followed
by: *"Registration is a filing requirement. It does not mean the SEC, FINRA or
any other regulator has approved, endorsed or passed on the merits of this firm
or anything it offers."* The same sentence is in the footer of every page.

### 3. "Over 8,000 funds across every asset class and strategy" — 2210(d)(1)(A), (d)(1)(B)

Two problems in one line. The count is a material statement of fact that
depends on the clearing firm's platform and changes without anyone at the firm
noticing; and "every asset class and strategy" is an absolute that cannot be
true.

→ Removed. The catalog lists mutual funds without a number.

### 4. "IRAs with no annual fee" and "No Annual Inactivity Fee" — 2210(d)(1)(A)

Fee claims. They are almost certainly descriptions of the **clearing firm's**
fee schedule, not the firm's, and that schedule is not under this firm's
control. A fee claim that goes stale is a misleading statement from the day it
does.

→ Removed. What an account costs is described in Form CRS, which the site
links from every page.

### 5. "Free Annuity Review" — 2210(d)(1)(B)

An offer of a free service whose natural outcome is a commissionable
recommendation — in the product category (variable and indexed annuities) that
draws more FINRA attention than any other.

→ Removed.

### 6. Benefits with no mention of risk — 2210(d)(1)(A)

The prototype described mutual funds, retirement plans, annuities and managed
portfolios with no risk language anywhere except one line of footer text. Fine
print is not a sound basis for evaluating the facts.

→ Added a **disclosure band** at readable size on every page, immediately after
the copy it qualifies. It covers loss of principal, the absence of any assurance
of profit, the FDIC/bank-guarantee language, what SIPC does and does not cover,
the commission conflict, the absence of monitoring, and the absence of tax and
legal advice. Annuity-specific limits — surrender charges, rider fees, and the
fact that contract guarantees depend on the **issuing insurer's** claims-paying
ability rather than on the firm or on SIPC — sit on `/services/`, next to the
annuities.

### 7. The Form CRS link was broken — Exchange Act Rule 17a-14

The prototype's Form CRS page linked `assets/pdf/form_crs.pdf`. **That file does
not exist and returns 404.** The document is on the live host under a different
name, `assets/pdf/CRS form.pdf`, with a space in it.

Rule 17a-14 requires a firm that has a public website to post its current Form
CRS there. A posted link that 404s does not satisfy that, and Form CRS is the
one document in this whole set that a regulator will check first.

→ The document is now hosted in this repository at
`/assets/docs/FAF-Form-CRS.pdf`, linked from the footer of every page, from
`/disclosures/` as item 01, and from a dedicated `/form-crs/` page.
`netlify.toml` redirects all three historical paths — the space-in-name
version, the URL-encoded version, and the prototype's broken one — to it.

### 8. The "complete listing" was not complete — 2210(d)(1)(B)

The prototype's catalogue was headed *"A complete listing of the products and
services offered by First Asset Financial"* and omitted stocks, bonds,
exchange-traded funds, municipal securities, U.S. government securities,
brokered CDs, options and health savings plans — **all of which the firm's own
Form CRS lists as retail brokerage services it offers**. It also listed "Tax
Shelter Products", a phrase that means nothing specific and reads badly.

→ The catalog on `/services/` is rebuilt from the Form CRS product list, the
"complete listing" framing is gone, and the page states plainly that what any
individual representative can offer depends on the licenses they hold — the
Series 6 / Series 7 distinction that Form CRS draws.

### 9. The Prospective Brokers page published its own credentials — not a FINRA issue, but it had to go

The page carried a password gate and, immediately below it, the instructions for
getting through:

> Using lower case letters, enter "broker" in the User Name field. For the
> password field, enter the word that precedes your test designation number.

A gate whose credentials are printed above it protects nothing. It also put an
access-control mechanism on a public page for no benefit, and the copy behind it
was recruiting material of the ordinary kind.

→ The gate is gone. `/brokers/` states what the firm is, what the first
conversation covers, and asks for a call. It carries a line stating that nothing
on the page is an offer of employment or of any particular compensation
arrangement.

### 10. Seventy-eight third-party links, unverified — 2210(d)(1)(B)

The Investor Resources page carried 78 outbound links assembled around 2006 and
never revised. Checked on 25 September 2026:

- **21 do not resolve at all** — `fundalarm.com`, `vankampen.com`,
  `columbiafunds.com`, `jhfunds.com`, `rydexfunds.com`, the whole
  `bygpub.com` calculator set, both `siionline.com` PDFs, and both of the
  FINRA tool URLs, among others.
- **4 return an error** — `dinkytown.com`, `usatoday.com`, `genworth.com`,
  `reuters.com`.
- **At least a dozen resolve to a different company than the link text names.**
  "AIM" lands on Invesco. "American Funds" lands on Capital Group. "Heritage"
  lands on Eagle Asset. "AIG SunAmerica" lands on Corebridge. "MMA Praxis" lands
  on Praxis. "Federated" lands on Federated Hermes.
- One — the Commonwealth retirement calculator — resolves to that firm's own
  404 page with an HTTP 200, so an automated check would call it healthy.

A link carrying one firm's name that opens a different firm's sales page is a
communication the member cannot stand behind, and there is no version of
maintaining 78 of these that stays accurate.

→ The archive is retired rather than patched. `/resources/` now carries **nine**
links: FINRA, the SEC's Investor.gov, MSRB EMMA, SIPC, TreasuryDirect and
BrokerCheck. No fund-company home pages at all — a representative sends the
prospectus, which is the document that governs. Every link carries the date it
was verified, in `content/resources.json`, and the page says so. The page also
explains, in plain terms, why the old list is gone.

### Other wording tightened

| Was | Now | Why |
|---|---|---|
| "dedicated to helping clients achieve and maintain financial independence" | "a full-service broker-dealer in Salina, KS" | The original implies an outcome the firm cannot promise |
| "These seasoned professionals are dedicated to your long-term success" | Removed | A characterisation of every representative that the firm would have to stand behind for each of them |
| "will be able to create value-added service in aiding you in your selection of investments" | Removed | Means nothing, and "value-added" is an unsubstantiated benefit claim |
| "Registered. Regulated. Trusted." | "How the firm is registered" | See item 2 |
| "A Tradition of Financial Independence" | Removed | A 2005 firm does not have a tradition, and the phrase implies results |
| "Small Firm, Big Capabilities" | "Small firm, institutional clearing" — attributed to the clearing firm by name | The original claimed capabilities; the replacement states a fact about who clears |
| "Competitive payout" / "Fair Compensation" (brokers page) | "Economics: payout, the costs that come out of it, and what the transition looks like" — framed as what the first call covers | A payout claim is a claim, even to a recruiting audience |
| "Our staff demonstrates willingness to go above and beyond" | "One number, staffed by people who know your business" | Removes a service-level promise |
| Contact page: "We are here to answer your questions and respond to your needs" | "Call the home office and we will pair you with a representative licensed in your state" | Describes what happens instead of promising responsiveness |

### Additions the prototype did not have

- **"How we are paid" on the home page**, above the fold-and-a-half. Commission
  per transaction; the firm makes more when there are more transactions; the
  firm does not monitor accounts; no proprietary products, sales contests or
  limited menu. Every one of those four is a direct restatement of the firm's
  own filed Form CRS, which is what makes them safe to publish.
- **An email-security line on `/contact/`**: no account numbers, no Social
  Security numbers, no trade instructions, and orders are not accepted by email.
- **A complaint route on `/contact/`**: how to reach the firm's compliance
  department, and the statement that a customer may go to FINRA at any time
  regardless.
- **The state limitation** in the footer of every page — the firm is licensed in
  23 states and the site is visible everywhere.

---

## Open items — all seven are in the firm's records, not in website copy

### 1. The filed Form CRS gives the wrong address. Look at this first.

The posted Form CRS states:

> "The Corporate Offices are located in McDonough, GA."

**FINRA BrokerCheck for CRD 139107 gives the main office and the mailing address
as 110 E. Iron Ave., Salina, KS 67401**, and the firm is recorded as established
in Kansas since 15 June 2005. The website — old and new — says Salina. The
telephone number in the same Form CRS, 785-825-5050, is a Kansas number and
matches BrokerCheck.

So the website is right and **the filed document appears to be wrong**. Form CRS
must be amended within 30 days of any information becoming materially
inaccurate, and a filed relationship summary that misstates where the firm is
located is not a small thing for a document whose purpose is to tell retail
investors who they are dealing with.

Two possibilities worth separating before anything is filed: either the sentence
is an error, or there is a McDonough, GA office that BrokerCheck does not
reflect — in which case the Form BD branch information is what needs attention
instead. **This site publishes the Salina address, from BrokerCheck.**

### 2. The posted Form CRS refers to a packet it is not part of

The posted document says further Reg BI detail "can be found in this 'packet' on
pages 9-10". The posted PDF is two pages. Either the wrong file is posted, or
the standalone version carries a cross-reference to a longer document that a
website reader does not have. Confirm which, and post the version intended for
standalone delivery.

### 3. MSRB registration is asserted but not visible on BrokerCheck

The old site said the firm "is registered with the Municipal Securities
Rulemaking Board" and the Form CRS says "member FINRA/SIPC/MSRB". BrokerCheck's
**Other Registrations** field for CRD 139107 lists SEC federally and **FINRA
only** as a self-regulatory organisation.

That is not necessarily a contradiction — MSRB registration runs through Form
A-12 and is not an SRO membership BrokerCheck reports in that field. But the
site now names the MSRB and lists municipal securities in the catalog, so
**confirm the A-12 registration is current** before this goes live. If it is not,
both the MSRB reference and municipal securities come off the site.

### 4. Two phone numbers, and it is not obvious which is primary

The website publishes **(800) 825-5511**. BrokerCheck and the Form CRS
compliance line both give **785-825-5050**. The Form CRS uses the 800 number for
requesting the packet and the 785 number for compliance questions and for
requesting a copy of the relationship summary — so both appear to be live, in
different roles.

The site now publishes both, labelled: the 800 number as the toll-free line, the
785 number as the home office and compliance line. **Confirm both ring, and
confirm the labelling.**

### 5. The clearing firm is named on the site

`/services/` and `/brokers/` name **Hilltop Securities Inc.** as the clearing
firm, taken from the Form CRS footnote. Naming a clearing firm is ordinary and
useful, but it is a statement about a third party and about a contract.
**Confirm the relationship is current** and that Hilltop has no objection to
being named.

### 6. The state count

The site says the firm works through representatives in **23 states**, from
BrokerCheck as of 25 September 2026. It is a number that changes. When it does,
change `STATE_COUNT` in `build.py` and rebuild; the footer's "registered or
exempt" sentence carries the load in the meantime.

### 7. The 2013 FINRA sanction

Form CRS discloses it, and characterises it as "an email retention violation
that was an administrative regulation issue, not an investor related issue".
BrokerCheck shows one regulatory event.

The website does not describe the event and is not required to. It links
BrokerCheck from the footer of every page, from `/resources/` and from
`/contact/`, and the Form CRS that discloses it is item 01 on `/disclosures/`.
**That is a deliberate choice and it is recorded here.** If the firm would
rather address it directly on the site, that copy needs principal approval like
anything else.

---

## Do not add without compliance review

The site is currently clean on the areas that generate most Rule 2210
enforcement, **because it contains none of them**. Adding any one changes the
analysis completely, and two of them also trigger a FINRA filing.

- **Any performance figure, projection or hypothetical.** Returns, growth rates,
  "what $10,000 would have become", a sample portfolio, an illustration of an
  annuity's accumulation. **Rule 2210(d)(1)(F) prohibits predictions and
  projections of performance outright** — this is stricter than the rule that
  governs advisers, and there is no disclosure that cures it.
- **Testimonials, client quotes, reviews, star ratings.** Rule 2210(d)(6)
  requires disclosure that the testimonial may not be representative, that it is
  no guarantee of future performance, and — if more than $100 in value was paid
  — that it was paid for.
- **Rankings or comparisons involving investment companies.** Rule 2212 has its
  own conditions, and a retail communication concerning a registered investment
  company that includes a ranking must be **filed with FINRA Advertising
  Regulation within 10 business days of first use** under Rule 2210(c)(3)(A).
- **Naming specific funds or fund families.** This is how the old resources page
  ended up where it did. It also pulls the page toward 2210(c)(3) filing and
  toward prospectus-delivery questions under Rule 156.
- **Revenue, production, representative counts, assets, or awards.** Each is a
  material statement of fact needing a sound basis under 2210(d)(1)(A), and the
  credentials table on the home page deliberately carries no numbers of that
  kind.
- **A payout figure on `/brokers/`.** A recruiting communication is still a
  communication. If the firm wants to publish a number, it needs to be true for
  everyone who reads it and supportable from the representative agreements.
- **Anything that implies account monitoring, ongoing review, financial
  planning, or advice.** This is item 1 above, and it is the one most likely to
  creep back in through ordinary marketing language.

---

## Recordkeeping — 2210(b)(4) and Rule 17a-4(b)(4)

The firm must retain each retail communication for three years from last use,
with the name of the principal who approved it and the date.

**This repository satisfies the retention mechanic well.** The full text of every
page is in git, every change is a commit with a date and an author, and any
prior version of the site can be reproduced exactly. That is a better
advertising archive than most firms of this size have.

Two gaps the repository does not close on its own:

1. **Principal approval is not a commit.** Rule 2210(b)(1)(A) requires approval
   by a registered principal *before first use*, evidenced with the principal's
   name and the date. Record that separately — against the commit hash that was
   approved, which makes the record exact — before DNS cutover, and again
   whenever copy changes.
2. **Substantiation records** for anything that is ever added back live outside
   this repository. File them where the CCO keeps advertising support, and
   cross-reference this file.

---

## Before cutover

- [ ] **Registered principal approval under Rule 2210(b)(1)(A).** Record the
      approver's name, the date, and the commit hash approved. Nothing else on
      this list matters if this one is skipped.
- [ ] **Resolve the Form CRS address** — open item 1. If the document is amended,
      drop the new PDF into `public/assets/docs/` under a **new dated filename**,
      repoint `content/disclosures.json`, and rebuild. Do not overwrite the
      existing file: `netlify.toml` caches that folder for a week.
- [ ] **Confirm MSRB registration** — open item 3 — or remove the MSRB reference
      and municipal securities from `/services/` and the footer.
- [ ] **Confirm both telephone numbers ring**, and the labelling of each.
- [ ] **Confirm Hilltop Securities is still the clearing firm.**
- [ ] **Delete the `X-Robots-Tag = "noindex, nofollow"` block from
      `netlify.toml`.** It is there to keep the staging URL out of search while
      the site is in review. It is a blanket rule, so if it survives the cutover
      the real site stays invisible to Google indefinitely, silently, with
      nothing on the page to show for it.

---

## On "guaranteeing" compliance

This review was done carefully and against primary sources — the firm's own
filed Form CRS, FINRA BrokerCheck for CRD 139107, and the text of the rules. It
cannot be a guarantee, and treating it as one would itself be a compliance
failure:

- Whether a statement misleads depends on facts in the firm's agreements, its
  clearing arrangement and its actual practices, none of which were available to
  this review.
- Rule 2210 is principles-based in its general standards. It turns on facts and
  circumstances, and reasonable compliance professionals differ.
- **The obligation to approve this site sits with a registered principal of the
  firm, and it has not been discharged.** A commit is not an approval.

What this review does provide: the site is free of the specific problems listed
above, every remaining material statement is traceable to the firm's own filing
or to BrokerCheck, the categories that generate most enforcement are absent by
design, and the seven open items are written down with enough detail to act on.

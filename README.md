# firstassetfinancial.com

A hand-built static site. No framework, no build toolchain, no SPA.

**Deploy `public/` as the web root.** There is no build step at deploy time —
`netlify.toml` already sets the publish directory, and the generated HTML is
committed. This file lives outside `public/`, so it is never served.

---

## What this replaced

Two things, actually.

The **live site** is a Dreamweaver-era PHP site from around 2006, running on
**PHP 5.6** — a version that stopped receiving security patches in 2018. Its
navigation is a row of JPEG images with `MM_swapImage` rollovers, its markup is
XHTML 1.0 Transitional, and it carries an `<!--[if lt IE 7]>` block. There is no
`robots.txt` and no sitemap.

The **prototype** was a Base44-generated React app at
`first-asset-flow.base44.app`. It was a real improvement on the look, but every
page was rendered in the browser from one JavaScript bundle, so the pages did
not exist as files, the copy could not be reviewed in a diff, and the logo and
hero art were hosted on `base44.app` and `media.base44.com` — buckets that go
away with the platform.

This repository is the same site as plain HTML: eight pages, one stylesheet, one
inline script for the mobile menu, and every filing and form served from our own
domain.

## The thing the rebuild actually fixed

The prototype advertised **"Managed Portfolios — professionally managed
portfolios tailored to your objectives."**

The firm's own filed Form CRS says, in the second sentence, that First Asset
Financial *is not* a registered investment adviser, and says later that it does
not monitor accounts on a continuing basis. A broker-dealer advertising managed,
objective-tailored portfolios is describing a business its registration does not
cover.

It also linked a Form CRS that **404s** — the SEC requires that document to be
posted on the firm's public website, and the link pointed at a filename that
does not exist on the host.

Both are fixed, along with eight other items. The full review is in
[`content/COMPLIANCE.md`](content/COMPLIANCE.md), which is the most important
file in this repository and should be read before any copy changes.

## Layout

| Path | What it is |
|---|---|
| `public/` | **The deployable site.** Point the host's publish directory here. |
| `public/assets/` | Stylesheet, logos, icons, social card. |
| `public/assets/docs/` | The filings and account forms, self-hosted. |
| `build.py` | Generates every page. |
| `content/COMPLIANCE.md` | The rule-by-rule review. Read this first. |
| `content/disclosures.json` | The regulatory document roster. |
| `content/forms.json` | The account-form roster. |
| `content/resources.json` | The third-party links, each with the date it was verified. |
| `content/og-card.html` | Source of the social image (see below). |

## Pages

| Path | Reader |
|---|---|
| `/` | Both — states the firm, says how it is paid, then forks |
| `/services/` | Investors — what can be placed, and brokerage vs. advisory |
| `/disclosures/` | Investors, regulators, anyone checking us out |
| `/form-crs/` | The one document an examiner looks for first |
| `/forms/` | Customers opening or moving an account |
| `/resources/` | Investors, and it is deliberately short |
| `/brokers/` | Registered representatives considering a move |
| `/contact/` | Both |

## Editing

Every page is generated, the home page included — there is no hand-maintained
page to drift away from the shell. Edit `build.py`, then:

```bash
python3 build.py
```

> **Do not hand-edit anything under `public/` except `assets/`.** The next build
> overwrites the HTML.

Firm-wide facts — the phone numbers, the address, CRD and SEC numbers, the state
count, the clearing firm — are constants at the top of `build.py` and are used by
the header, the footer, the page bodies and the JSON-LD. Change the constant, not
the eight places it appears.

**Copy changes need a registered principal's approval before they go live**, under
FINRA Rule 2210(b)(1)(A). Record the approval against the commit hash. A commit
is not an approval.

### Filings and forms

The rosters live in `content/disclosures.json` and `content/forms.json`. The PDFs
themselves are **committed to this repository** under `public/assets/docs/`,
because the previous copies lived on the old PHP host under names like
`new_accout_form_finra-fillable.pdf` and `CRS form.pdf` — one of them misspelled,
one with a space in it, and one (`form_crs.pdf`) that the prototype linked and
that never existed at all.

When a document is replaced, add the new file under a new dated name and point
the JSON at it. **Do not overwrite a file in place:** `netlify.toml` caches that
folder for a week, so an overwritten document would sit stale in caches while the
superseded version was still being served.

### Third-party links

`content/resources.json` carries a `checked` date on every entry, and the page
prints it. Re-verify annually.

The reason for the ceremony is in `COMPLIANCE.md`, item 10: the page this
replaced carried 78 links, of which 21 were dead and at least a dozen silently
resolved to a different company than the link text named. Two decades is long
enough for a fund family to be acquired twice.

### The social image

`public/assets/og-image.png` is rendered from `content/og-card.html`, which is
kept out of `public/` so it is never served as a page of the site. To regenerate
it after a copy change:

```bash
cp content/og-card.html public/_ogcard.html && python3 -m http.server 8899 --directory public &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
  --window-size=1200,630 --virtual-time-budget=8000 \
  --screenshot=public/assets/og-image.png http://localhost:8899/_ogcard.html
rm public/_ogcard.html
```

### Previewing

```bash
python3 -m http.server 8811 --directory public
```

Note that this does **not** reproduce the host's behaviour for 404s or the
redirects in `netlify.toml`. Use `netlify dev` if you need those.

## Design

The palette is the navy and gold of the firm's own mark (`#0B1F3A`, `#F0B743`)
on warm paper, with the gold darkened to `#7A5F16` wherever it has to carry text
on a light ground — the mark's own gold fails contrast at body size. Type is
Playfair Display for what the firm commits to and Inter for everything that is
interface, both from Google Fonts. Both were the prototype's choices and are kept
deliberately, so the rebuild is not a surprise to anyone who saw it.

### The logo

Everything is derived from the two supplied files, so there is no hand-traced art
anywhere:

| File | What it is |
|---|---|
| `faf-logo-compact.svg` | **What the site actually uses.** Mark plus FIRST ASSET FINANCIAL, no membership line, on the navy header and footer |
| `faf-logo-whitetext.svg` | The full supplied lockup, membership line included. Used on the social card and right for anything 400px or wider |
| `faf-logo-compact-navy.svg` | The compact lockup for light grounds. Not currently used — kept for print and any future light header |
| `faf-logo-navytext.svg` | The full lockup for light grounds |
| `faf-icon-white.svg` | The supplied mark alone |
| `faf-mark-navy.svg` | The mark for light grounds |
| `favicon.svg` | The mark on its own navy ground, padded into a 512-square so a round icon mask does not crop the wings |
| `favicon-32.png`, `apple-touch-icon.png`, `icon-512.png` | Rendered from `favicon.svg`, for clients that will not take an SVG icon |

**Why the site drops the membership line.** The supplied lockup sets
"MEMBER SIPC | FINRA" at roughly a tenth the cap height of the name. At the
200–240px the header and footer can spare, that line is below the size anyone can
read — and it forces FIRST ASSET FINANCIAL small to make room for text nobody is
reading. The compact lockup is the same artwork with the viewBox cropped at
y=206, which cuts cleanly between the wordmark and the membership line. No paths
were edited.

Nothing is lost by dropping it: the footer of every page states the FINRA and
SIPC membership in full, in a sentence, where it can actually be read — which is
what Rule 2210(d)(3) is interested in anyway.

The full lockup is not deleted, and it is the right one above about 400px wide,
where the membership line becomes legible again — the social card, print, a
slide. Switching back is two `img` tags in `build.py` and two widths in the
stylesheet.

To regenerate the rasters after a logo change, render `favicon.svg` at 512px and
downsample — the commands are the same headless-Chrome pattern as the social
image above.

### No photography, by decision

The prototype used two AI-generated images: a glass-skyscraper skyline behind the
hero and a fountain pen on textured paper. Neither was kept.

The skyline is the stock idea of a financial firm and it is the wrong idea for
this one — a 20-person broker-dealer on Iron Avenue in Salina, Kansas is not a
firm with a tower, and the picture quietly told a reader otherwise. Generated
imagery also has no licence trail, which matters more than usual for a file that
would be sitting on a regulated firm's website.

So the design carries its weight with type, rule and colour instead, and the
pages are faster for it. **If real photography is ever commissioned**, the
obvious slot is behind `.hero` on the home page, as a CSS background under a
navy scrim — the pattern the Your IA site uses, which is worth copying because a
missing file degrades to the plain navy ground rather than to a broken image.
What to shoot: the actual office, the actual people, in Salina.

## Known gaps

- **No contact form, by decision.** The prototype had none either — the contact
  page lists a telephone number, and that is how this firm actually works.
  Adding one would mean either a host-side form handler or a third-party embed,
  and the embed would have to be named in the `Content-Security-Policy` in
  `netlify.toml` **in the same commit**, or it will fail silently. A form would
  also collect personal information from prospective customers, which brings
  privacy-notice and books-and-records questions with it. The telephone number
  has none of those problems.
- **No analytics, by decision.** The upside is real: because the pages load
  Google Fonts and nothing else third-party, `netlify.toml` carries an actual
  `Content-Security-Policy`.

  **If analytics is ever added, the CSP must change in the same commit.** A
  `script-src` that does not name the analytics origin blocks the tag silently —
  no error a visitor or an editor would ever see, just a site that quietly
  records nothing. A cookieless provider avoids the consent-banner question
  entirely and needs one origin added to `script-src` and `connect-src`.
- **The broker portal is gone.** The prototype's password gate is removed, with
  its reasoning in `COMPLIANCE.md` item 9. If the firm wants gated recruiting
  material, that belongs behind real authentication on a separate host, not
  behind a password printed above the form.
- **`/resources/` lost 69 links.** That is a real loss of a page some people
  bookmarked, accepted deliberately. The reasoning is on the page itself and in
  `COMPLIANCE.md` item 10.

## Before cutover

The compliance checklist is in
[`content/COMPLIANCE.md`](content/COMPLIANCE.md#before-cutover) and comes first.
The technical list:

- [ ] **Delete the `X-Robots-Tag = "noindex, nofollow"` block from
      `netlify.toml`.** It is there to keep the staging URL out of search while
      the site is in review. It is a blanket rule, so if it survives the cutover
      the real site stays invisible to Google indefinitely, silently, with
      nothing on the page to show for it. **This is the single easiest step to
      forget and the most expensive one to discover late.**
- [ ] **Export the old host's configuration before tearing it down.** The live
      site runs on Apache with PHP 5.6. There is no database, but there may be
      `.htaccess` rules, and the mail configuration for
      `FAF@FirstAssetFinancial.com` is the thing that will hurt if it is lost.
- [ ] **Export all DNS records first, especially MX, SPF, DKIM and DMARC.**
      `FAF@FirstAssetFinancial.com` is live mail; moving nameservers without
      carrying those over silently kills it.
- [ ] Lower DNS TTLs to ~300s a day ahead.
- [ ] **Re-check the redirect list against the old host.** `netlify.toml` covers
      all seven `.php` pages, all sixteen PDF paths under `/assets/pdf/`, and the
      prototype's paths. Netlify paths are case-sensitive; if the old site's logs
      show capitalised variants, add them.
- [ ] Confirm the host serves `index.html` for directory requests and
      `404.html` for unmatched paths.
- [ ] Submit the new `sitemap.xml`. The old site had neither a sitemap nor a
      `robots.txt`, so there is no stale one to supersede.

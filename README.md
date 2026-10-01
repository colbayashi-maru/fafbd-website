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

## What the firm is, as of September 2026

**First Asset Financial is a limited-scope broker-dealer.** Its securities
business is four product lines: mutual funds, variable annuities, registered
index-linked annuities (RILAs) and variable universal life. It places no
individual securities of any kind — no stocks, bonds, ETFs, municipal
securities, options or CDs.

The firm restricted its business in September 2026 to the three variable
contracts, then added mutual funds back on 1 October 2026. Both moves are
recorded in the compliance file; the second one raises a FINRA Rule 1017
question that has to be answered before this site goes live.

That restriction is recent, and it reaches much further through this site than
a product list. `WHAT_WE_ARE` and `WHAT_WE_PLACE` at the top of `build.py` are
the two strings that carry it; the word "full-service" appears nowhere, because
it was true of the old business and is not true of this one.

**Read [`content/COMPLIANCE.md`](content/COMPLIANCE.md), section "The scope
change", before touching any product copy.** In particular: the Form CRS
currently posted on this site describes the *old* business, and cannot ship as
it stands.

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
| `public/assets/photos/` | The hero photograph, as JPEG and WebP. |
| `build.py` | Generates every page. |
| `brand/` | The supplied logo files. **Never edited.** |
| `tools/make-assets.py` | Derives every logo and icon in `public/assets/` from `brand/`. |
| `content/COMPLIANCE.md` | The rule-by-rule review. Read this first. |
| `content/disclosures.json` | The regulatory document roster. |
| `content/forms.json` | The account-form roster. |
| `content/resources.json` | The third-party links, each with the date it was verified. |
| `content/og-card.html` | Source of the social image (see below). |

## Pages

| Path | Reader |
|---|---|
| `/` | Both — states the firm, says how it is paid, then forks |
| `/services/` | Investors — the four products, what they cost, and brokerage vs. advisory |
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
count, the clearing firm, and **what the firm is permitted to sell** — are
constants at the top of `build.py` and are used by the header, the footer, the
page bodies and the JSON-LD. Change the constant, not the eight places it
appears.

`WHAT_WE_ARE`, `WHAT_WE_PLACE` and `WHAT_WE_DO_NOT` are the three that matter
most. They are the firm's regulatory scope in prose, and they appear in the
hero, the footer of every page, the JSON-LD and every meta description. The
negative one exists as a constant so the two places it appears cannot drift
apart. **If the membership agreement changes again, change them first.**

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

The palette is the two colours of the firm's own mark: the brand slate
`#2B3439` and the gold `#F0B743`, on warm paper.

**Note what this corrects.** The Base44 prototype was built in a navy,
`#0B1F3A`, that appears nowhere in the brand files — it is a colour the
generator chose. The supplied artwork is drawn in `#2B3439`, a dark slate with a
green cast, and the site now uses that. It is a quieter, warmer colour than the
navy and it sits better against the paper.

The one derived value is `--gold-deep`, `#7A5F16`. The brand gold reads at
6.99:1 on the slate and is used as supplied there, but on paper it is 1.64:1 —
invisible. Anywhere the accent has to carry text on a light ground, the darkened
version is used instead: 5.45:1 on paper, 5.08:1 on the warm band.

Type is Playfair Display for what the firm commits to and Inter for everything
that is interface, both from Google Fonts. Both were the prototype's choices and
are kept deliberately, so the rebuild is not a surprise to anyone who saw it.

### The logo

`brand/` holds the four files as the designer supplied them and is **never
edited**. Everything under `public/assets/` that carries the mark is generated
from them by `tools/make-assets.py`, so there is no hand-traced art anywhere:

```bash
python3 tools/make-assets.py
```

| Source in `brand/` | Supplied as |
|---|---|
| `faf-lockup.svg` | Mark plus FIRST ASSET FINANCIAL, no membership line |
| `faf-lockup-with-memberships.svg` | The same with MEMBER SIPC \| FINRA beneath |
| `faf-mark.svg` | The winged A alone |
| `faf-wordmark.svg` | The type alone |

| Generated in `public/assets/` | What it is |
|---|---|
| `faf-lockup-reversed.svg` | **What the header and footer actually use.** The lockup recoloured for the slate ground |
| `faf-lockup.svg` | The same for light grounds — print, a document, a future light header |
| `faf-lockup-full-reversed.svg` | The membership lockup, reversed. **The social card uses this** |
| `faf-lockup-full.svg` | The membership lockup for light grounds |
| `faf-mark.svg`, `faf-mark-reversed.svg` | The mark alone, both grounds |
| `faf-wordmark.svg` | The type alone |
| `favicon.svg` | The mark on its own slate ground, padded into a 512-square so a round icon mask does not crop the wings |
| `favicon-32.png`, `apple-touch-icon.png`, `icon-512.png` | Rendered from `favicon.svg`, for clients that will not take an SVG icon |

The only change the script makes to the artwork is colour: `#2b3439` becomes
white for the reversed variants. **The gold is never touched** — it reads at
6.99:1 on the slate, so there is no reason to.

**Which lockup goes where.** The membership line is set at roughly a tenth the
cap height of the name. At the 208–240px the header and footer can spare, it is
below the size anyone can read, so those use the lockup without it. The social
card runs the logo at 440px, where the line is legible, so it uses the full one.
Roughly 400px is the crossover.

Nothing is lost in the header by dropping that line: the footer of every page
states the FINRA and SIPC membership in full, in a sentence, where it can
actually be read — which is what Rule 2210(d)(3) is interested in anyway.

To regenerate the rasters after a brand revision, replace the file in `brand/`,
re-run the script, then render `favicon.svg` at 512px and downsample — the
commands are the same headless-Chrome pattern as the social image above.

### The hero photograph

`public/assets/photos/home-hero.jpg` sits behind the home page hero, as a CSS
background under a scrim — not an `<img>`. Two consequences worth knowing:

1. **A missing file is not a broken image.** `build.py` emits the `hero-photo`
   class and its custom properties only when the file exists, and the
   stylesheet draws the brand ground underneath either way. Delete the photo
   and the hero still reads, on plain slate.
2. **The left ~55% of the frame is under a near-opaque scrim**, because the
   headline sits there. Any replacement wants its subject **right of centre**.
   The CSS anchors at `68% 58%`.

`build.py` emits both a plain `url()` every browser understands and an
`image-set()` override that modern browsers use to take the WebP instead, at
roughly half the bytes. **Below 720px the image is dropped entirely** — the
headline fills the frame at that width, so phones never download it.

To swap one in:

```bash
python3 - <<'EOF'
from PIL import Image
i = Image.open('/path/to/new.jpg').convert('RGB')
i.save('public/assets/photos/home-hero.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
i.save('public/assets/photos/home-hero.webp', 'WEBP', quality=74, method=6)
EOF
python3 build.py
```

**About the image that is there now.** It is the one the Base44 prototype used:
an AI-generated blue-hour glass tower beside a neoclassical building, mirrored
so the lit colonnade falls right of the scrim, cropped 16:9 out of the 1024px
square original and stripped of metadata. Two things to know about it, recorded
because they are easy to forget:

- **It has no licence trail.** It was generated, not shot or licensed, so there
  is no invoice and no rights holder to point at. That is usually fine and
  occasionally is not.
- **It is not this firm.** A glass tower is the stock idea of a financial firm;
  First Asset Financial is twenty-odd people on Iron Avenue in Salina, Kansas.

Neither is a reason it cannot ship, and it is the client's call. But if real
photography is ever commissioned, the slot is already built and the swap is the
four lines above. What to shoot: the actual office, the actual people, in
Salina.

The prototype's second generated image — a fountain pen on textured paper — is
not used. Stock-photo shorthand for signing something, in a design that does
not need it.

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

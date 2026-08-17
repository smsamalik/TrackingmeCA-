# TrackingmeCA Website

A static, multi-page, SEO-ready marketing website for Trackingme Ltd. (TrackingmeCA), a Canadian fleet technology company (ELD, GPS, AI dashcams, installation). No runtime build step or dependencies to *serve* the site — open `index.html` directly or serve the folder with any static file host. A small Jinja2 build step (see below) generates the pages listed under "Templated pages" from shared partials, so the *source* doesn't require hand-copying the header/footer into every file.

## 2026 repositioning

The site was rebuilt around a new commercial strategy: TrackingmeCA as "Canada's practical fleet technology partner" (ELD + GPS + video, professionally installed and Canadian-supported) rather than a generic telematics vendor. See the [rebuild manifest](https://claude.ai/code/artifact/87a3be7d-311e-4192-a858-dd2ee4fb944a) for the audit, sitemap, wireframe, design-system and SEO-map this was built against.

## Structure

```
index.html               Homepage — generated, see build/templates/pages/index.html.j2
eld-canada/               ELD Canada (generated)
eld-dashcam-canada/       ELD + Dashcam bundle, the flagship conversion page (generated)
fleet-dashcam-canada/     AI dashcams / video telematics (generated)
gps-fleet-tracking-canada/  GPS fleet tracking (generated)
solutions/                Driver monitoring, CAN Bus, fuel monitoring, cold-chain (hand-authored, URLs kept)
industries/               Hub + trucking, logistics, construction, courier-delivery, towing,
                          field-service, cold-chain (generated)
installation-network/    Canada installation coverage (generated)
become-an-installer/     Installer recruitment + application form (generated)
partners.html            Reseller / affiliate / installer referral program (generated)
cross-border-fleet/      Canada-U.S. cross-border considerations (generated)
integrations/            Integration categories; intentionally lists no specific partners
                          until confirmed (generated)
careers/                 Careers page; ships with zero fake listings (generated)
contact.html             Smart lead-generation form (hand-authored)
about.html, resources.html, blog.html, blog/  (hand-authored, unchanged this pass)
privacy-policy.html, terms.html               (hand-authored, unchanged this pass)
_redirects                Netlify/Cloudflare Pages-style 301 map for retired URLs
solutions/eld.html, solutions/dashcams.html,  Meta-refresh + noindex redirect stubs
solutions/gps-tracking.html, industries.html  (see "Redirect map" below)
css/style.css             Design system (design tokens, components)
css/fonts/                Self-hosted Montserrat (brand-mandated typeface)
js/main.js                Nav, dropdowns, FAQ accordion, tabs, reveal-on-scroll, lead-form submit
js/lead-config.js         Google Sheets Apps Script endpoint (see "Lead capture setup")
tools/apps-script/Code.gs Apps Script source for the lead-capture Sheet
assets/                   Real brand logo exports + favicons + SVG infographics
build/                    Jinja2 templates + build.py (see "Templated pages" below)
brand-source/             Original client-uploaded files — kept for reference, not linked
robots.txt, sitemap.xml
```

## Templated pages

Every page listed as "(generated)" above is rendered by `build/build.py` from
`build/templates/base.html.j2` (shared header/mega-menu/footer/mobile CTA bar)
plus a per-page template in `build/templates/pages/`. Page metadata (title,
description, canonical, JSON-LD) lives in the `PAGES` list in `build.py`
itself — that list is also the authoritative SEO map for these pages.

To rebuild after editing a template or `build/data/site.json`:

```
pip install -r build/requirements.txt   # once
python3 build/build.py
```

This is the *only* thing that writes the generated paths above — every
hand-authored page (solutions/driver-monitoring.html, about.html, blog/*,
etc.) is untouched by it. Seven industry pages share one generic template
(`industry.html.j2`) driven by per-industry data in `build.py`'s
`industry_page()` calls, rather than seven near-duplicate files.

## Redirect map

Four URLs were replaced by clean, keyword-qualified equivalents. Rather than
deleting the old indexed URLs, each retired path is now a `noindex` stub with
`rel=canonical` and an instant meta-refresh to its replacement, and the same
mapping is duplicated in `_redirects` for hosts that honour that format
(Netlify, Cloudflare Pages):

| Old URL | New URL |
|---|---|
| `/solutions/eld.html` | `/eld-canada/` |
| `/solutions/dashcams.html` | `/fleet-dashcam-canada/` |
| `/solutions/gps-tracking.html` | `/gps-fleet-tracking-canada/` |
| `/industries.html` | `/industries/` |

Everything else kept its existing URL (`/solutions/driver-monitoring.html`,
`/solutions/can-bus.html`, `/solutions/fuel-monitoring.html`,
`/solutions/cold-chain.html`, `/about.html`, `/contact.html`,
`/resources.html`, `/blog.html`, `/blog/*`, `/partners.html`,
`/privacy-policy.html`, `/terms.html`) — nothing was redirected to the
homepage as a catch-all.

**Known gap:** internal links from the hand-authored pages that weren't
touched this pass (about.html, resources.html, contact.html, blog.html,
blog/*, solutions/driver-monitoring.html, solutions/can-bus.html,
solutions/fuel-monitoring.html, solutions/cold-chain.html) still point at the
four old URLs above and their old-style single-column nav — they'll reach the
right page via the redirect/old nav, but not by the shortest path, and their
header/footer don't yet match the new mega-menu. Bringing those into
`build/build.py` as templated pages (same pattern as `partners.html`) is the
cleanest way to close this gap; flagging it here rather than leaving it
implicit.

## Brand assets — now using the real TrackingMe.ca brand

The client uploaded the official logo files and brand guidelines
(`brand-source/Tracking Brand Guidelines (Canada).pdf`, v2.1) directly to the
repo. The site was updated to match:

- **Colours** — Dark Turquoise `#00ABBE` and Sunshade Orange `#F99E4B` (the two
  official brand colours), plus black/white as guideline-approved neutrals.
  Defined as CSS variables in `css/style.css` (`--turquoise`, `--orange`, `--ink`,
  etc). Neither raw brand hue meets WCAG AA text contrast on white (turquoise
  ≈2.8:1, orange ≈2.1:1), so accessible **derived shades** (`--turquoise-deep`,
  `--turquoise-deeper`) are used for text, links, buttons-with-white-text and
  focus states, while the raw brand hues are reserved for large fills, icons
  and decorative accents. Primary buttons use orange with dark ink text
  (8.5:1), which stays fully accessible while keeping the vivid brand colour.
- **Typography** — Montserrat, self-hosted as a variable-font WOFF2
  (`css/fonts/`, ~57KB total for the full weight range + italic) so the
  mandated typeface loads with no third-party font request.
- **Logo** — `assets/logo-full-color.png` (header, on white) and
  `assets/logo-white.png` (footer/dark sections) are extracted directly from
  the true vector paths in the client's `brand-source/Tracking Canada_Logo.pdf`
  (via PyMuPDF → SVG → transparent PNG), not redrawn or traced — so edges are
  pixel-perfect at any size, with no JPEG compression artifacts. No artwork
  was altered, per the guideline's "do not edit the logo" rule.
  `assets/favicon-*.png` / `apple-touch-icon.png` crop just the icon mark
  from the same vector source (favicons necessarily can't fit the wordmark);
  the guidelines reserve icon-alone usage for the marketing team, so please
  have them confirm that exception. The horizontal lockup mentioned in the
  guidelines (icon beside wordmark) wasn't included in the uploaded files —
  only the stacked "Main Version" was, so that's what's used sitewide, sized
  to stay legible in the nav header.
- **Contact email** — `info@trackingme.ca`, the address given in the brand
  guidelines, now used everywhere (replacing the earlier placeholder).
- **Phone number** — real number `(416) 779-7382` / `tel:+14167797382`, now used
  everywhere (site text, `tel:` links, and the LocalBusiness/Organization JSON-LD),
  replacing the earlier `1-800-555-0199` placeholder.
- **Social links** — footer icons now point to the real accounts (Facebook,
  X, Instagram) and are listed in the Organization schema's `sameAs`. Added to
  every page's footer, not just the homepage.
- **Hardware terminology** — light, factual mentions added to
  `solutions/dashcams.html` (MDVR / G-sensor / night-vision hardware class),
  `solutions/gps-tracking.html` (plug-and-play trackers with no monthly
  SIM fee as one hardware option), and `solutions/cold-chain.html` (Elitech
  RCW-360Pro–class 4G wireless sensors), based on reference product graphics
  provided directly. No specific prices, model availability, or claims beyond
  what was shown were added — confirm current SKUs before publishing.
- **Infographics** — all 22 `.photo-frame` placeholder boxes (dashed border +
  emoji icon) across the homepage, About, Blog and every solution page have
  been replaced with real custom SVG illustrations in `assets/infographics/`:
  dashboard/gauge mockups (fleet map, ELD Hours-of-Service dials, cold-chain
  temperature gauge, CAN Bus diagnostics cluster, fuel-tank sensor with
  theft alert) and diagrams (dashcam camera coverage, driver-monitoring risk
  icons, a Canada coverage map). 11 unique graphics are reused across the 22
  slots where the same page appears in multiple contexts (e.g., the ELD
  dashboard illustrates the homepage ELD section, the ELD solution page, and
  its blog card). These are illustrative diagrams, not real product
  screenshots — swap in actual UI screenshots and licensed photography
  before launch if you'd like the real thing instead.

## Remaining placeholders that still need real content before launch

- **Live site cross-check** — `trackingme.ca` and the Facebook/Instagram/X pages
  all block automated fetches (403), so facts like a physical address, exact
  published pricing, or testimonials couldn't be pulled from them automatically.
- **Pricing** — "starting from $XX" badges on the homepage are illustrative
  placeholders pending a real pricing sheet; all comparison-table claims avoid
  unverifiable "cheaper than X" statements per the brief.
- **Testimonials / case studies** — placeholder cards, explicitly labeled "pending
  customer approval," ready to swap for real quotes.
- **Lead-routing** — wired to a Google Sheet, not yet deployed (see "Lead capture
  setup" below). Until the Apps Script Web App is deployed, submissions are
  logged to the browser console instead of sent anywhere — nothing is lost, but
  nothing is delivered either.

## Lead capture setup

Every form with a `data-lead-form` attribute (homepage quote form, `contact.html`,
`partners.html` partner application, and any new lead forms added later) submits
to a Google Sheet acting as the CRM, via a Google Apps Script Web App. Each
submission is also emailed to `info@trackingme.ca`.

1. Create (or open) a Google Sheet to hold leads.
2. In that Sheet: **Extensions → Apps Script**, delete the boilerplate, and
   paste in the contents of `tools/apps-script/Code.gs`.
3. **Deploy → New deployment**, type **Web app**, execute as **Me**, access
   **Anyone**. Authorize the requested permissions (it needs to write to the
   Sheet and send email as you).
4. Copy the deployment URL and paste it into `js/lead-config.js` as
   `LEAD_ENDPOINT`, replacing the `REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL`
   placeholder. That's the only code change needed.
5. If `Code.gs` is edited later, create a **new version** under **Manage
   deployments** — editing the script doesn't update a live deployment on its
   own.

A `Leads` sheet tab is created automatically on first submission, with one
column per field collected across the site's forms (name, company, fleet
size, current provider, timeline, UTM parameters, landing page, etc.) — see
the `COLUMNS` list in `Code.gs` for the exact schema. Every form also carries
a hidden `_gotcha` honeypot field; a filled-in honeypot is treated as spam and
the submission is dropped client-side before it reaches the endpoint.

## Compliance notes (please review before publishing)

- **ELD certification language** is scoped throughout to "certified and approved
  configurations" per the brief — verify actual certification status of the
  specific hardware/firmware you sell before publishing.
- **B.C. dashcam section** (`solutions/dashcams.html#bc`) is based on verified,
  sourced public reporting as of this build: B.C.'s Bill M217, the *Dashboard
  Cameras in Commercial Vehicles Act*, passed third reading May 25, 2026, applies
  to commercial vehicles over 11,793 kg GVWR, requires a forward-facing camera
  only, and takes effect ~6 months after royal assent. The exact royal-assent
  date and final published regulations were not yet available — the page
  includes a disclaimer and should be re-verified against the Government of
  B.C.'s official published regulations before launch.
- **Privacy Policy / Terms** are placeholders meant to be finalized by qualified
  legal counsel — they are not legal advice.

## French readiness

The site is English-first with `lang="en-CA"` set on every page and a footer
"EN | FR — coming soon" indicator, per the brief's "French-language readiness"
requirement. No French content has been authored.

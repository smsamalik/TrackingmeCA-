# TrackingMe.ca Website

A static, multi-page, SEO-ready marketing website for TrackingMe.ca, a Canadian fleet telematics company. No build step or dependencies — open `index.html` directly or serve the folder with any static file host.

## Structure

```
index.html              Homepage (18 sections per the site brief)
solutions/               ELD, dashcams, driver monitoring, GPS, CAN Bus, fuel, cold-chain
industries.html          13 industry sections
partners.html            Reseller / affiliate / installer program + application form
contact.html             Smart lead-generation form
about.html
resources.html           FAQ hub (FAQPage schema)
blog.html                Blog index (3 full articles + coming-soon teasers)
blog/                    Full articles: ELD compliance, B.C. dashcam law, fuel theft prevention
privacy-policy.html      PIPEDA-oriented privacy policy incl. in-cab video/audio consent
terms.html
css/style.css            Design system (design tokens, components)
css/fonts/               Self-hosted Montserrat (brand-mandated typeface)
js/main.js               Nav, dropdowns, FAQ accordion, tabs, reveal-on-scroll, form UX
assets/                  Real brand logo exports (see below) + favicons
brand-source/            Original files uploaded by the client (brand guidelines PDF,
                         logo JPGs/PNG/PDF) — kept for reference, not linked from any page
robots.txt, sitemap.xml
```

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
- **Lead-routing** — `js/main.js` intercepts form submits and shows a confirmation
  message client-side only. Wire the `data-lead-form` submit handler to a real
  CRM/lead-routing endpoint before launch.

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

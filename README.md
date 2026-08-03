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

## Remaining placeholders that still need real content before launch

- **Photography** — every photo slot is a clearly labeled dashed-style placeholder
  (`.photo-frame`) with a caption describing exactly what authentic Canadian fleet
  photography should go there. No stock imagery was used.
- **Phone number** — `1-800-555-0199` (the North American reserved fictional
  number range) is still a placeholder pending a real support line.
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

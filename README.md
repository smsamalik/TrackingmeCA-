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
js/main.js               Nav, dropdowns, FAQ accordion, tabs, reveal-on-scroll, form UX
assets/favicon.svg       Placeholder brand mark
robots.txt, sitemap.xml
```

## Important: placeholders that need real content before launch

This was built from scratch — the repository contained no existing logo, brand
guidelines, photography, pricing, or contact details. The following were used
as clearly-marked placeholders and **must** be replaced before go-live:

- **Logo / brand mark** — an original navy/red pin-mark SVG wordmark was created
  (no existing TrackingMe.ca logo file was found in the repo). Swap `assets/favicon.svg`
  and the inline SVG in every page header/footer for the real logo.
- **Brand colours** — navy (`#0a2342`), ice blue and a red accent (`#d62828`) were
  chosen as a plausible, premium, restrained-Canadian palette (defined as CSS
  variables in `css/style.css`). Update the `:root` tokens if the real brand
  palette differs.
- **Photography** — every photo slot is a clearly labeled dashed-style placeholder
  (`.photo-frame`) with a caption describing exactly what authentic Canadian fleet
  photography should go there. No stock imagery was used.
- **Phone / email** — `1-800-555-0199` (the North American reserved fictional
  number range) and `hello@trackingme.ca` are placeholders.
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

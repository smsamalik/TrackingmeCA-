#!/usr/bin/env python3
"""Static site builder for TrackingmeCA.

Renders build/templates/pages/*.html.j2 against build/templates/base.html.j2
into the repo root, using the page metadata + output paths declared in PAGES
below. This is the ONLY thing that writes the files listed in PAGES — every
other page in the repo (solutions/*.html, blog/*.html, about.html, etc.) is
hand-authored and untouched by this script.

Why a build step at all, on a static site with no server: hand-copying the
header/mega-menu/footer into 40+ pages doesn't scale and drifts. This keeps
the *output* pure static HTML (deploys anywhere, no runtime dependency) while
keeping the *source* maintainable. See README > "Rebuilding the templated
pages" for the one-command usage.

Usage:
    pip install -r build/requirements.txt   # once
    python3 build/build.py
"""
import json
import pathlib

from jinja2 import Environment, FileSystemLoader, pass_context

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"

with open(BUILD_DIR / "data" / "site.json") as f:
    SITE = json.load(f)


def schema(*blocks):
    return [json.dumps(b, indent=2) for b in blocks]


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def industry_page(slug, name, eyebrow, h1, sub, capabilities_heading, capabilities,
                   infographic, infographic_alt, infographic_caption,
                   why_heading, why_cards, faqs, cta_heading, cta_sub,
                   title, description, disclaimer=None):
    return {
        "template": "industry.html.j2",
        "output": f"industries/{slug}/index.html",
        "root": "../../",
        "title": title,
        "description": description,
        "canonical": f"/industries/{slug}/",
        "schema_blocks": schema(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": f"Fleet Technology for {name}",
                "provider": {"@type": "Organization", "name": "Trackingme Ltd."},
                "areaServed": "CA",
                "description": description,
            },
            faq_schema(faqs),
        ),
        "industry_name": name,
        "eyebrow": eyebrow,
        "h1": h1,
        "sub": sub,
        "capabilities_heading": capabilities_heading,
        "capabilities": capabilities,
        "infographic": infographic,
        "infographic_alt": infographic_alt,
        "infographic_caption": infographic_caption,
        "why_heading": why_heading,
        "why_cards": why_cards,
        "faqs": faqs,
        "cta_heading": cta_heading,
        "cta_sub": cta_sub,
        "disclaimer": disclaimer,
    }


FAQS = [
    ("What is an ELD?", "An Electronic Logging Device automatically records a commercial driver's Hours of Service, replacing paper logbooks."),
    ("Do Canadian truck drivers need ELDs?", "Federally regulated commercial drivers in Canada are generally required to use a certified ELD to record Hours of Service — requirements vary by operation type and jurisdiction, so confirm what applies to your fleet."),
    ("Can TrackingmeCA install ELDs?", "Yes — professional installation is part of every ELD package, not a separate step you have to arrange yourself."),
    ("Can ELD and dashcam work together?", "Yes, our ELD + Vision package connects HOS, GPS and video in one dashboard instead of two separate systems."),
    ("Can I track trucks in real time?", "Yes — real-time GPS location is included in every package, from ELD-only through Fleet360."),
    ("Can the system support fleets crossing into the U.S.?", "Our packages support Canada-U.S. cross-border operation — see our cross-border fleet page for what to confirm before you rely on it operationally."),
    ("Does TrackingmeCA support small fleets?", "Yes — our packages are built primarily for 2-50 vehicle fleets, and scale to larger deployments."),
    ("Can TrackingmeCA replace an existing system?", "In many cases, yes. Request a Free Fleet Technology Review and we'll tell you honestly whether switching makes sense before you commit to anything."),
    ("How quickly can a fleet be installed?", "Timelines depend on fleet size and configuration — your fleet advisor will give you a specific installation schedule after your fleet review."),
    ("Do you provide support after installation?", "Yes — configuration, driver training and ongoing support are part of every package."),
]

FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in FAQS
    ],
}

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Trackingme Ltd.",
    "alternateName": "TrackingmeCA",
    "url": "https://www.trackingme.ca/",
    "logo": "https://www.trackingme.ca/assets/logo-full-color.png",
    "image": "https://www.trackingme.ca/assets/logo-full-color.png",
    "telephone": SITE["phone_href"].replace("tel:", ""),
    "email": SITE["email"],
    "sameAs": [SITE["social"]["facebook"], SITE["social"]["x"], SITE["social"]["instagram"]],
    "areaServed": "CA",
}

# Each entry drives one output file. `root` is the "../" depth prefix used by
# rootlink() and every asset/nav link in base.html.j2. This list is also the
# canonical SEO map for every page this build step owns — keep title/
# description in sync with what's actually on the page.
PAGES = [
    {
        "template": "index.html.j2",
        "output": "index.html",
        "root": "",
        "title": "ELD, GPS & Fleet Dashcams Canada | TrackingmeCA",
        "description": "ELD, GPS fleet tracking, AI dashcams and professional fleet technology installation for Canadian businesses. Get local support and fleet pricing from TrackingmeCA.",
        "canonical": "/",
        "schema_blocks": schema(ORG_SCHEMA, FAQ_SCHEMA),
    },
    {
        "template": "eld-canada.html.j2",
        "output": "eld-canada/index.html",
        "root": "../",
        "title": "ELD Canada | Electronic Logging Devices for Fleets | TrackingmeCA",
        "description": "ELD solutions for Canadian trucking fleets: Hours of Service, DVIR, IFTA mileage support and GPS, professionally installed and Canadian-supported.",
        "canonical": "/eld-canada/",
        "schema_blocks": schema(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": "Electronic Logging Device (ELD) Compliance",
                "provider": {"@type": "Organization", "name": "Trackingme Ltd."},
                "areaServed": "CA",
                "description": "ELD compliance solutions including Hours of Service monitoring, electronic driver logs, DVIR and IFTA mileage support for Canadian fleets.",
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": "Is TrackingmeCA's ELD certified for use in Canada?", "acceptedAnswer": {"@type": "Answer", "text": "Compliance claims apply only to certified and approved ELD hardware/firmware configurations, used and installed as directed. Certification can vary by device model and firmware version - confirm current certification for your specific configuration before relying on it for regulatory compliance."}},
                    {"@type": "Question", "name": "Is this suitable for a single owner-operator truck?", "acceptedAnswer": {"@type": "Answer", "text": "Yes - the platform is designed to scale from one truck to large commercial fleets, with pricing and packages suited to each."}},
                    {"@type": "Question", "name": "Does it support IFTA reporting?", "acceptedAnswer": {"@type": "Answer", "text": "The platform provides IFTA mileage support to help simplify fuel-tax reporting. Consult your tax advisor or provincial authority to confirm your specific filing obligations."}},
                ],
            },
        ),
    },
    {
        "template": "eld-dashcam-canada.html.j2",
        "output": "eld-dashcam-canada/index.html",
        "root": "../",
        "title": "ELD + Dashcam Canada | Connected Compliance & Video | TrackingmeCA",
        "description": "Compliance, GPS and video in one connected package for Canadian fleets. ELD, GPS, 4G dashcam, ECM data and IFTA mileage support, professionally installed.",
        "canonical": "/eld-dashcam-canada/",
        "schema_blocks": schema(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": "ELD and Dashcam Fleet Package",
                "provider": {"@type": "Organization", "name": "Trackingme Ltd."},
                "areaServed": "CA",
                "description": "Combined ELD compliance and AI dashcam video telematics package for Canadian fleets, connecting HOS, GPS, ECM and video in one dashboard.",
            }
        ),
    },
    {
        "template": "fleet-dashcam-canada.html.j2",
        "output": "fleet-dashcam-canada/index.html",
        "root": "../",
        "title": "Fleet Dashcams Canada | AI Video Telematics | TrackingmeCA",
        "description": "AI dashcams and video telematics for Canadian fleets: 4G LTE cameras, event detection, remote video retrieval and driver coaching, professionally installed.",
        "canonical": "/fleet-dashcam-canada/",
        "schema_blocks": schema(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": "Fleet Dashcams and Video Telematics",
                "provider": {"@type": "Organization", "name": "Trackingme Ltd."},
                "areaServed": "CA",
                "description": "AI dashcam and video telematics solutions including live streaming, automatic event capture, GPS-linked video and driver coaching for Canadian fleets.",
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": "Do dashcams increase insurance savings?", "acceptedAnswer": {"@type": "Answer", "text": "Video evidence can help speed up claims and disputes, but we don't make guaranteed insurance-savings claims - ask your insurer how dashcam footage affects your specific policy."}},
                    {"@type": "Question", "name": "Is a driver-facing camera required?", "acceptedAnswer": {"@type": "Answer", "text": "No - driver-facing cameras are optional on most configurations. B.C.'s current dashcam bill, as reported, only requires a forward-facing camera."}},
                ],
            },
        ),
    },
    {
        "template": "gps-fleet-tracking-canada.html.j2",
        "output": "gps-fleet-tracking-canada/index.html",
        "root": "../",
        "title": "GPS Fleet Tracking Canada | Commercial Vehicle Tracking",
        "description": "Real-time GPS fleet tracking for Canadian businesses: live location, geofencing, route history, idle monitoring and asset tracking, Canadian-supported.",
        "canonical": "/gps-fleet-tracking-canada/",
        "schema_blocks": schema(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": "GPS Fleet Tracking",
                "provider": {"@type": "Organization", "name": "Trackingme Ltd."},
                "areaServed": "CA",
                "description": "Real-time GPS fleet tracking including live location, geofencing, route history, idle monitoring and asset tracking for Canadian commercial fleets.",
            }
        ),
    },
    {
        "template": "installation-network.html.j2",
        "output": "installation-network/index.html",
        "root": "../",
        "title": "ELD, GPS & Dashcam Installation Canada | TrackingmeCA",
        "description": "Professional installation for ELD, GPS and dashcam fleet technology across Canada. Coverage available in Ontario, Alberta and B.C., expanding nationally.",
        "canonical": "/installation-network/",
        "schema_blocks": schema(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": "Fleet Technology Installation",
                "provider": {"@type": "Organization", "name": "Trackingme Ltd."},
                "areaServed": ["Ontario", "Alberta", "British Columbia"],
                "description": "Professional installation and configuration of ELD, GPS and dashcam fleet technology for Canadian commercial vehicles.",
            }
        ),
    },
    {
        "template": "become-an-installer.html.j2",
        "output": "become-an-installer/index.html",
        "root": "../",
        "title": "Become a Fleet Installer Canada | TrackingmeCA Installer Program",
        "description": "Join the TrackingmeCA installation network. For 12V technicians, GPS and dashcam installers, and mobile mechanics across Canada.",
        "canonical": "/become-an-installer/",
        "schema_blocks": schema(ORG_SCHEMA),
    },
    {
        "template": "partners.html.j2",
        "output": "partners.html",
        "root": "",
        "title": "Fleet Technology Partner Program Canada | TrackingmeCA",
        "description": "Join the TrackingmeCA partner program: recurring revenue, partner pricing, training and marketing support for resellers, affiliates and installation partners across Canada.",
        "canonical": "/partners.html",
        "schema_blocks": schema(ORG_SCHEMA),
    },
    {
        "template": "industries-hub.html.j2",
        "output": "industries/index.html",
        "root": "../",
        "title": "Fleet Technology by Industry Canada | TrackingmeCA",
        "description": "ELD, GPS and dashcam fleet technology by industry: trucking, logistics, construction, courier and delivery, towing, field service and cold-chain fleets.",
        "canonical": "/industries/",
        "schema_blocks": schema(ORG_SCHEMA),
    },
    industry_page(
        slug="trucking", name="Trucking",
        eyebrow="🚛 Trucking & Transportation",
        h1="Fleet Technology for Canadian Trucking Companies",
        sub="ELD compliance, GPS visibility and video evidence for long-haul, regional and cross-border trucking fleets.",
        capabilities_heading="Built Around How Trucking Fleets Operate",
        capabilities=[
            "ELD — Hours of Service (HOS) &amp; DVIR",
            "IFTA mileage support",
            "Canada–U.S. cross-border operation support",
            "Real-time GPS location &amp; route history",
            "AI dashcams for incident evidence",
            "ECM engine diagnostics &amp; fault codes",
        ],
        infographic="eld-hos-dashboard.svg",
        infographic_alt="ELD Hours of Service dashboard for trucking fleets",
        infographic_caption="HOS, DVIR and IFTA mileage, in one dashboard.",
        why_heading="What Trucking Fleets Deal With",
        why_cards=[
            {"icon": "📋", "title": "HOS Compliance", "desc": "Electronic logs and DVIR reduce paperwork and audit risk."},
            {"icon": "🛂", "title": "Cross-Border Operation", "desc": "Support for fleets running Canada-U.S. routes."},
            {"icon": "⛽", "title": "Fuel &amp; IFTA", "desc": "Mileage data that supports fuel-tax reporting."},
        ],
        faqs=[
            ("Does this work for owner-operators, not just large fleets?", "Yes &mdash; our ELD packages scale from a single truck to large commercial fleets."),
            ("Can I add dashcams to my existing ELD?", "In many cases, yes &mdash; ask a fleet advisor to review your current setup."),
        ],
        cta_heading="Keep Your Trucks Compliant and Visible",
        cta_sub="Get pricing for ELD, GPS and video &mdash; sized to your fleet.",
        title="Fleet Technology for Trucking Companies | TrackingmeCA",
        description="ELD, GPS and dashcam fleet technology for Canadian trucking companies: HOS compliance, IFTA mileage support and cross-border operation.",
        disclaimer="<strong>Compliance disclaimer:</strong> ELD compliance claims apply only to certified and approved hardware/firmware configurations, installed and used as directed. Confirm current certification for your specific configuration before relying on it for regulatory compliance.",
    ),
    industry_page(
        slug="logistics", name="Logistics",
        eyebrow="📦 Logistics",
        h1="Fleet Technology for Logistics Operators",
        sub="Visibility across multi-stop routes, fuel efficiency and fleet utilization for logistics and distribution fleets.",
        capabilities_heading="Built for Multi-Stop, Multi-Vehicle Operations",
        capabilities=[
            "Real-time GPS location across the fleet",
            "Route history &amp; trip playback",
            "Fleet utilization dashboards",
            "Idling &amp; fuel efficiency reporting",
            "Geofences for depots &amp; delivery zones",
            "Driver behaviour reporting",
        ],
        infographic="mockup-fleet-map.svg",
        infographic_alt="Fleet GPS tracking map for logistics operations",
        infographic_caption="Every vehicle, every stop, on one map.",
        why_heading="What Logistics Fleets Deal With",
        why_cards=[
            {"icon": "🗺️", "title": "Route Visibility", "desc": "See where every vehicle is against planned routes."},
            {"icon": "⛽", "title": "Fuel Costs", "desc": "Idling and driver-behaviour data to control fuel spend."},
            {"icon": "📊", "title": "Utilization", "desc": "Know which vehicles are underused before renewing a lease."},
        ],
        faqs=[
            ("Can this integrate with our dispatch software?", "Some integrations are available &mdash; see our <a href=\"../../integrations/\">integrations page</a> for confirmed options."),
            ("Does it support trailer tracking too?", "Yes &mdash; battery-powered asset trackers are available for trailers and equipment."),
        ],
        cta_heading="See Every Vehicle, Every Stop",
        cta_sub="Get pricing for GPS visibility across your logistics fleet.",
        title="Fleet Technology for Logistics Operators | TrackingmeCA",
        description="GPS fleet tracking and reporting for Canadian logistics operators: route visibility, utilization and fuel-efficiency reporting.",
    ),
    industry_page(
        slug="construction", name="Construction",
        eyebrow="🏗️ Construction",
        h1="Fleet &amp; Equipment Technology for Construction Companies",
        sub="Equipment tracking, idle time and fuel monitoring for vehicles and machinery that move between job sites.",
        capabilities_heading="Built for Job Sites, Not Just Highways",
        capabilities=[
            "Equipment &amp; asset tracking",
            "Fleet GPS across trucks and machinery",
            "Idle-time reporting",
            "Fuel monitoring &amp; theft detection",
            "Geofences for job-site boundaries",
            "AI dashcams for incident evidence",
        ],
        infographic="fuel-tank-sensor.svg",
        infographic_alt="Fuel tank sensor diagram with theft alert for construction equipment",
        infographic_caption="Catch fuel theft on equipment that sits overnight on site.",
        why_heading="What Construction Fleets Deal With",
        why_cards=[
            {"icon": "📦", "title": "Equipment Loss", "desc": "Geofencing and alerts for equipment that moves off-site."},
            {"icon": "⛽", "title": "Fuel Theft", "desc": "Sudden fuel-drop alerts on equipment left overnight."},
            {"icon": "⏱️", "title": "Idle Time", "desc": "See how much fuel is burned idling versus working."},
        ],
        faqs=[
            ("Can you track equipment without an ignition, like generators?", "Battery-powered portable asset trackers are available for equipment without constant power."),
            ("Do you track engine hours, not just mileage?", "Yes &mdash; ECM data includes engine-hour tracking where supported by the equipment."),
        ],
        cta_heading="Know Where Every Truck and Machine Is",
        cta_sub="Get pricing for equipment tracking and fuel monitoring.",
        title="Fleet & Equipment Technology for Construction | TrackingmeCA",
        description="GPS, fuel monitoring and asset tracking for Canadian construction fleets and equipment moving between job sites.",
    ),
    industry_page(
        slug="courier-delivery", name="Courier & Delivery",
        eyebrow="📮 Courier & Delivery",
        h1="Fleet Technology for Courier &amp; Delivery Fleets",
        sub="Last-mile visibility, route history and driver safety for high-stop-density delivery operations.",
        capabilities_heading="Built for High-Volume, Multi-Stop Delivery",
        capabilities=[
            "Real-time GPS location",
            "Route history &amp; trip playback",
            "Idling &amp; utilization reports",
            "AI dashcams for driver safety",
            "Geofences for depots &amp; delivery zones",
            "Driver behaviour reporting",
        ],
        infographic="mockup-fleet-map.svg",
        infographic_alt="Fleet GPS tracking map for delivery routes",
        infographic_caption="Route history for every stop, every driver.",
        why_heading="What Delivery Fleets Deal With",
        why_cards=[
            {"icon": "⏱️", "title": "Delivery Windows", "desc": "Route history helps verify arrival and departure times."},
            {"icon": "🛡️", "title": "Driver Safety", "desc": "Dashcams provide evidence for high-frequency stop-and-go driving."},
            {"icon": "📈", "title": "Utilization", "desc": "See which routes and vehicles are most efficient."},
        ],
        faqs=[
            ("Can this help with delivery disputes?", "Route history and, where equipped, dashcam footage can help verify what happened on a specific stop."),
            ("Does it work for vans as well as trucks?", "Yes &mdash; our hardware supports cars, vans, straight trucks and tractors."),
        ],
        cta_heading="Get Visibility Into Every Route",
        cta_sub="Get pricing for GPS and dashcams sized to your delivery fleet.",
        title="Fleet Technology for Courier & Delivery Fleets | TrackingmeCA",
        description="GPS tracking and AI dashcams for Canadian courier and delivery fleets: route visibility, utilization and driver safety.",
    ),
    industry_page(
        slug="towing", name="Towing",
        eyebrow="🚨 Towing",
        h1="Fleet Technology for Towing Companies",
        sub="Dispatch visibility, driver safety and incident evidence for towing operations working around the clock.",
        capabilities_heading="Built for Roadside and Recovery Work",
        capabilities=[
            "Real-time GPS location for dispatch",
            "AI dashcams for roadside incident evidence",
            "Driver safety events",
            "Idling &amp; utilization reports",
            "ECM vehicle health &amp; fault codes",
            "Geofences for yard &amp; impound lots",
        ],
        infographic="dashcam-coverage.svg",
        infographic_alt="Dashcam camera coverage diagram for towing vehicles",
        infographic_caption="Video evidence for roadside incidents and disputes.",
        why_heading="What Towing Fleets Deal With",
        why_cards=[
            {"icon": "📍", "title": "Dispatch Accuracy", "desc": "Know which truck is closest to the next call."},
            {"icon": "🎥", "title": "Roadside Disputes", "desc": "Video evidence for incidents that happen roadside."},
            {"icon": "🔧", "title": "Vehicle Uptime", "desc": "ECM fault data helps catch issues before a breakdown."},
        ],
        faqs=[
            ("Can dispatchers see all trucks in real time?", "Yes &mdash; real-time GPS location is included in every package."),
            ("Does video help with liability disputes?", "Video evidence can help establish what happened on a call, though we don't guarantee case outcomes."),
        ],
        cta_heading="Dispatch Smarter, Protect Every Call",
        cta_sub="Get pricing for GPS and dashcams sized to your towing fleet.",
        title="Fleet Technology for Towing Companies | TrackingmeCA",
        description="GPS tracking and AI dashcams for Canadian towing companies: dispatch visibility, driver safety and roadside incident evidence.",
    ),
    industry_page(
        slug="field-service", name="Field Service",
        eyebrow="🧰 Field Service",
        h1="Fleet Technology for Field Service Businesses",
        sub="Job-site arrival tracking, route history and vehicle health for technicians on the road all day.",
        capabilities_heading="Built for Multi-Job-Site Days",
        capabilities=[
            "Real-time GPS location",
            "Route history &amp; job-site arrival tracking",
            "Geofences for customer sites",
            "ECM vehicle health &amp; fault codes",
            "Idling &amp; utilization reports",
            "Driver behaviour reporting",
        ],
        infographic="can-bus-gauges.svg",
        infographic_alt="CAN Bus vehicle diagnostics gauges for field service vehicles",
        infographic_caption="Catch vehicle issues before they cause a missed appointment.",
        why_heading="What Field Service Fleets Deal With",
        why_cards=[
            {"icon": "🕒", "title": "Arrival Verification", "desc": "Route history helps confirm when a technician arrived on-site."},
            {"icon": "🔧", "title": "Vehicle Reliability", "desc": "ECM fault data helps prevent a missed appointment from a breakdown."},
            {"icon": "🗺️", "title": "Territory Coverage", "desc": "See utilization across your service territory."},
        ],
        faqs=[
            ("Can we set geofences for customer locations?", "Yes &mdash; geofences can be configured for depots, customer sites or any relevant location."),
            ("Does this work for a small fleet of 3-5 vehicles?", "Yes &mdash; our packages are built primarily for 2-50 vehicle fleets."),
        ],
        cta_heading="Know Where Your Technicians Are",
        cta_sub="Get pricing for GPS and vehicle health monitoring.",
        title="Fleet Technology for Field Service Businesses | TrackingmeCA",
        description="GPS tracking and vehicle diagnostics for Canadian field service fleets: job-site visibility, route history and vehicle health.",
    ),
    industry_page(
        slug="cold-chain", name="Cold Chain",
        eyebrow="🌡️ Cold Chain",
        h1="Fleet Technology for Cold-Chain Logistics",
        sub="Temperature, humidity and door-sensor monitoring with documented proof of conditions for every delivery.",
        capabilities_heading="Built for Temperature-Sensitive Cargo",
        capabilities=[
            "Real-time temperature &amp; humidity monitoring",
            "Multi-zone cargo monitoring",
            "Door-open alerts",
            "Temperature-excursion alerts",
            "Historical reports for proof of compliance",
            "GPS &amp; route history",
        ],
        infographic="coldchain-gauge.svg",
        infographic_alt="Cold-chain monitoring dashboard showing temperature, humidity and door status",
        infographic_caption="Continuous temperature and humidity monitoring, zone by zone.",
        why_heading="What Cold-Chain Fleets Deal With",
        why_cards=[
            {"icon": "🌡️", "title": "Temperature Excursions", "desc": "Alerts when cargo temperature moves outside range."},
            {"icon": "📄", "title": "Proof of Conditions", "desc": "Historical reports document conditions for a specific delivery."},
            {"icon": "🚪", "title": "Door Discipline", "desc": "Door-open alerts help catch conditions that risk spoilage."},
        ],
        faqs=[
            ("Can I monitor multiple temperature zones in one trailer?", "Yes &mdash; multi-zone monitoring supports trailers with separate compartments for different temperature ranges."),
            ("How do I prove compliance for a delivery?", "Historical temperature and humidity reports can be exported to document conditions for a specific trip."),
        ],
        cta_heading="Protect Every Degree, Start to Finish",
        cta_sub="Get pricing for cold-chain monitoring sized to your fleet.",
        title="Fleet Technology for Cold-Chain Logistics | TrackingmeCA",
        description="Temperature and humidity monitoring for Canadian cold-chain fleets: door alerts, excursion alerts and proof-of-compliance reporting.",
    ),
    {
        "template": "cross-border-fleet.html.j2",
        "output": "cross-border-fleet/index.html",
        "root": "../",
        "title": "Cross-Border Fleet Technology Canada-U.S. | TrackingmeCA",
        "description": "Fleet technology considerations for Canada-U.S. cross-border operations: HOS differences, vehicle visibility, driver logs and IFTA.",
        "canonical": "/cross-border-fleet/",
        "schema_blocks": schema(ORG_SCHEMA),
    },
    {
        "template": "integrations.html.j2",
        "output": "integrations/index.html",
        "root": "../",
        "title": "Fleet Technology Integrations | TrackingmeCA",
        "description": "Confirmed integrations across ELD platforms, fleet management, hardware, cameras, sensors and business systems for TrackingmeCA.",
        "canonical": "/integrations/",
        "schema_blocks": schema(ORG_SCHEMA),
    },
    {
        "template": "careers.html.j2",
        "output": "careers/index.html",
        "root": "../",
        "title": "Careers at TrackingmeCA | Canadian Fleet Technology Jobs",
        "description": "Careers at TrackingmeCA, a Canadian fleet technology company growing across Ontario, Alberta and British Columbia.",
        "canonical": "/careers/",
        "schema_blocks": schema(ORG_SCHEMA),
    },
]


@pass_context
def rootlink(context, href):
    """Resolve a site-absolute href ('/eld-canada/') against the current page's root prefix."""
    root = context.get("root", "")
    if href.startswith("/"):
        return root + href.lstrip("/")
    return href


def main():
    env = Environment(
        loader=FileSystemLoader(str(BUILD_DIR / "templates")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["rootlink"] = rootlink
    env.globals["site"] = SITE

    for page in PAGES:
        tmpl = env.get_template(f"pages/{page['template']}")
        html = tmpl.render(**page)
        out_path = ROOT / page["output"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)
        print(f"built {page['output']}")


if __name__ == "__main__":
    main()

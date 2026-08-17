/**
 * TrackingmeCA lead capture — Google Apps Script Web App.
 *
 * Every form on the site with a [data-lead-form] attribute POSTs a JSON body
 * here (see js/lead-capture.js). This script appends the submission as a row
 * in a "Leads" sheet and emails a copy to NOTIFY_EMAIL.
 *
 * ── One-time setup ──────────────────────────────────────────────────────
 * 1. Create (or open) a Google Sheet to act as the lead CRM.
 * 2. Extensions > Apps Script, delete the boilerplate, paste this whole file.
 * 3. Deploy > New deployment > type "Web app".
 *      Execute as:      Me
 *      Who has access:  Anyone
 * 4. Copy the deployment URL and paste it into js/lead-config.js as
 *    LEAD_ENDPOINT. That's the only code change needed on the site side.
 * 5. Re-run "Deploy > Manage deployments" and create a new version any time
 *    this file changes — editing the script does not update a live deployment
 *    on its own.
 */

const NOTIFY_EMAIL = "info@trackingme.ca";
const SHEET_NAME = "Leads";

// Column order also defines what's written to each row — keep it in sync
// with the fields collected across the site's forms (see js/lead-capture.js
// for the full metadata every submission carries).
const COLUMNS = [
  "timestamp", "form", "name", "company", "email", "phone",
  "province", "city", "fleet_size", "industry", "vehicle_types",
  "solutions", "solution_required", "current_provider", "current_eld",
  "current_gps", "current_dashcam", "cross_border", "renewal_date",
  "primary_challenge", "timeline", "install_date", "message",
  "landing_page", "utm_source", "utm_medium", "utm_campaign", "utm_term",
];

function doPost(e) {
  try {
    const sheet = getOrCreateSheet_();
    const data = JSON.parse(e.postData.contents);
    data.timestamp = data.timestamp || new Date().toISOString();

    const row = COLUMNS.map(function (key) {
      const value = data[key];
      if (Array.isArray(value)) return value.join(", ");
      return value === undefined || value === null ? "" : value;
    });
    sheet.appendRow(row);

    sendNotification_(data);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(COLUMNS);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function sendNotification_(data) {
  const who = data.company || data.name || "Unknown";
  const subject = "New " + (data.form || "website") + " lead — " + who;
  const lines = COLUMNS
    .filter(function (key) { return data[key]; })
    .map(function (key) { return key + ": " + data[key]; });
  MailApp.sendEmail(NOTIFY_EMAIL, subject, lines.join("\n"));
}

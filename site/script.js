// You don't need to edit this file. It reads your settings from config.js.

const config = window.SITE_CONFIG || {};

// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

// ---------- Stretch goal 1: visitor counter ----------
async function showVisitorCount() {
  const url = config.VISITOR_COUNTER_URL;
  if (!url) return;
  const el = document.getElementById("visitor-count");
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    el.textContent = `You are visitor #${Number(data.visits).toLocaleString()}`;
    el.hidden = false;
  } catch (err) {
    // Keep the page working even if the counter is down.
    console.warn("Visitor counter unavailable:", err);
  }
}

// ---------- Stretch goal 2: contact form ----------
function setUpContactForm() {
  const url = config.CONTACT_FORM_URL;
  if (!url) return;

  const section = document.getElementById("contact");
  const form = document.getElementById("contact-form");
  const status = document.getElementById("contact-status");
  section.hidden = false;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      status.textContent = "Please fill in your name, a valid email and a message.";
      return;
    }

    const button = form.querySelector("button");
    button.disabled = true;
    status.textContent = "Sending…";

    const payload = Object.fromEntries(new FormData(form).entries());
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
      form.reset();
      status.textContent = "Thanks! Your message has been sent.";
    } catch (err) {
      console.warn("Contact form error:", err);
      status.textContent = "Sorry, something went wrong. Please try again later.";
    } finally {
      button.disabled = false;
    }
  });
}

showVisitorCount();
setUpContactForm();

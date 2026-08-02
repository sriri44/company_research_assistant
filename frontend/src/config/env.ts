// The only file allowed to read `import.meta.env` directly (see
// docs/ARCHITECTURE.md §13 — Configuration Strategy). Everything else
// imports `config` from here.
//
// No hardcoded fallback URL on purpose: silently defaulting to some dev
// URL risks a production build quietly pointing at the wrong backend.
// Every environment (local dev, production build) must set
// VITE_API_BASE_URL explicitly — see .env.example / .env.production.

interface AppConfig {
  apiBaseUrl: string;
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error(
    "VITE_API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env " +
      "(for local dev) and set it to your backend URL — see frontend/.env.production " +
      "for the production value.",
  );
}

export const config: AppConfig = { apiBaseUrl };

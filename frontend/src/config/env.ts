// The only file allowed to read `import.meta.env` directly (see
// docs/ARCHITECTURE.md §13 — Configuration Strategy). Everything else
// imports `config` from here.

interface AppConfig {
  apiBaseUrl: string;
}

export const config: AppConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
};

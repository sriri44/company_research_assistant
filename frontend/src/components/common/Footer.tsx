import { Link } from "react-router-dom";

import { Logo } from "@/components/common/Logo";

const FOOTER_LINKS = [
  { label: "Research", to: "/research" },
  { label: "Settings", to: "/settings" },
];

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="container flex flex-col items-center justify-between gap-6 py-10 sm:flex-row">
        <div className="flex flex-col items-center gap-3 sm:items-start">
          <Logo />
          <p className="max-w-xs text-center text-sm text-muted-foreground sm:text-left">
            AI-powered company research, competitor analysis, and growth opportunities — in
            seconds.
          </p>
        </div>

        <nav aria-label="Footer" className="flex items-center gap-6">
          {FOOTER_LINKS.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
      <div className="border-t border-border py-4">
        <p className="text-center text-xs text-muted-foreground">
          © {new Date().getFullYear()} ResearchAI. Built for demonstration purposes — no data
          leaves your browser.
        </p>
      </div>
    </footer>
  );
}

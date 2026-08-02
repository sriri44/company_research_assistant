import { Outlet } from "react-router-dom";

import { Footer } from "@/components/common/Footer";
import { Navbar } from "@/components/common/Navbar";

/** Shell for the Landing (and 404) pages: sticky Navbar + Footer, no
 * research sidebar. */
export function MarketingLayout() {
  return (
    <div className="flex min-h-dvh flex-col">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

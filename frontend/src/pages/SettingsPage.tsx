import { motion } from "framer-motion";

import { ApplicantForm } from "@/components/common/ApplicantForm";
import { ModelSettingsSection } from "@/components/common/ModelSettingsSection";
import { ThemeSettingsSection } from "@/components/common/ThemeSettingsSection";

export default function SettingsPage() {
  return (
    <div className="h-full overflow-y-auto scrollbar-thin">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="mx-auto w-full max-w-2xl space-y-6 px-4 py-8 sm:px-6"
      >
        <div>
          <h1 className="text-xl font-semibold tracking-tight">Settings</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your appearance, default model, and profile. Everything here is stored locally
            in your browser.
          </p>
        </div>

        <ThemeSettingsSection />
        <ModelSettingsSection />
        <ApplicantForm />
      </motion.div>
    </div>
  );
}

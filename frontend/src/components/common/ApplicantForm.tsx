import { Save } from "lucide-react";
import { useForm } from "react-hook-form";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useSettingsStore } from "@/hooks/useSettingsStore";
import { useToastStore } from "@/hooks/useToastStore";

interface SettingsFormValues {
  applicantName: string;
  applicantEmail: string;
  discordWebhookUrl: string;
  discordChannel: string;
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** Applicant profile + Discord integration placeholders, saved together
 * via a single "Save Settings" action — everything here is local-only
 * (see useSettingsStore), there is no backend to send it to yet. */
export function ApplicantForm() {
  const { applicantName, applicantEmail, discordWebhookUrl, discordChannel, saveSettings } =
    useSettingsStore();
  const showToast = useToastStore((state) => state.showToast);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SettingsFormValues>({
    defaultValues: { applicantName, applicantEmail, discordWebhookUrl, discordChannel },
  });

  const onSubmit = handleSubmit(async (values) => {
    await new Promise((resolve) => setTimeout(resolve, 400)); // mimic a save round-trip
    saveSettings(values);
    showToast({
      title: "Settings saved",
      description: "Stored locally in your browser — no backend yet.",
      variant: "success",
    });
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle>Profile & Integrations</CardTitle>
        <CardDescription>Used to personalize your reports. Nothing is sent anywhere.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-5" noValidate>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="space-y-1.5">
              <Label htmlFor="applicantName">Applicant Name</Label>
              <Input
                id="applicantName"
                placeholder="Ada Lovelace"
                aria-invalid={Boolean(errors.applicantName)}
                {...register("applicantName", { required: "Name is required" })}
              />
              {errors.applicantName && (
                <p className="text-xs text-destructive">{errors.applicantName.message}</p>
              )}
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="applicantEmail">Applicant Email</Label>
              <Input
                id="applicantEmail"
                type="email"
                placeholder="ada@example.com"
                aria-invalid={Boolean(errors.applicantEmail)}
                {...register("applicantEmail", {
                  required: "Email is required",
                  pattern: { value: EMAIL_PATTERN, message: "Enter a valid email" },
                })}
              />
              {errors.applicantEmail && (
                <p className="text-xs text-destructive">{errors.applicantEmail.message}</p>
              )}
            </div>
          </div>

          <Separator />

          <div>
            <div className="mb-3 flex items-center gap-2">
              <p className="text-sm font-medium">Discord Delivery</p>
              <Badge variant="secondary">Coming soon</Badge>
            </div>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="space-y-1.5">
                <Label htmlFor="discordWebhookUrl">Webhook URL</Label>
                <Input
                  id="discordWebhookUrl"
                  placeholder="https://discord.com/api/webhooks/..."
                  {...register("discordWebhookUrl")}
                />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="discordChannel">Channel Name</Label>
                <Input id="discordChannel" placeholder="#research-reports" {...register("discordChannel")} />
              </div>
            </div>
          </div>

          <Button type="submit" disabled={isSubmitting} className="gap-2">
            <Save className="size-4" />
            {isSubmitting ? "Saving…" : "Save Settings"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

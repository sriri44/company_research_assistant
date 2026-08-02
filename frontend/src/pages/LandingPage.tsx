import { LandingFeatures } from "@/components/common/LandingFeatures";
import { LandingHero } from "@/components/common/LandingHero";
import { LandingHowItWorks } from "@/components/common/LandingHowItWorks";

export default function LandingPage() {
  return (
    <>
      <LandingHero />
      <LandingFeatures />
      <LandingHowItWorks />
    </>
  );
}

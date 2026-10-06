import { CtaSection } from "@/components/sections/CtaSection";
import { FaqSection } from "@/components/sections/FaqSection";
import { HeroSection } from "@/components/sections/HeroSection";
import { ScamTypesSection } from "@/components/sections/ScamTypesSection";
import { StepsSection } from "@/components/sections/StepsSection";
import { TeamSection } from "@/components/sections/TeamSection";
import { WhySection } from "@/components/sections/WhySection";

export function IndividualsPageView() {
  return (
    <main className="page-template-services">
      <HeroSection />
      <StepsSection />
      <ScamTypesSection />
      <WhySection />
      <TeamSection />
      <FaqSection />
      <CtaSection />
    </main>
  );
}

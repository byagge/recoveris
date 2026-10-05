/** Page content for "Solution For Individuals" — edit all text here. */

export const pageMeta = {
  title: "Solution For Individuals - Recoveris",
  description:
    "Every blockchain transaction leaves a permanent, traceable record. While scammers count on you giving up, Recoveris investigators are experts at following the trail they left behind - tell us what happened, and we'll review the path of your funds and give you an assessment of recovery options.",
};

export const hero = {
  title: "For",
  titleHighlight: "Individuals",
  subtitle: "Your crypto was stolen, but it's not gone.",
  paragraphs: [
    "Every blockchain transaction leaves a permanent, traceable record. While scammers count on you giving up, we are able to follow the trail they left behind.",
    "Tell us what happened. We'll review the path of your funds and give you an honest assessment of whether recovery is possible.",
  ],
};

export const steps = {
  title: "Three steps",
  titleRest: "to recovery",
  subtitle:
    "We've turned the complex world of blockchain investigations into a clear, structured path toward getting your funds back.",
  items: [
    {
      title: "1. Initial Case Assessment",
      description:
        "You tell us what happened and share your transaction details. We immediately trace the movement of your funds to determine whether they've reached a point, such as a regulated exchange, where they can be intercepted.",
      icon: "assessment" as const,
    },
    {
      title: "2. Strategic Recovery Plan",
      description:
        "Based on our assessment, you receive a formal offer with a transparent breakdown of costs and the specific strategy we'll pursue: working with exchange compliance teams, token issuers, law enforcement, or a combination.",
      icon: "plan" as const,
    },
    {
      title: "3. Execution & Enforcement",
      description:
        "Our team produces court-admissible forensic reports, coordinates with the relevant authorities, and manages the freeze and recovery process. You stay informed at every stage until the funds are ready to be returned.",
      icon: "enforcement" as const,
    },
  ],
};

export const scamTypes = {
  title: "How did you lose",
  titleHighlight: "your crypto?",
  subtitle:
    "Scammers follow specific playbooks. Identifying how you were targeted is the first step in our investigation.",
  items: [
    {
      title: "1. Romance Scam",
      content:
        'Someone you met on social media or a dating app built trust over weeks or months. They introduced you to a "trading platform" where your balance appeared to grow. When you tried to withdraw, they demanded additional fees, taxes, or deposits.',
    },
    {
      title: "2. The Impersonation Scam",
      content:
        'You received an urgent call or message from someone posing as an exchange, a bank, a government agency, or tech support. They claimed your account was compromised and instructed you to move funds to a "safe wallet" or share your recovery phrase.',
    },
    {
      title: "3. Investment Scam",
      content:
        "A platform or individual promised guaranteed returns, insider information, or risk-free profits. You invested a small amount, it appeared to double, and you were encouraged to deposit much more. Withdrawals were then blocked or made conditional on further payments.",
    },
    {
      title: "4. Fake Exchange or Investing Platform",
      content:
        "You deposited funds into what appeared to be a legitimate trading platform. It had a professional interface, customer support, and even showed your portfolio growing. But the platform was entirely fabricated, and withdrawals were never processed.",
    },
    {
      title: "5. Malicious Link or Wallet Drainer",
      content:
        "You clicked a link promoting a free airdrop, NFT mint, or security update. When you connected your wallet or approved a transaction, your assets disappeared instantly.",
    },
    {
      title: "6. Hack or Malware",
      content:
        "Your device or wallet was compromised without any direct interaction with an attacker. Malware harvested your seed phrase from your computer, a clipboard hijacker swapped the destination address during a transaction, or a malicious browser extension drained your wallet in the background. By the time you noticed the unauthorized transaction, your funds had already been moved.",
    },
    {
      title: "7. Physical Theft or Coerced Transfer",
      content:
        'Someone gained direct physical access to your private keys, recovery phrase, hardware wallet, or login credentials — through a stolen device, a break-in, or written notes kept at home or in the office. In more severe cases, victims are threatened or physically forced to transfer their crypto themselves, known as a "wrench attack." The transaction looks legitimate on-chain, which is exactly why forensic tracing of where the funds moved next is critical to any recovery effort.',
    },
  ],
  alert: {
    title: "Don't see your exact situation?",
    text: "It doesn't matter. Our forensic tools look past the story and follow the actual movement of assets on the blockchain. Every scam leaves a trail.",
  },
};

export const whyRecoveris = {
  title: "Why",
  titleHighlight: "Recoveris",
  items: [
    {
      title: "Swiss-based, globally connected",
      description:
        "Headquartered in Zug, Switzerland, we're part of international task forces led by Interpol and have direct channels to compliance teams at 150+ crypto exchanges — so when stolen funds hit a platform that can freeze them, we know who to call.",
      icon: "swiss" as const,
    },
    {
      title: "A team you can verify",
      description:
        "Our investigators come from law enforcement, government financial intelligence, and leading blockchain firms. They publish research, speak at major industry events, and train authorities worldwide. Search their names, check their credentials.",
      icon: "verify" as const,
    },
    {
      title: "Heritage in law enforcement",
      description:
        "We are former law enforcement officers, financial intelligence experts, and forensic specialists. We know how criminals think and what prosecutors need to act. Today, we work with cybercrime units in 30+ countries and train investigators alongside the OSCE, Guardia di Finanza, and Cambridge University.",
      icon: "heritage" as const,
    },
    {
      title: "Human expertise, enhanced by AI",
      description:
        "Automated tools hit dead ends at mixers and bridges. Our team combines proprietary technology with hands-on forensic analysis to trace funds through obfuscation techniques that software alone cannot follow.",
      icon: "ai" as const,
    },
  ],
  warning: {
    title: "Be aware of crypto recovery scammers!",
    text: "Be cautious of fraudulent recovery firms that use pressure, artificial urgency, or promise guaranteed outcomes. Always verify you are interacting through official domains, check for media presence, and confirm team profiles on platforms like LinkedIn.",
    linkLabel: "More information",
    linkHref: "https://recoveris.io/impersonation-recovery-scams-warning/",
  },
};

export const team = {
  title: "Meet your",
  titleHighlight: "investigators",
  subtitle:
    "We know that every case carries real urgency and personal consequences. Our investigators have handled thousands of cases and recovered millions in stolen assets, combining advanced forensic techniques with hands-on case management to pursue the best possible outcome for you.",
  members: [
    {
      name: "Sol Cinosi",
      position: "Chief Government & Corporate Affairs Officer",
      image: "/images/team/sol-cinosi.png",
      linkedin: "http://linkedin.com/in/solcinosi",
      bio: "Attorney, co-created the Specialized Cryptoasset Investigation Task Force within the Cybercrime Department of the Public Prosecutor's Office of Buenos Aires, with 10+ years in criminal investigations. Expert in cross-border enforcement and virtual asset recovery. GBBC Ambassador and AWIC Spain Chapter President. International educator and speaker, coordinating global training for investigators and prosecutors on illicit crypto flows.",
    },
    {
      name: "Umberto Buonora",
      position: "Head of Investigations",
      image: "/images/team/umberto-buonora.png",
      linkedin: "https://www.linkedin.com/in/umberto-buonora-158569197/",
      bio: "Former Italian Law Enforcement (Guardia di Finanza) with 10+ years in cybercrime. Creator of virtual asset seizure methodologies used by police forces.",
    },
    {
      name: "Alessandro Rella",
      position: "Blockchain Investigations Manager",
      image: "/images/team/alessandro-rella.png",
      linkedin: "https://www.linkedin.com/in/alessandrorella/",
      bio: "Former Police Detective and Head of Digital Forensics at Guardia di Finanza. Expert in Darkweb investigations and creator of the CWFE certification.",
    },
    {
      name: "Dominik Konopacki",
      position: "Blockchain Investigations Manager",
      image: "/images/team/dominik-konopacki.png",
      linkedin: "https://www.linkedin.com/in/dominik-konopacki-443737191/",
      bio: "Specialist in privacy-oriented protocols and demixing. Provides high-stakes Source of Funds analysis for Swiss banks.",
    },
    {
      name: "Dawid Koperski",
      position: "Blockchain Investigations Manager",
      image: "/images/team/dawid-koperski.png",
      linkedin: "https://www.linkedin.com/in/dawidkoperski/",
      bio: "Former Global Investigations Lead at MoonPay. Certified expert across multiple industry-leading forensic platforms; Specialist in AML and sanction evasion detection.",
    },
    {
      name: "Aleksandra Grevceva",
      position: "Junior Blockchain Investigator",
      image: "/images/team/aleksandra-grevceva.png",
      linkedin: "https://www.linkedin.com/in/aleksandra-grevceva/",
      bio: "Former diplomat with 8 years at Latvia's Ministry of Foreign Affairs, including a posting at the Embassy of Latvia in Beijing, specializing in Asia-focused foreign policy analysis and diplomatic engagement. Background in investigative journalism and OSINT, now applied to blockchain intelligence and on-chain investigations. Fluent in Russian, English, Latvian, and Chinese, with working Spanish.",
    },
  ],
  videos: [
    {
      title: "YouTube video player",
      src: "https://www.youtube.com/embed/cwsvqd1nD4s?si=AiYceih5Btj4eSaI",
    },
    {
      title: "YouTube video player",
      src: "https://www.youtube.com/embed/4KZuiWkdHIc?si=VWanYmRxzvew70mK",
    },
  ],
};

export const faq = {
  title: "FAQ",
  items: [
    {
      question: "1. Is it really possible to get my crypto back?",
      answer:
        "Yes. Blockchain transactions are permanent, publicly visible records, which means the funds aren't invisible. We trace the movement of stolen assets until they reach a chokepoint, like a regulated exchange where the scammer tries to convert them. At that point, we work with authorities and platforms to freeze and recover the funds.",
    },
    {
      question: "2. How long does the recovery process take?",
      answer:
        "Every case is different. If funds have moved quickly to a compliant exchange, action can sometimes happen within days. Complex cases involving legal proceedings or international coordination can take weeks or months. We provide a realistic timeline after our initial assessment.",
    },
    {
      question: "3. How much will this cost me?",
      answer:
        "Our process starts with a case review. If we determine your funds are recoverable, we provide a formal offer based on the complexity of the investigation. No hidden fees, and we only proceed when there is a clear strategy.",
    },
    {
      question: "4. Do I need to file a police report first?",
      answer:
        "You don't need a report to start our analysis, but we strongly recommend filing one. Our forensic reports are designed to be court-admissible, giving police and prosecutors exactly what they need to act. We can guide you on what information to include.",
    },
    {
      question: '5. Can you still help if the scammers used a "mixer" or "bridge"?',
      answer:
        "Yes. Many people believe that mixers or cross-chain bridges make crypto untraceable. While they add complexity, our investigators use advanced techniques and proprietary tools to follow the trail through these obfuscation layers to the final destination.",
    },
    {
      question: "6. Why do I need to tell you what happened before we speak?",
      answer:
        "Speed matters in recovery. By sharing your transaction details upfront, our investigators can immediately check the blockchain and assess where your funds are. This means our first conversation can focus on a real recovery strategy instead of intake.",
    },
    {
      question: "7. How do I know Recoveris is legitimate and not another scam?",
      answer:
        "We understand the concern. After being scammed once, trust is hard. Here's how to verify us: our team members have public LinkedIn profiles with years of professional history, we are referenced in industry media, we collaborate with organizations like the OSCE and Circle, and we are a registered Swiss company with a physical headquarters in Zug.",
    },
  ],
};

export const cta = {
  title: "Don't let your stolen crypto become a permanent loss",
  text: "Every hour matters. The longer you wait, the harder recovery becomes. Scammers move fast to hide stolen funds. But as long as assets are moving, there is a trail our investigators can follow. Tell us what happened, and we'll give you an assessment of your options.",
};

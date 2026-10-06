import Image from "next/image";
import Link from "next/link";
import { LinkedInIcon, XIcon, YouTubeIcon } from "@/components/icons";
import { site } from "@/content/site";

export function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-wrapper">
          <div className="footer-details">
            <p>
              {site.legalName}
              <br />
              {site.address.street}
              <br />
              {site.address.city}
              <br />
              {site.address.country}
            </p>
          </div>

          <div className="footer-center">
            <Link className="header-logo" href="/" aria-label={site.name}>
              <Image
                src="/images/logo.svg"
                alt={site.name}
                width={204}
                height={40}
              />
            </Link>
            <div className="footer-img">
              <Image
                src="/images/soc2.png"
                alt="SOC2"
                width={80}
                height={80}
              />
            </div>
          </div>

          <div className="footer-links">
            <ul>
              {site.footerLinks.map((link) => (
                <li key={link.href}>
                  <Link href={link.href}>{link.label}</Link>
                </li>
              ))}
            </ul>

            <p>{site.copyright}</p>

            <div className="footer-socials">
              <a href={site.social.linkedin} aria-label="LinkedIn">
                <LinkedInIcon size={40} />
              </a>
              <a href={site.social.x} aria-label="X">
                <XIcon />
              </a>
              <a href={site.social.youtube} aria-label="YouTube">
                <YouTubeIcon />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

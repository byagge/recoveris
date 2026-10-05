import Image from "next/image";
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
            <a className="header-logo" href={site.url} aria-label={site.name}>
              <Image
                src="/images/logo.svg"
                alt={site.name}
                width={204}
                height={40}
              />
            </a>
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
                  <a href={link.href}>{link.label}</a>
                </li>
              ))}
            </ul>

            <p>{site.copyright}</p>

            <div className="footer-socials">
              <a
                href={site.social.linkedin}
                target="_blank"
                rel="noreferrer"
                aria-label="LinkedIn"
              >
                <LinkedInIcon size={40} />
              </a>
              <a
                href={site.social.x}
                target="_blank"
                rel="noreferrer"
                aria-label="X"
              >
                <XIcon />
              </a>
              <a
                href={site.social.youtube}
                target="_blank"
                rel="noreferrer"
                aria-label="YouTube"
              >
                <YouTubeIcon />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

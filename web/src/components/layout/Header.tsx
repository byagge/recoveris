"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { navigation } from "@/content/navigation";
import { site } from "@/content/site";

function AppLink({
  href,
  className,
  children,
  onClick,
}: {
  href: string;
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
}) {
  const external = href.startsWith("http") || href.startsWith("mailto:");
  if (external) {
    return (
      <a href={href} className={className} onClick={onClick}>
        {children}
      </a>
    );
  }
  return (
    <Link href={href} className={className} onClick={onClick}>
      {children}
    </Link>
  );
}

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const closeMenu = useCallback(() => {
    setMenuOpen(false);
    setOpenDropdown(null);
  }, []);

  return (
    <header
      className={`header${scrolled ? " scrolled" : ""}${menuOpen ? " active" : ""}`}
      id="app-header"
    >
      <div className="container">
        <div className="header-wrapper">
          <AppLink className="header-logo" href="/" onClick={closeMenu}>
            <Image
              src="/images/logo.svg"
              alt={site.name}
              width={204}
              height={40}
              priority
            />
          </AppLink>

          <button
            type="button"
            className={`header-trigger${menuOpen ? " active" : ""}`}
            aria-label="Меню"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((v) => !v)}
          >
            <span />
            <span />
            <span />
          </button>

          <nav id="main-nav">
            <ul>
              {navigation.map((item) =>
                item.children ? (
                  <li className="dropdown-menu" key={item.label}>
                    <span
                      className="header-link dropdown-toggle-btn"
                      role="button"
                      tabIndex={0}
                      onClick={() =>
                        setOpenDropdown((cur) =>
                          cur === item.label ? null : item.label,
                        )
                      }
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          e.preventDefault();
                          setOpenDropdown((cur) =>
                            cur === item.label ? null : item.label,
                          );
                        }
                      }}
                    >
                      {item.label}
                    </span>
                    <ul
                      className={`submenu${openDropdown === item.label ? " show" : ""}`}
                      role="menu"
                    >
                      {item.children.map((child) => (
                        <li key={child.href}>
                          <AppLink
                            href={child.href}
                            className="header-link"
                            onClick={closeMenu}
                          >
                            {child.label}
                          </AppLink>
                        </li>
                      ))}
                    </ul>
                  </li>
                ) : (
                  <li key={item.label}>
                    <AppLink
                      href={item.href ?? "/"}
                      className="header-link"
                      onClick={closeMenu}
                    >
                      {item.label}
                    </AppLink>
                  </li>
                ),
              )}
              <li>
                <AppLink
                  href={site.headerCta.href}
                  className="btn btn--outline"
                  onClick={closeMenu}
                >
                  {site.headerCta.label}
                </AppLink>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}

import { ArrowIcon } from "@/components/icons";

type ButtonProps = {
  href: string;
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "outline";
  className?: string;
  showArrow?: boolean;
};

export function Button({
  href,
  children,
  variant = "primary",
  className = "",
  showArrow = true,
}: ButtonProps) {
  return (
    <a href={href} className={`btn btn--${variant} ${className}`.trim()}>
      {children}
      {showArrow ? <ArrowIcon /> : null}
    </a>
  );
}

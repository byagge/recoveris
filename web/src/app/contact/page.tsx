import type { Metadata } from "next";
import { ContactForm } from "@/components/sections/ContactForm";

export const metadata: Metadata = {
  title: "Контакты",
  description: "Свяжитесь с Recoveris для оценки дела и консультации.",
};

export default function ContactPage() {
  return <ContactForm />;
}

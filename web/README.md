# Recoveris — Solution for Individuals

Modern rewrite of the Recoveris landing page (Next.js + React + TypeScript).

Visual design matches the original site. All copy lives in editable content files.

## Stack

- **Next.js 16** (App Router)
- **React 19** + **TypeScript**
- **Swiper** (team slider)
- Original design tokens / CSS (Poppins, green/yellow palette)

## Edit content

| File | What to change |
|------|----------------|
| `src/content/individuals.ts` | Hero, steps, scam types, why, team, FAQ, CTA |
| `src/content/navigation.ts` | Header menu + submenus |
| `src/content/site.ts` | Company info, CTA links, social, footer |

## Run locally

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Scripts

- `npm run dev` — development server
- `npm run build` — production build
- `npm run start` — serve production build

## Project structure

```
web/
  public/images/     # logo, backgrounds, team photos
  src/
    app/             # Next.js routes + global CSS
    components/      # UI + page sections
    content/         # ← edit text here
```

The original scraped WordPress HTML is kept in `../_legacy` for reference.

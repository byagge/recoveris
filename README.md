# Recoveris — Solution for Individuals

Next.js + React + TypeScript rewrite of the Recoveris landing page.

## Local development

```bash
cd web
npm install
npm run dev
```

Open http://localhost:3000

## Edit content

| File | Purpose |
|------|---------|
| `web/src/content/individuals.ts` | Page copy (hero, steps, FAQ, team…) |
| `web/src/content/navigation.ts` | Header menu |
| `web/src/content/site.ts` | Brand, CTAs, footer, social |

## Production (recoveris.arix.vu)

- App path: `/var/www/recoveris.arix.vu`
- PM2 process: `recoveris` on `127.0.0.1:3011`
- Nginx site: `recoveris.arix.vu` only

```bash
cd /var/www/recoveris.arix.vu/web
npm ci
npm run build
pm2 start ecosystem.config.cjs
pm2 save
```

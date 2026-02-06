# Skill: Business Website Builder
## Deploy and manage business websites

---

## Overview

Rapidly build, deploy, and manage professional business websites with brand guidelines, lead capture, and dashboards.

---

## Capabilities

### 1. Sparkling Solutions (Airbnb Cleaning)
**Type:** Service Business Website
**Status:** ✅ Complete, ready for deployment

**Features:**
- Professional brand identity (colors, typography, voice)
- Homepage with property management lead capture
- Host dashboard:
  - Calendar integration
  - Restocking checklists
  - Affiliate product recommendations
- Responsive design
- SEO optimized

**Files:**
- `workspace/brands/sparkling-solutions/index.html`
- `workspace/brands/sparkling-solutions/dashboard.html`
- `workspace/brands/sparkling-solutions/brand-guidelines.md`

**Deployment:**
```bash
# Deploy to Vercel
cd ~/workspace/brands/sparkling-solutions
vercel --prod

# Or Netlify
cd ~/workspace/brands/sparkling-solutions
netlify deploy --prod
```

---

### 2. BE Repaired (Handyman Services)
**Type:** Service Business Website
**Status:** ✅ Complete, ready for deployment

**Features:**
- Brand guidelines (professional, trustworthy)
- Service pricing pages
- CTA funnels for lead capture
- Contact forms
- Service area showcase
- Testimonials section

**Files:**
- `workspace/brands/be-repaired/index.html`
- `workspace/brands/be-repaired/brand-guidelines.md`

**Services:**
- General repairs
- Plumbing
- Electrical
- Carpentry
- Painting

---

### 3. Personal Tech (Portfolio)
**Type:** Personal Portfolio
**Status:** ✅ Deployed

**Features:**
- Professional portfolio layout
- Project showcase
- Tech stack display
- Cross-links to all business sites
- Contact integration

**Files:**
- `workspace/brands/personal-tech/index.html`

---

## Quick Commands

```bash
# Deploy any business site
deploy-site() {
    site=$1
    cd ~/workspace/brands/$site
    vercel --prod
}

# Deploy all sites
deploy-all-sites() {
    for site in sparkling-solutions be-repaired personal-tech; do
        echo "Deploying $site..."
        deploy-site $site
    done
}
```

---

## Integration with Life OS

**Dashboard:** All sites tracked in Life OS Dashboard (Websites tab)
**Agents:** Hype Man manages social media, Mechanic handles deployments
**Automation:** n8n workflows for lead capture notifications

---

## Tech Stack

- HTML5/CSS3/JavaScript
- Vanilla (no frameworks)
- Responsive design
- Dark/light mode support
- SEO meta tags
- Analytics ready (Google Analytics, Plausible)

---

## Future Enhancements

- [ ] Booking system integration (Calendly, Acuity)
- [ ] Payment processing (Stripe)
- [ ] CMS integration (Strapi, Sanity)
- [ ] Multi-language support
- [ ] PWA capabilities

---

## Usage

```bash
# Edit a site
nano ~/workspace/brands/sparkling-solutions/index.html

# Preview locally
cd ~/workspace/brands/sparkling-solutions
python3 -m http.server 8080

# Deploy
vercel --prod
```

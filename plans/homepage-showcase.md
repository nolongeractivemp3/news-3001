# News3001 — Static Showcase Homepage Plan

## Overview
A standalone static HTML page that showcases the News3001 project — what it does, how it works, and its tech stack. This is a portfolio/landing page, separate from the actual app UI.

## Location
- `homepage/index.html` — single self-contained HTML file
- `homepage/screenshot.png` — screenshot of the app in action (to be added manually)

## Tech Stack for the Page
- Plain HTML + Tailwind CSS (via CDN)
- No build tools, no PHP, no backend — purely static
- Dark theme to match the app's aesthetic

## Page Sections

### 1. Hero Section
- Large title: **News3001**
- Tagline: "Alle Köpenick News zusammengefasst in einem Feed"
- Subtle animated gradient or mesh background
- CTA button linking to the live app (`https://news.jaypo.ch`)

### 2. What It Does
- Brief description of the project: local news aggregator for Berlin-Köpenick
- Key highlights in icon cards:
  - 📰 Aggregates news from multiple sources
  - 🤖 AI-powered summaries via OpenRouter
  - 🏷️ Automatic badge/category tagging
  - 📡 RSS feed support
  - 🔧 Source filtering via settings

### 3. How It Works (Architecture)
- Visual diagram or styled list showing the pipeline:
  1. Scraper collects news from various sources
  2. AI enrichment adds badges and generates daily reports
  3. PocketBase stores everything
  4. FastAPI serves the data
  5. PHP + HTMX frontend renders it

### 4. Tech Stack Grid
- Styled grid/pills showing technologies:
  - Python, FastAPI, PocketBase, PHP, HTMX, DaisyUI, Tailwind CSS, Docker, OpenRouter AI, Nginx

### 5. Screenshot / Preview
- Placeholder area for an app screenshot or mockup
- Could use the existing app icons as fallback

### 6. Footer
- Link to GitHub repo (if public)
- "Built by Jay" or similar attribution
- Link back to the live app

## Visual Style
- Dark background (#1a1b2e or similar deep navy/purple)
- Accent color matching the app's primary (DaisyUI primary blue)
- Clean typography — Inter or system font stack
- Smooth scroll, subtle fade-in animations via CSS
- Responsive: mobile-first, looks good on all screen sizes

## Page Layout Wireframe

```
┌─────────────────────────────────────────┐
│              HERO SECTION               │
│                                         │
│            News3001                     │
│   Alle Köpenick News in einem Feed     │
│         [ Zur App → ]                  │
│                                         │
├─────────────────────────────────────────┤
│           WHAT IT DOES                  │
│                                         │
│  📰 Aggregation  🤖 AI Summaries      │
│  🏷️ Auto Tags    📡 RSS Support       │
│                                         │
├─────────────────────────────────────────┤
│          HOW IT WORKS                   │
│                                         │
│  Scrape → Enrich → Store → Serve → UI │
│                                         │
├─────────────────────────────────────────┤
│           TECH STACK                    │
│                                         │
│  [Python] [FastAPI] [PocketBase] ...   │
│                                         │
├─────────────────────────────────────────┤
│           SCREENSHOT                    │
│                                         │
│        [ app preview image ]           │
│                                         │
├─────────────────────────────────────────┤
│             FOOTER                      │
│     Built by Jay · GitHub · Live App   │
└─────────────────────────────────────────┘
```

## Implementation Steps

1. Create `homepage/index.html` with full HTML structure
2. Add Tailwind CSS via CDN for styling
3. Build all sections with responsive layout
4. Add CSS animations for fade-in on scroll and hero gradient
5. Test responsiveness on mobile and desktop viewports
6. Optionally add a screenshot of the running app

<!DOCTYPE html>
<html lang="de" data-theme="dark">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News3001 — Köpenick News Aggregator</title>
    <link rel="canonical" href="https://news.jaypo.ch/">
    <meta name="description"
        content="Alle Köpenick News zusammengefasst in einem Feed. KI-gestützte Nachrichtenzusammenfassung für Berlin-Köpenick. Köpenick News, Köpenick feed Köpenick News feed">
    <link rel="icon" type="image/png" sizes="32x32" href="/app/icons/icon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/app/icons/icon-72x72.png">

    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css">
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="/homepage/style.css">
</head>

<body class="min-h-screen flex flex-col">

    <!-- Nav -->
    <nav class="border-b border-subtle bg-black/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="#" class="flex items-center gap-2">
                <span class="text-xl">📰</span>
                <span class="text-lg tracking-tight">News3001</span>
            </a>
            <div class="flex items-center gap-6 font-mono text-sm">
                <a href="#features"
                    class="nav-link text-white/70 hover:text-white transition-colors hidden sm:inline">Funktionen</a>
                <a href="#architecture"
                    class="nav-link text-white/70 hover:text-white transition-colors hidden sm:inline">System</a>
                <a href="#tech"
                    class="nav-link text-white/70 hover:text-white transition-colors hidden sm:inline">Tech</a>
                <a href="/app/" target="_blank"
                    class="px-3 py-1.5 border border-[--red] text-[--red] hover:bg-[--red] hover:text-white transition-colors">
                    → App
                </a>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <header class="border-b border-subtle">
        <div class="max-w-5xl mx-auto px-6 py-24 sm:py-32">
            <p class="font-mono text-xs tracking-widest uppercase text-[--gold] mb-8 fade-in">
                Berlin-Köpenick News
            </p>
            <h1 class="display-text mb-8 fade-in">
                Alle Köpenick News<br><em>in einem Feed</em>
            </h1>
            <p class="text-xl text-white/60 max-w-2xl mb-12 fade-in">
                Local Nachichten. Ein Python-basierter Scraper sammelt Nachrichten aus verschiedenen Quellen,
                OpenRouter AI generiert tägliche Zusammenfassungen und Themen. Das Ergebnis: ein sauberer,
                fokussierter News-Feed für deinen Bezirk.
            </p>
            <div class="flex flex-wrap gap-6 fade-in">
                <a href="/app/" target="_blank"
                    class="px-8 py-4 bg-[--red] text-white font-medium hover:bg-[--red-hover] transition-colors">
                    Zur App →
                </a>
                <a href="#architecture"
                    class="px-8 py-4 border border-white/20 text-white/70 hover:text-white hover:border-white/40 transition-colors">
                    Wie es funktioniert
                </a>
            </div>
        </div>
    </header>

    <!-- Stats -->
    <div class="border-b border-subtle">
        <div class="max-w-5xl mx-auto px-6 py-12 grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
                <p class="font-mono text-xs text-[--gold] uppercase tracking-widest mb-2">Sources</p>
                <p class="text-3xl">10+</p>
                <p class="text-white/40 text-sm">Newsquellen</p>
            </div>
            <div>
                <p class="font-mono text-xs text-[--gold] uppercase tracking-widest mb-2">Daily</p>
                <p class="text-3xl">~8</p>
                <p class="text-white/40 text-sm">Artikel/Tag</p>
            </div>
            <div>
                <p class="font-mono text-xs text-[--gold] uppercase tracking-widest mb-2">KI</p>
                <p class="text-3xl">Yes</p>
                <p class="text-white/40 text-sm">Auto-Themen</p>
            </div>
            <div>
                <p class="font-mono text-xs text-[--gold] uppercase tracking-widest mb-2">live</p>
                <p class="text-3xl">✓</p>
                <p class="text-white/40 text-sm">von Google alerts</p>
            </div>
        </div>
    </div>

    <!-- Features -->
    <section id="features" class="border-b border-subtle">
        <div class="max-w-5xl mx-auto px-6 py-24">
            <div class="flex items-start gap-12 mb-16">
                <div class="flex-shrink-0">
                    <span class="font-mono text-xs tracking-widest uppercase text-[--gold]">01</span>
                    <div class="accent-line mt-4"></div>
                </div>
                <div>
                    <h2 class="text-3xl sm:text-4xl mb-6">Features</h2>
                    <p class="text-white/50 max-w-xl">Was News3001 von anderen News-Aggregatoren unterscheidet.</p>
                </div>
            </div>

            <div class="grid md:grid-cols-2 gap-px bg-white/10">
                <div class="card bg-[--ink]">
                    <p class="text-2xl mb-4">📰</p>
                    <h3 class="text-xl mb-3">Automatische Aggregation</h3>
                    <p class="text-white/50">Scraper sammeln täglich News aus verschiedenen Quellen. Kein manuelles
                        Kuratieren erforderlich.</p>
                </div>
                <div class="card bg-[--ink]">
                    <p class="text-2xl mb-4">🤖</p>
                    <h3 class="text-xl mb-3">KI-Zusammenfassung</h3>
                    <p class="text-white/50">OpenRouter generiert tägliche Zusammenfassungen des
                        Nachrichtengeschehens.</p>
                </div>
                <div class="card bg-[--ink]">
                    <p class="text-2xl mb-4">🏷️</p>
                    <h3 class="text-xl mb-3">Auto-Badges</h3>
                    <p class="text-white/50">Jeder Artikel bekommt automatisch Tags: Offiziel, Unfall, Politik, Unfall etc. Auf
                        einen Blick erkennbar.</p>
                </div>
                <div class="card bg-[--ink]">
                    <p class="text-2xl mb-4">📡</p>
                    <h3 class="text-xl mb-3">Google Alerts</h3>
                    <p class="text-white/50">Es werden nachichten automatisch aus einem google feed gesammelt um live updates zu erhalten.</p>
                </div>
                <div class="card bg-[--ink]">
                    <p class="text-2xl mb-4">🔧</p>
                    <h3 class="text-xl mb-3">Quellen-Filter</h3>
                    <p class="text-white/50">Filtere unerwünschte Quellen heraus. Dein Feed, deine Regeln.</p>
                </div>
                <div class="card bg-[--ink]">
                    <p class="text-2xl mb-4">📱</p>
                    <h3 class="text-xl mb-3">PWA</h3>
                    <p class="text-white/50">Progressive Web App mit Offline-Support. Installierbar auf Mobile und
                        Desktop.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Architecture (inverted) -->
    <section id="architecture" class="section-inverted">
        <div class="max-w-5xl mx-auto px-6 py-24">
            <div class="flex items-start gap-12 mb-16">
                <div class="flex-shrink-0">
                    <span class="font-mono text-xs tracking-widest uppercase text-[--red]">02</span>
                    <div class="accent-line mt-4"></div>
                </div>
                <div>
                    <h2 class="text-3xl sm:text-4xl mb-6">Architecture</h2>
                    <p class="text-black/50 max-w-xl">Vom Scraper bis zur Anzeige — ein Blick unter die Haube.</p>
                </div>
            </div>

            <pre
                class="code-block mb-16"><span class="cmt"># News3001 Pipeline</span>
<span class="kw">import</span> scraper, ai, db, api, ui

news     = scraper.<span class="str">collect_daily()</span>   <span class="cmt"># 1. Scrape sources</span>
enriched = ai.<span class="str">enrich(news)</span>           <span class="cmt"># 2. Add badges &amp; summary</span>
db.<span class="str">save(enriched)</span>                     <span class="cmt"># 3. Store in PocketBase</span>
api.<span class="str">expose(db.query())</span>                <span class="cmt"># 4. Serve via FastAPI</span>
ui.<span class="str">render()</span>                           <span class="cmt"># 5. Render with PHP + HTMX</span></pre>

            <div class="grid md:grid-cols-5 gap-8">
                <div class="step">
                    <h3 class="text-lg mb-2">🕷️ Scraper</h3>
                    <p class="text-black/50 text-sm">Python-Skripte sammeln täglich Artikel von regionalen Newsquellen.
                    </p>
                </div>
                <div class="step">
                    <h3 class="text-lg mb-2">🧠 AI</h3>
                    <p class="text-black/50 text-sm">OpenRouter API generiert Badges und tägliche Zusammenfassung.</p>
                </div>
                <div class="step">
                    <h3 class="text-lg mb-2">💾 DB</h3>
                    <p class="text-black/50 text-sm">PocketBase speichert alle Artikel, Tags und Reports.</p>
                </div>
                <div class="step">
                    <h3 class="text-lg mb-2">🚀 API</h3>
                    <p class="text-black/50 text-sm">FastAPI-Server liefert JSON an das Frontend.</p>
                </div>
                <div class="step">
                    <h3 class="text-lg mb-2">🎨 UI</h3>
                    <p class="text-black/50 text-sm">PHP + HTMX rendert dynamisch ohne JS-Framework.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Tech Stack -->
    <section id="tech" class="border-b border-subtle">
        <div class="max-w-5xl mx-auto px-6 py-24">
            <div class="flex items-start gap-12 mb-16">
                <div class="flex-shrink-0">
                    <span class="font-mono text-xs tracking-widest uppercase text-[--gold]">03</span>
                    <div class="accent-line mt-4"></div>
                </div>
                <div>
                    <h2 class="text-3xl sm:text-4xl mb-6">Tech Stack</h2>
                    <p class="text-white/50 max-w-xl">Built with open source. Simple, reliable, maintainable.</p>
                </div>
            </div>

            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-px bg-white/10">
                <div class="card bg-[--ink]">
                    <span class="font-mono text-xs text-[--gold]">Backend</span>
                    <h3 class="text-lg mt-2">Python + FastAPI</h3>
                    <p class="text-white/40 text-sm mt-2">Moderne, schnelle Python-Bibliotheken. Typisiert mit Pydantic.
                    </p>
                </div>
                <div class="card bg-[--ink]">
                    <span class="font-mono text-xs text-[--gold]">Database</span>
                    <h3 class="text-lg mt-2">PocketBase</h3>
                    <p class="text-white/40 text-sm mt-2">SQLite-basiert, Admin-UI inklusive. Einfach &amp; performant.
                    </p>
                </div>
                <div class="card bg-[--ink]">
                    <span class="font-mono text-xs text-[--gold]">AI</span>
                    <h3 class="text-lg mt-2">OpenRouter</h3>
                    <p class="text-white/40 text-sm mt-2">Unified API für GPT, Claude, und andere LLMs.</p>
                </div>
                <div class="card bg-[--ink]">
                    <span class="font-mono text-xs text-[--gold]">Frontend</span>
                    <h3 class="text-lg mt-2">PHP + HTMX</h3>
                    <p class="text-white/40 text-sm mt-2">Server-side rendering mit dynamischen Updates. Kein React
                        nötig.</p>
                </div>
                <div class="card bg-[--ink]">
                    <span class="font-mono text-xs text-[--gold]">Styling</span>
                    <h3 class="text-lg mt-2">Tailwind + DaisyUI</h3>
                    <p class="text-white/40 text-sm mt-2">Utility-first CSS mit komponentenorientierter Ergänzung.</p>
                </div>
                <div class="card bg-[--ink]">
                    <span class="font-mono text-xs text-[--gold]">Infrastructure</span>
                    <h3 class="text-lg mt-2">Docker</h3>
                    <p class="text-white/40 text-sm mt-2">Containerisiert mit Docker Compose. Deploy überall.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="border-b border-subtle">
        <div class="max-w-5xl mx-auto px-6 py-24 text-center">
            <h2 class="text-3xl sm:text-4xl mb-6">Probier es aus</h2>
            <p class="text-white/50 max-w-lg mx-auto mb-10">
                Alle Köpenick News an einem Ort. RSS, KI-Zusammenfassungen, Filter — alles dabei.
            </p>
            <a href="/app/" target="_blank"
                class="inline-block px-10 py-5 bg-[--red] text-white text-lg hover:bg-[--red-hover] transition-colors">
                → Zur App
            </a>
        </div>
    </section>

    <?php include __DIR__ . "/../app/components/footer.php"; ?>

</body>

</html>

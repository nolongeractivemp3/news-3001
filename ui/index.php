<!DOCTYPE html>
<html lang="de" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News3001 — Köpenick News Aggregator</title>
    <link rel="canonical" href="https://news.jaypo.ch/">
    <meta name="description" content="Alle Köpenick News zusammengefasst in einem Feed. KI-gestützte Nachrichtenzusammenfassung für Berlin-Köpenick.">
    <link rel="icon" type="image/png" sizes="32x32" href="/app/icons/icon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/app/icons/icon-72x72.png">

    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css">
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        body { 
            background-color: #1d232a; 
            color: white; 
            font-family: system-ui, -apple-system, sans-serif; 
        }
        html { scroll-behavior: smooth; }
        
        .card-custom {
            background-color: #3B4754;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .fade-up { 
            opacity: 0; 
            transform: translateY(20px); 
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
        }
        .fade-up.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .delay-100 { transition-delay: 100ms; }
        .delay-200 { transition-delay: 200ms; }
        
        .text-gold { color: #d4a853; }
        .bg-red-custom { background-color: #e63946; }
        .bg-red-custom:hover { background-color: #c92a37; }
        .text-red-custom { color: #e63946; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Navbar -->
    <div class="navbar shadow-sm sticky top-0 z-50" style="background-color: rgba(29, 35, 42, 0.9); backdrop-filter: blur(8px);">
        <div class="navbar-start">
            <div class="dropdown">
                <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
                </div>
                <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow rounded-box w-52" style="background-color: #3B4754;">
                    <li><a href="#features">Features</a></li>
                    <li><a href="#architecture">System</a></li>
                    <li><a href="#tech">Tech Stack</a></li>
                </ul>
            </div>
            <a href="#" class="btn btn-ghost normal-case text-xl gap-2">
                <span class="text-2xl">📰</span>
                News3001
            </a>
        </div>
        <div class="navbar-center hidden lg:flex">
            <ul class="menu menu-horizontal px-1">
                <li><a href="#features" class="hover:text-white/80">Features</a></li>
                <li><a href="#architecture" class="hover:text-white/80">System</a></li>
                <li><a href="#tech" class="hover:text-white/80">Tech Stack</a></li>
            </ul>
        </div>
        <div class="navbar-end">
            <a href="/app/" class="btn btn-primary btn-sm sm:btn-md">Zur App →</a>
        </div>
    </div>

    <!-- Hero -->
    <div class="hero min-h-[70vh]">
        <div class="hero-content text-center max-w-4xl px-4 py-20">
            <div class="fade-up">
                <div class="inline-block px-4 py-1 rounded-full border border-[var(--color-primary)] text-primary text-sm font-semibold mb-8 tracking-widest uppercase">
                    Berlin-Köpenick News
                </div>
                <h1 class="text-5xl md:text-7xl font-bold mb-8 tracking-tight leading-tight">Alle Köpenick News <br/><span class="text-primary italic font-serif">in einem Feed</span></h1>
                <p class="py-6 text-xl opacity-80 mb-8 max-w-2xl mx-auto">
                    Lokale Nachrichten. Ein Python-basierter Scraper sammelt Nachrichten aus verschiedenen Quellen, OpenRouter KI generiert tägliche Zusammenfassungen und Themen. Das Ergebnis: ein sauberer, fokussierter News-Feed für deinen Bezirk.
                </p>
                <div class="flex flex-wrap gap-4 justify-center">
                    <a href="/app/" class="btn btn-primary btn-lg border-none">App öffnen</a>
                    <a href="#architecture" class="btn btn-outline btn-lg">Wie es funktioniert</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Stats -->
    <div class="border-y border-white/10" style="background-color: rgba(59, 71, 84, 0.3);">
        <div class="max-w-5xl mx-auto px-4 py-8">
            <div class="stats stats-vertical lg:stats-horizontal shadow-none w-full bg-transparent fade-up delay-100">
                <div class="stat place-items-center">
                    <div class="stat-title text-gold uppercase tracking-widest text-xs">Quellen</div>
                    <div class="stat-value text-4xl mt-2">10+</div>
                    <div class="stat-desc mt-1 opacity-60">Lokale Newsquellen</div>
                </div>
                <div class="stat place-items-center">
                    <div class="stat-title text-gold uppercase tracking-widest text-xs">Frequenz</div>
                    <div class="stat-value text-4xl mt-2">~8</div>
                    <div class="stat-desc mt-1 opacity-60">Artikel pro Tag</div>
                </div>
                <div class="stat place-items-center">
                    <div class="stat-title text-gold uppercase tracking-widest text-xs">KI-Analysen</div>
                    <div class="stat-value text-4xl mt-2">Auto</div>
                    <div class="stat-desc mt-1 opacity-60">Zusammenfassung & Badges</div>
                </div>
                <div class="stat place-items-center">
                    <div class="stat-title text-gold uppercase tracking-widest text-xs">Updates</div>
                    <div class="stat-value text-4xl mt-2 text-info">Live</div>
                    <div class="stat-desc mt-1 opacity-60">via Google Alerts</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Features -->
    <section id="features" class="py-24">
        <div class="max-w-5xl mx-auto px-6">
            <div class="flex items-center gap-4 mb-12 fade-up">
                <div class="w-12 h-1 bg-primary rounded"></div>
                <h2 class="text-4xl font-bold">Features</h2>
            </div>
            <p class="opacity-70 max-w-2xl mb-12 fade-up">Was News3001 von anderen News-Aggregatoren unterscheidet und zu deiner besten lokalen Nachrichtenquelle macht.</p>
            
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 fade-up delay-100">
                <!-- Card 1 -->
                <div class="card card-custom shadow-xl hover:-translate-y-1 transition-transform">
                    <div class="card-body">
                        <div class="text-4xl mb-4">📰</div>
                        <h2 class="card-title text-xl mb-2">Automatische Aggregation</h2>
                        <p class="opacity-70 text-sm">Scraper sammeln täglich News aus verschiedenen Quellen. Kein manuelles Kuratieren erforderlich.</p>
                    </div>
                </div>
                <!-- Card 2 -->
                <div class="card card-custom shadow-xl hover:-translate-y-1 transition-transform">
                    <div class="card-body">
                        <div class="text-4xl mb-4">🤖</div>
                        <h2 class="card-title text-xl mb-2">KI-Zusammenfassung</h2>
                        <p class="opacity-70 text-sm">OpenRouter generiert tägliche Zusammenfassungen des Nachrichtengeschehens.</p>
                    </div>
                </div>
                <!-- Card 3 -->
                <div class="card card-custom shadow-xl hover:-translate-y-1 transition-transform">
                    <div class="card-body">
                        <div class="text-4xl mb-4">🏷️</div>
                        <h2 class="card-title text-xl mb-2">Auto-Badges</h2>
                        <p class="opacity-70 text-sm">Jeder Artikel bekommt automatisch Tags: Offizielles, Unfall, Politik, Kultur etc. Auf einen Blick erkennbar.</p>
                    </div>
                </div>
                <!-- Card 4 -->
                <div class="card card-custom shadow-xl hover:-translate-y-1 transition-transform">
                    <div class="card-body">
                        <div class="text-4xl mb-4">📡</div>
                        <h2 class="card-title text-xl mb-2">Google Alerts</h2>
                        <p class="opacity-70 text-sm">Nachrichten werden automatisch aus einem Google-Feed gesammelt, um Live-Updates zu erhalten.</p>
                    </div>
                </div>
                <!-- Card 5 -->
                <div class="card card-custom shadow-xl hover:-translate-y-1 transition-transform">
                    <div class="card-body">
                        <div class="text-4xl mb-4">🔧</div>
                        <h2 class="card-title text-xl mb-2">Quellen-Filter</h2>
                        <p class="opacity-70 text-sm">Filtere unerwünschte Quellen heraus. Dein Feed, deine Regeln.</p>
                    </div>
                </div>
                <!-- Card 6 -->
                <div class="card card-custom shadow-xl hover:-translate-y-1 transition-transform">
                    <div class="card-body">
                        <div class="text-4xl mb-4">📱</div>
                        <h2 class="card-title text-xl mb-2">PWA Ready</h2>
                        <p class="opacity-70 text-sm">Progressive Web App mit Offline-Support. Installierbar auf Mobile und Desktop für schnellen Zugriff.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Architecture -->
    <section id="architecture" class="py-24 border-y border-white/10" style="background-color: rgba(59, 71, 84, 0.3);">
        <div class="max-w-5xl mx-auto px-6">
            <div class="flex items-center gap-4 mb-12 fade-up">
                <div class="w-12 h-1 bg-primary rounded"></div>
                <h2 class="text-4xl font-bold">Architektur</h2>
            </div>
            
            <div class="flex flex-col lg:flex-row gap-16 items-start">
                <div class="lg:w-1/2 fade-up">
                    <p class="opacity-70 mb-10 text-lg">Vom Scraper bis zur Anzeige — ein Blick unter die Haube. Die gesamte Pipeline läuft automatisiert und effizient jeden Tag.</p>
                    
                    <ul class="steps steps-vertical">
                        <li class="step step-primary" data-content="🕷️">
                            <div class="text-left ml-2">
                                <strong class="block text-lg">Scraper</strong>
                                <span class="text-sm opacity-70">Python-Skripte sammeln Artikel</span>
                            </div>
                        </li>
                        <li class="step step-primary" data-content="🧠">
                            <div class="text-left ml-2">
                                <strong class="block text-lg">KI Verarbeitung</strong>
                                <span class="text-sm opacity-70">OpenRouter generiert Badges & Zusammenfassung</span>
                            </div>
                        </li>
                        <li class="step step-primary" data-content="💾">
                            <div class="text-left ml-2">
                                <strong class="block text-lg">Datenbank</strong>
                                <span class="text-sm opacity-70">Speicherung in PocketBase</span>
                            </div>
                        </li>
                        <li class="step step-primary" data-content="🚀">
                            <div class="text-left ml-2">
                                <strong class="block text-lg">API Server</strong>
                                <span class="text-sm opacity-70">FastAPI liefert JSON aus</span>
                            </div>
                        </li>
                        <li class="step step-primary" data-content="🎨">
                            <div class="text-left ml-2">
                                <strong class="block text-lg">Frontend UI</strong>
                                <span class="text-sm opacity-70">PHP + HTMX rendert dynamisch</span>
                            </div>
                        </li>
                    </ul>
                </div>
                
                <div class="lg:w-1/2 w-full fade-up delay-200">
                    <div class="mockup-code shadow-2xl border border-white/10" style="background-color: #1d232a;">
                        <pre data-prefix="1" class="text-white/50"><code># News3001 Pipeline</code></pre>
                        <pre data-prefix="2"><code><span class="text-primary">import</span> scraper, ki, db, api, ui</code></pre>
                        <pre data-prefix="3"><code></code></pre>
                        <pre data-prefix="4"><code>news     = scraper.collect_daily()   <span class="text-white/40"># 1. Scrape sources</span></code></pre>
                        <pre data-prefix="5"><code>enriched = ki.enrich(news)           <span class="text-white/40"># 2. Add badges & summary</span></code></pre>
                        <pre data-prefix="6"><code>db.save(enriched)                    <span class="text-white/40"># 3. Store in PocketBase</span></code></pre>
                        <pre data-prefix="7"><code>api.expose(db.query())               <span class="text-white/40"># 4. Serve via FastAPI</span></code></pre>
                        <pre data-prefix="8"><code>ui.render()                          <span class="text-white/40"># 5. Render with PHP + HTMX</span></code></pre>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Tech Stack -->
    <section id="tech" class="py-24">
        <div class="max-w-5xl mx-auto px-6 text-center fade-up">
            <h2 class="text-4xl font-bold mb-6">Tech Stack</h2>
            <p class="opacity-70 max-w-2xl mx-auto mb-16">Built with open source. Simple, reliable, maintainable.</p>
            
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div class="card card-custom shadow hover:-translate-y-1 transition-transform">
                    <div class="card-body items-center text-center p-6">
                        <div class="text-3xl mb-2">🐍</div>
                        <h3 class="font-bold">Python</h3>
                        <p class="text-xs opacity-60">FastAPI Backend</p>
                    </div>
                </div>
                <div class="card card-custom shadow hover:-translate-y-1 transition-transform">
                    <div class="card-body items-center text-center p-6">
                        <div class="text-3xl mb-2">🗄️</div>
                        <h3 class="font-bold">PocketBase</h3>
                        <p class="text-xs opacity-60">Database</p>
                    </div>
                </div>
                <div class="card card-custom shadow hover:-translate-y-1 transition-transform">
                    <div class="card-body items-center text-center p-6">
                        <div class="text-3xl mb-2">🧠</div>
                        <h3 class="font-bold">OpenRouter</h3>
                        <p class="text-xs opacity-60">LLM API</p>
                    </div>
                </div>
                <div class="card card-custom shadow hover:-translate-y-1 transition-transform">
                    <div class="card-body items-center text-center p-6">
                        <div class="text-3xl mb-2">🐘</div>
                        <h3 class="font-bold">PHP</h3>
                        <p class="text-xs opacity-60">Server Rendering</p>
                    </div>
                </div>
                <div class="card card-custom shadow hover:-translate-y-1 transition-transform">
                    <div class="card-body items-center text-center p-6">
                        <div class="text-3xl mb-2">⚡</div>
                        <h3 class="font-bold">HTMX</h3>
                        <p class="text-xs opacity-60">Dynamic Updates</p>
                    </div>
                </div>
                <div class="card card-custom shadow hover:-translate-y-1 transition-transform">
                    <div class="card-body items-center text-center p-6">
                        <div class="text-3xl mb-2">🎨</div>
                        <h3 class="font-bold">Tailwind</h3>
                        <p class="text-xs opacity-60">DaisyUI Styles</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="py-32 relative overflow-hidden" style="background-color: rgba(59, 71, 84, 0.5);">
        <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(circle at center, var(--color-primary) 0%, transparent 70%);"></div>
        <div class="max-w-3xl mx-auto px-6 text-center relative z-10 fade-up">
            <h2 class="text-4xl md:text-5xl font-bold mb-6">Probier es aus</h2>
            <p class="text-xl mb-10 opacity-80 font-light">
                Alle Köpenick News an einem Ort. RSS, KI-Zusammenfassungen, Filter — alles dabei.
            </p>
            <a href="/app/" class="btn btn-primary btn-lg border-none px-12 shadow-lg hover:shadow-primary/50 transition-shadow">
                Jetzt zur App →
            </a>
        </div>
    </section>

    <?php include __DIR__ . "/app/components/footer.php"; ?>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            document.querySelectorAll('.fade-up').forEach(el => {
                observer.observe(el);
            });
        });
    </script>
</body>
</html>

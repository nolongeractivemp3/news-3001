<?php
$searchQuery = $_GET["q"] ?? "";
$searchQuery = trim($searchQuery);
$pageTitle = "Archive - News3001";
?>
<!DOCTYPE html>
<html lang="de" data-theme="dark">

<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://news.jaypo.ch/app/archive.php">
    <link rel="icon" type="image/x-icon" href="./favicon.png">
    <meta name="description" content="Durchsuche alle Köpenick News aus dem Archiv.">
    <title><?php echo $pageTitle; ?> | Köpenick</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

    <link rel="manifest" href="./manifest.json">
    <meta name="theme-color" content="#333446">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="News3001">

    <link rel="apple-touch-icon" href="./icons/icon-192x192.png">
    <link rel="apple-touch-icon" sizes="152x152" href="./icons/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="144x144" href="./icons/icon-144x144.png">
    <link rel="apple-touch-icon" sizes="128x128" href="./icons/icon-128x128.png">

    <link rel="icon" type="image/png" sizes="32x32" href="./icons/icon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="./icons/icon-72x72.png">

    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js"
        integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz"
        crossorigin="anonymous"></script>
    <script src="./js/settings.js" defer></script>
</head>

<body class="min-h-screen flex flex-col">
    <style>
        body {
            background-color: #1d232a;
            color: white;
        }
        .htmx-indicator {
            display: none;
        }
        .htmx-request .htmx-indicator,
        .htmx-request.htmx-indicator {
            display: inline-block;
        }
    </style>

    <main class="w-full flex-1 p-4 flex flex-col">
        <div hx-get="components/navbar.php?archive=true" hx-trigger="load" hx-target="#navbar"></div>
        <div hx-get="components/searchbox.php<?php echo $searchQuery ? '?q=' . urlencode($searchQuery) : ''; ?>" hx-trigger="load" hx-target="#searchbox"></div>
        <div hx-get="components/searchcard.php<?php echo $searchQuery ? '?q=' . urlencode($searchQuery) : ''; ?>" hx-trigger="load" hx-target="#news"></div>
        <div hx-get="components/settings.php" hx-trigger="load" hx-target="#settings"></div>

        <div id="navbar"> </div>
        <div id="searchbox"> </div>
        <div id='news'></div>
        <div id="settings"> </div>

    </main>

    <?php include __DIR__ . "/components/footer.php"; ?>

    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js')
                    .then((registration) => {
                        console.log('SW registered:', registration.scope);
                    })
                    .catch((error) => {
                        console.log('SW registration failed:', error);
                    });
            });
        }
    </script>

</body>

</html>

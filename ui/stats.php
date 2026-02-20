<?php
$isRss = isset($_GET["rss"]);
$defaultDate = date("Y-m-d");
$selectedDate = false;

$pageTitle = $isRss ? "RSS Feed" : "News Feed 3001";
$navbarRss = $isRss ? "true" : "false";

$reportContent = "";
$rawReport = @file_get_contents("http://backend:5000/report");
$reportContent = str_replace(
    ["\r", "\n", '\r', '\n'], // Covers real enters AND literal text "\n"
    "", 
    $rawReport);  // FIX: Use $rawReport as the subject, not empty $reportContent
?>
<!DOCTYPE html>
<html lang="de" data-theme="dark">

<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://news.jaypo.ch/stats.php">
    <link rel="icon" type="image/x-icon" href="/favicon.png">
    <meta name="description" content="change later">
    <title>Stats | Köpenick</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

    <!-- PWA Meta Tags -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#333446">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="News3001">

    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/icons/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/icons/icon-144x144.png">
    <link rel="apple-touch-icon" sizes="128x128" href="/icons/icon-128x128.png">

    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="/icons/icon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/icons/icon-72x72.png">

    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js"
        integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz"
        crossorigin="anonymous"></script>
    <script src="/js/settings.js" defer></script>
</head>

<body>
    <style>
        body {
            background-color: #1d232a;
            color: white;
        }
    </style>
    <script>        function getReport() {
            // Open the modal properly
            document.getElementById("report_modal").showModal();
        }
</script>


    <main class="p-4">
        <div hx-get="components/navbar.php?rss=false&selectedDate=false" hx-trigger="load" hx-target="#navbar"></div>
        <div hx-get="components/stats/charts.php" hx-trigger="load" hx-target="#charts"></div>
        <div hx-get="components/report.php?name=report_modal&textstr=<?php echo urlencode(
                $reportContent,
            ); ?>" hx-trigger="load" hx-target="#report"></div>
        <div hx-get="components/settings.php" hx-trigger="load" hx-target="#settings"></div>

        <div id="navbar"> </div>
        <div id='charts'></div>
        <div id="report"> </div>
        <div id="settings"> </div>
        <?php if ($isRss): ?>
            <div id="rss"> </div>
        <?php endif; ?>
    </main>

    <!-- Service Worker Registration -->
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
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

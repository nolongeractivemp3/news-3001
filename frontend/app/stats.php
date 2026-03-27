<?php
$isRss = isset($_GET["rss"]);
$defaultEndDate = date("Y-m-d");
$defaultStartDate = date("Y-m-d", strtotime("-29 days"));

function normalizeStatsDate(string $date, string $fallback): string
{
    $dateObject = DateTime::createFromFormat("Y-m-d", $date);
    if ($dateObject === false || $dateObject->format("Y-m-d") !== $date) {
        return $fallback;
    }

    return $date;
}

$startDate = normalizeStatsDate($_GET["start_date"] ?? $defaultStartDate, $defaultStartDate);
$endDate = normalizeStatsDate($_GET["end_date"] ?? $defaultEndDate, $defaultEndDate);

if ($startDate > $endDate) {
    [$startDate, $endDate] = [$endDate, $startDate];
}

$pageTitle = $isRss ? "RSS Feed" : "News Feed 3001";
$navbarRss = $isRss ? "true" : "false";
$chartsQuery = "?start_date=" .
    urlencode($startDate) .
    "&end_date=" .
    urlencode($endDate);

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
    <script src="./js/settings.js" defer></script>
</head>

<body class="min-h-screen flex flex-col">
    <style>
        body {
            background-color: #1d232a;
            color: white;
        }
    </style>
    <script>
        function getReport() {
            const modal = document.getElementById("report_modal");
            if (!modal || typeof modal.showModal !== "function") {
                return;
            }
            modal.showModal();
        }
    </script>


    <main class="w-full flex-1 p-4 flex flex-col">
        <div hx-get="components/navbar.php?rss=false&date=false&statsRange=true&startDate=<?php echo urlencode(
                $startDate,
            ); ?>&endDate=<?php echo urlencode(
                $endDate,
            ); ?>&dropdown=true" hx-trigger="load" hx-target="#navbar"></div>
        <div hx-get="components/stats/charts.php<?php echo $chartsQuery; ?>" hx-trigger="load" hx-target="#charts"></div>
        <div hx-get="components/report.php?name=report_modal&date=<?php echo urlencode(
                $endDate,
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

    <?php include __DIR__ . "/components/footer.php"; ?>

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

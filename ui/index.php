<?php
$isRss = isset($_GET["rss"]);
$pageTitle = $isRss ? "RSS Feed" : "News Feed 3001";
$navbarRss = $isRss ? "true" : "false";
$cardDomain = $isRss ? "?domain=rss" : "";
?>
<!DOCTYPE html>
<html lang="de">
<head>
    <meta name="description" content="Alle Koepenick News in einem Feed">
    <title><?php echo $pageTitle; ?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" crossorigin="anonymous"></script>
    <html data-theme="dark"></html>
</head>
<body>
    <style>
        body {
            background-color: 333446;
            color: white;
        }
    </style>
    <script>
    <?php if ($isRss): ?>
    function getExplanation() {
      document.getElementById("rssexplanation").showModal();
    }
    <?php endif; ?>
    function getReport() {
        // Open the modal properly
        document.getElementById("report_modal").showModal();
    }
    </script>

    <main class="p-4">
        <div hx-get="components/navbar.php?rss=<?php echo $navbarRss; ?>" hx-trigger="load" hx-target="#navbar"></div>
        <div hx-get="components/card.php<?php echo $cardDomain; ?>" hx-trigger="load" hx-target="#news"></div>
        <div hx-get="components/report.php?name=report_modal&textstr=<?php echo urlencode(
            file_get_contents("http://backend:5000/report"),
        ); ?>" hx-trigger="load" hx-target="#report"></div>
        <?php if ($isRss): ?>
        <div hx-get="components/report.php?name=rssexplanation&textstr=<?php echo urlencode(
            "<p>RSS liefert Nachrichten schneller in Echtzeit, werden aber nicht gefiltert und sind nicht in der Zusammenfassung. (vielleicht später wenn ich mehr lust darauf habe ;) </p>",
        ); ?>" hx-trigger="load" hx-target="#rss"></div>
        <?php endif; ?>

        <div id="navbar"> </div>
        <div id='news'></div>
        <div id="report"> </div>
        <?php if ($isRss): ?>
        <div id="rss"> </div>
        <?php endif; ?>
    </main>

</body>
</html>

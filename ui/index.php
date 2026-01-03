<!DOCTYPE html>
<head>
    <title>News Feed 3001</title>
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
    function getReport() {
        // Open the modal properly
        document.getElementById("report_modal").showModal();
    }
    </script>

    <main class="p-4">
        <div hx-get="components/navbar.php?rss=false" hx-trigger="load" hx-target="#navbar"></div>
        <div hx-get="components/card.php" hx-trigger="load" hx-target="#news"></div>
        <div hx-get="components/report.php?name=report_modal&textstr=<?php echo urlencode(
            file_get_contents("http://backend:5000/report"),
        ); ?>" hx-trigger="load" hx-target="#report"></div>
        <div id="navbar"> </div>
        <div id='news'></div>
        <div id="report"> </div>
        </main>

</body>

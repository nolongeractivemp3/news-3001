<!DOCTYPE html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/dist/markdown-it.min.js"></script>
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
        const reportstr = <?php echo json_encode(
            file_get_contents("http://backend:5000/report"),
        ); ?>;
        const md = window.markdownit();

        // Just render the content directly into the prose container
        document.getElementById("ReportContent").innerHTML = md.render(reportstr);

        // Open the modal properly
        document.getElementById("report_modal").showModal();
    }
    </script>

    <main class="p-4">

        <div hx-get="components/navbar.php" hx-trigger="load" hx-target="#navbar"></div>
        <div hx-get="components/card.php" hx-trigger="load" hx-target="#news"></div>
        <div hx-get="components/report.php" hx-trigger="load" hx-target="#report"></div>
        <div id="navbar"> </div>
        <div id='news'></div>
        <div id="report"> </div>
        </main>

</body>

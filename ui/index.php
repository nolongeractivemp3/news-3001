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
    <style>
    #Report {
      display: none; /* Keep this for logic */
      opacity: 0;
      position: absolute;
      top: 5%;
      left: 5%;
      z-index: 9999;
      width: 90%;
      background-color: #3B4754;
      font-size: 28px;
      transform: translate(-50%, -50%) scale(0.9) translateY(20px);
      transition: all 0.3s ease-out;
    }

    #Report.active {
      display: block; /* Show it */
      opacity: 1;
      transform: scale(1) translateY(0);
    }
    </style>
    <main class="p-4">
        <div class="navbar bg-base-100 shadow-sm">
            <div class="navbar-start">
                <a class="btn btn-ghost normal-case text-xl">News</a>
            </div>
            <div class="navbar-end">
                <button class="btn btn-primary" onclick="getReport()">
                    Get Report
                </button>
            </div>
        </div>


        <dialog id="report_modal" class="modal">
            <div class="modal-box w-full md:w-11/12 max-w-3xl border border-primary/20 bg-neutral shadow-2xl p-4 md:p-6">
            <form method="dialog">
              <button class="btn btn-sm btn-circle btn-ghost absolute right-4 top-4 text-primary">✕</button>
            </form>
                <article id="ReportContent" class="prose prose-invert prose-sm md:prose-lg max-w-none text-left">
                </article>
            </div>
          <form method="dialog" class="modal-backdrop bg-black/60 backdrop-blur-sm">
            <button>close</button>
          </form>
        </dialog>
        <div hx-get="/card.php" hx-trigger="load" hx-target="#news"></div>
        <div id='news'></div>
        </main>

</body>

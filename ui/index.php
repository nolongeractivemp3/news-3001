<!DOCTYPE html>
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-88171FSWS3"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-88171FSWS3');
    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

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
            // json_encode adds quotes and escapes special characters automatically
            const report = <?php echo json_encode(
                file_get_contents("http://backend:5000/report"),
            ); ?>;
            console.log(report);
        }
        echo "</div>";
        ?>
    </main>

</body>

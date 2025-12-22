<head>
    <link rel="stylesheet" href="css/pico.min.css" />
    <link rel="stylesheet" href="css/style.css" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body>
    <main class="container">
        <?php
        $response = file_get_contents("http://backend:5000");
        $news = json_decode($response, true);

        foreach ($news as $item) {
            echo "<div class='card w-96 bg-base-100 card-xs shadow-sm' style='background-color: black; color: white;'>";
            echo "<div class='card-body'>";
            echo "<header>";
            echo "<strong>" . htmlspecialchars($item["source"]) . "</strong>";
            echo "</header>";

            echo "<h5>" . htmlspecialchars($item["title"]) . "</h5>";
            echo "<p>" . htmlspecialchars($item["description"]) . "</p>";

            echo "<footer>";
            echo '<a target="_blank" href="' .
                htmlspecialchars($item["link"]) .
                '" role="button" class="outline">Read More</a>';
            echo "</footer>";
            echo "</div>";
            echo "</div>";
        }
        ?>
    </main>

</body>

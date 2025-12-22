<!DOCTYPE html>
<head>
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
    <main class="p-4">
        <?php
        $response = file_get_contents("http://backend:5000");
        $news = json_decode($response, true);
        echo "<div class='grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4'>";
        foreach ($news as $item) {
            echo "<div class='card bg-base-100 shadow-sm min-w-0'>";
            echo "<div class='card-body'>";
            echo "<h2 class='card-title'>" .
                htmlspecialchars($item["source"]) .
                "</h2>";
            echo "<p>" . htmlspecialchars($item["title"]) . "</p>";
            echo "<p>" . htmlspecialchars($item["description"]) . "</p>";
            echo "<div class='card-actions justify-end'>";
            echo '<button class="btn btn-primary">';
            echo '<a target="_blank" href="' .
                htmlspecialchars($item["link"]) .
                '">Read More</a>';
            echo "</button>";
            echo "</div>";
            echo "</div>";
            echo "</div>";
        }
        echo "</div>";
        ?>
    </main>

</body>

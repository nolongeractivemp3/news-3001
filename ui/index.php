<head>
    <link rel="stylesheet" href="css/pico.min.css" />
    <link rel="stylesheet" href="css/style.css" />
</head>
<body>
    <main class="container">
        <?php
        $response = file_get_contents("http://backend:5000");
        $news = json_decode($response, true);

        foreach ($news as $item) {
            echo "<article>";
            echo "<header>";
            echo "<strong>" . htmlspecialchars($item["source"]) . "</strong>";
            echo "</header>";

            echo "<h5>" . htmlspecialchars($item["title"]) . "</h5>";
            echo "<p>" . htmlspecialchars($item["description"]) . "</p>";

            echo "<footer>";
            echo '<a href="' .
                htmlspecialchars($item["link"]) .
                '" role="button" class="outline">Read More</a>';
            echo "</footer>";
            echo "</article>";
        }
        ?>
    </main>

</body>

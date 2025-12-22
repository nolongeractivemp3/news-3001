<head>
    <link rel="stylesheet" href="css/pico.min.css" />
</head>
<body>
    <table id="newsTable">
        <thead>
            <tr style="display: relative;">
                <th style="width: 5%;">Source</th>
                <th style="width: 20%;">Title</th>
                <th style="">Description</th>
                <th style="width: 3%;">Link</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $response = file_get_contents("http://backend:5000");

            $news = json_decode($response, true);
            foreach ($news as $item) {
                echo "<tr>";
                echo "<td>" . htmlspecialchars($item["source"]) . "</td>";
                echo "<td style='font-weight: bold;'>" .
                    htmlspecialchars($item["title"]) .
                    "</td>";
                echo "<td>" . htmlspecialchars($item["description"]) . "</td>";
                echo '<td><a style="scale: 80%;" role="button" href="' .
                    htmlspecialchars($item["link"]) .
                    '">Link</a></td>';
                echo "</tr>";
            }
            ?>
        </tbody>
    </table>

</body>

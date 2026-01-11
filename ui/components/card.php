<?php
$mode = $_GET["domain"] ?? "";
$domain = $response = file_get_contents("http://backend:5000/" . $mode);
$news = json_decode($response, true);
?>
<div class='grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4'>
    <?php foreach ($news as $item): ?>
    <div class='card bg-base-100 shadow-sm min-w-0' style='background-color: #3B4754;'>
        <div class='card-body'>
            <h2 class='card-title'><?php echo $item["title"]; ?></h2>
            <p><?php echo $item["source"]; ?></p>
            <p><?php echo $item["description"]; ?></p>
            <div class='card-actions flex items-center '>

                <div class="flex items-center  mr-auto">
                    <?php if ($mode != "rss"): ?>
                    <div hx-get="/components/badge.php?badge=<?php echo htmlspecialchars(
                        urlencode(json_encode($item["badges"])),
                    ); ?>"
                         hx-trigger="load"
                         hx-target="next .badgeslot">
                    </div>
                    <?php endif; ?>
                    <div class="badgeslot flex gap-1 flex-nowrap"></div>
                </div>

                <button class="btn btn-primary btn-sm flex-shrink-0">
                    <a target="_blank" href="<?php echo htmlspecialchars(
                        $item["link"],
                    ); ?>">Öffnen</a>
                </button>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>

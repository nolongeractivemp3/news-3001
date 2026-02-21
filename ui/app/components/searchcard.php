<?php
$search = $_GET["q"] ?? "";
$search = trim($search);

$endpoint = $search 
    ? "http://backend:5000/search?q=" . urlencode($search)
    : "http://backend:5000/recent";

$response = @file_get_contents($endpoint);
if ($response === false) {
    $news = [];
} else {
    $news = json_decode($response, true) ?: [];
}

$ignoreEnabled =
    isset($_COOKIE["ignore_enabled_v1"]) &&
    $_COOKIE["ignore_enabled_v1"] === "true";
$ignoredSources = [];
if ($ignoreEnabled && isset($_COOKIE["ignored_sources_v1"])) {
    $ignoredSources = json_decode($_COOKIE["ignored_sources_v1"], true) ?: [];
}
$ignoredSet = array_flip($ignoredSources);
?>
<?php if (empty($news)): ?>
    <div class="text-center py-8 text-white/60">
        <?php if ($search): ?>
            <p>Keine Ergebnisse gefunden für "<?php echo htmlspecialchars($search, ENT_QUOTES, 'UTF-8'); ?>"</p>
        <?php else: ?>
            <p>Keine Artikel gefunden.</p>
        <?php endif; ?>
    </div>
<?php else: ?>
<div class='grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4'>
    <?php foreach ($news as $item): ?>
        <?php
        $sourceNormalized = strtolower(trim($item["source"]));
        if ($ignoreEnabled && isset($ignoredSet[$sourceNormalized])) {
            continue;
        }
        ?>
    <div class='card bg-base-100 shadow-sm min-w-0' style='background-color: #3B4754;'>
        <div class='card-body'>
            <h2 class='card-title'><?php echo htmlspecialchars($item["title"], ENT_QUOTES, 'UTF-8'); ?></h2>
            <p><?php echo htmlspecialchars($item["source"], ENT_QUOTES, 'UTF-8'); ?></p>
            <p><?php echo htmlspecialchars($item["description"], ENT_QUOTES, 'UTF-8'); ?></p>
            <div class='card-actions flex items-center '>

                <div class="flex items-center mr-auto">
                    <div hx-get="/app/components/badge.php?badge=<?php echo htmlspecialchars(
                        urlencode(json_encode($item["badges"])),
                    ); ?>"
                         hx-trigger="load"
                         hx-target="next .badgeslot">
                    </div>
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
<?php endif; ?>

<?php
$year = date("Y");
$footerLinks = [
    ["href" => "/", "label" => "News"],
    ["href" => "/index.php?rss", "label" => "RSS"],
    ["href" => "/stats.php", "label" => "Stats"],
    ["href" => "/homepage/index.php", "label" => "Homepage"],
    ["href" => "https://github.com/nolongeractivemp3/news-3001", "label" => "Github Mirror"],
];
?>

<footer class="mt-auto w-full border-t border-white/20 pt-6">
    <div class="mx-auto flex w-full max-w-5xl flex-col gap-3 px-4 py-6 text-sm text-white/80 sm:flex-row sm:items-center sm:justify-between">
        <p> News 3001 entwickelt von einem Nerd in Köpenick</p>
        <nav class="flex flex-wrap gap-x-4 gap-y-2">
            <?php foreach ($footerLinks as $link): ?>
                <a href="<?php echo htmlspecialchars($link["href"]); ?>" class="text-white/80 transition-colors hover:text-white">
                    <?php echo htmlspecialchars($link["label"]); ?>
                </a>
            <?php endforeach; ?>
        </nav>
    </div>
</footer>

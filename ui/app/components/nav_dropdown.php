<?php
$rss = $_GET["rss"] ?? "false";
$isRss = $rss === "true";
$isDropdown = ($_GET["dropdown"] ?? "true") === "true";

$preference = $_COOKIE["news_preference"] ?? "news";
$prefIsRss = $preference === "rss";
?>

<?php if ($isDropdown): ?>
<div class="dropdown dropdown-bottom sm:hidden">
    <div tabindex="0" role="button" class="btn btn-ghost normal-case text-base px-3">
        <?php echo $isRss ? "RSS" : "News"; ?>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
    </div>
    <ul tabindex="0" class="dropdown-content menu bg-base-200 rounded-box z-10 w-32 p-2 shadow-sm">
        <li>
            <a href="./" class="<?php echo !$isRss ? "active" : ""; ?>">News</a>
        </li>
        <li>
            <a href="./index.php?rss" class="<?php echo $isRss ? "active" : ""; ?>">RSS</a>
        </li>
    </ul>
</div>
<?php else: ?>
<a href="./index.php<?php echo $prefIsRss ? "?rss" : ""; ?>" class="btn btn-ghost normal-case text-base px-3 sm:hidden"><?php echo $prefIsRss ? "RSS" : "News"; ?></a>
<?php endif; ?>

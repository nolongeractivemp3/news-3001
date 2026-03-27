<?php
$rss = $_GET["rss"] ?? "false";
$date = $_GET["date"] ?? "false";
$statsRange = $_GET["statsRange"] ?? "false";
$dropdown = $_GET["dropdown"] ?? "false";
?>

<div class="navbar bg-base-100 shadow-sm gap-0">
    <div class="navbar-start w-auto flex-nowrap items-center gap-0">
        <a href="./" class="btn btn-ghost normal-case text-xl px-2 sm:px-3 hidden sm:inline-flex">News</a>
        <a href="./index.php?rss" class="btn btn-ghost normal-case px-2 sm:px-3 hidden sm:inline-flex">RSS</a>
        <?php include __DIR__ . "/nav_dropdown.php"; ?>
        <a href="./stats.php" class="btn btn-ghost normal-case px-2 sm:px-3">Stats</a>
        <?php if ($date === "true" || $statsRange === "true"): ?>
            <div
                hx-get="components/datepicker.php?selectedDate=<?php echo urlencode(
                    $_GET["selectedDate"] ?? "",
                ); ?>&statsRange=<?php echo urlencode(
                    $statsRange,
                ); ?>&startDate=<?php echo urlencode(
                    $_GET["startDate"] ?? "",
                ); ?>&endDate=<?php echo urlencode(
                    $_GET["endDate"] ?? "",
                ); ?>"
                hx-trigger="load"
                hx-target="this">
            </div>
        <?php endif; ?>
        <?php if ($rss === "true"): ?>
            <a onclick="getExplanation()" class="btn btn-ghost btn-square btn-sm" aria-label="RSS Erklärung">?</a>
        <?php endif; ?>
    </div>

    <div class="navbar-end ml-auto w-auto flex-none">
        <button class="btn btn-ghost" onclick="openSettingsModal()">
            <span class="hidden sm:inline">Settings</span>
            <span class="sm:hidden">⚙️</span>
        </button>
        <button class="btn btn-primary" onclick="getReport()">
            <span class="hidden sm:inline">Zusammenfassung</span>
            <span class="sm:hidden">📋</span>

        </button>
    </div>
</div>

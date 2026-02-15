<?php
$rss = $_GET["rss"] ?? "false";
$date = $_GET["date"] ?? "false";
?>

<div class="navbar bg-base-100 shadow-sm gap-0">
    <div class="navbar-start w-auto flex-nowrap items-center gap-0">
        <a href="/" class="btn btn-ghost normal-case text-xl px-2 sm:px-3">News</a>
        <a href="/index.php?rss" class="btn btn-ghost normal-case px-2 sm:px-3">RSS</a>
        <?php if ($date === "true"): ?>
            <?php include __DIR__ . "/datepicker.php"; ?>
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

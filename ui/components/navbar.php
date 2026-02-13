<?php
$rss = $_GET["rss"]; ?>

<div class="navbar bg-base-100 shadow-sm">
    <div class="navbar-start">
        <a href="/" class="btn btn-ghost normal-case text-xl">News</a>
        <a href="?rss" class="btn btn-ghost normal-case ">RSS</a>
        <?php if ($rss == "true"): ?>
            <a onclick="getExplanation()" class="btn btn-ghost small">?</a>
        <?php endif; ?>
    </div>

    <div class="navbar-end">
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

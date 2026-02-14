<?php
$rss = $_GET["rss"] ?? "false";
$date = $_GET["date"] ?? "false";
$selectedDate = $_GET["selectedDate"] ?? date("Y-m-d");
$selectedDateObj = DateTime::createFromFormat("Y-m-d", $selectedDate);
if ($selectedDateObj === false || $selectedDateObj->format("Y-m-d") !== $selectedDate) {
    $selectedDate = date("Y-m-d");
}
?>

<div class="navbar bg-base-100 shadow-sm gap-0">
    <div class="navbar-start w-auto flex-nowrap items-center gap-0">
        <a href="/" class="btn btn-ghost normal-case text-xl px-2 sm:px-3">News</a>
        <a href="/index.php?rss" class="btn btn-ghost normal-case px-2 sm:px-3">RSS</a>
        <a href="/history.php" class="btn btn-ghost normal-case px-2 sm:px-3">Date</a>
        <?php if ($date === "true"): ?>
        <div class="relative h-10 w-10 shrink-0 overflow-hidden rounded-btn sm:hidden">
            <div class="btn btn-ghost btn-square h-10 min-h-10 w-10 pointer-events-none" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
            </div>
            <input type="date"
                   id="history-date-picker-mobile"
                   name="date"
                   class="absolute inset-0 m-0 h-full w-full cursor-pointer appearance-none border-0 bg-transparent opacity-0"
                   value="<?php echo htmlspecialchars($selectedDate, ENT_QUOTES, "UTF-8"); ?>"
                   max="<?php echo date("Y-m-d"); ?>"
                   aria-label="Datum auswählen"
                   hx-get="/components/card.php"
                   hx-trigger="change"
                   hx-target="#news"
                   hx-swap="innerHTML"
                   onchange="if (window.htmx) { htmx.ajax('GET', '/components/report.php?name=report_modal&date=' + encodeURIComponent(this.value), { target: '#report', swap: 'innerHTML' }); } const desktopPicker = document.getElementById('history-date-picker-desktop'); if (desktopPicker) desktopPicker.value = this.value;" />
        </div>
        <input type="date"
               id="history-date-picker-desktop"
               name="date"
               class="input input-sm hidden sm:inline-flex h-9 w-36"
               value="<?php echo htmlspecialchars($selectedDate, ENT_QUOTES, "UTF-8"); ?>"
               max="<?php echo date("Y-m-d"); ?>"
               hx-get="/components/card.php"
               hx-trigger="change"
               hx-target="#news"
               hx-swap="innerHTML"
               onchange="if (window.htmx) { htmx.ajax('GET', '/components/report.php?name=report_modal&date=' + encodeURIComponent(this.value), { target: '#report', swap: 'innerHTML' }); } const mobilePicker = document.getElementById('history-date-picker-mobile'); if (mobilePicker) mobilePicker.value = this.value;" />
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

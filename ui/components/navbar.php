<?php
$rss = $_GET["rss"] ?? "false";
$date = $_GET["date"] ?? "false";
$selectedDate = $_GET["selectedDate"] ?? date("Y-m-d");
$selectedDateObj = DateTime::createFromFormat("Y-m-d", $selectedDate);
if ($selectedDateObj === false || $selectedDateObj->format("Y-m-d") !== $selectedDate) {
    $selectedDate = date("Y-m-d");
}
?>

<div class="navbar bg-base-100 shadow-sm">
    <div class="navbar-start">
        <a href="/" class="btn btn-ghost normal-case text-xl">News</a>
        <a href="?rss" class="btn btn-ghost normal-case ">RSS</a>
        <a href="history.php" class="btn btn-ghost normal-case ">Date</a>
        <?php if ($date === "true"): ?>
        <input type="date"
               id="history-date-picker"
               name="date"
               class="input"
               value="<?php echo htmlspecialchars($selectedDate, ENT_QUOTES, "UTF-8"); ?>"
               max="<?php echo date("Y-m-d"); ?>"
               hx-get="/components/card.php"
               hx-trigger="change"
               hx-target="#news"
               hx-swap="innerHTML" />
        <?php endif; ?>
        <?php if ($rss === "true"): ?>
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

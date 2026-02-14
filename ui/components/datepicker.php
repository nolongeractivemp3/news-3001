<?php
$selectedDate = $_GET["selectedDate"] ?? date("Y-m-d");
$selectedDateObj = DateTime::createFromFormat("Y-m-d", $selectedDate);
if ($selectedDateObj === false || $selectedDateObj->format("Y-m-d") !== $selectedDate) {
    $selectedDate = date("Y-m-d");
}
?>

<!-- Mobile date picker (visible on small screens) -->
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
           onchange="window.location.href = '/history.php?date=' + encodeURIComponent(this.value);" />
</div>
<!-- Desktop date picker (visible on larger screens) -->
<input type="date"
       id="history-date-picker-desktop"
       name="date"
       class="input input-sm hidden sm:inline-flex h-9 w-36"
       value="<?php echo htmlspecialchars($selectedDate, ENT_QUOTES, "UTF-8"); ?>"
       max="<?php echo date("Y-m-d"); ?>"
       onchange="window.location.href = '/history.php?date=' + encodeURIComponent(this.value);" />

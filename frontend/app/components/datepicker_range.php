<?php
$startDate = $_GET["startDate"] ?? date("Y-m-d", strtotime("-29 days"));
$endDate = $_GET["endDate"] ?? date("Y-m-d");
?>
<script>
    function updateStatsRangeDate() {
        const startDate = document.getElementById("stats-start-date-picker").value;
        const endDate = document.getElementById("stats-end-date-picker").value;
        window.location.href =
            "/app/stats.php?start_date=" +
            encodeURIComponent(startDate) +
            "&end_date=" +
            encodeURIComponent(endDate);
    }
</script>
<div class="flex items-center gap-2 ml-2">
    <input type="date"
           id="stats-start-date-picker"
           name="start_date"
           class="input input-sm h-9 w-32 sm:w-36"
           value="<?php echo htmlspecialchars(
               $startDate,
               ENT_QUOTES,
               "UTF-8",
           ); ?>"
           max="<?php echo htmlspecialchars($endDate, ENT_QUOTES, "UTF-8"); ?>"
           aria-label="Startdatum auswählen"
           onchange="updateStatsRangeDate()" />
    <input type="date"
           id="stats-end-date-picker"
           name="end_date"
           class="input input-sm h-9 w-32 sm:w-36"
           value="<?php echo htmlspecialchars(
               $endDate,
               ENT_QUOTES,
               "UTF-8",
           ); ?>"
           min="<?php echo htmlspecialchars($startDate, ENT_QUOTES, "UTF-8"); ?>"
           max="<?php echo date("Y-m-d"); ?>"
           aria-label="Enddatum auswählen"
           onchange="updateStatsRangeDate()" />
</div>

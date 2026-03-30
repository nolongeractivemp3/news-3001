<?php
$startDate = $_GET["startDate"] ?? date("Y-m-d", strtotime("-29 days"));
$endDate = $_GET["endDate"] ?? date("Y-m-d");
?>
<div class="bg-base-100 shadow-sm mt-2 p-2 flex justify-start">
    <div
        hx-get="components/datepicker.php?statsRange=true&startDate=<?php echo urlencode(
            $startDate,
        ); ?>&endDate=<?php echo urlencode(
            $endDate,
        ); ?>"
        hx-trigger="load"
        hx-target="this">
    </div>
</div>

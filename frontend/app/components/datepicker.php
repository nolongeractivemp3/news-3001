<?php
function normalizePickerDate(string $value, string $fallback): string
{
    $date = DateTime::createFromFormat("Y-m-d", $value);
    if ($date === false || $date->format("Y-m-d") !== $value) {
        return $fallback;
    }

    return $value;
}

$statsRange = $_GET["statsRange"] ?? "false";

if ($statsRange === "true") {
    $defaultEndDate = date("Y-m-d");
    $defaultStartDate = date("Y-m-d", strtotime("-29 days"));
    $startDate = normalizePickerDate(
        $_GET["startDate"] ?? $defaultStartDate,
        $defaultStartDate,
    );
    $endDate = normalizePickerDate(
        $_GET["endDate"] ?? $defaultEndDate,
        $defaultEndDate,
    );

    if ($startDate > $endDate) {
        [$startDate, $endDate] = [$endDate, $startDate];
    }

    $query = http_build_query([
        "startDate" => $startDate,
        "endDate" => $endDate,
    ]);
    ?>
    <div
        hx-get="components/datepicker_range.php?<?php echo htmlspecialchars(
            $query,
            ENT_QUOTES,
            "UTF-8",
        ); ?>"
        hx-trigger="load"
        hx-target="this">
    </div>
    <?php
    return;
}

$defaultDate = date("Y-m-d");
$selectedDate = normalizePickerDate($_GET["selectedDate"] ?? $defaultDate, $defaultDate);
$query = http_build_query([
    "selectedDate" => $selectedDate,
]);
?>
<div
    hx-get="components/datepicker_single.php?<?php echo htmlspecialchars(
        $query,
        ENT_QUOTES,
        "UTF-8",
    ); ?>"
    hx-trigger="load"
    hx-target="this">
</div>

<?php
$name = $_GET["name"] ?? "report_modal";
$reportstr =
    $_GET["textstr"] ??
    "<p>Für dieses Datum ist keine Zusammenfassung verfügbar.</p>";
$date = $_GET["date"] ?? null;

if ($date !== null) {
    $dateObj = DateTime::createFromFormat("Y-m-d", $date);
    if ($dateObj !== false && $dateObj->format("Y-m-d") === $date) {
        $rawReport = @file_get_contents(
            "http://backend:5000/oldreport?date=" . urlencode($date),
        );
        if ($rawReport !== false) {
            $decodedReport = json_decode($rawReport, true);
            if (is_string($decodedReport) && trim($decodedReport) !== "") {
                $reportstr = $decodedReport;
            } elseif (
                json_last_error() === JSON_ERROR_NONE &&
                is_array($decodedReport)
            ) {
                $reportstr =
                    "<p>Für den " .
                    htmlspecialchars($date, ENT_QUOTES, "UTF-8") .
                    " ist keine Zusammenfassung verfügbar.</p>";
            } elseif (trim($rawReport) !== "") {
                $reportstr = $rawReport;
            } else {
                $reportstr =
                    "<p>Für den " .
                    htmlspecialchars($date, ENT_QUOTES, "UTF-8") .
                    " ist keine Zusammenfassung verfügbar.</p>";
            }
        } else {
            $reportstr =
                "<p>Für den " .
                htmlspecialchars($date, ENT_QUOTES, "UTF-8") .
                " ist keine Zusammenfassung verfügbar.</p>";
        }
    } else {
        $reportstr = "<p>Ungültiges Datumsformat.</p>";
    }
}

$reportstr = str_replace(
    ["\r", "\n", '\r', '\n'],
    "",
    $reportstr,
);
?>
<style>
h1 {
 font-size: 1rem;
 font-weight: bold;
 margin-bottom: 0.2rem;
}

h2 {
 font-size: 0.875rem;
 font-weight: bold;
 margin-bottom: 0.1rem;
}

h3 {
 font-size: 0.75rem;
 font-weight: bold;
 margin-bottom: 0.05rem;
}

</style>

<dialog id="<?php echo $name; ?>" class="modal block overflow-y-auto bg-black/60 backdrop-blur-sm">
  <div class="relative w-[95%] max-w-3xl my-8 mx-auto border border-primary/20 bg-neutral shadow-2xl p-6 rounded-2xl">

    <form method="dialog">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-4 top-2 text-primary">✕</button>
    </form>

    <article id="ReportContent" class="prose prose-invert prose-sm max-w-none text-left break-words">
       <?php echo $reportstr; ?>
    </article>

  </div>
</dialog>

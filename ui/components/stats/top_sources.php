<?php
$raw_data = urldecode($_GET["data"] ?? "{}");
$parsed_data = json_decode($raw_data, true);
$daily = is_array($parsed_data["daily"] ?? null) ? $parsed_data["daily"] : [];
$daily_json = json_encode(
    $daily,
    JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT,
);
?>

<section class="stats-chart-card">
  <h2 class="stats-chart-title">Top Quellen (Gesamt)</h2>
  <p class="stats-chart-subtitle">Haeufigste Quellen im aktuellen Zeitfenster.</p>
  <div class="stats-chart-canvas-wrap">
    <canvas id="chart-top-sources"></canvas>
  </div>
</section>

<script>
  (() => {
    const daily = <?php echo $daily_json ?: "[]"; ?>;
    const totals = {};

    daily.forEach((entry) => {
      const sourceCounts = Array.isArray(entry.source_counts) ? entry.source_counts : [];
      sourceCounts.forEach((sourceEntry) => {
        const source = String(sourceEntry.source ?? "").trim();
        if (!source) {
          return;
        }
        const count = Number(sourceEntry.count ?? 0);
        totals[source] = (totals[source] || 0) + count;
      });
    });

    const sorted = Object.entries(totals)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);

    const labels = sorted.map(([source]) => source);
    const values = sorted.map(([, count]) => count);
    const colors = window.newsStatsCharts?.colors || {};

    window.newsStatsCharts?.mountChart("chart-top-sources", {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Artikel je Quelle",
            data: values,
            borderWidth: 1,
            borderColor: colors.amberBorder || "rgba(251, 191, 36, 1)",
            backgroundColor: colors.amber || "rgba(251, 191, 36, 0.8)",
          },
        ],
      },
      options: {
        indexAxis: "y",
        plugins: {
          legend: {
            labels: {
              color: colors.slateText || "#cbd5e1",
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              color: colors.slateText || "#cbd5e1",
              precision: 0,
            },
            grid: {
              color: colors.slateGrid || "rgba(148, 163, 184, 0.2)",
            },
          },
          y: {
            ticks: {
              color: colors.slateText || "#cbd5e1",
            },
            grid: {
              color: "rgba(148, 163, 184, 0.08)",
            },
          },
        },
      },
    });
  })();
</script>

<?php
if (!isset($parsed_data) || !is_array($parsed_data)) {
    $raw_data = urldecode($_GET["data"] ?? "{}");
    $parsed_data = json_decode($raw_data, true);
}
$daily = is_array($parsed_data["daily"] ?? null) ? $parsed_data["daily"] : [];
$daily_json = json_encode(
    $daily,
    JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT,
);
?>

<section class="stats-chart-card">
  <h2 class="stats-chart-title">Top Themen (Gesamt)</h2>
  <p class="stats-chart-subtitle">Häufigste Themen im aktuellen Zeitfenster.</p>
  <div class="stats-chart-canvas-wrap">
    <canvas id="chart-top-tags"></canvas>
  </div>
</section>

<script>
  (() => {
    const daily = <?php echo $daily_json ?: "[]"; ?>;
    const totals = {};

    daily.forEach((entry) => {
      const tagCounts = Array.isArray(entry.tag_counts) ? entry.tag_counts : [];
      tagCounts.forEach((tagEntry) => {
        const tag = String(tagEntry.tag ?? "").trim();
        if (!tag) {
          return;
        }
        const count = Number(tagEntry.count ?? 0);
        totals[tag] = (totals[tag] || 0) + count;
      });
    });

    const sorted = Object.entries(totals)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);

    const labels = sorted.map(([tag]) => tag);
    const values = sorted.map(([, count]) => count);
    const colors = window.newsStatsCharts?.colors || {};

    window.newsStatsCharts?.mountChart("chart-top-tags", {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Tag-Nennungen",
            data: values,
            borderWidth: 1,
            borderColor: colors.violetBorder || "rgba(167, 139, 250, 1)",
            backgroundColor: colors.violet || "rgba(167, 139, 250, 0.7)",
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

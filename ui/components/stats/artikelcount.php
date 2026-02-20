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
  <h2 class="stats-chart-title">Artikel pro Tag</h2>
  <p class="stats-chart-subtitle">Anzahl aller erfassten Artikel je Datum.</p>
  <div class="stats-chart-canvas-wrap">
    <canvas id="chart-article-count"></canvas>
  </div>
</section>

<script>
  (() => {
    const daily = <?php echo $daily_json ?: "[]"; ?>;
    const labels = daily.map((entry) => entry.date ?? "");
    const articleCounts = daily.map((entry) => Number(entry.article_count ?? 0));
    const colors = window.newsStatsCharts?.colors || {};

    window.newsStatsCharts?.mountChart("chart-article-count", {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Artikel",
            data: articleCounts,
            borderWidth: 1,
            borderColor: colors.blueBorder || "rgba(56, 189, 248, 1)",
            backgroundColor: colors.blue || "rgba(56, 189, 248, 0.8)",
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            labels: {
              color: colors.slateText || "#cbd5e1",
            },
          },
        },
        scales: {
          x: {
            ticks: {
              color: colors.slateText || "#cbd5e1",
            },
            grid: {
              color: "rgba(148, 163, 184, 0.08)",
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: colors.slateText || "#cbd5e1",
              precision: 0,
            },
            grid: {
              color: colors.slateGrid || "rgba(148, 163, 184, 0.2)",
            },
          },
        },
      },
    });
  })();
</script>

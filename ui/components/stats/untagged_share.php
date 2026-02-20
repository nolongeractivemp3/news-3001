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
  <h2 class="stats-chart-title">Anteil ungetaggt (%)</h2>
  <p class="stats-chart-subtitle">Prozentsatz ungetaggter Artikel je Tag.</p>
  <div class="stats-chart-canvas-wrap">
    <canvas id="chart-untagged-share"></canvas>
  </div>
</section>

<script>
  (() => {
    const daily = <?php echo $daily_json ?: "[]"; ?>;
    const labels = daily.map((entry) => entry.date ?? "");
    const untaggedShare = daily.map((entry) => {
      const articleCount = Number(entry.article_count ?? 0);
      const untaggedCount = Number(entry.untagged_article_count ?? 0);
      if (articleCount <= 0) {
        return 0;
      }
      return Number(((untaggedCount / articleCount) * 100).toFixed(1));
    });
    const colors = window.newsStatsCharts?.colors || {};

    window.newsStatsCharts?.mountChart("chart-untagged-share", {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Ungetaggt (%)",
            data: untaggedShare,
            borderWidth: 2,
            borderColor: colors.amberBorder || "rgba(251, 191, 36, 1)",
            backgroundColor: colors.amber || "rgba(251, 191, 36, 0.8)",
            pointRadius: 3,
            pointHoverRadius: 5,
            tension: 0.25,
            fill: false,
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
          tooltip: {
            callbacks: {
              label(context) {
                return `${context.dataset.label}: ${context.parsed.y}%`;
              },
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
            max: 100,
            ticks: {
              color: colors.slateText || "#cbd5e1",
              callback(value) {
                return `${value}%`;
              },
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

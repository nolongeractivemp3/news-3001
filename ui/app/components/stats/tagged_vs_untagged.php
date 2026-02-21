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
  <h2 class="stats-chart-title">Getaggt vs. Nicht Getaggt</h2>
  <p class="stats-chart-subtitle">Wie viele News nach Themen kategorisiert sind</p>
  <div class="stats-chart-canvas-wrap">
    <canvas id="chart-tagged-vs-untagged"></canvas>
  </div>
</section>

<script>
  (() => {
    const daily = <?php echo $daily_json ?: "[]"; ?>;
    const labels = daily.map((entry) => entry.date ?? "");
    const untagged = daily.map((entry) => Number(entry.untagged_article_count ?? 0));
    const tagged = daily.map((entry) => {
      const articleCount = Number(entry.article_count ?? 0);
      const untaggedCount = Number(entry.untagged_article_count ?? 0);
      return Math.max(articleCount - untaggedCount, 0);
    });
    const colors = window.newsStatsCharts?.colors || {};

    window.newsStatsCharts?.mountChart("chart-tagged-vs-untagged", {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Getaggt",
            data: tagged,
            borderWidth: 1,
            borderColor: colors.greenBorder || "rgba(74, 222, 128, 1)",
            backgroundColor: colors.green || "rgba(74, 222, 128, 0.7)",
            stack: "article_tag_state",
          },
          {
            label: "Ungetaggt",
            data: untagged,
            borderWidth: 1,
            borderColor: colors.roseBorder || "rgba(251, 113, 133, 1)",
            backgroundColor: colors.rose || "rgba(251, 113, 133, 0.75)",
            stack: "article_tag_state",
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
            stacked: true,
            ticks: {
              color: colors.slateText || "#cbd5e1",
            },
            grid: {
              color: "rgba(148, 163, 184, 0.08)",
            },
          },
          y: {
            stacked: true,
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

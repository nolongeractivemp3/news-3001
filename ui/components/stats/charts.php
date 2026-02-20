<?php
$raw_data = urldecode($_GET["data"] ?? "{}");
$encoded_data = urlencode($raw_data);
?>

<style>
  .stats-charts-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    width: 100%;
    margin-top: 1rem;
  }

  .stats-chart-card {
    background: #3b4754;
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 0.9rem;
    padding: 1rem;
  }

  .stats-chart-title {
    margin: 0 0 0.2rem 0;
    font-size: 1rem;
    font-weight: 700;
    color: #f8fafc;
  }

  .stats-chart-subtitle {
    margin: 0 0 0.75rem 0;
    color: #cbd5e1;
    font-size: 0.875rem;
  }

  .stats-chart-canvas-wrap {
    position: relative;
    width: 100%;
    height: 250px;
  }

  @media (min-width: 768px) {
    .stats-chart-canvas-wrap {
      height: 300px;
    }
  }

  @media (min-width: 1280px) {
    .stats-charts-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }
</style>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js"></script>
<script>
  (() => {
    if (window.newsStatsCharts) {
      return;
    }

    const instances = {};

    const waitForChart = (callback, retries = 120) => {
      if (typeof window.Chart !== "undefined") {
        callback();
        return;
      }
      if (retries <= 0) {
        return;
      }
      setTimeout(() => waitForChart(callback, retries - 1), 50);
    };

    window.newsStatsCharts = {
      colors: {
        blue: "rgba(56, 189, 248, 0.8)",
        blueBorder: "rgba(56, 189, 248, 1)",
        green: "rgba(74, 222, 128, 0.7)",
        greenBorder: "rgba(74, 222, 128, 1)",
        amber: "rgba(251, 191, 36, 0.8)",
        amberBorder: "rgba(251, 191, 36, 1)",
        rose: "rgba(251, 113, 133, 0.75)",
        roseBorder: "rgba(251, 113, 133, 1)",
        violet: "rgba(167, 139, 250, 0.7)",
        violetBorder: "rgba(167, 139, 250, 1)",
        slateText: "#cbd5e1",
        slateGrid: "rgba(148, 163, 184, 0.2)",
      },
      mountChart(canvasId, config) {
        waitForChart(() => {
          const canvas = document.getElementById(canvasId);
          if (!canvas) {
            return;
          }

          if (instances[canvasId]) {
            instances[canvasId].destroy();
          }

          const mergedOptions = Object.assign(
            {
              responsive: true,
              maintainAspectRatio: false,
            },
            config.options || {}
          );

          const finalConfig = Object.assign({}, config, { options: mergedOptions });
          instances[canvasId] = new window.Chart(canvas, finalConfig);
        });
      },
    };
  })();
</script>

<div class="stats-charts-grid">
  <div id="stats-chart-articlecount"
       hx-get="components/stats/artikelcount.php?data=<?php echo $encoded_data; ?>"
       hx-trigger="load"></div>

  <div id="stats-chart-tagged-untagged"
       hx-get="components/stats/tagged_vs_untagged.php?data=<?php echo $encoded_data; ?>"
       hx-trigger="load"></div>

  <div id="stats-chart-top-sources"
       hx-get="components/stats/top_sources.php?data=<?php echo $encoded_data; ?>"
       hx-trigger="load"></div>

  <div id="stats-chart-top-tags"
       hx-get="components/stats/top_tags.php?data=<?php echo $encoded_data; ?>"
       hx-trigger="load"></div>
</div>

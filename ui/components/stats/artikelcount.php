<?php 
$raw_data = urldecode($_GET["data"]);
?>
<div>
  <canvas id="myChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js"></script><script>
  const ctx = document.getElementById('myChart');
  const data = JSON.parse('<?php echo $raw_data; ?>');
  console.log(data);
  labels = [];
  numbers = [];
  for (let i = 0; i < data["daily"].length; i++) {
    labels.push(data["daily"][i]["date"]);
    numbers.push(data["daily"][i]["article_count"]);
  }
  // Wait for Chart to be available before initializing (fixes CDN loading race condition)
  function initChart() {
    if (typeof Chart === 'undefined') {
      setTimeout(initChart, 100);
      return;
    }
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Number of articles',
          data: numbers,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
  
  initChart();
</script>

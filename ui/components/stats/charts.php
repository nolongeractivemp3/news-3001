<?php 
$raw_data = urldecode($_GET["data"]);
?>
<head></head>
<body>
  <div hx-get="components/stats/artikelcount.php?data=<?php echo urlencode($raw_data); ?>" hx-trigger="load" hx-target="#chart"></div>
</body>

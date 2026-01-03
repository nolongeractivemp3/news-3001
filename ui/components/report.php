<?php
$name = $_GET["name"];
$reportstr = $_GET["textstr"];
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

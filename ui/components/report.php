<style>
#report_modal {
  padding: 0;
  border: none;
  background: transparent;
}

#report_modal::backdrop {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}


</style>
<dialog id="report_modal" class="modal">
    <div class="modal-box w-full md:w-11/12 max-w-3xl border border-primary/20 bg-neutral ">
        <form method="dialog">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-4 top-4 text-primary">✕</button>
        </form>
        <article id="ReportContent" class="prose prose-invert prose-sm max-w-none
                        prose-h1:text-xl prose-h1:mb-2
                        prose-h2:text-lg prose-h2:mb-1
                        prose-h3:text-base prose-h3:mb-1
                        break-words"><?php echo $reportstr; ?></article>
    </div>
    <form method="dialog" class="modal-backdrop bg-black/60 backdrop-blur-sm">
        <button>close</button>
    </form>
</dialog>

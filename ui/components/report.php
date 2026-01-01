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
<dialog id="report_modal" class="modal">
    <div class="modal-box w-full md:w-11/12 max-w-3xl border border-primary/20 bg-neutral ">
        <form method="dialog">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-4 top-4 text-primary">✕</button>
        </form>
        <article id="ReportContent" class="prose prose-invert prose-sm md:prose-lg max-w-none text-left break-words overflow-x-hidden"></article>
    </div>
    <form method="dialog" class="modal-backdrop bg-black/60 backdrop-blur-sm">
        <button>close</button>
    </form>
</dialog>

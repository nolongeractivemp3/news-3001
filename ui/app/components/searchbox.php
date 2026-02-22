<?php
$searchQuery = $_GET["q"] ?? "";
$searchQuery = trim($searchQuery);
?>

<div class="w-full max-w-2xl mx-auto py-4">
    <input 
        type="text" 
        name="q" 
        id="search-input"
        placeholder="Suche in allen Artikeln..." 
        class="input input-bordered w-full"
        value="<?php echo htmlspecialchars($searchQuery, ENT_QUOTES, 'UTF-8'); ?>"
        hx-get="components/searchcard.php"
        hx-trigger="keyup changed delay:300ms, search"
        hx-target="#news"
        hx-indicator="#search-indicator"
        hx-params="q"
        hx-on::htmx:after-request="if(this.value.trim()){history.replaceState(null,'','./archive.php?q='+encodeURIComponent(this.value.trim()))}else{history.replaceState(null,'','./archive.php')}"
    />
    <div class="flex items-center gap-2 mt-2">
        <span id="search-indicator" class="htmx-indicator loading loading-spinner loading-sm"></span>
        <p class="text-sm text-white/60">
            <?php if ($searchQuery): ?>
                Ergebnisse für: <strong><?php echo htmlspecialchars($searchQuery, ENT_QUOTES, 'UTF-8'); ?></strong>
            <?php else: ?>
                Neueste Artikel werden angezeigt. Tippe um zu suchen.
            <?php endif; ?>
        </p>
    </div>
</div>

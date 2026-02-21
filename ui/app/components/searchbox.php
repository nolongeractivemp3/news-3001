<?php
$searchQuery = $_GET["q"] ?? "";
$searchQuery = trim($searchQuery);
?>

<div class="w-full max-w-2xl mx-auto py-4">
    <form method="GET" action="./archive.php" class="flex gap-2">
        <input 
            type="text" 
            name="q" 
            placeholder="Suche in allen Artikeln..." 
            class="input input-bordered flex-1"
            value="<?php echo htmlspecialchars($searchQuery, ENT_QUOTES, 'UTF-8'); ?>"
            minlength="2"
        />
        <button type="submit" class="btn btn-primary">
            Suchen
        </button>
    </form>
    <?php if ($searchQuery): ?>
        <p class="text-sm text-white/60 mt-2">
            Ergebnisse für: <strong><?php echo htmlspecialchars($searchQuery, ENT_QUOTES, 'UTF-8'); ?></strong>
        </p>
    <?php else: ?>
        <p class="text-sm text-white/60 mt-2">
            Neueste Artikel werden angezeigt. Gib einen Suchbegriff ein, um das Archiv zu durchsuchen.
        </p>
    <?php endif; ?>
</div>

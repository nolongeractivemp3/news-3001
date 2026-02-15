<dialog id="settings_modal" class="modal">
    <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">Einstellungen</h3>

        <div class="form-control">
            <label class="label cursor-pointer">
                <span class="label-text">Filter benutzen</span>
                <input
                    type="checkbox"
                    id="ignore_enabled"
                    class="checkbox checkbox-primary"
                />
            </label>
        </div>

        <div class="form-control mt-4">
            <label class="label">
                <span class="label-text">Ignorierte quellen (mit komma unterteilen)</span>
            </label>
            <textarea
                id="ignored_sources"
                class="textarea textarea-bordered w-full"
                placeholder="bild,nius,Tagespiegel"
            ></textarea>
        </div>

        <div class="modal-action">
            <button class="btn" onclick="saveSettings()">Speichern</button>
            <button class="btn btn-ghost" onclick="resetSettings()">Reset</button>
            <button class="btn" onclick="document.getElementById('settings_modal').close()">schließen</button>
        </div>
    </div>
    <form method="dialog" class="modal-backdrop">
        <button>schließen</button>
    </form>
</dialog>

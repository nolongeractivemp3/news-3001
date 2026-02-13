<dialog id="settings_modal" class="modal">
    <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">Einstellungen</h3>
        <div class="form-control">
            <label class="label cursor-pointer">
                <span class="label-text">Filter benutzen</span>
                <input type="checkbox" id="ignore_enabled" class="checkbox checkbox-primary" />
            </label>
        </div>
        <div class="form-control mt-4">
            <label class="label">
                <span class="label-text">Ignorierte quellen (mit komma unterteilen)</span>
            </label>
            <textarea id="ignored_sources" class="textarea textarea-bordered w-full" placeholder="bild,nius,Tagespiegel"></textarea>
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
<script>
    function openSettingsModal() {
        loadSettings();
        document.getElementById("settings_modal").showModal();
    }
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }
    function setCookie(name, value, days = 365) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/';
    }
    function deleteCookie(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    }
    function loadSettings() {
        const enabled = getCookie("ignore_enabled_v1") === "true";
        const sourcesJson = getCookie("ignored_sources_v1") || "[]";
        let sources = [];
        try { sources = JSON.parse(sourcesJson); } catch (e) { sources = []; }
        document.getElementById("ignore_enabled").checked = enabled;
        document.getElementById("ignored_sources").value = sources.join(", ");
    }
    function normalizeSources(input) {
        return [...new Set(
            input.split(",")
                .map(s => s.trim().toLowerCase())
                .filter(s => s.length > 0)
        )];
    }
    function saveSettings() {
        const enabled = document.getElementById("ignore_enabled").checked;
        const sources = normalizeSources(document.getElementById("ignored_sources").value);
        setCookie("ignore_enabled_v1", enabled ? "true" : "false");
        setCookie("ignored_sources_v1", JSON.stringify(sources));
        location.reload();
    }
    function resetSettings() {
        deleteCookie("ignore_enabled_v1");
        deleteCookie("ignored_sources_v1");
        location.reload();
    }
</script>

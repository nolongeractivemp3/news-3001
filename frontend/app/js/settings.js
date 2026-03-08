(function () {
    if (window.__settingsModuleInitialized) {
        return;
    }
    window.__settingsModuleInitialized = true;

    const IGNORE_ENABLED_COOKIE = "ignore_enabled_v1";
    const IGNORED_SOURCES_COOKIE = "ignored_sources_v1";
    const IGNORE_ENABLED_ID = "ignore_enabled";
    const IGNORED_SOURCES_ID = "ignored_sources";
    

    function getCookie(name) {
        const match = document.cookie.match(
            new RegExp(`(^| )${name}=([^;]+)`),
        );
        return match ? decodeURIComponent(match[2]) : null;
    }

    function setCookie(name, value, days = 365) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(
            value,
        )}; expires=${expires}; path=/`;
    }

    function deleteCookie(name) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
    }

    function normalizeSources(input) {
        if (typeof input !== "string") {
            return [];
        }

        return [
            ...new Set(
                input
                    .split(",")
                    .map((source) => source.trim().toLowerCase())
                    .filter((source) => source.length > 0),
            ),
        ];
    }

    function parseIgnoredSources(value) {
        if (!value) {
            return [];
        }
        try {
            const parsed = JSON.parse(value);
            return Array.isArray(parsed) ? parsed : [];
        } catch (error) {
            return [];
        }
    }

    function loadSettings() {
        const enabledElement = document.getElementById(IGNORE_ENABLED_ID);
        const sourcesElement = document.getElementById(IGNORED_SOURCES_ID);
        if (!enabledElement || !sourcesElement) {
            return false;
        }

        enabledElement.checked = getCookie(IGNORE_ENABLED_COOKIE) === "true";

        const parsedSources = parseIgnoredSources(
            getCookie(IGNORED_SOURCES_COOKIE),
        );
        sourcesElement.value = normalizeSources(parsedSources.join(",")).join(
            ", ",
        );

        return true;
    }

    function saveSettings() {
        const enabledElement = document.getElementById(IGNORE_ENABLED_ID);
        const sourcesElement = document.getElementById(IGNORED_SOURCES_ID);
        if (!enabledElement || !sourcesElement) {
            return;
        }

        const enabled = enabledElement.checked;
        const sources = normalizeSources(sourcesElement.value);
        setCookie(IGNORE_ENABLED_COOKIE, enabled ? "true" : "false");
        setCookie(IGNORED_SOURCES_COOKIE, JSON.stringify(sources));

        location.reload();
    }

    function resetSettings() {
        deleteCookie(IGNORE_ENABLED_COOKIE);
        deleteCookie(IGNORED_SOURCES_COOKIE);

        location.reload();
    }

    function openSettingsModal() {
        const modal = document.getElementById("settings_modal");
        if (!modal || typeof modal.showModal !== "function") {
            return;
        }

        loadSettings();
        modal.showModal();
    }

    window.openSettingsModal = openSettingsModal;
    window.saveSettings = saveSettings;
    window.resetSettings = resetSettings;
})();

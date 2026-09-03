(() => {
    const STORAGE_KEY = "databoard-theme";
    const root = document.documentElement;

    const getSystemTheme = () => (
        window.matchMedia("(prefers-color-scheme: light)").matches
            ? "light"
            : "dark"
    );

    let theme = getSystemTheme();

    try {
        const savedTheme = window.localStorage.getItem(STORAGE_KEY);

        if (savedTheme === "light" || savedTheme === "dark") {
            theme = savedTheme;
        }
    } catch {
        // Mantém o tema do sistema quando o armazenamento não está disponível.
    }

    root.dataset.theme = theme;
    root.setAttribute("data-bs-theme", theme);
    root.style.colorScheme = theme;
})();
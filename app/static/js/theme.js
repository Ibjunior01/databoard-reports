(() => {
    const STORAGE_KEY = "databoard-theme";
    const root = document.documentElement;

    const mediaQuery = window.matchMedia(
        "(prefers-color-scheme: light)"
    );

    const getStoredTheme = () => {
        try {
            const savedTheme = window.localStorage.getItem(
                STORAGE_KEY
            );

            if (
                savedTheme === "light"
                || savedTheme === "dark"
            ) {
                return savedTheme;
            }
        } catch {
            return null;
        }

        return null;
    };

    const persistTheme = (theme) => {
        try {
            window.localStorage.setItem(
                STORAGE_KEY,
                theme
            );
        } catch {
            // O tema continua funcionando sem persistência.
        }
    };

    const getCssVariable = (name) => (
        getComputedStyle(root)
            .getPropertyValue(name)
            .trim()
    );

    const updateToggle = (theme) => {
        const button = document.getElementById(
            "themeToggle"
        );

        const icon = document.getElementById(
            "themeToggleIcon"
        );

        const label = document.getElementById(
            "themeToggleLabel"
        );

        if (!button || !icon || !label) {
            return;
        }

        const isDark = theme === "dark";

        const actionLabel = isDark
            ? "Ativar tema claro"
            : "Ativar tema escuro";

        icon.textContent = isDark ? "☀" : "☾";
        label.textContent = actionLabel;

        button.setAttribute(
            "aria-label",
            actionLabel
        );

        button.setAttribute(
            "title",
            actionLabel
        );

        button.setAttribute(
            "aria-pressed",
            String(!isDark)
        );
    };

    const syncPlotlyTheme = () => {
        if (!window.Plotly) {
            return;
        }

        const textColor = getCssVariable(
            "--color-text"
        );

        const mutedColor = getCssVariable(
            "--color-text-muted"
        );

        const gridColor = getCssVariable(
            "--color-chart-grid"
        );

        const hoverBackground = getCssVariable(
            "--color-chart-hover-bg"
        );

        const hoverText = getCssVariable(
            "--color-chart-hover-text"
        );

        document
            .querySelectorAll(".plotly-graph-div")
            .forEach((graph) => {
                window.Plotly.relayout(
                    graph,
                    {
                        paper_bgcolor: "rgba(0,0,0,0)",
                        plot_bgcolor: "rgba(0,0,0,0)",

                        "font.color": textColor,
                        "title.font.color": textColor,
                        "legend.font.color": textColor,

                        "xaxis.color": textColor,
                        "yaxis.color": textColor,

                        "xaxis.title.font.color": textColor,
                        "yaxis.title.font.color": textColor,

                        "xaxis.gridcolor": gridColor,
                        "yaxis.gridcolor": gridColor,

                        "xaxis.zerolinecolor": gridColor,
                        "yaxis.zerolinecolor": gridColor,

                        "xaxis.tickfont.color": mutedColor,
                        "yaxis.tickfont.color": mutedColor,

                        "hoverlabel.bgcolor": hoverBackground,
                        "hoverlabel.font.color": hoverText,
                    }
                );
            });
    };

    const applyTheme = (
        theme,
        {
            persist = false,
        } = {}
    ) => {
        root.dataset.theme = theme;

        root.setAttribute(
            "data-bs-theme",
            theme
        );

        root.style.colorScheme = theme;

        if (persist) {
            persistTheme(theme);
        }

        updateToggle(theme);

        window.requestAnimationFrame(() => {
            syncPlotlyTheme();
        });
    };

    const toggleTheme = () => {
        const currentTheme = (
            root.dataset.theme === "light"
                ? "light"
                : "dark"
        );

        const nextTheme = (
            currentTheme === "dark"
                ? "light"
                : "dark"
        );

        applyTheme(
            nextTheme,
            {
                persist: true,
            }
        );
    };

    const handleSystemThemeChange = (event) => {
        if (getStoredTheme() !== null) {
            return;
        }

        applyTheme(
            event.matches
                ? "light"
                : "dark"
        );
    };

    const initialize = () => {
        const button = document.getElementById(
            "themeToggle"
        );

        const currentTheme = (
            root.dataset.theme === "light"
                ? "light"
                : "dark"
        );

        updateToggle(currentTheme);

        if (button) {
            button.addEventListener(
                "click",
                toggleTheme
            );
        }

        mediaQuery.addEventListener(
            "change",
            handleSystemThemeChange
        );

        syncPlotlyTheme();

        window.setTimeout(
            syncPlotlyTheme,
            100
        );
    };

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initialize,
            {
                once: true,
            }
        );
    } else {
        initialize();
    }
})();
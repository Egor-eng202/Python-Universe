(function () {
    function applyTheme() {
        if (localStorage.getItem("pu_theme") === "dark") {
            document.body.classList.add("dark");
        }
    }

    if (document.body) {
        applyTheme();
    } else {
        document.addEventListener("DOMContentLoaded", applyTheme);
    }

    document.addEventListener("DOMContentLoaded", function () {
        const nav = document.querySelector("nav");
        if (!nav) return;

        const btn = document.createElement("button");
        btn.id = "theme-toggle";
        btn.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
        nav.appendChild(btn);

        btn.addEventListener("click", function () {
            document.body.classList.toggle("dark");
            const isDark = document.body.classList.contains("dark");
            localStorage.setItem("pu_theme", isDark ? "dark" : "light");
            btn.textContent = isDark ? "☀️" : "🌙";
        });
    });
})();
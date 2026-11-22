document.addEventListener("DOMContentLoaded", async function () {
    const TOTAL_LESSONS = 25;

    const me = await Auth.me();
    const navUser = document.getElementById("nav-user");
    if (navUser && me.logged_in) navUser.textContent = " | " + me.username;

    const match = window.location.pathname.match(/^\/lesson(\d+)$/);

    if (!match) return; 

    const current = parseInt(match[1], 10);

    if (me.logged_in) {
        await Auth.markLessonDone("lesson" + current);
    }

    const nav = document.createElement("div");
    nav.style.marginTop = "30px";

    if (current > 1) {
        const prev = document.createElement("a");
        prev.href = "/lesson" + (current - 1);
        prev.innerHTML = "<button>← Предыдущий урок</button>";
        nav.appendChild(prev);
    }

    if (current < TOTAL_LESSONS) {
        const next = document.createElement("a");
        next.href = "/lesson" + (current + 1);
        next.innerHTML = "<button>Следующий урок →</button>";
        next.style.marginLeft = "10px";
        nav.appendChild(next);
    } else {
        const back = document.createElement("a");
        back.href = "/lessons";
        back.innerHTML = "<button>Вернуться к списку уроков</button>";
        back.style.marginLeft = "10px";
        nav.appendChild(back);
    }

    const footer = document.querySelector("footer");
    if (footer) {
        footer.parentNode.insertBefore(nav, footer);
    } else {
        document.body.appendChild(nav);
    }
});
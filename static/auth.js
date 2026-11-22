const Auth = {
    async me() { return await (await fetch("/api/me")).json(); },
    async register(u, p) {
        return await (await fetch("/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username: u, password: p }) })).json();
    },
    async login(u, p) {
        return await (await fetch("/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username: u, password: p }) })).json();
    },
    async logout() { return await (await fetch("/logout", { method: "POST" })).json(); },
    async getProgress() {
        const r = await fetch("/api/progress");
        return r.ok ? await r.json() : [];
    },
    async markLessonDone(lesson) {
        await fetch("/api/progress", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lesson }) });
    },
};

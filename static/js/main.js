async function loadLanguage(lang) {
    try {
        const response = await fetch(`/static/lang/${lang}.json`, { cache: "no-store" });
        const translations = await response.json();
        document.querySelectorAll("[data-translate]").forEach(el => {
            const key = el.getAttribute("data-translate");
            if (translations[key]) {
                el.textContent = translations[key];
            }
        });
        document.querySelectorAll(".lang-btn").forEach(btn => {
            btn.classList.toggle("bg-blue-500", btn.dataset.lang === lang);
            btn.classList.toggle("text-white", btn.dataset.lang === lang);
        });
        localStorage.setItem("lang", lang);
    } catch (e) {
        console.error("Error loading language:", e);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const currentLang = localStorage.getItem("lang") || "ro";
    loadLanguage(currentLang);

    document.querySelectorAll(".lang-btn").forEach(btn =>
        btn.addEventListener("click", () => loadLanguage(btn.dataset.lang))
    );

    const hamburger = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobileMenu");
    hamburger.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
    });

    document.getElementById("cfFetch").addEventListener("click", async () => {
        const handle = document.getElementById("cfHandle").value;
        if (!handle) return;
        const res = await fetch(`/api/codeforces/${handle}`);
        document.getElementById("cfOutput").textContent = JSON.stringify(await res.json(), null, 2);
    });

    document.getElementById("ghFetch").addEventListener("click", async () => {
        const user = document.getElementById("ghUser").value;
        if (!user) return;
        const res = await fetch(`/api/github/${user}`);
        document.getElementById("ghOutput").textContent = JSON.stringify(await res.json(), null, 2);
    });
});

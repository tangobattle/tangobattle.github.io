let LANG;

function initLangSelector(languages) {
    function createLangStyle() {
        const style = document.createElement("style");
        style.textContent = "[lang][data-localize] { display: none; }";
        return style;
    }

    const langStyle = createLangStyle();
    document.head.appendChild(langStyle);

    function setLanguage(lang) {
        LANG = lang;
        langStyle.textContent =
            "[lang][data-localize]:not([lang=" + lang + "]) { display: none; }";
        document.documentElement.lang = lang;
        window.localStorage.setItem("lang", lang);
    }

    setLanguage(
        (() => {
            let currentLanguage = null;

            // 1. Check querystring language.
            if (!currentLanguage) {
                currentLanguage = new URLSearchParams(
                    window.location.search
                ).get("lang");
            }

            // 2. Check remembered language.
            if (!currentLanguage) {
                currentLanguage = window.localStorage.getItem("lang");
            }

            // 3. Check navigator language.
            if (!currentLanguage) {
                currentLanguage = navigator.language.split(/-/)[0];
            }

            currentLanguage = currentLanguage || languages[0].code;
            if (languages.findIndex((l) => l.code == currentLanguage) == -1) {
                currentLanguage = languages[0].code;
            }

            return currentLanguage;
        })()
    );
}

initLangSelector([
    { code: "en", name: "en" },
    { code: "ja", name: "日本語" },
]);

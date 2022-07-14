function initLangSelector(languages) {
    let LANG;

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
                currentLanguage = navigator.language;
            }

            let locale = null;
            try {
                locale = new Intl.Locale(
                    currentLanguage || languages[0]
                ).maximize();
            } catch (e) {
                currentLanguage = languages[0];
            }

            if (locale != null) {
                currentLanguage = languages.find((lang) =>
                    locale.baseName.startsWith(lang)
                );
            }

            if (currentLanguage == null) {
                currentLanguage = languages[0];
            }

            return currentLanguage;
        })()
    );
}

initLangSelector(["en", "ja", "zh-Hans", "es"]);

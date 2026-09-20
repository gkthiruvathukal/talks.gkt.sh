/*
 * Shared light/dark theme toggle for talks.gkt.sh and every talk under it.
 * Stores the explicit choice in localStorage under "gkt-theme" ("light" | "dark").
 * Since every talk is served from the same origin, picking a theme on the
 * landing page or inside any deck applies everywhere else too.
 * With no explicit choice, the OS-level prefers-color-scheme is used instead.
 */
(function () {
	var KEY = "gkt-theme";
	var root = document.documentElement;

	function stored() {
		try { return localStorage.getItem(KEY); } catch (e) { return null; }
	}

	function apply(theme) {
		if (theme === "light" || theme === "dark") {
			root.setAttribute("data-theme", theme);
		} else {
			root.removeAttribute("data-theme");
		}
	}

	// Applied immediately (script is loaded early, before body renders) to avoid a flash.
	apply(stored());

	function effective() {
		var explicit = root.getAttribute("data-theme");
		if (explicit) return explicit;
		return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
	}

	function resync() {
		if (window.Reveal && typeof window.Reveal.sync === "function") {
			window.Reveal.sync();
		}
	}

	function mount() {
		var btn = document.createElement("button");
		btn.type = "button";
		btn.className = "gkt-theme-toggle";
		btn.setAttribute("aria-label", "Toggle color theme");

		function sync() {
			var eff = effective();
			btn.textContent = eff === "dark" ? "☀" : "☽";
			btn.title = eff === "dark" ? "Switch to light mode" : "Switch to dark mode";
		}
		sync();

		btn.addEventListener("click", function () {
			var next = effective() === "dark" ? "light" : "dark";
			apply(next);
			try { localStorage.setItem(KEY, next); } catch (e) {}
			sync();
			resync();
		});

		document.body.appendChild(btn);

		window.addEventListener("storage", function (e) {
			if (e.key === KEY) {
				apply(e.newValue);
				sync();
				resync();
			}
		});
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", mount);
	} else {
		mount();
	}
})();

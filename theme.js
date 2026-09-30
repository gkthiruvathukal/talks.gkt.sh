/*
 * Shared light/dark theme toggle for talks.gkt.sh and every talk under it.
 * Stores the explicit choice in localStorage under "gkt-theme" ("light" | "dark").
 * Since every talk is served from the same origin, picking a theme on the
 * landing page or inside any deck applies everywhere else too.
 *
 * OS-level prefers-color-scheme is deliberately ignored (mobile browsers were
 * inconsistent about honoring it, notably iOS Safari and Edge on the deck):
 * the toggle is the only source of truth, and the default with no explicit
 * choice yet is "dark".
 */
(function () {
	var KEY = "gkt-theme";
	var DEFAULT = "dark";
	var root = document.documentElement;

	function stored() {
		try {
			var v = localStorage.getItem(KEY);
			return (v === "light" || v === "dark") ? v : null;
		} catch (e) { return null; }
	}

	function apply(theme) {
		root.setAttribute("data-theme", theme === "light" ? "light" : "dark");
	}

	// Applied immediately (script is loaded early, before body renders) to avoid a flash.
	apply(stored() || DEFAULT);

	function effective() {
		return root.getAttribute("data-theme") === "light" ? "light" : "dark";
	}

	// WebKit (iOS Safari, and iOS Edge which is WebKit under the hood too) has
	// been seen picking up `color-scheme` on a toggled [data-theme] attribute
	// immediately (native chrome recolors) while failing to repaint elements
	// whose background/color come from the custom properties that same
	// attribute change cascades — notably reveal.js's slide canvas, which
	// sits inside a transformed/contained subtree. A synchronous
	// display:none/reflow/restore forces a full repaint of the whole page as
	// a blunt but reliable workaround; it happens within one JS task, before
	// the browser's next paint, so nothing actually flashes on screen.
	function forceRepaint() {
		var body = document.body;
		var prevDisplay = body.style.display;
		body.style.display = "none";
		void body.offsetHeight;
		body.style.display = prevDisplay;
	}

	function resync() {
		if (window.Reveal && typeof window.Reveal.sync === "function") {
			window.Reveal.sync();
		}
		forceRepaint();
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
				apply(e.newValue === "light" ? "light" : DEFAULT);
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

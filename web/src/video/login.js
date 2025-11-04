let AUTH_PASSWORD = "";
const COOKIE_NAME = "video_auth";
const COOKIE_EXPIRY_DAYS = 7;

const setCookie = (name, value, days) => {
	const date = new Date();
	date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
	document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
};

const getCookie = (name) => {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(";").shift();
	return null;
};

document.addEventListener("DOMContentLoaded", async () => {
	try {
		const response = await fetch("/api/config");
		const config = await response.json();
		AUTH_PASSWORD = config.password;
	} catch (error) {
		console.error("Failed to load config:", error);
	}

	if (getCookie(COOKIE_NAME) === "true") {
		window.location.href = "/video/index.html";
		return;
	}

	document.getElementById("auth-form").addEventListener("submit", (e) => {
		e.preventDefault();
		const password = document.getElementById("password").value;
		const errorMessage = document.getElementById("error-message");

		if (password === AUTH_PASSWORD) {
			setCookie(COOKIE_NAME, "true", COOKIE_EXPIRY_DAYS);
			errorMessage.classList.add("hidden");
			window.location.href = "/video/index.html";
		} else {
			errorMessage.classList.remove("hidden");
		}
	});
});

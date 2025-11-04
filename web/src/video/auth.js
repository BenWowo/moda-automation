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

const deleteCookie = (name) => {
	document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
};

const checkAuth = () => {
	return getCookie(COOKIE_NAME) === "true";
};

const showVideo = () => {
	document.getElementById("auth-container").classList.add("hidden");
	document.getElementById("video-container").classList.remove("hidden");
};

const showAuth = () => {
	document.getElementById("auth-container").classList.remove("hidden");
	document.getElementById("video-container").classList.add("hidden");
};

document.addEventListener("DOMContentLoaded", async () => {
	try {
		const response = await fetch("/api/config");
		const config = await response.json();
		AUTH_PASSWORD = config.password;
	} catch (error) {
		console.error("Failed to load config:", error);
	}

	if (checkAuth()) {
		showVideo();
	}

	document.getElementById("auth-form").addEventListener("submit", (e) => {
		e.preventDefault();
		const password = document.getElementById("password").value;
		const errorMessage = document.getElementById("error-message");

		if (password === AUTH_PASSWORD) {
			setCookie(COOKIE_NAME, "true", COOKIE_EXPIRY_DAYS);
			errorMessage.classList.add("hidden");
			showVideo();
		} else {
			errorMessage.classList.remove("hidden");
		}
	});

	document.getElementById("logout-btn").addEventListener("click", () => {
		deleteCookie(COOKIE_NAME);
		showAuth();
		document.getElementById("password").value = "";
	});
});

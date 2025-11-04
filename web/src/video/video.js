const COOKIE_NAME = "video_auth";

const getCookie = (name) => {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(";").shift();
	return null;
};

const deleteCookie = (name) => {
	document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
};

document.addEventListener("DOMContentLoaded", () => {
	if (getCookie(COOKIE_NAME) !== "true") {
		window.location.href = "/video/login.html";
		return;
	}

	document.getElementById("logout-btn").addEventListener("click", () => {
		deleteCookie(COOKIE_NAME);
		window.location.href = "/video/login.html";
	});
});

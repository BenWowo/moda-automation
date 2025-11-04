class CookieStore {
	constructor() {
		this.COOKIE_NAME = "video_auth";
		this.COOKIE_EXPIRY_DAYS = 7;
	}

	setCookie(name, value, days) {
		const date = new Date();
		date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
		document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
	}

	getCookie(name) {
		const value = `; ${document.cookie}`;
		const parts = value.split(`; ${name}=`);
		if (parts.length === 2) return parts.pop().split(";").shift();
		return null;
	}

	deleteCookie(name) {
		document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
	}

	// Convenience methods for auth cookie
	setAuthCookie(value = "yummy") {
		this.setCookie(this.COOKIE_NAME, value, this.COOKIE_EXPIRY_DAYS);
	}

	getAuthCookie() {
		return this.getCookie(this.COOKIE_NAME);
	}

	deleteAuthCookie() {
		this.deleteCookie(this.COOKIE_NAME);
	}

	checkAuth() {
		return this.getAuthCookie() === "yummy";
	}
}

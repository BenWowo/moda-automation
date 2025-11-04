document.addEventListener("DOMContentLoaded", function () {
	const cookieStore = new CookieStore();
	const logoutButton = document.getElementById("logout-btn");

	const redirectToLogin = () => {
		window.location.href = "login.html";
	};

	const handleLogout = () => {
		console.log("Logging out user...");
		cookieStore.deleteAuthCookie();
		redirectToLogin();
	};

	if (!cookieStore.checkAuth()) {
		console.log("User not authenticated, redirecting to login page...");
		redirectToLogin();
		return;
	}

	console.log("User authenticated, access granted to video content");

	if (logoutButton) {
		logoutButton.addEventListener("click", handleLogout);
	}
});

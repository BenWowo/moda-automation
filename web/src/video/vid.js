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

	// Check authentication on page load
	if (!cookieStore.checkAuth()) {
		console.log("User not authenticated, redirecting to login page...");
		redirectToLogin();
		return; // Stop further execution if not authenticated
	}

	console.log("User authenticated, access granted to video content");

	// Add logout functionality
	if (logoutButton) {
		logoutButton.addEventListener("click", handleLogout);
	}
});

document.addEventListener("DOMContentLoaded", function () {
	const cookieStore = new CookieStore();
	const form = document.querySelector("form");
	const passwordInput = document.getElementById("password");
	const submitButton = document.getElementById("submit");
	const errorMessage = document.getElementById("wrong password message");
	const CORRECT_PASSWORD = "daniel";

	const showErrorMessage = () => {
		errorMessage.classList.remove("invisible");
	};

	const hideErrorMessage = () => {
		errorMessage.classList.add("invisible");
	};

	const redirectToVideo = () => {
		window.location.href = "vid.html";
	};

	const handleFormSubmission = (event) => {
		event.preventDefault();
		const enteredPassword = passwordInput.value;
		if (enteredPassword === CORRECT_PASSWORD) {
			hideErrorMessage();
			cookieStore.setAuthCookie("yummy");
			console.log("Login successful! Redirecting to video page...");
			redirectToVideo();
		} else {
			showErrorMessage();
			passwordInput.value = "";
			passwordInput.focus();
		}
	};

	if (cookieStore.checkAuth()) {
		console.log("User already authenticated, redirecting to video page...");
		redirectToVideo();
	}

	passwordInput.addEventListener("input", function () {
		hideErrorMessage();
	});

	form.addEventListener("submit", handleFormSubmission);
	submitButton.addEventListener("click", handleFormSubmission);
});

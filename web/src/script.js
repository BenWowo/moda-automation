document.addEventListener("DOMContentLoaded", function () {
	const form = document.querySelector("form");
	const STORAGE_KEY = "modaFormData";

	const modalRequest = async (url, method = "GET", body = null) => {
		try {
			return await fetch(url, {
				method: method,
				headers: {
					"Content-Type": "application/json",
				},
				body: body ?? null,
			});
		} catch (error) {
			console.error("Error in modalRequest:", error);
		}
	};

	const uploadConfigToModal = async (config) => {
		await modalRequest(
			"https://benwowo--moda-automation-update-config.modal.run/",
			"POST",
			config
		);
	};

	const getModaPermit = async (config) => {
		await modalRequest(
			"https://benwowo--moda-automation-get-moda-permit-webhook.modal.run/",
			"POST",
			config
		);
	};

	const loadFormData = () => {
		try {
			const savedData = localStorage.getItem(STORAGE_KEY);
			if (savedData) {
				const formValues = JSON.parse(savedData);
				Object.keys(formValues).forEach((key) => {
					const element = document.getElementById(key);
					if (element && formValues[key]) {
						element.value = formValues[key];
					}
				});
				console.log("Form data loaded from localStorage");
			}
		} catch (error) {
			console.error("Error loading form data:", error);
		}
	};

	const saveFormData = () => {
		try {
			const formData = new FormData(form);
			const formValues = Object.fromEntries(formData);
			localStorage.setItem(STORAGE_KEY, JSON.stringify(formValues));
		} catch (error) {
			console.error("Error saving form data:", error);
		}
	};

	const clearFormData = () => {
		localStorage.removeItem(STORAGE_KEY);
		console.log("Form data cleared from localStorage");
	};

	const clearValidationError = (field) => {
		field.style.borderColor = "";
	};

	const handleFormSubmission = (event, isRecurring = false) => {
		event.preventDefault();
		const formData = new FormData(form);
		const formValues = Object.fromEntries(formData);
		const requiredFields = form.querySelectorAll("[required]");
		let isValid = true;
		requiredFields.forEach((field) => {
			if (!field.value.trim()) {
				field.style.borderColor = "red";
				isValid = false;
			} else {
				field.style.borderColor = "";
			}
		});

		if (!isValid) {
			return;
		}

		const config = JSON.stringify(formValues);
		if (isRecurring) {
			uploadConfigToModal(config);
		}
		getModaPermit(config);

		const successMessage = document.getElementById("successMessage");
		successMessage.classList.remove("invisible");

		// Clear form data from localStorage after successful submission
		const rememberCheckbox = document.getElementById("remember-me");
		if (!rememberCheckbox.checked) {
			clearFormData();
			form.reset();
		}
	};

	loadFormData();

	const formInputs = form.querySelectorAll("input, select");
	formInputs.forEach((input) => {
		input.addEventListener("input", function () {
			saveFormData();
			clearValidationError(this);
		});

		input.addEventListener("change", function () {
			saveFormData();
			clearValidationError(this);
		});
	});

	document
		.getElementById("oneTimeSubmit")
		.addEventListener("click", (event) => {
			handleFormSubmission(event, false);
		});

	document
		.getElementById("recurringSubmit")
		.addEventListener("click", (event) => {
			handleFormSubmission(event, true);
		});
});

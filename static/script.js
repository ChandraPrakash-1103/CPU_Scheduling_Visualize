(() => {
    "use strict";

    const algorithmSelect = document.getElementById("algorithm");
    const quantumField = document.getElementById("quantum-field");
    const quantumInput = document.getElementById("quantum");
    const priorityFields = document.querySelectorAll(".priority-field");
    const priorityInputs = document.querySelectorAll('input[name="priority"]');
    const processCountSelect = document.getElementById("process_count");
    const form = document.getElementById("scheduler-form");

    function updateAlgorithmFields() {
        if (!algorithmSelect) return;

        const isRoundRobin = algorithmSelect.value === "RR";
        const isPriority = algorithmSelect.value === "Priority";

        if (quantumField) quantumField.style.display = isRoundRobin ? "block" : "none";
        if (quantumInput) {
            quantumInput.required = isRoundRobin;
            quantumInput.disabled = !isRoundRobin;
        }

        priorityFields.forEach((field) => {
            field.style.display = isPriority ? "block" : "none";
        });

        priorityInputs.forEach((input) => {
            input.required = isPriority;
            input.disabled = !isPriority;
        });
    }

    if (algorithmSelect) {
        algorithmSelect.addEventListener("change", updateAlgorithmFields);
        updateAlgorithmFields();
    }

    // Preserve the Flask POST workflow: changing the count submits action=update.
    if (processCountSelect && form) {
        processCountSelect.addEventListener("change", () => {
            const updateButton = form.querySelector('button[name="action"][value="update"]');
            if (updateButton) updateButton.click();
        });
    }

    // Highlight the selected sidebar destination; this does not affect scheduling.
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            navLinks.forEach((item) => item.classList.remove("active"));
            link.classList.add("active");
        });
    });
})();

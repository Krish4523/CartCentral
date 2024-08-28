function loadScript() {
    let toggle = false;
    let changedData = {};

    for (let field of document.getElementsByClassName("input-field")) {
        field.addEventListener("change", () => {
            changedData[field.getAttribute("name")] = field.value;
        });
    }

    document.getElementById("saveBtn").addEventListener("click", async () => {
        const res = await fetch("/customer/changedata", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({changedData}),
        });
        if (res.ok) {
            document.getElementById("success").classList.remove("d-none");
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        }
    });

    document.getElementById("editBtn").addEventListener("click", () => {
        const inputFields = document.getElementsByClassName("input-field");
        for (let input of inputFields) {
            if (!toggle) {
                input.removeAttribute("disabled");
                input.removeAttribute("readonly");
                document.getElementById("editBtn").classList.add("active");
                document.getElementById("saveBtn").classList.remove("disabled");
            } else {
                input.disabled = true;
                input.readonly = true;
                document.getElementById("changeWarning").classList.add("d-none");
                document.getElementById("editBtn").classList.remove("active");
                document.getElementById("saveBtn").classList.add("disabled");
            }
        }
        toggle = !toggle;
    });

    let usernameField = document.getElementById("username");
    let emailField = document.getElementById("email");
    let currPassword = document.getElementById("currPassword");
    let password = document.getElementById("password");
    // usernameField.addEventListener("input", async () => {
    // 	console.log(usernameField.value)

    // });
    let inputFields = document.querySelectorAll(".validation");
    inputFields.forEach(async (input) => {
        input.addEventListener('input', async () => {
            let data = await fetch("/profile/check", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify({
                    username: usernameField.value,
                    email: emailField.value,
                    currPassword: currPassword.value,
                    password: currPassword.value,
                }),
            });

            data = await data.json();
            console.log(data["hasUsername"], data["hasEmail"], data["hasPassword"], data["validPassword"])
            if (!(data["hasUsername"] && data["hasEmail"] && data["hasPassword"] && data["validPassword"])) {
                document.getElementById("changeWarning").classList.add("d-none");
                document.getElementById("saveBtn").classList.remove("disabled");
            }
            if (data["hasUsername"]) {
                document.getElementById("changeWarning").classList.remove("d-none");
                document.getElementById("saveBtn").classList.add("disabled");
            }

            if (data["hasEmail"]) {
                document.getElementById("changeWarning").classList.remove("d-none");
                document.getElementById("saveBtn").classList.add("disabled");
            }

        });
    });


}

loadScript();
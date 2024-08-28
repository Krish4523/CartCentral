let hasUsername = false,
    hasPassword = false;

let usernameField = document.getElementById("username");
usernameField.addEventListener("input", async () => {
    let data = await fetch("/login/admin/check", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({username: usernameField.value}),
    });

    data = await data.json();
    if (!data["hasUser"]) {
        hasUsername = false;
        document.getElementById("warning").classList.remove("d-none");
    } else {
        hasUsername = true;
        document.getElementById("warning").classList.add("d-none");
    }

    if (hasPassword && hasUsername) {
        document.getElementById("loginBtn").classList.remove("disabled");
    } else {
        document.getElementById("loginBtn").classList.add("disabled");
    }
});

let passwordField = document.getElementById("password");
passwordField.addEventListener("input", async () => {
    let data = await fetch("/login/admin/check", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            username: usernameField.value,
            password: passwordField.value,
        }),
    });

    data = await data.json();
    if (!data["hasUser"]) {
        hasPassword = false;
        document.getElementById("warning").classList.remove("d-none");
    } else {
        hasPassword = true;
        document.getElementById("warning").classList.add("d-none");
    }

    if (hasPassword && hasUsername) {
        document.getElementById("loginBtn").classList.remove("disabled");
    } else {
        document.getElementById("loginBtn").classList.add("disabled");
    }
});

const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".main__container");
const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");

sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});
sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});

sign_up_btn2.addEventListener("click", () => {
    container.classList.add("sign-up-mode2");
});
sign_in_btn2.addEventListener("click", () => {
    container.classList.remove("sign-up-mode2");
});

let usernameField = document.getElementById("signupUsername");
usernameField.addEventListener("input", async () => {
    let data = await fetch("/register/customer/check", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            username: usernameField.value,
            email: emailField.value,
        }),
    });

    data = await data.json();
    if (!(data["hasUsername"] && data["hasEmail"])) {
        document.getElementById("signupWarning").classList.add("d-none");
        document.getElementById("sign-up-btn1").classList.remove("disabled");
    }
    if (data["hasUsername"]) {
        document.getElementById("signupWarning").classList.remove("d-none");
        document.getElementById("sign-up-btn1").classList.add("disabled");
    }

    if (data["hasEmail"]) {
        document.getElementById("signupWarning").classList.remove("d-none");
        document.getElementById("sign-up-btn1").classList.add("disabled");
    }
});

let emailField = document.getElementById("signupEmail");
emailField.addEventListener("input", async () => {
    let data = await fetch("/register/customer/check", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            username: usernameField.value,
            email: emailField.value,
        }),
    });

    data = await data.json();
    if (!(data["hasUsername"] && data["hasEmail"])) {
        document.getElementById("signupWarning").classList.add("d-none");
        document.getElementById("sign-up-btn1").classList.remove("disabled");
    }
    if (data["hasUsername"]) {
        document.getElementById("signupWarning").classList.remove("d-none");
        document.getElementById("sign-up-btn1").classList.add("disabled");
    }

    if (data["hasEmail"]) {
        document.getElementById("signupWarning").classList.remove("d-none");
        document.getElementById("sign-up-btn1").classList.add("disabled");
    }
});

// Login

let hasPassword = false;
hasUsername = false;

let loginUsernameField = document.getElementById("loginUsername");
loginUsernameField.addEventListener("input", async () => {
    let data = await fetch("/login/customer/check", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({username: loginUsernameField.value}),
    });

    data = await data.json();
    if (!data["hasUser"]) {
        hasUsername = false;
        document.getElementById("loginWarning").classList.remove("d-none");
    } else {
        hasUsername = true;
        document.getElementById("loginWarning").classList.add("d-none");
    }

    if (hasPassword && hasUsername) {
        document.getElementById("loginBtn").classList.remove("disabled");
    } else {
        document.getElementById("loginBtn").classList.add("disabled");
    }
});

let passwordField = document.getElementById("loginPasssword");
passwordField.addEventListener("input", async () => {
    let data = await fetch("/login/customer/check", {
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
        document.getElementById("loginWarning").classList.remove("d-none");
    } else {
        hasPassword = true;
        document.getElementById("loginWarning").classList.add("d-none");
    }

    if (hasPassword && hasUsername) {
        document.getElementById("loginBtn").classList.remove("disabled");
    } else {
        document.getElementById("loginBtn").classList.add("disabled");
    }
});

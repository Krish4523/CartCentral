let dataArea = document.getElementById("dataArea");

function setActive(button) {
    let buttons = document.getElementsByClassName("buttons");
    for (let button of buttons) {
        button.classList.remove("active");
    }
    button.classList.add("active");
}

async function getOrdersData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/customer/orders")
    data = await data.json();
    let script = document.createElement("script");
    dataArea.innerHTML = data["template"];
    script.src = data["jsUrl"];
    dataArea.appendChild(script);
}

async function getProfileData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/customer/profile");
    data = await data.json();
    let script = document.createElement("script");
    script.src = data["jsUrl"];
    dataArea.innerHTML = data["template"];
    dataArea.appendChild(script);
}

async function getCartData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/customer/cart");
    data = await data.json();
    let script = document.createElement("script");
    script.src = data["jsUrl"];
    dataArea.innerHTML = data["template"];
    dataArea.appendChild(script);
}

async function getProductData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/customer/home_products");
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}

getProductData(document.getElementById("prof")).then(() => {});
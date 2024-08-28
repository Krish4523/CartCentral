let dataArea = document.getElementById("dataArea");

function setActive(button) {
    let buttons = document.getElementsByClassName("buttons");
    for (let button of buttons) {
        button.classList.remove("active");
    }
    button.classList.add("active");
}

async function getProductsData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/merchant/product-list");
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}

async function getProfileData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/merchant/profile");
    data = await data.json();
    let script = document.createElement("script");
    script.src = data["jsUrl"];
    dataArea.innerHTML = data["template"];
    dataArea.appendChild(script);
}

async function getProducts() {
    let data = await fetch("/merchant/product-list");
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}

async function addProductData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/merchant/add-product");
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}

async function getSalesData(currentButton) {
    setActive(currentButton);
    let data = await fetch("/merchant/sales");
    data = await data.json();
    let script = document.createElement("script");
    script.src = data["jsUrl"];
    dataArea.innerHTML = data["template"];
    dataArea.appendChild(script);
}

getSalesData(document.getElementById("prof"));
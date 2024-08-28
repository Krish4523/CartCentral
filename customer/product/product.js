async function addToCart(button) {
    const productId = button.getAttribute("data-product-id");
    console.log("Add to Cart clicked for productList ID:", productId);
    console.log("/addCart/" + productId)
    let data = await fetch("/addCart/" + productId);
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}

// Define a function to handle immediate purchase
async function buyNow(button) {
    var productId = button.getAttribute('data-product-id');
    console.log('Immediate purchase initiated for product: ' + productId);
    let data = await fetch("/buynow/" + productId);
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}


async function productPage(element) {
  const productId = parseInt(element.getAttribute("data-product-id"));
  let data = await fetch("/products/" + productId);
  data = await data.json();
  dataArea.innerHTML = data["template"];
  let script = document.createElement("script");
  script.src = data["jsUrl"]
  dataArea.appendChild(script);
}

async function cancel(button) {
  const orderId = button.getAttribute("data-order-id");
  let confirm = await fetch("/cancel/" + orderId);
  confirm = confirm.text();
  if (Boolean(confirm)) {
    let order = document.getElementById(orderId);
    order.parentElement.removeChild(order);
  } else {
    alert("Error");
  }
}

async function buynow(button) {
  const productId = button.getAttribute("data-product-id");
  console.log("Buy Now clicked for productList ID:", productId);
  let data = await fetch("/buynow/" + productId);
  data = await data.json();
  dataArea.innerHTML = data["template"];
  let script = document.createElement("script");
  script.src = data["jsUrl"]
  dataArea.appendChild(script);
}
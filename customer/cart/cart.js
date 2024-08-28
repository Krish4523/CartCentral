function handleUpdateQuantity(card) {
  const plusBtn = card.querySelector(".cardButtons:nth-child(3)");
  const minusBtn = card.querySelector(".cardButtons:nth-child(1)");
  const quantitySpan = card.querySelector(".cart-item span");

  let quantity = parseInt(quantitySpan.textContent);

  const updateQuantity = async (newQuantity) => {
    quantity = newQuantity;
    quantitySpan.textContent = quantity;
    minusBtn.disabled = quantity === 1;
    const productId = card.getAttribute("data-product-id");
    await fetch("/updateCartQuantity", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        productId: productId,
        quantity: quantity,
      }),
    });
  };

  plusBtn.addEventListener("click", async () => {
    await updateQuantity(quantity + 1);
  });

  minusBtn.addEventListener("click", async () => {
    if (quantity > 1) {
      await updateQuantity(quantity - 1);
    }
  });
}


function card() {
  let cards = document.querySelectorAll(".cart-products .card");
  cards.forEach((card) => {
    handleUpdateQuantity(card);
    // card.querySelector(".cart-btn").addEventListener("click", () => {
    //   console.log(this)
    //   removeFromCart(this);
    // });
  });
}

async function removeFromCart(button) {
  try {
    let productId = button.getAttribute("data-product-id");
    console.log(productId);
    const response = await fetch("/removeCart/" + productId, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (response.ok) {
      let productCard = button.closest(".card");
      productCard.parentNode.removeChild(productCard);
    } else {
      console.error('Failed to remove product from cart');
    }
  } catch (error) {
    console.error('Error while removing product from cart:', error);
  }
}


async function buyNow(button) {
  console.log(button)
  const productId = button.getAttribute("data-product-id");
  console.log("Buy Now clicked for productList ID:", productId);
  let data = await fetch("/buynow/" + productId);
  data = await data.json();
  dataArea.innerHTML = data["template"];
  let script = document.createElement("script");
  script.src = data["jsUrl"]
  dataArea.appendChild(script);
}

card()
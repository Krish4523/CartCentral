function load() {
  const selectMM = document.getElementById("expiryMonth");
  for (let i = 1; i <= 12; i++) {
    let mm = i.toString().padStart(2, "0");
    selectMM.innerHTML += `<option value="${mm}">${mm}</option>`;
  }

  const selectYY = document.getElementById("expiryYear");
  let yy = new Date().getFullYear();
  for (let i = 0; i < 20; i++, yy++) {
    selectYY.innerHTML += `
			<option value="${yy}">${yy.toString().substring(2, 4)}</option>
		`;
  }
  const cashForm = document.getElementById("cashForm");
  const upiForm = document.getElementById("upiForm");
  const creditForm = document.getElementById("creditForm");
  cashForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const product_id = cashForm.getAttribute("data-product-id");
    const formData = {paymentMethod: 'cash'};
    await sendOrderData('cash', product_id, formData);
  });

  // Event listener for UPI payment form
  upiForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const product_id = upiForm.getAttribute("data-product-id");
    const input = document.getElementById("upiID");
    const formData = {
      paymentMethod: 'upi',
      upiID: input.value
    };
    await sendOrderData('upi', product_id, formData);
  });

  // Event listener for credit card payment form
  creditForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const product_id = creditForm.getAttribute("data-product-id");
    const formData = {paymentMethod: 'credit_card'};
    const inputs = creditForm.querySelectorAll("input");
    const selects = creditForm.querySelectorAll("select");
    inputs.forEach((input) => {
      formData[input.name] = input.value;
    });
    selects.forEach((select) => {
      formData[select.name] = select.value;
    });
    await sendOrderData('credit_card', product_id, formData);
  });

}

function filterInput(cvv) {
  cvv.value = cvv.value.replace(/\D/g, "").substring(0, 3);
}

async function sendOrderData(paymentMethod, productID, formData) {
  const price = parseFloat(document.getElementById("price").innerHTML);
  const quantity = parseInt(document.getElementById("quantity").innerHTML);
  console.log(price, quantity);
  const address = document.getElementById('address').innerHTML;
  const data = {
    paymentMethod: paymentMethod,
    productID: productID,
    formData: {
      ...formData,
      price: price,
      quantity: quantity,
      delivery_address: address
    }
  };
  console.log(data)
  try {
    let orderData = await fetch('/payment/order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    let order = await orderData.json();
    console.log(order)
    let resultDiv = document.querySelector('#paymentWarning');
    resultDiv.classList.remove("d-none");
    resultDiv.innerHTML = order.message;
    if (order.success) {
      resultDiv.classList.add("text-success");
    } else {
      resultDiv.classList.add("text-danger");
    }
    setTimeout(() => {
      window.location.reload();
    }, 2000);

  } catch (error) {
    console.log(error);
  }
}

load()
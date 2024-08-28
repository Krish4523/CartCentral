let specs = document.getElementsByClassName("acc");
let specCategories = [];
for (const spec of specs) {
  specCategories.push(spec.value);
}

document.getElementById("applyButton").addEventListener("click", async () => {
  let filtersSpecs = {};
  for (const specCategory of specCategories) {
    let chekBoxes = document.querySelectorAll(
      `.${specCategory.replace(" ", "")}Selectors:checked`
    );
    let checkboxValues = [];
    chekBoxes.forEach((checkbox) => {
      checkboxValues.push(checkbox.value);
    });
    if (checkboxValues.length != 0) {
      filtersSpecs[specCategory] = checkboxValues;
    }
  }
  if(Object.keys(filtersSpecs).length > 0){
    let data = await fetch("/products/filter", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(filtersSpecs),
    });

    document.getElementById("product-list").innerHTML = await data.text();
    filtersSpecs = {};
  }
});

async function productPage(element) {
  const productId = parseInt(element.getAttribute("data-product-id"));
  let data = await fetch("/products/" + productId);
  data = await data.json();
  dataArea.innerHTML = data["template"];
  let script = document.createElement("script");
  script.src = data["jsUrl"];
  dataArea.appendChild(script);
}

async function addToCart(button) {
  const productId = button.getAttribute("data-product-id");
  console.log("Add to Cart clicked for productList ID:", productId);
  console.log("/addCart/" + productId);
  let data = await fetch("/addCart/" + productId);
  data = await data.json();
  dataArea.innerHTML = data["template"];
  let script = document.createElement("script");
  script.src = data["jsUrl"];
  dataArea.appendChild(script);
}

async function buyNow(button) {
  var productId = button.getAttribute("data-product-id");
  console.log("Immediate purchase initiated for product: " + productId);
  let data = await fetch("/buynow/" + productId);
  data = await data.json();
  console.log(data)
  dataArea.innerHTML = data["template"];
  let script = document.createElement("script");
  script.src = data["jsUrl"];
  dataArea.appendChild(script);
}

let isFiltersVisible = false;

function showHide() {
  const showFiltersBtn = document.getElementById("showFiltersBtn");
  const filtersAccordion = document.getElementById("filtersAccordion");
  if (!isFiltersVisible) {
    filtersAccordion.style.display = "block";
    showFiltersBtn.textContent = "Hide Filters";
  } else {
    filtersAccordion.style.display = "none";
    showFiltersBtn.textContent = "Show Filters";
  }
  isFiltersVisible = !isFiltersVisible;
}

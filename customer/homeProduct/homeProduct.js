function category() {
    let categoryButtons = document.querySelectorAll('.categories button');

    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            const categoryId = button.id; // Get the ID of the clicked category button
            const products = document.querySelectorAll('.sub-cat'); // Get all sub-category product containers

            // Loop through each sub-category product container
            products.forEach(product => {
                if (product.classList.contains(categoryId)) {
                    product.style.display = 'block'; // Display products of the clicked category
                } else {
                    product.style.display = 'none'; // Hide products of other categories
                }
            });
        });
    });
    categoryButtons.item(0).click()
}

category()

async function productPage(element) {
    const productId = parseInt(element.getAttribute("data-product-id"));
    let data = await fetch("/products/" + productId);
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}

async function seeAll(element) {
    const subcatid = parseInt(element.getAttribute("data-sub-id"));
    let data = await fetch("/product-list/" + subcatid);
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    script.src = data["jsUrl"]
    dataArea.appendChild(script);
}
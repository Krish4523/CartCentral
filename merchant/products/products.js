async function deleteProduct(button) {
    const productId = button.getAttribute("data-product-id");
    if (confirm('are u sure u want to delete')) {
        try {
            const response = await fetch("/merchant/delete/" + productId, {
                method: "DELETE"
            });
            if (response.ok) {
                const productElement = button.closest(".product");
                productElement.remove();
                console.log("Product deleted successfully");
            } else {
                throw new Error("Failed to delete product");
            }
        } catch (error) {
            console.error("Error deleting product:", error);
        }
        getProducts()
    }
}


async function previewProduct(button) {
    const productId = button.getAttribute("data-product-id");
    let data = await fetch("/products/" + productId);
    data = await data.json();
    dataArea.innerHTML = data["template"];
    let script = document.createElement("script");
    dataArea.appendChild(script);
}
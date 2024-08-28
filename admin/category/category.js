function add(catID) {
    let subCatList = document.getElementById(`${catID}subCatList`);
    let div = document.createElement("div");
    div.classList.add("m-3");

    let catButton = document.createElement("input");
    catButton.type = "text";
    catButton.classList.add("form-control");
    catButton.id = "newSubCatInput";
    catButton.placeholder = "Enter SubCategory Name";
    catButton.addEventListener("change", async () => {
        if (catButton.value != "") {
            let subcatTemplate = await fetch("/admin/addSubcategory", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify({
                    catId: catID,
                    categoryName: catButton.value,
                }),
            });

            subcatTemplate = await subcatTemplate.text();
            let subCat = document.createElement("div");
            subCat.innerHTML = subcatTemplate;
            subCatList.appendChild(subCat);
            subCatList.removeChild(div);
        }
    });

    div.appendChild(catButton);
    subCatList.appendChild(div);
}

function edit(catID) {
    let catButton = document.getElementById(catID);
    let current = catButton.value;
    catButton.contentEditable = true;
    catButton.focus();

    catButton.addEventListener("keydown", async (event) => {
        if (event.key == "Enter") {
            if (catButton.textContent == "") {
                catButton.value = current;
                catButton.textContent = current;
            } else {
                catButton.value = catButton.textContent;
                current = catButton.value;
                await fetch("/admin/updateCategory", {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json",
                    },
                    body: JSON.stringify({
                        catId: catID,
                        categoryType: current,
                    }),
                });
                catButton.textContent = current;
            }
            catButton.contentEditable = false;
        } else if (event.key == "Escape") {
            catButton.value = current;
            catButton.textContent = current;
            catButton.contentEditable = false;
        }
    });

    catButton.addEventListener("focusout", () => {
        catButton.value = current;
        catButton.textContent = current;
        catButton.contentEditable = false;
    });
}

async function remove(catID) {
    document
        .getElementById("categoryList")
        .removeChild(document.getElementById(catID).parentElement.parentElement);
    await fetch("/admin/removeCategory", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            catId: catID,
        }),
    });
}

function editSubCat(subCatId) {
    let catButton = document.getElementById(`sub${subCatId}`);
    let current = catButton.value;
    catButton.contentEditable = true;
    catButton.focus();

    catButton.addEventListener("keydown", async (event) => {
        if (event.key == "Enter") {
            if (catButton.value == "") {
                catButton.value = current;
                catButton.textContent = current;
            } else {
                catButton.value = catButton.textContent;
                current = catButton.value.trim();
                let newTemplate = await fetch("/admin/updateSubcategory", {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json",
                    },
                    body: JSON.stringify({
                        subCatId: subCatId,
                        categoryName: current,
                    }),
                });
            }
            catButton.contentEditable = false;
        } else if (event.key == "Escape") {
            catButton.value = current;
            catButton.textContent = current;
            catButton.contentEditable = false;
        }
    });

    catButton.addEventListener("focusout", () => {
        catButton.value = current;
        catButton.textContent = current;
        catButton.contentEditable = false;
    });
}

async function removeSubCat(subCatId) {
    let button = document.getElementById(`sub${subCatId}`);
    button.parentElement.parentElement.parentElement.removeChild(
        button.parentElement.parentElement
    );
    await fetch("/admin/removeSubcategory", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            subCatId: subCatId,
        }),
    });
}

function addNew() {
    let categoryList = document.getElementById("categoryList");
    let div = document.createElement("div");
    div.classList.add("m-3");

    let catButton = document.createElement("input");
    catButton.type = "text";
    catButton.classList.add("form-control");
    catButton.id = "catInput";
    catButton.placeholder = "Enter Category Name";
    catButton.addEventListener("change", async () => {
        if (catButton.value != "") {
            let catTemplate = await fetch("/admin/addCategory", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify({
                    categoryType: catButton.value.trim(),
                }),
            });

            catTemplate = await catTemplate.text();
            let category = document.createElement("div");
            category.classList.add("accordion-item", "bg-transparent", "mt-2");
            category.innerHTML = catTemplate;
            categoryList.appendChild(category);
            categoryList.removeChild(div);
        }
    });

    div.appendChild(catButton);
    categoryList.appendChild(div);
}

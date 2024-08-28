function addSpecField() {
    let specFieldIndex = 0;
    const specFieldsContainer = document.getElementById('specFields');
    const specField = document.createElement('div');
    specField.classList.add('mb-3');
    specField.innerHTML = `
        <div class="row">
            <div class="col">
                <input type="text" class="form-control spec-name" name="specName_${specFieldIndex}" placeholder="Spec Name" required>
            </div>
            <div class="col">
                <input type="text" class="form-control spec-value" name="specValue_${specFieldIndex}" placeholder="Spec Value" required>
            </div>
            <div class="col-auto">
                <button type="button" class="btn btn-danger" onclick="removeField(this)">Remove</button>
            </div>
        </div>
    `;
    specFieldsContainer.appendChild(specField);
    specFieldIndex++;
}

function addImageField() {
    let imageFieldIndex = 0;
    const imageFieldsContainer = document.getElementById('imageFields');
    const imageField = document.createElement('div');
    imageField.classList.add('mb-3');
    imageField.innerHTML = `
        <div class="row">
            <div class="col">
                <input type="file" class="form-control" name="image" accept="image/*" required>
            </div>
            <div class="col-auto">
                <button type="button" class="btn btn-danger" onclick="removeField(this)">Remove</button>
            </div>
        </div>
    `;
    imageFieldsContainer.appendChild(imageField);
    imageFieldIndex++;
}

function removeField(button) {
    button.closest('.mb-3').remove();
}

function populateCategories(categories, subcategories) {
    const categorySelect = document.getElementById('productCategory');
    categorySelect.innerHTML = '<option value="" disabled selected>Select category</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });
    categorySelect.addEventListener("change", function () {
        populateSubcategories(subcategories);
    });
}

function populateSubcategories(subcategories) {
    const categorySelect = document.getElementById('productCategory');
    const subcategorySelect = document.getElementById('productSubcategory');
    const categoryId = categorySelect.value;
    subcategorySelect.innerHTML = '<option value="" disabled selected>Select subcategory</option>';
    const filteredSubcategories = subcategories.filter(subcategory => subcategory.catid == categoryId);
    filteredSubcategories.forEach(subcategory => {
        const option = document.createElement('option');
        option.value = subcategory.id;
        option.textContent = subcategory.name;
        subcategorySelect.appendChild(option);
    });
}

async function fetchCategoriesAndSubcategories() {
    try {
        const response = await fetch('/merchant/get-categories-and-subcategories');
        if (response.ok) {
            const data = await response.json();
            populateCategories(data.categories, data.subcategories);
            console.log('Fetch Successful');
        } else {
            console.error('Failed to fetch categories and subcategories:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching categories and subcategories:', error);
    }
}

fetchCategoriesAndSubcategories();

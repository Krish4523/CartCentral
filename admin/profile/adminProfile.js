let toggle = false;
let changedData = {};

for (let field of document.getElementsByClassName("input-field")) {
    field.addEventListener("change", () => {
        changedData[field.getAttribute("name")] = field.value;
    });
}

document.getElementById("saveBtn").addEventListener("click", async () => {
    await fetch("/admin/changedata", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({changedData}),
    });
});

document.getElementById("editBtn").addEventListener("click", () => {
    const inputFields = document.getElementsByClassName("input-field");
    for (let input of inputFields) {
        if (!toggle) {
            input.removeAttribute("disabled");
            input.removeAttribute("readonly");
            document.getElementById("editBtn").classList.add("active");
        } else {
            input.disabled = true;
            input.readonly = true;
            document.getElementById("editBtn").classList.remove("active");
        }
    }
    toggle = !toggle;
});
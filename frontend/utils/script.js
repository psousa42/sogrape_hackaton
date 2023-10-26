const loginButton = document.getElementById("submit");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value.toLowerCase();
    const ean = document.getElementById("ean").value;

    if (name === "" && ean === "") {
        
        alert("Please fill a field!");
    } else {
        alert("Product Added Successfully!\nNext check the product will apear on the dashboard");
        window.location.href = "/dashboard/index.html";
    }
})
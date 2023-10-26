const loginButton = document.getElementById("submit");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value.toLowerCase();
    const password = document.getElementById("password").value;

    if (username === "sogrape" && password === "sogrape") {
        window.location.href = "/dashboard/index.html";
        alert("You have successfully logged in.");
    } else {
        alert("Wrong Password/Username");
    }
})  
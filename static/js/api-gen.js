var password = document.getElementById("apiKey");

function genPassword() {
    var chars = "0123456789abcdefghijklmnopqrstuvwxyz";
    var password1 = "";
    var password2 = "";
    var password3 = "";
    var password4 = "";
    var password5 = "";

    for (var i = 0; i <= 8; i++) {
        var randomNumber = Math.floor(Math.random() * chars.length);
        password1 += chars.substring(randomNumber, randomNumber + 1);
    }
    for (var i = 0; i <= 4; i++) {
        var randomNumber = Math.floor(Math.random() * chars.length);
        password2 += chars.substring(randomNumber, randomNumber + 1);
    }
    for (var i = 0; i <= 4; i++) {
        var randomNumber = Math.floor(Math.random() * chars.length);
        password3 += chars.substring(randomNumber, randomNumber + 1);
    }
    for (var i = 0; i <= 4; i++) {
        var randomNumber = Math.floor(Math.random() * chars.length);
        password4 += chars.substring(randomNumber, randomNumber + 1);
    }
    for (var i = 0; i <= 12; i++) {
        var randomNumber = Math.floor(Math.random() * chars.length);
        password5 += chars.substring(randomNumber, randomNumber + 1);
    }
    password = password1.concat("-", password2, "-", password3, "-", password4, "-", password5);
    document.getElementById("apiKey").value = password;

}

function copyPassword(id) {
    var value = document.getElementById(id).innerHTML;
    var input_temp = document.createElement("input");
    input_temp.value = value;
    document.body.appendChild(input_temp);
    input_temp.select();
    document.execCommand("copy");
    document.body.removeChild(input_temp);
    alert("API-KEY has been Copied! : " + value);
}
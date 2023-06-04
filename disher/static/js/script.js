var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        setTimeout(()=>{
            document.getElementById("loader_container").style.display = "none";
            document.getElementById("content-container").style.display = "block";
        },500);
    }
};
xhttp.open("GET", "/", true);
xhttp.send();

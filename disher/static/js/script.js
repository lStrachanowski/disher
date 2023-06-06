

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        setTimeout(() => {
            document.getElementById("loader_container").style.display = "none";
            document.getElementById("content-container").style.display = "block";
        }, 500);
    }
};
xhttp.open("GET", "/", true);
xhttp.send();

// Is showing options in user recepie element
let optionsClick = (id) => {
    elementId = `user-recepie-${id}`;
    optionsId = `user-options-${id}`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    idList = document.querySelectorAll("[id^='user']");
    for (let i = 0; i < idList.length; i++) {
            if (elementId == idList[i].id){
                if (parentElement.style.display !== "none") {
                    parentElement.style.cssText = 'display:none !important';
                    optionElement.style.cssText = 'display:inline-flex!important';
                } else {
                    parentElement.style.cssText = 'display:inline-flex !important';
                    optionElement.style.cssText = 'display:none !important';
                }
            }else{

            }
    }
}

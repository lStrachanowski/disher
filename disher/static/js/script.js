

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


// Is showing options for user day elements
let dayOptionsClick =(name, id) =>{
    elementId = `${name}-${id}`;
    optionsId = `${name}-option-${id}`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    collapseElement = document.getElementById("collapseBreakfast");
    idList = document.querySelectorAll("[id^="+`${name}`+"]");
    for(let i=0 ; i< idList.length; i++){
        if(elementId == idList[i].id){
            if (!parentElement.classList.contains("hide-element")) {
                parentElement.classList.add("hide-element");
                optionElement.classList.add("show-element");
                collapseElement.classList.add("hide-element")
            } else {
                parentElement.classList.remove("hide-element");
                optionElement.classList.remove("show-element");
                collapseElement.classList.remove("hide-element");
                collapseElement.classList.remove("show");
            }
        }else{

        }
    }
} 
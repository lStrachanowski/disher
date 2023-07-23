

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("loader_container").style.display = "none";
        document.getElementById("content-container").style.display = "block";
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


// Is showing options for day edit elements
let dayEditOptionsClick =(name) =>{
    elementId = `${name}-edit`;
    optionsId = `${name}-edit-options`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    idList = document.querySelectorAll("[id^="+`${name}`+"]");
    for(let i=0 ; i< idList.length; i++){
        if(elementId == idList[i].id){
            if (!parentElement.classList.contains("hide-element")) {
                parentElement.classList.add("hide-element");
                optionElement.classList.add("show-element");
            } else {
                parentElement.classList.remove("hide-element");
                optionElement.classList.remove("show-element");
            }
        }else{

        }
    }
} 

// Is chcanging color of daycontainer and showing generate shoplist button
let dayChecked =(name)=>{
    elementName = name.split("-");
    checkBox = document.getElementById(name);
    container = document.getElementById(name);
    containerBody = document.getElementById(elementName[0]);
    containerHeader = document.getElementById(elementName[0]+"-edit");
      if(checkBox.checked){
        containerBody.style.backgroundColor = "var(--bs-gray-200)";
        containerHeader.style.backgroundColor = "var(--bs-gray-600)";
        document.getElementById("createShopList").style.display = "none";
        document.getElementById("generateShopList").classList.remove("generate-shoplist-button");
        document.getElementById("generateShopList").style.display = "block";
    }else{
        containerBody.style.backgroundColor = "var(--white)";
        containerHeader.style.backgroundColor = "var(--breakfast-color)";
        document.getElementById("createShopList").style.display = "block";
        document.getElementById("generateShopList").style.display = "none";
    }
}


// let showModal =() =>{
//     // Get a reference to the modal element
// const myModal = document.getElementById('exampleModalCenter');

// // Create a new Bootstrap Modal instance
// const modal = new bootstrap.Modal(myModal);

// // Show the modal
// modal.show();

// }

// Is hiding message container in login and register form. 
let hideMessage = () =>{
    document.getElementById("messageBox").style.display = "none";
}

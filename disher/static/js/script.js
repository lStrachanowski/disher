var dayId = "";

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
        if (elementId == idList[i].id) {
            if (parentElement.style.display !== "none") {
                parentElement.style.cssText = 'display:none !important';
                optionElement.style.cssText = 'display:inline-flex!important';
            } else {
                parentElement.style.cssText = 'display:inline-flex !important';
                optionElement.style.cssText = 'display:none !important';
            }
        } else {

        }
    }
}


// Is showing options for user day elements
let dayOptionsClick = (name, id) => {
    elementId = `${name}-${id}`;
    optionsId = `${name}-option-${id}`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    collapseElement = document.getElementById("collapseBreakfast");
    idList = document.querySelectorAll("[id^=" + `${name}` + "]");
    for (let i = 0; i < idList.length; i++) {
        if (elementId == idList[i].id) {
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
        } else {

        }
    }
}


// Is showing options for day edit elements
let dayEditOptionsClick = (name) => {
    elementId = `${name}-edit`;
    optionsId = `${name}-edit-options`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    idList = document.querySelectorAll("[id^=" + `${name}` + "]");
    for (let i = 0; i < idList.length; i++) {
        if (elementId == idList[i].id) {
            if (!parentElement.classList.contains("hide-element")) {
                parentElement.classList.add("hide-element");
                optionElement.classList.add("show-element");
            } else {
                parentElement.classList.remove("hide-element");
                optionElement.classList.remove("show-element");
            }
        } else {

        }
    }
}

// Is chcanging color of daycontainer and showing generate shoplist button
let dayChecked = (name) => {
    elementName = name.split("-");
    checkBox = document.getElementById(name);
    container = document.getElementById(name);
    containerBody = document.getElementById(elementName[0]);
    containerHeader = document.getElementById(elementName[0] + "-edit");
    if (checkBox.checked) {
        containerBody.style.backgroundColor = "var(--bs-gray-200)";
        containerHeader.style.backgroundColor = "var(--bs-gray-600)";
        document.getElementById("createShopList").style.display = "none";
        document.getElementById("generateShopList").classList.remove("generate-shoplist-button");
        document.getElementById("generateShopList").style.display = "block";
    } else {
        containerBody.style.backgroundColor = "var(--white)";
        containerHeader.style.backgroundColor = "var(--breakfast-color)";
        document.getElementById("createShopList").style.display = "block";
        document.getElementById("generateShopList").style.display = "none";
    }
}


let showModal = (id) => {
    dayId = id;
    // Get a reference to the modal element
    const myModal = document.getElementById('staticBackdrop');

    // Create a new Bootstrap Modal instance
    const modal = new bootstrap.Modal(myModal);

    // Show the modal
    modal.show();

}

// Is hiding message container in login and register form. 
let hideMessage = () => {
    document.getElementById("messageBox").style.display = "none";
}


// Prevents select meal modal form refershing the page after submit
document.getElementById("modalForm").addEventListener("submit", function (event) {
    event.preventDefault();
});



/**Is creating element in user day
 * 
 * @param {string} id - Element id
 * 
 * */
let addDishMeal = (id) => {

    let selectedValue = document.getElementById("selectedMeal").value;
    let elementId = dayId + "-" + selectedValue;
    translateTable = {
        "Breakfast": "Śniadanie",
        "Brunch": "2 Śniadanie",
        "Dinner": "Obiad",
        "Dessert": "Przekąska",
        "Supper": "Kolacja",
    }

    let mealName = translateTable[selectedValue];
    if (document.getElementById(elementId)) {
        if (confirm("Masz już śniadanie , chcesz dodać kolejne ?")) {
            console.log(selectedValue);
            let number = document.getElementsByClassName(selectedValue).length;
            console.log(number);
            elementId = elementId + "-" + number
          } else {
            return false
        }
    }
    const mealElementTemplate = `<div class="d-flex day-element m-3 p-2 align-items-center" id=${elementId}>
    <div class="col-6 text-start p-2 ${selectedValue}">
       ${mealName}
    </div>
    <div class="col-3">
    </div>
    <div class="col-2 add-button add-button-day d-flex align-items-center justify-content-center text-center cursor">
    <div class="cross-button cross-button-day"></div>
    </div>
    <div class="col-2 text-end">
        <img src="/static/img/close.svg" class="day-icons-options-size" onclick="deleteElement('${elementId}');">
    </div>
    </div>`
    let selectedDay = document.getElementById(id);
    selectedDay.insertAdjacentHTML('beforebegin', mealElementTemplate);
}

/**Is deleting element in user day
 * 
 * @param {string} id - Element id
 * 
 * */
let deleteElement = (id) => {
    let selectedElement = document.getElementById(id);
    selectedElement.remove();
}
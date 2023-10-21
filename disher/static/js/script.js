var dayId = "";
var globalElementId = "";
var globalMealName = "";
var globalSelectedValue = "";

var translateTable = {
    "Breakfast": "Śniadanie",
    "Brunch": "2 Śniadanie",
    "Dinner": "Obiad",
    "Dessert": "Przekąska",
    "Supper": "Kolacja",
}

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
let mealOptionsClick = (name) => {
    elementId = `${name}`;
    optionsId = `${name}-edit-options`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    collapseElement = document.getElementById("collapseBreakfast");
    if (!parentElement.classList.contains("hide-element")) {
        parentElement.classList.add("hide-element");
        optionElement.classList.add("show-element");
        if (collapseElement) {
            collapseElement.classList.add("hide-element");
        }

    } else {
        parentElement.classList.remove("hide-element");
        optionElement.classList.remove("show-element");
        collapseElement.classList.remove("hide-element");
        collapseElement.classList.remove("show");
    }
    
    let recepieDiv = document.getElementById(name + '-collapse');
    recepieDiv.classList.add("hide-element");
}


// Is showing options for day edit elements
let mealEditOptionsClick = (name) => {
    elementId = `${name}`;
    optionsId = `${name}-edit-options`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    if (!parentElement.classList.contains("hide-element")) {
        parentElement.classList.add("hide-element");
        optionElement.classList.add("show-element");
    } else {
        parentElement.classList.remove("hide-element");
        optionElement.classList.remove("show-element");
    }
    let recepieDiv = document.getElementById(name + '-collapse');

    recepieDiv.classList.remove("hide-element");
    if(recepieDiv.classList.contains('show') ){
        recepieDiv.classList.remove('show');
     }
}

// Is showing options for day edit elements
let dayEditOptionsClick = (name) => {
    elementId = `${name}-edit`;
    optionsId = `${name}-edit-options`;
    parentElement = document.getElementById(elementId);
    optionElement = document.getElementById(optionsId);
    if (!parentElement.classList.contains("hide-element")) {
        parentElement.classList.add("hide-element");
        optionElement.classList.add("show-element");
    } else {
        parentElement.classList.remove("hide-element");
        optionElement.classList.remove("show-element");
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


let showMealModal = (id) => {
    dayId = id;
    // Get a reference to the modal element
    const myModal = document.getElementById('staticBackdrop');

    // Create a new Bootstrap Modal instance
    const modal = new bootstrap.Modal(myModal);

    // Show the modal
    modal.show();

}

let showSearchMealModal = (id) => {
    dayId = id;
    globalElementId = id.split("-").slice(1,).join("-");
    // Get a reference to the modal element
    const myModal = document.getElementById('staticBackdropSearch');

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
if (document.getElementById("modalForm")) {
    document.getElementById("modalForm").addEventListener("submit", function (event) {
        event.preventDefault();
    });
}



// Prevents select meal modal form refershing the page after submit
if (document.getElementById("modalFormSearch")) {
    document.getElementById("modalFormSearch").addEventListener("submit", function (event) {
        event.preventDefault();
    });
}


// Template with meal element added to user day
let dishElementTemplate = (elementId, mealName, selectedValue) => {
    return `<div class="d-flex day-element m-3 p-2 align-items-center" data-bs-toggle="collapse" data-bs-target="#${elementId}-collapse" aria-expanded="false" aria-controls="${elementId}-collapse" id=${elementId}>
    <div class="col-6 text-start p-2 ${selectedValue}">
       ${mealName}
    </div>
    <div class="col-3">
    </div>
    <button class="col-2 add-button add-button-day d-flex align-items-center justify-content-center text-center cursor" onclick="showSearchMealModal('add-${elementId}')">
    <div class="cross-button cross-button-day" id="add-${elementId}" ></div>
    </button>
    <div class="col-2 text-end">
        <img src="/static/img/close.svg" class="day-icons-options-size" onclick="deleteElement('${elementId}');">
    </div>
    </div>
    `
}

let mealElementTemplate = (globalElementId, slug, dish) => {
    return `<div class="collapse" id="${globalElementId}-collapse">
    <div class="card card-body m-3 p-3 align-items-center day-element-card cursor" onclick="location.href='/recepie/'+'${slug}'">
        ${dish}
    </div>
    </div>`
}


let mealOptions = (id) => {
    return `<div class="d-flex day-element day-options m-3 p-2 align-items-center"
    id="${id}-edit-options">
    <div class="col-6">
        Usuń
    </div>
    <div class="col-4">
        Kopiuj
    </div>
    <div class="col-2 text-end p-2">
        <img src="/static/img/close.svg" class="day-icons-options-size"
            onclick="mealEditOptionsClick('${id}')" id="close-img-${id}">
    </div>
    </div>
    `
}

let mealElementWithData = (id, mealName, calories) => {
    return `
    <div class="d-flex day-element m-3 p-2 align-items-center " data-bs-toggle="collapse"
    data-bs-target="#${globalElementId}-collapse" aria-expanded="false" aria-controls="${globalElementId}-collapse"
    id="${id}">
    <div class="col-6 text-start p-2">
        ${mealName}
    </div>
    <div class="col-5">
        ${calories} kcal
    </div>
    <div class="col-1" onclick="mealOptionsClick('${id}')">
        <img src="/static/img/options.svg" class="day-icons-options-size"
             id="img-${globalElementId}">
    </div>
    </div>`
}

let dayElementTemplate = (id, number) =>{
    return `<div class="col-lg-3 col-md-6">
    <div class="d-flex form-check text-start align-items-center">
        <input class="form-check-input p-2" type="checkbox" value="" id="${id}-checkbox" onclick="dayChecked('${id}-checkbox')">
        <label class="form-check-label p-2" for="flexCheckDefault">
            Dodaj do listy zakupów
        </label>
    </div>
    <div class="recepie-container white-background" id="${id}">
        <!-- Naglowek dnia -->
        <div class="d-flex align-items-center justify-content-between col-12 day-header-color day-header-font day-header-border p-2 min-height cursor" id="${id}-edit">
            <div class="col-5 text-start p-3">
                Dzień ${number}
            </div>
            <div class="col-5 text-end">
                0 kcal
            </div>
            <div class="col-2 text-end p-2">
                <img src="/static/img/options.svg" class="day-options-icon-color day-icons-options-size" onclick="dayEditOptionsClick('${id}')">
            </div>
        </div>

        <!-- Edycja naglowka dnia -->
        <div class="d-flex align-items-center justify-content-between col-12 day-header-color day-header-font day-header-border p-2 min-height cursor day-edit-options" id="${id}-edit-options">

            <div class="col-6 p-3">
                Usuń
            </div>
            <div class="col-4">
                Kopiuj
            </div>
            <div class="col-2 text-end p-2">
                <img src="/static/img/close.svg" class="day-options-icon-color day-icons-options-size" onclick="dayEditOptionsClick('${id}')">
            </div>
        </div>

        <div class="col-12 empty-day-font greey-font" id="day-${number}-add">Dodaj posiłek</div>
        <div class="col-12 d-flex justify-content-center">
            <button class="add-button d-flex align-items-center justify-content-center cursor m-2 mb-3" type="button" onclick="showMealModal('day-${number}-add');">
                <div class="cross-button"></div>
            </button>

        </div>
    </div>

</div>`
}

let buttonTemplate = (id) =>{
    return `<button type="submit" class="btn btn-success" data-bs-dismiss="modal"
    onclick="addDishMeal('day-${id}-add');">Dodaj</button>`
}

/**Is creating element in user day
 * 
 * @param {string} id - Element id
 * 
 * */
let addDishMeal = (id) => {
    console.log(id);
    let selectedValue = document.getElementById("selectedMeal").value;
    let elementId = dayId + "-" + selectedValue;
    globalElementId = elementId;
    let mealName = translateTable[selectedValue];
    let mealNAmeLowerCase = mealName.toLowerCase();
    globalMealName = mealName;
    globalSelectedValue = selectedValue;
    if (document.getElementById(elementId)) {
        if (confirm(`Masz już ${mealNAmeLowerCase}, chcesz dodać kolejne ?`)) {
            let number = document.getElementsByClassName(selectedValue).length;
            elementId = elementId + "-" + number
            globalElementId = elementId;
        } else {
            globalElementId = elementId;
            return false
        }
    }
    const htmlTemplate = dishElementTemplate(elementId, mealName, selectedValue);
    let selectedDay = document.getElementById(id);
    selectedDay.insertAdjacentHTML('beforebegin', htmlTemplate);
    console.log(id);
    // let modalTemplate = document.getElementById('dayAddButtonID');
    // modalTemplate.insertAdjacentHTML('beforeend', buttonTemplate(id) );

}



/**Is creating element in user selected dish
 * 
 * @param {string} id - Element id
 * 
 * */
let addMealToDay = (id, slug, dish, calories) => {
    let mealName = translateTable[globalElementId.split("-")[3]];
    let collapseMEal = document.getElementById(globalElementId + "-collapse");
    if (!collapseMEal) {
        const htmlWithMeal = mealElementTemplate(globalElementId, slug, dish);
        let selectedDay = document.getElementById(globalElementId);
        selectedDay.insertAdjacentHTML('afterend', htmlWithMeal);
        selectedDay.remove();
        let selectedMeal = document.getElementById(globalElementId + "-collapse");
        selectedMeal.remove();

        let selectedParent = document.getElementById(id);
        elementId = id.split("-").slice(1,).join("-");
        let newSelectedDay = mealElementWithData(globalElementId, mealName, calories);
        selectedParent.insertAdjacentHTML('beforebegin', newSelectedDay);

        let newSelectedMeal = document.getElementById(globalElementId);
        newSelectedMeal.insertAdjacentHTML('afterend', htmlWithMeal);

        let mealOptionsTemplate = mealOptions(globalElementId);
        newSelectedMeal.insertAdjacentHTML('afterend', mealOptionsTemplate);

    } else {
        alert("Już masz dodany posiłek ");
    }

}

let addDay = (id) =>{
    let parent = document.getElementById("mainDashboard");
    parent.insertAdjacentHTML('afterend', dayElementTemplate("day"+id, id));
}

/**Is deleting element in user day
 * 
 * @param {string} id - Element id
 * 
 * */
let deleteElement = (id) => {
    let selectedElement = document.getElementById(id);
    selectedElement.remove();
    let selectedElementCollapse = document.getElementById("day"+ id + "-collapse");
    if (selectedElementCollapse) {
        selectedElementCollapse.remove();
    }

}



// Shows products fields in add recepie route
if (document.getElementById("addProductButton")) {
    document.getElementById("addProductButton").addEventListener("click", function (event) {
        event.preventDefault();
        let inputsFields = document.getElementById("addProductInputFields");
        let saveProductBtn = document.getElementById("saveProductButtonContainer");
        inputsFields.classList.remove("hide-element");
        saveProductBtn.classList.remove("hide-element");
    });
}

// Is hiding products fields in add recepie route
let hideAddedProduct = () =>{
        let inputsFields = document.getElementById("addProductInputFields");
        let saveProductBtn = document.getElementById("saveProductButtonContainer");
        inputsFields.classList.add("hide-element");
        saveProductBtn.classList.add("hide-element");
}
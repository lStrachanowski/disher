var dayId = "";
var globalElementId = null;
var globalMealName = "";
var globalSelectedValue = "";
var dayData = null;
var shopListSelectedDays = [];
var persons = 1;
var baseAmounts = [];
var baseAmountsUnits = [];
var DATA_URL = '/user/dashboard/daydata';
var NEW_DAY = '/user/dashboard/addnewday';
var DELETE_MEAL = '/user/deletemealfromday/';
var DELETE_DAY = '/user/deleteday/';
var COPY_DAY = '/user/copyday/';
var COPY_DISH = '/user/copydish/';
var DAYS_PRODUCTS_LIST = '/user/productslist/';
var SEARCH_DATA_URL = window.location.protocol + "//" + window.location.host + '/getproductsearch/';
var SEARCH_RECEPIE_URL = window.location.protocol + "//" + window.location.host + '/getrecepiesearch/';
var SEARCH_USER_RESEPIES = window.location.protocol + "//" + window.location.host + '/recepie/getuserrecepies/';
var tempAddedProduct = null;
var productList = [];
var expandValue = false;

let productContainer = document.getElementById("addProductContainer");
let saveButtonContainer = document.getElementById("productButtonsContainer");
let productLoader = document.getElementById("productLoader");
let saveButton = document.getElementById("saveButton");
let saveDishButton = document.getElementById("saveDishButton");
let cancelButton = document.getElementById("cancelButton");
let addContainertBox = document.getElementById("addContainertBox");
let productsContainerHeader = document.getElementById("productsContainerHeader");

var translateTable = {
    "Breakfast": "Śniadanie",
    "Brunch": "2 Śniadanie",
    "Dinner": "Obiad",
    "Dessert": "Przekąska",
    "Supper": "Kolacja",
}


var symbolTable = {
    "B": ["Śniadanie", "Breakfast"],
    "B2": ["2 Śniadanie", "Brunch"],
    "D": ["Obiad", "Dinner"],
    "D2": ["Przekąska", "Dessert"],
    "S": ["Kolacja", "Supper"],
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


// Template with meal element added to user day
let dishElementTemplate = (elementId, mealName, selectedValue) => {
    return `<div class="d-flex day-element m-3 p-2 align-items-center" data-bs-toggle="collapse" data-bs-target="#${elementId}-collapse" aria-expanded="false" aria-controls="${elementId}-collapse" id="${elementId}">
    <div class="col-6 text-start p-2 ${selectedValue}">
       ${mealName}
    </div>
    <div class="col-3">
    </div>
    <button class="col-2 add-button add-button-day d-flex align-items-center justify-content-center text-center cursor" onclick="showSearchMealModal('add-${elementId}');">
    <div class="cross-button cross-button-day" id="add-${elementId}" ></div>
    </button>
    <div class="col-2 text-end">
        <img src="/static/img/close.svg" class="day-icons-options-size" onclick="deleteMealElement('${elementId}');">
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


let mealOptions = (id, day_id, meal_id) => {
    return `<div class="d-flex day-element day-options m-3 p-2 align-items-center"
    id="${id}-edit-options">
    <div class="col-6" onclick="deleteMealOptionElement('${id}', '${day_id}', '${meal_id}');" >
        Usuń
    </div>
    <div class="col-4" onclick="copyMeal('${id}', '${day_id}','${meal_id}');">
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
    <div class="col-1" onclick="mealOptionsClick('${id}');">
        <img src="/static/img/options.svg" class="day-icons-options-size"
             id="img-${globalElementId}">
    </div>
    </div>`
}

let dayElementTemplate = (id, number) => {
    return `<div class="col-lg-3 col-md-6" id="${id}-container">
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
                ${number}
            </div>
            <div class="col-5 text-end" id="${id}-counter">
                0 kcal
            </div>
            <div class="col-2 text-end p-2">
                <img src="/static/img/options.svg" class="day-options-icon-color day-icons-options-size" onclick="dayEditOptionsClick('${id}')">
            </div>
        </div>

        <!-- Edycja naglowka dnia -->
        <div class="d-flex align-items-center justify-content-between col-12 day-header-color day-header-font day-header-border p-2 min-height cursor day-edit-options" id="${id}-edit-options">

            <div class="col-6 p-3" onclick="deleteDay('${id}')">
                Usuń
            </div>
            <div class="col-4" onclick="copyDay('${id}')">
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

let searchResultTemplate = (name, id) => {
    return `<div class="col-12 d-flex align-items-center justify-content-center mt-2 m-1 product-search-result">
    <div
        class="col-8 d-flex align-items-center justify-content-around  recepie-container  white-background cursor" id
        =${id}>
        <div class="col-lg-4  m-3 font-bold cursor">${name}</div>
        <div class="col-lg-2  text-center"></div>
        <div class="col-lg-2  text-center" onclick="chooseProduct('${name}', '${id}');">Wybierz</div>
    </div>
</div>`
}


let dishProductSearchContainer = () => {
    return `<div class="form-group col-lg-6 col-12" id="dishProductSearchContainer">
    <label for="dish_product_search">Wyszukaj produkt </label>
    <input type="text" class="form-control " id="dish_product_search" name="dish_product_search" onkeydown="debouncedSearchData();" required="">
    </div>`;
}

let productListItem = (productName, quantity, unit) => {
    return `     <div
    class="col-12 d-flex align-items-center justify-content-around  recepie-container  white-background cursor mt-2 m-1">
    <div class="col-lg-2  text-center m-3 font-bold cursor">${productName}</div>
    <div class="col-lg-7  text-start cursor">${quantity} ${unit}</div>
    <div class="col-lg-2  text-center">usuń</div>
    </div>`;
}


let shopListButtonTemplate = () => {
    return `<div class="row col-12 align-items-center justify-content-center m-3 " id="shopListContainer">
            <button class="btn btn-primary col-lg-2 col-md-4 col-8  generate-list-button-color" id="createShopList">
                Utwórz listę zakupów
            </button>
            <button class="btn btn-primary col-lg-2 col-md-4 col-8  generate-shoplist-button-color generate-shoplist-button" id="generateShopList" onclick="getDaysProductsList();">
                Generuj listę zakupów
            </button>
    </div>`;
}

let userRecepiesTemplate = (dish, index) => {
    let selectedMealType = '';
    if (dish.dish_type == 'B') {
        selectedMealType = "Śniadanie";
    }
    if (dish.dish_type == 'B2') {
        selectedMealType = "2 Śniadanie";
    }
    if (dish.dish_type == 'D') {
        selectedMealType = "Obiad";
    }
    if (dish.dish_type == 'D2') {
        selectedMealType = "Przekąska";
    }
    if (dish.dish_type == 'S') {
        selectedMealType = "Kolacja";
    }


    let template = ` <div class="col-12 d-flex align-items-center justify-content-center mt-2 m-1 user-recepie-class" id="${index}">
            <div class="col-lg-7 col-12 d-flex align-items-center justify-content-between user-recepie-container white-background"
                id="user-recepie-${index}">
                <div class="col-lg-2  text-center m-3 font-bold cursor"> 
                ${selectedMealType}  
                </div>
                <div class="col-8  text-center cursor"  onclick="location.href='/recepie/${dish.slug}'">  ${dish.dish_name}</div>
                <div class="col-2  text-center">
                     <img src="/static/img/share.svg"
                        class="cursor user-recepie-icons-padding user-recepie-icons-size user-recepie-icons-show" onclick="copyToClipboard('/recepie/${dish.slug}')">
                    <img src="/static/img/options.svg"
                        class="cursor user-recepie-icons-padding user-recepie-icons-size m-3"
                        id="recepie-options-id-click" onclick=optionsClick(${index})>
                </div>
            </div>

            <div class="col-lg-7 col-12 d-flex align-items-center justify-content-between recepie-container white-background user-recepie-options-id"
                id="user-options-${index}">
                <div class="col-2  text-center m-3 font-bold cursor dark-font">Edytuj</div>
                <div class="col-8  text-center cursor font-bold dark-font recepie-options-delete"
                    id="recepie-options-delete-click">Usuń</div>
                <div class="col-2  text-center">
                    <img src="/static/img/close.svg"
                        class="cursor user-recepie-icons-padding user-recepie-icons-size m-3"
                        id="recepie-options-id-close-click" onclick=optionsClick(${index})>
                </div>
            </div>
        </div>`
    return template;
}

let recepieSearchResultItem = (dishData) => {
    console.log(globalElementId);
    let meal_type = "";
    let container = document.getElementById("recepieContainer");
    let day_id = globalElementId.split("-")[1];
    for (v in symbolTable) {
        if (symbolTable[v].includes(globalElementId.split('-')[3])) {
            meal_type = v;
        }
    }
    container.replaceChildren();
    if (dishData && dishData.length > 0) {
        dishData.forEach(recepie => {
            const recepieDiv = document.createElement("div");
            recepieDiv.className = "col-xl-3 col-lg-5 col-md-10 text-center recepie-container white-background m-3";
            recepieDiv.id = recepie.id;
            console.log(recepie);
            recepieDiv.innerHTML = `
                    <div class="d-flex row align-items-center align-items-stretch">
                        <div class="d-flex align-items-center justify-content-center col-8 recepie-header-color recepie-header-font recepie-header-border p-2 min-height cursor"
                            onclick="location.href='/recepie/${recepie.dish_slug}'">
                            ${recepie.name}
                        </div>
                        <div class="d-flex align-items-center justify-content-center col-4 recepie-header-font ${getDishTypeClass(recepie.dish_type)} recepie-meal-border p-2">
                            ${getDishTypeName(recepie.dish_type)}
                        </div>
                        <div class="col-8 p-3 recepie-font recepie-font-spacing text-start d-block">
                            <div class="col-12 min-h ">
                                ${recepie.dish_description}
                            </div>
                            <div class="col-12">
                                <a href="/recepie/${recepie.slug}" class="font-bold">więcej...</a>
                            </div>
                        </div>
                        <div class="col-4 p-2">
                            <div class="row justify-content-around">
                                <div class="col-lg-12 p-1">
                                    <img src="/static/img/iconfire.svg" class="icon-size-15">
                                </div>
                                <div class="col-lg-12 recepie-font font-bold">
                                    ${recepie.dish_calories} kcal
                                </div>
                                <div class="col-lg-12 p-1">
                                    <img src="/static/img/iconclock.svg" class="icon-size-15">
                                </div>
                                <div class="col-lg-12 recepie-font font-bold">
                                    ${getPreparationTimeName(recepie.preparation_time)}
                                </div>
                            </div>
                        </div>
                        <div class="col-12 d-flex justify-content-center">
                            <div class="d-flex align-items-center justify-content-center cursor m-2 mb-3 addMealButtonSelectorContainer">
                                <button class="add-button d-flex align-items-center justify-content-center cursor m-2 mb-3 addMealButtonSelector"
                                    data-bs-dismiss="modal" type="button"
                                    onclick="addMealToDay( '${globalElementId}', '${recepie.dish_slug}', '${recepie.name}', '${recepie.dish_calories}', '${meal_type}', '${day_id}', 'true');">
                                    <div class="cross-button"></div>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            container.appendChild(recepieDiv);
        });
    } else {
        const recepieDiv = document.createElement("div");
        recepieDiv.className = "col-12 text-center";
        recepieDiv.innerHTML = 'Nothing to show';
        container.appendChild(recepieDiv);
    }
}

function getDishTypeClass(dishType) {
    switch (dishType) {
        case 'B': return 'recepie-meal-color-breakfast';
        case 'B2': return 'recepie-meal-color-second-breakfast';
        case 'D': return 'recepie-meal-color-dinner';
        case 'D2': return 'recepie-meal-color-snack';
        case 'S': return 'recepie-meal-color-supper';
        default: return '';
    }
}

function getDishTypeName(dishType) {
    switch (dishType) {
        case 'B': return 'Śniadanie';
        case 'B2': return '2 Śniadanie';
        case 'D': return 'Obiad';
        case 'D2': return 'Przekąska';
        case 'S': return 'Kolacja';
        default: return '';
    }
}

function getPreparationTimeName(preparationTime) {
    switch (preparationTime) {
        case 'S': return 'Szybkie';
        case 'M': return 'Średni';
        case 'L': return 'Długi';
        default: return '';
    }
}

let addNewElementData = async (day_id, slug, meal_type) => {
    try {
        let response = await fetch('/user/addmealtoday/' + day_id + '/' + slug + '/' + meal_type);
        let data = await response.json();
        fetchDataFromWeb(updateCookies);
        setUserIdLCookie();
        return JSON.parse(data).id;
    } catch (error) {
        console.log('Error fetching data:', error);
    }
}

/**Is creating element in user selected dish
 * 
 * @param {string} id - Element id
 * 
 * */
let addMealToDay = async (id, slug, dish, calories, meal_type, day_id, new_element, meal_id) => {
    let newMealId = null;
    // Upddating data when new element is created
    if (new_element == 'true') {
        newMealId = await addNewElementData(day_id, slug, meal_type);
        fetchDataFromWeb(countCalories);
    }
    // Generating globalElementId
    if (meal_type) {
        if (id.slice(3, id.length)[0] == '-') {
            globalElementId = "day" + id.slice(3, id.length);
        } else {
            globalElementId = "day-" + id.slice(3, id.length) + "-" + symbolTable[meal_type][1];
        }

    } else {
        globalElementId = id;
    }
    let mealName = '';
    let selectedParent = null;

    if (meal_type) {
        mealName = symbolTable[meal_type][0];
    } else {
        mealName = translateTable[globalElementId.split("-")[3]];
    }

    let collapseMEal = document.getElementById(globalElementId + "-collapse");

    if (!collapseMEal) {
        // When there is no other day wit meal
        const htmlWithMeal = mealElementTemplate(globalElementId, slug, dish);
        let selectedDay = document.getElementById(globalElementId);
        if (selectedDay) {
            selectedDay.insertAdjacentHTML('afterend', htmlWithMeal);
            selectedDay.remove();
        }
        let selectedMeal = document.getElementById(globalElementId + "-collapse");

        if (selectedMeal) {
            selectedMeal.remove();
        }

        if (meal_type) {
            if (day_id) {
                selectedParent = document.getElementById("day-" + day_id + "-add");
            } else {
                selectedParent = document.getElementById("day-" + id.split("-")[1] + "-add");
                console.log(selectedParent);
            }
        } else {
            if (day_id) {
                parentID = "day-" + day_id + "-add";
                selectedParent = document.getElementById(parentID);
            } else {
                parentID = "day-" + id.split("-")[1] + "-add";
                selectedParent = document.getElementById(parentID);
            }

        }

        elementId = id.split("-").slice(1,).join("-");

        let newSelectedDay = mealElementWithData(globalElementId, mealName, calories);
        selectedParent.insertAdjacentHTML('beforebegin', newSelectedDay);

        let newSelectedMeal = document.getElementById(globalElementId);
        newSelectedMeal.insertAdjacentHTML('afterend', htmlWithMeal);
        if (newMealId) {
            let mealOptionsTemplate = mealOptions(globalElementId, day_id, newMealId);
            newSelectedMeal.insertAdjacentHTML('afterend', mealOptionsTemplate);
        } else {
            let mealOptionsTemplate = mealOptions(globalElementId, day_id, meal_id);
            newSelectedMeal.insertAdjacentHTML('afterend', mealOptionsTemplate);
        }

    } else {
        let number = document.getElementsByClassName("collapse").length;
        elementId = elementId + "-" + number
        globalElementId = elementId;
        const htmlWithMeal = mealElementTemplate(globalElementId, slug, dish);
        let selectedDay = document.getElementById(globalElementId);


        if (selectedDay) {
            selectedDay.insertAdjacentHTML('afterend', htmlWithMeal);
            selectedDay.remove();
        }
        let selectedMeal = document.getElementById(globalElementId + "-collapse");

        if (selectedMeal) {
            selectedMeal.remove();
        }

        if (meal_type) {
            if (day_id) {
                selectedParent = document.getElementById("day-" + day_id + "-add");
            } else {
                selectedParent = document.getElementById("day-" + id.split("-")[1] + "-add");
                console.log(selectedParent);
            }
        } else {
            if (day_id) {
                parentID = "day-" + day_id + "-add";
                selectedParent = document.getElementById(parentID);
            } else {
                parentID = "day-" + id.split("-")[1] + "-add";
                selectedParent = document.getElementById(parentID);
            }

        }

        elementId = id.split("-").slice(1,).join("-");

        let newSelectedDay = mealElementWithData(globalElementId, mealName, calories);
        selectedParent.insertAdjacentHTML('beforebegin', newSelectedDay);

        let newSelectedMeal = document.getElementById(globalElementId);
        newSelectedMeal.insertAdjacentHTML('afterend', htmlWithMeal);

        if (newMealId) {
            let mealOptionsTemplate = mealOptions(globalElementId, day_id, newMealId);
            newSelectedMeal.insertAdjacentHTML('afterend', mealOptionsTemplate);
        } else {
            let mealOptionsTemplate = mealOptions(globalElementId, day_id, meal_id);
            newSelectedMeal.insertAdjacentHTML('afterend', mealOptionsTemplate);
        }

    }

}




let modalButtonTemplate = (id) => {
    return `<div class="modal-footer justify-content-center" id="dayAddButtonID">
    <button type="submit" class="btn btn-success" data-bs-dismiss="modal"
        onclick="addDishMeal('${id}');">Dodaj</button>
    </div>`
}

let buttonTemplate = (id) => {
    return `<button type="submit" class="btn btn-success" data-bs-dismiss="modal"
    onclick="addDishMeal('day-${id}-add');">Dodaj</button>`
}

let addDay = (id) => {
    let parent = document.getElementById("mainDashboard");
    parent.insertAdjacentHTML('afterend', dayElementTemplate("day" + id, id));
}

function clearInput() {
    const inputElement = document.getElementById("search");
    inputElement.value = '';
}

function readCookie(parameter) {
    let cookie = document.cookie.split(';');
    for (value of cookie) {
        if (value.split('=')[0].trim() === parameter) {
            let data = value.split('=')[1];
            return data;
        }
    }
}

// Checking if user is in dahsboard url
const currentUrl = window.location.pathname;

if (currentUrl == '/user/dashboard') {
    if (checkForDataInCookies()) {
        let user_id = document.getElementsByClassName("user-id-selector")[0].id;
        let cookie_id = readCookie('user_id');
        if (user_id === cookie_id) {
            console.log("cookies");
            fetchDataFromCookies(dayChange);
        } else {
            console.log("web, differnet user");
            fetchDataFromWeb(dayChange);
            setUserIdLCookie();
        }
    } else {
        console.log("web");
        fetchDataFromWeb(dayChange);
        setUserIdLCookie();
    }
}


window.addEventListener('popstate', function (event) {
    console.log('Current URL:', window.location.href);

    // Perform actions based on the current URL change here
});

function checkForDataInCookies() {
    let data = readCookie('data');
    if (data) {
        return true;
    }
}

function setUserIdLCookie() {
    fetch('/setidcookie')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        }).catch(error => {
            console.log('Error fetching data:', error);
        });
}

function getUserIdCookie() {
    fetch('/getidcookie')
        .then(response => response.json())
        .then(data => {
            return data;
        }).catch(error => {
            console.log('Error fetching data:', error);
        });
}



function fetchDataFromCookies(callback) {
    data = readCookie('data');
    callback(data);
}


// Fetching data about user days from server
function fetchDataFromWeb(callback) {
    fetch(DATA_URL)
        .then(response => response.json())
        .then(data => {
            let valueCheck = JSON.parse(data);
            if (valueCheck.message) {
                console.log(valueCheck.message);
                document.cookie = "data=";
            } else {
                document.cookie = "data=" + data;
                callback(data);
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function checkIfShopListButtonExist() {
    let shoplistButton = document.getElementById("generateShopList");
    let dayContainers = document.getElementsByClassName("form-check").length;
    if (shoplistButton && dayContainers < 1) {
        console.log("Ukryj button");
        shoplistButton.style.display = 'none';
        shoplistButton.remove();
        return
    }

}

function updateCookies(data) {
    document.cookie = "data=" + "";
    document.cookie = "data=" + data;
    console.log("cookie updated");
}

// function addNewDay(getList=false) {
//     fetch(NEW_DAY)
//         .then(response => response.json())
//         .then(data => {
//             let valueCheck = JSON.parse(data);
//             day_id_list = []
//             for (value of valueCheck) {
//                 day_id_list.push(value.day_id);
//             }
//             fetchDataFromWeb(updateCookies);
//             addDay((day_id_list[day_id_list.length - 1]));
//             if(getList){
//                 return (day_id_list[day_id_list.length - 1]);
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });

// }

async function addNewDay(getList = false) {
    try {
        const response = await fetch(NEW_DAY);
        const data = await response.json();
        const valueCheck = JSON.parse(data);

        const day_id_list = valueCheck.map(value => value.day_id);
        fetchDataFromWeb(updateCookies);
        addDay(day_id_list[day_id_list.length - 1]);

        // checkIfShopListButtonExist();

        if (getList) {
            return day_id_list[day_id_list.length - 1];
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


// Rendering data about user day in dashboard
function dayChange(newData, parsed) {
    dayData = JSON.parse(newData);

    if (parsed) {
        for (item of dayData.day_items) {
            addMealToDay('day' + dayData.day_id + '-add', item.slug, item.name, item.cal, item.type, dayData.day_id, 'true', item.dish_id);
        }
    } else {
        for (day of dayData) {
            addDay(day.day_id);
            for (item of day.day_items) {
                addMealToDay('day' + day.day_name + '-add', item.slug, item.name, item.cal, item.type, day.day_id, 'false', item.dish_id);
            }
            updateCalories(dayData, day.day_id);
        }
    }


}

function updateCalories(dayData, day_id) {
    let caloriesSum = countCaloriesSum(dayData, day_id);
    getCounterElement(day_id, caloriesSum);
}

//Counts total day calories
function countCaloriesSum(data, day_id) {
    for (day of data) {
        if (day.day_id == day_id) {
            let caloriesSum = 0;
            for (item of day.day_items) {
                caloriesSum += item.cal;
            }
            return caloriesSum;
        }

    }
}

function getCounterElement(id, caloriesSum) {
    document.getElementById("day" + id + "-counter").innerHTML = caloriesSum + " cal";
}


// Changes buttons attributes in searchdialog
function setElementID(id, dbDayID) {
    let meal_type = null;
    for (v in symbolTable) {
        if (symbolTable[v].includes(id.split('-')[4])) {
            meal_type = v;
        }
    }
    new_id = id.split("-").slice(1).join("-");
    var buttons = document.getElementsByClassName('addMealButtonSelector');
    for (var i = 0; i < buttons.length; i++) {
        let attributeToChange = buttons[i].getAttribute('onclick');
        var regex = /\(([^)]+)\)/;
        var matches = regex.exec(attributeToChange);
        var atributesArray = matches[1].split(',');
        atributesArray[0] = new_id;
        for (var j = 1; j < 4; j++) {
            atributesArray[j] = atributesArray[j].replace(/["']/g, '')
            if (j != 2) {
                atributesArray[j] = atributesArray[j].replace(/\s/g, "");
            }
        }
        buttons[i].setAttribute('onclick', `addMealToDay('${atributesArray[0]}', '${atributesArray[1]}', '${atributesArray[2]}', '${atributesArray[3]}', '${meal_type}', '${dbDayID}', 'true');`);
    }
}


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
    if (recepieDiv.classList.contains('show')) {
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
    let dayId = elementName[0].slice(3);
    checkBox = document.getElementById(name);
    container = document.getElementById(name);
    containerBody = document.getElementById(elementName[0]);
    containerHeader = document.getElementById(elementName[0] + "-edit");
    containerHeaderOptions = document.getElementById(elementName[0] + "-edit-options");

    if (checkBox.checked) {
        shopListSelectedDays.push(dayId);
        containerBody.style.backgroundColor = "var(--bs-gray-200)";
        containerHeader.style.backgroundColor = "var(--bs-gray-600)";
        containerHeaderOptions.style.backgroundColor = "var(--bs-gray-600)";
        // document.getElementById("createShopList").style.display = "none";
        document.getElementById("generateShopList").classList.remove("generate-shoplist-button");
        document.getElementById("generateShopList").style.display = "block";
    } else {
        shopListSelectedDays = shopListSelectedDays.filter(item => item !== dayId);
        containerBody.style.backgroundColor = "var(--white)";
        containerHeader.style.backgroundColor = "var(--breakfast-color)";
        containerHeaderOptions.style.backgroundColor = "var(--breakfast-color)";
        if (shopListSelectedDays.length < 1) {
            // document.getElementById("createShopList").style.display = "block";
            document.getElementById("generateShopList").style.display = "none";
        }

    }
}


let showMealModal = (id) => {
    dayId = id;
    const myModal = document.getElementById('staticBackdrop');
    const oldButton = document.getElementById('dayAddButtonID');
    oldButton.remove();
    let newSelectedModal = document.getElementById('modalForm');
    let newButton = modalButtonTemplate(id);
    newSelectedModal.insertAdjacentHTML('afterend', newButton);


    // Create a new Bootstrap Modal instance
    const modal = new bootstrap.Modal(myModal);

    // Show the modal
    modal.show();

}


let showSearchMealModal = (id) => {
    dbdDayID = id.split("-")[2];
    setElementID(id, dbdDayID);
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

/**Is creating element in user day
 * 
 * @param {string} id - Element id
 * 
 * */
let addDishMeal = (id) => {
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
    // let modalTemplate = document.getElementById('dayAddButtonID');
    // modalTemplate.insertAdjacentHTML('beforeend', buttonTemplate(id) );

}

/**Is deleting element in user day
 * 
 * @param {string} id - Element id
 * 
 * */
let deleteMealElement = (id) => {
    let selectedElement = document.getElementById(id);
    selectedElement.remove();
    let selectedElementCollapse = document.getElementById("day" + id + "-collapse");
    if (selectedElementCollapse) {
        selectedElementCollapse.remove();
    }
}

/**Is deleting element in user day, which was populated with dish
 * 
 * @param {string} id - Element id
 * 
 * */
let deleteMealOptionElement = (id, day_id, meal_id) => {
    deleteMealInDb(day_id, meal_id);
    let selectedElement = document.getElementById(id);
    selectedElement.remove();
    let selectedOptionsElement = document.getElementById(id + "-edit-options");
    selectedOptionsElement.remove();
    let selectedOptionsElementCollapse = document.getElementById(id + "-collapse");
    selectedOptionsElementCollapse.remove();

}

/**Is deleting day
 * 
 * @param {string} id - Element id
 * 
 * */
let deleteDay = (id) => {
    deleteDayInDb(id);
    let dayElement = document.getElementById(id + '-container');
    dayElement.remove();
}

let removeSearchResults = () => {
    const toRemove = document.querySelectorAll(".product-search-result");
    toRemove.forEach(element => {
        element.remove();
    });
}

function searchProduct() {
    var inputValue = document.getElementById("dish_product_search").value;
    const toRemove = document.querySelectorAll(".product-search-result");
    if (inputValue.length >= 3) {
        fetchSearchReasultsFromWeb(inputValue);
    } else {
        if (toRemove) {
            removeSearchResults();
        }
    }


}


const debounce = (mainFunction, delay) => {
    let timer;
    return function () {
        clearTimeout(timer);
        timer = setTimeout(() => {
            mainFunction();
        }, delay);
    };
};


const debouncedSearchData = debounce(searchProduct, 1000);


/**Download product data from db
 * 
 * @param {string}searchQuery - product name
 * 
 * */
function fetchSearchReasultsFromWeb(searchQuery) {
    showProductSpiner();
    fetch(SEARCH_DATA_URL + searchQuery)
        .then(response => response.json())
        .then(data => {
            hideProductSpiner();
            var parsedData = JSON.parse(data.results);
            generateSearchResults(parsedData);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}






/**Adding and removing searchr results to template
 * 
 * @param {string}searchQuery - product name
 * 
 * */
let generateSearchResults = (data) => {
    var getParent = document.getElementById("productBox");
    removeSearchResults();
    for (element of data) {
        getParent.insertAdjacentHTML('afterend', searchResultTemplate(element.product_name, element.id));
    }
}



if (productLoader) {
    productLoader.style.display = 'none';
}

if (saveButtonContainer) {
    saveButtonContainer.style.display = 'none';
}

if (productsContainerHeader) {
    productsContainerHeader.style.visibility = 'hidden';
}

if (saveButton) {
    saveButton.disabled = true;
}

if (productContainer) {
    productContainer.style.display = 'none';
}

if (saveDishButton) {
    saveDishButton.disabled = true;
}


let showProductContainer = () => {
    productContainer.style.display = 'flex';
    saveButtonContainer.style.display = 'flex';
    saveButton.disabled = true;
    addContainertBox.style.display = "none";
}

let saveProduct = () => {
    productContainer.style.display = 'none';
    saveButtonContainer.style.display = 'none';
    const productListBox = document.getElementById("productsList");
    const productName = document.getElementById("dish_product_search");
    const productAmount = document.getElementById("dish_product_amount");
    const productUnit = document.getElementById("product_unit");

    let productsContainer = document.getElementById("addProductContainer");
    let productsSearchContainer = document.getElementById("dishProductSearchContainer");
    if (!productsSearchContainer) {
        productsContainer.insertAdjacentHTML('afterbegin', dishProductSearchContainer());
    }

    if (tempAddedProduct != null) {
        tempAddedProduct.amount = productAmount.value;
        tempAddedProduct.unit = productUnit.value;
        productList.push(tempAddedProduct);
    }


    productListBox.insertAdjacentHTML('afterend', productListItem(productName.value, productAmount.value, productUnit.value));
    let inputAmount = document.getElementById("dish_product_amount");
    let inputProduct = document.getElementById("dish_product_search");
    inputAmount.value = '';
    inputProduct.value = '';
    addContainertBox.style.display = "block";
    productsContainerHeader.style.visibility = "visible";

}

let productCancelButton = () => {
    let inputAmount = document.getElementById("dish_product_amount");
    let inputProduct = document.getElementById("dish_product_search");
    productContainer.style.display = 'none';
    saveButtonContainer.style.display = 'none';
    addContainertBox.style.display = "block";
    if (inputAmount) {
        inputProduct.value = '';
    }
    if (inputProduct) {
        inputProduct.value = '';
    }
    removeSearchResults();
}

let showProductSpiner = () => {
    productLoader.style.display = 'flex';
}

let hideProductSpiner = () => {
    productLoader.style.display = 'None';
}

let chooseProduct = (name, id) => {
    tempAddedProduct = { "name": name, "id": id };
    const searchbox = document.getElementById("dish_product_search");
    searchbox.value = name;
    removeSearchResults();
}

let checkProductFieldsValidity = () => {
    const productName = document.getElementById("dish_product_search");
    const productAmount = document.getElementById("dish_product_amount");
    const productUnit = document.getElementById("product_unit");
    if (productName.checkValidity() == true && productAmount.checkValidity() == true && productAmount.value > 0 && productUnit.checkValidity() == true) {
        saveButton.disabled = false;
    } else {
        saveButton.disabled = true;
    }
}


let checkDishFielsdValidity = () => {
    const dishDescription = document.getElementById("dishDescription");
    const dishTitle = document.getElementById("dish_title");
    const dishCalories = document.getElementById("dish_calories");
    const dishDuration = document.getElementById("duration");
    const dishType = document.getElementById("type_of_meal");
    if (dishTitle.checkValidity() == true && dishCalories.checkValidity() == true && dishDuration.checkValidity() == true && dishType.checkValidity() == true && dishDescription.checkValidity() == true, productList.length > 0) {
        saveDishButton.disabled = false;
    } else {
        saveDishButton.disabled = true;
    }
}

let saveDishButtonClick = () => {
    const productName = document.getElementById("dish_product_search");
    const productAmount = document.getElementById("dish_product_amount");
    const productJson = document.getElementById("json_data")
    productName.required = false;
    productAmount.required = false;
    productJson.value = JSON.stringify(productList);
}

let cancelDishButtonClick = () => {
    window.location.href = '/user/dashboard';
}

let deleteMealInDb = (day_id, meal_id) => {
    fetch(DELETE_MEAL + day_id + "/" + meal_id)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            fetchDataFromWeb(updateCookies);
            fetchDataFromWeb(countCalories);
        }).catch(error => {
            console.log('Error fetching data:', error);
        });
}


let deleteDayInDb = (day_id) => {
    let id = day_id.split("day")[1];
    fetch(DELETE_DAY + id)
        .then(response => response.json())
        .then(data => {
            fetchDataFromWeb(updateCookies);
            checkIfShopListButtonExist();
        }).catch(error => {
            console.log('Error fetching data:', error);
        });
}



let countCalories = (newData) => {
    dayData = JSON.parse(newData);
    for (day of dayData) {
        updateCalories(dayData, day.day_id);
    }
}

let copyMeal = (element_id, day_id, dish_id) => {
    fetch(COPY_DISH + day_id + "/" + dish_id + "/" + element_id)
        .then(response => response.json())
        .then(data => {
            let elementData = JSON.parse(data);
            addMealToDay(elementData.element_id, elementData.slug, elementData.name, elementData.cal, elementData.type, elementData.day_id, elementData.new_element)
        }).catch(error => {
            console.log('Error fetching data:', error);
        });

}

let copyDay = async (day_id) => {
    try {
        const response = await fetch(COPY_DAY + day_id.split("day")[1]);
        const data = await response.json();
        let new_day_id = await addNewDay(true);
        let temp = await JSON.parse(data);
        temp.day_id = new_day_id;
        let new_data = JSON.stringify(temp);
        dayChange(new_data, true);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


/**Download product data from db
 * 
 * @param {string}searchQuery - recepie name
 * 
 * */

async function fetchRecepieSearchResultsFromWeb(searchQuery) {
    try {
        const response = await fetch(SEARCH_RECEPIE_URL + searchQuery);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

let searchRecepie = () => {
    let inputValue = document.getElementById("search").value;
    if (inputValue.length > 2) {
        fetchRecepieSearchResultsFromWeb(inputValue).then(data => {
            console.log(data.dish_data);
            recepieSearchResultItem(data.dish_data);
        }).catch(error => {
            console.error('Error logging data:', error);
        });
    } else {
        recepieSearchResultItem("");
        console.log("to short");
    }
}


async function getDaysProductsList() {
    var daysId = "";
    var daysId = shopListSelectedDays.join(",");
    try {
        const response = await fetch(DAYS_PRODUCTS_LIST + daysId);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        window.location.href = '/user/shoplist';
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}


let valueUp = () => {
    persons += 1;
    document.getElementById("personsCounter").innerHTML = "Liczba osób: " + persons;
    updateAmounts("recepie-amount");
    updateAmounts("recepie-amount-print");
};


let valueDown = () => {
    if (persons > 1) {
        persons -= 1;
        document.getElementById("personsCounter").innerHTML = "Liczba osób: " + persons;
        updateAmounts("recepie-amount");
        updateAmounts("recepie-amount-print");
    }
};


// Updates values in shoplist template
let updateAmounts = (clasname) => {
    const values = document.getElementsByClassName(clasname);
    let v = [...values];
    if (baseAmounts.length < 1) {
        baseAmounts = v.map(element => parseInt((element.textContent).split(" ")[0], 10));
        baseAmountsUnits = v.map(element => element.textContent.split(" ")[1]);
    }
    let tempAmount = baseAmounts.map(item => item * persons);
    v.forEach((v, k) => {
        values[k].textContent = tempAmount[k] + " " + baseAmountsUnits[k];
    });

}

let exportFile = () => {
    // Get the content from the container
    const content = document.getElementById('exportDiv').innerHTML;
    // Create a Blob from the content
    const blob = new Blob([content], { type: 'text/html' });

    // Create a link element
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'shoplist.html';

    // Append the link to the body
    document.body.appendChild(link);

    // Programmatically click the link to trigger the download
    link.click();

    // Remove the link from the document
    document.body.removeChild(link);
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue;
}

// Favourite star in template toggle
function replaceImage(slug) {
    const img = document.getElementById("starImage");
    const currentSrc = img.src;
    if (currentSrc.includes("star.svg")) {
        img.src = "/static/img/star_full.svg";
        addToFavourite(slug);
    } else {
        img.src = "/static/img/star.svg";
        removeFromFavourite(slug);
    }

}


function copyToClipboard(url) {
    let site = window.location.protocol + "//" + window.location.host + url;
    navigator.clipboard.writeText(site).then(() => {
        alert('Link copied to clipboard: ' + site); 
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}

function addToFavourite(slug) {
    fetch('addfavourite/' + slug, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            slug: slug
        })
    })
        .then(response => response.json())
        .then(data => {
            let valueCheck = JSON.parse(data);
            console.log(valueCheck.favourite_data[0].id);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function removeFromFavourite(slug) {
    fetch('removefavourite/' + slug, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            slug: slug
        })
    })
        .then(response => response.json())
        .then(data => {
            let valueCheck = JSON.parse(data);
            console.log(valueCheck);
            console.log(valueCheck.favourite_data[0].id);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });

}


async function getUserRecepies() {
    let expandImage = document.getElementById("expandImage");
    try {
        const response = await fetch(SEARCH_USER_RESEPIES);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        if(expandValue){
        let numberOfDisplayedElements = document.getElementsByClassName("user-recepie-container").length;
        if (data.userDishes.length > numberOfDisplayedElements) {
            let dishList = data.userDishes.slice(numberOfDisplayedElements,);
            let selectedParent = document.getElementById('yourDishes');
            let counter = numberOfDisplayedElements;
            for (element of dishList) {
                counter += 1;
                let newDishElement = userRecepiesTemplate(element, counter);
                selectedParent.insertAdjacentHTML('afterend', newDishElement);
            }
            
            expandImage.style.transform = "rotate(180deg)";
        }
        }
        if (!expandValue) {
            let userRecepiesList = document.querySelectorAll(".user-recepie-class");
            expandImage.style.transform = "rotate(360deg)";
            if (userRecepiesList.length >= 2){
                userRecepiesList.forEach((element, index) =>{
                    if(index > 2){
                        element.remove();
                    }
    
                });
            }
           
        }
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

if(document.getElementById('expandImage')){
    document.getElementById('expandImage').addEventListener('click', ()=>{
        expandValue = !expandValue;
    });
}

function removeFromShoplist(id) {
    let elementToRemove = document.getElementById(id);
    elementToRemove.remove();
}
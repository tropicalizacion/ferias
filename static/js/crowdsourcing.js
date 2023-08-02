// --------------------
// Opening hours inputs
// --------------------

var inputCount = 0;

function addOpeningDaysInput() {
    inputCount++;

    // Get the input container
    var inputContainer = document.getElementById("opening-days");

    // Create the title element
    var titleElement = document.createElement("h6");
    titleElement.textContent = "Jornada de operación " + inputCount;

    // Create the div row element
    var divRowElement = document.createElement("div");
    divRowElement.classList.add("row");
    divRowElement.classList.add("mb-3");

    // Create the div element 1
    var divElement1 = document.createElement("div");
    divElement1.classList.add("mb-3");
    divElement1.classList.add("col-md-4");

    // Create the label element 1
    var labelElement1 = document.createElement("label");
    labelElement1.setAttribute("for", "day_opens_" + inputCount);
    labelElement1.classList.add("form-label");
    labelElement1.textContent = "Día de la semana";

    // Create the select element 1
    var selectElement1 = document.createElement("select");
    selectElement1.classList.add("underline-input");
    selectElement1.setAttribute("id", "day_opens_" + inputCount);
    selectElement1.setAttribute("name", "day_opens_" + inputCount);
    selectElement1.setAttribute("aria-label", "Seleccione una opción");
    selectElement1.setAttribute("required", "required");

    // Create the default option
    var defaultOption1 = document.createElement("option");
    defaultOption1.setAttribute("selected", "selected");
    defaultOption1.textContent = "Seleccione una opción";
    selectElement1.appendChild(defaultOption1);

    // Add options for the days of the week
    var dayChoices = [
        ["Mo", "Lunes"],
        ["Tu", "Martes"],
        ["We", "Miércoles"],
        ["Th", "Jueves"],
        ["Fr", "Viernes"],
        ["Sa", "Sábado"],
        ["Su", "Domingo"]
    ];
    for (var i = 0; i < dayChoices.length; i++) {
        var option = document.createElement("option");
        option.setAttribute("value", dayChoices[i][0]);
        option.textContent = dayChoices[i][1];
        selectElement1.appendChild(option);
    }

    // Append the label and select elements to the div element
    divElement1.appendChild(labelElement1);
    divElement1.appendChild(selectElement1);

    // Create the div element 2
    var divElement2 = document.createElement("div");
    divElement2.classList.add("mb-3");
    divElement2.classList.add("col-md-4");

    // Create the label element 2
    var labelElement2 = document.createElement("label");
    labelElement2.setAttribute("for", "hour_opens_" + inputCount);
    labelElement2.classList.add("form-label");
    labelElement2.textContent = "Hora de apertura";

    // Create the time input element 2
    var inputElement2 = document.createElement("input");
    inputElement2.classList.add("underline-input");
    inputElement2.setAttribute("type", "time");
    inputElement2.setAttribute("id", "hour_opens_" + inputCount);
    inputElement2.setAttribute("name", "hour_opens_" + inputCount);
    inputElement2.setAttribute("required", "required");

    // Append the label and input elements to the div element
    divElement2.appendChild(labelElement2);
    divElement2.appendChild(inputElement2);

    // Create the div element 3
    var divElement3 = document.createElement("div");
    divElement3.classList.add("mb-3");
    divElement3.classList.add("col-md-4");

    // Create the label element 3
    var labelElement3 = document.createElement("label");
    labelElement3.setAttribute("for", "hour_closes_" + inputCount);
    labelElement3.classList.add("form-label");
    labelElement3.textContent = "Hora de cierre";

    // Create the time input element 3
    var inputElement3 = document.createElement("input");
    inputElement3.classList.add("underline-input");
    inputElement3.setAttribute("type", "time");
    inputElement3.setAttribute("id", "hour_closes_" + inputCount);
    inputElement3.setAttribute("name", "hour_closes_" + inputCount);
    inputElement3.setAttribute("required", "required");

    // Append the label and input elements to the div element
    divElement3.appendChild(labelElement3);
    divElement3.appendChild(inputElement3);

    // Append the div elements to the div row element
    divRowElement.appendChild(divElement1);
    divRowElement.appendChild(divElement2);
    divRowElement.appendChild(divElement3);

    // Append the div elements to the input container
    inputContainer.appendChild(titleElement);
    inputContainer.appendChild(divRowElement);
}

function deleteOpeningDaysInput() {
    if (inputCount > 0) {
        inputCount--;

        // Get the input container
        var inputContainer = document.getElementById("opening-days");

        // Remove the last childs
        inputContainer.removeChild(inputContainer.lastChild);
        inputContainer.removeChild(inputContainer.lastChild);
    }
}

// ----------------------------
// Phone, email and link inputs
// ----------------------------

var phoneInputCount = 0;

function addPhoneInput() {
    phoneInputCount++;

    // Get the input container
    var inputContainer = document.getElementById("phones");

    // Create the input element
    var inputElement = document.createElement("input");
    inputElement.classList.add("underline-input");
    inputElement.classList.add("mb-2");
    inputElement.setAttribute("type", "text");
    inputElement.setAttribute("id", "phone_" + phoneInputCount);
    inputElement.setAttribute("name", "phone_" + phoneInputCount);
    inputElement.setAttribute("placeholder", "Teléfono " + phoneInputCount);
    inputElement.setAttribute("style", "width: 100%;");
    inputElement.setAttribute("required", "required");

    // Append the input element to the input container
    inputContainer.appendChild(inputElement);

    // Focus on the new input
    inputElement.focus();
}

// Create button to delete last phone input
function deletePhoneInput() {
    if (phoneInputCount > 0) {
        phoneInputCount--;
        
        // Get the input container
        var inputContainer = document.getElementById("phones");

        // Remove the last child
        inputContainer.removeChild(inputContainer.lastChild);
    }
}


var emailInputCount = 0;

function addEmailInput() {
    emailInputCount++;

    // Get the input container
    var inputContainer = document.getElementById("emails");

    // Create the input element
    var inputElement = document.createElement("input");
    inputElement.classList.add("underline-input");
    inputElement.classList.add("mb-2");
    inputElement.setAttribute("type", "email");
    inputElement.setAttribute("id", "email_" + emailInputCount);
    inputElement.setAttribute("name", "email_" + emailInputCount);
    inputElement.setAttribute("placeholder", "Correo electrónico " + emailInputCount);
    inputElement.setAttribute("style", "width: 100%;");
    inputElement.setAttribute("required", "required");

    // Append the input element to the input container
    inputContainer.appendChild(inputElement);

    // Focus on the new input
    inputElement.focus();
}

// Create button to delete last email input
function deleteEmailInput() {
    if (emailInputCount > 0) {
        emailInputCount--;

        // Get the input container
        var inputContainer = document.getElementById("emails");

        // Remove the last child
        inputContainer.removeChild(inputContainer.lastChild);
    }
}

var linkInputCount = 0;

function addLinkInput() {
    linkInputCount++;

    // Get the input container
    var inputContainer = document.getElementById("links");

    // Create the input element
    var inputElement = document.createElement("input");
    inputElement.classList.add("underline-input");
    inputElement.classList.add("mb-2");
    inputElement.setAttribute("type", "text");
    inputElement.setAttribute("id", "link_" + linkInputCount);
    inputElement.setAttribute("name", "link_" + linkInputCount);
    inputElement.setAttribute("placeholder", "Link " + linkInputCount);
    inputElement.setAttribute("style", "width: 100%;");
    inputElement.setAttribute("required", "required");

    // Append the input element to the input container
    inputContainer.appendChild(inputElement);

    // Focus on the new input
    inputElement.focus();
}

// Create button to delete last link input
function deleteLinkInput() {
    if (linkInputCount > 0) {
        linkInputCount--;

        // Get the input container
        var inputContainer = document.getElementById("links");

        // Remove the last child
        inputContainer.removeChild(inputContainer.lastChild);
    }
}

// A function to ask the user to confirm the submission of the form when clicking the submit button
function confirmSubmission(event) {
    var confirmation = confirm("¿Desea enviar el formulario de sugerencias?");

    if (!confirmation) {
        event.preventDefault();
    }
}

show_hide_beat_creation_methods()

// Beat Generation: Show/Hide beat creation methods
function show_hide_beat_creation_methods() {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('DOM is loaded');
        let bc_options = document.querySelectorAll('.bc_option');
        for (let op of bc_options) {
            op.style.display = "none";
        }
    });

    const number_of_beats_element = document.querySelector("#number_of_beats");
    const cfs_per_beat_element = document.querySelector("#cfs_per_beat");

    let beat_creation_method_element = document.querySelector('#beat_creation_method');
    let beat_creation_method_id = document.querySelector('#beat_creation_method_id');


    beat_creation_method_element.addEventListener('change', () => {
        console.log("Beat creation method changed");

        let value = beat_creation_method_id.value;
        console.log(`Beat creation method value: ${value}`);

        if (value === "ATTRIBUTE_TARGET") {
            console.log("Case-1")
            cfs_per_beat_element.style.display = "block"
            number_of_beats_element.style.display = "none"
        } else if (value === "NUMBER_ZONES_AND_ATTRIBUTE") {
            console.log("Case-2")
            cfs_per_beat_element.style.display = "none"
            number_of_beats_element.style.display = "block"
        } else {
            number_of_beats_element.style.display = "none"
            cfs_per_beat_element.style.display = "none"
        }
    })
}


// DROP ZONE
let elOne = document.getElementById("div_id_city_shapefile");
let orDiv = document.createElement("div");
orDiv.innerHTML = "<p style='font-weight:bold'>OR</p>";
orDiv.style.marginLeft = "40px";
orDiv.style.marginRight = "40px";
orDiv.style.display = "flex";
orDiv.style.alignItems = "center";
elOne.insertAdjacentElement("afterend", orDiv);

let newNode = document.createElement("span");
newNode.innerHTML = "Drop file here or click to upload";
newNode.classList.add("drop-zone__prompt");

let parentDivOne = document.getElementById("id_city_shapefile").parentNode;
parentDivOne.classList.add("drop-zone");
parentDivOne.insertBefore(newNode, parentDivOne.firstChild);

let newNodeOne = document.createElement("span");
newNodeOne.innerHTML = "Drop file here or click to upload";
newNodeOne.classList.add("drop-zone__prompt");

let parentDivTwo = document.getElementById("id_crime_data").parentNode;
parentDivTwo.classList.add("drop-zone");
parentDivTwo.insertBefore(newNodeOne, parentDivTwo.firstChild);

document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
        inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
        if (inputElement.files.length) {
            updateThumbnail(dropZoneElement, inputElement.files[0]);
        }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
        dropZoneElement.addEventListener(type, (e) => {
            dropZoneElement.classList.remove("drop-zone--over");
        });
    });

    dropZoneElement.addEventListener("drop", (e) => {
        e.preventDefault();

        if (e.dataTransfer.files.length) {
            inputElement.files = e.dataTransfer.files;
            updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
        }

        dropZoneElement.classList.remove("drop-zone--over");
    });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
        dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
        thumbnailElement = document.createElement("div");
        thumbnailElement.classList.add("drop-zone__thumb");
        dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () => {
            thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
        };
    } else {
        thumbnailElement.style.backgroundImage = null;
    }
}

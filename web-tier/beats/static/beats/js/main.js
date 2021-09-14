function show_beat_gen_attribute() {
  const beat_creation_method_element = document.getElementById(
    "beat_creation_method"
  );
  const number_of_beats_element = document.getElementById("number_of_beats");
  const cfs_per_beat_element = document.getElementById("cfs_per_beat");

  if (beat_creation_method_element.value === "ATTRIBUTE_TARGET") {
    number_of_beats_element.style.display = "none";

    if (cfs_per_beat_element.style.display === "none") {
      cfs_per_beat_element.style.display = "block";
    }
  } else if (
    beat_creation_method_element.value === "NUMBER_ZONES_AND_ATTRIBUTE"
  ) {
    cfs_per_beat_element.style.display = "none";

    if (number_of_beats_element.style.display === "none") {
      number_of_beats_element.style.display = "block";
    }
  } else {
    if (cfs_per_beat_element.style.display === "none") {
      cfs_per_beat_element.style.display = "block";
    }
    if (number_of_beats_element.style.display === "none") {
      number_of_beats_element.style.display = "block";
    }
  }
}

// DROP ZONE
let elOne = document.getElementById("div_id_beats_shapefile");
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

let parentDivOne = document.getElementById("id_beats_shapefile").parentNode;
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

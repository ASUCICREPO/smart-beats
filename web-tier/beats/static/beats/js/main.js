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
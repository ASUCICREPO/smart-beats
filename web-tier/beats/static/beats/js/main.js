function show_beat_gen_attribute() {
    const beat_creation_method_element = document.getElementById('beat_creation_method');
    const number_of_beats_element = document.getElementById('number_of_beats');
    const cfs_per_beat_element = document.getElementById('cfs_per_beat');

    if (beat_creation_method_element.value === 'ATTRIBUTE_TARGET') {
        number_of_beats_element.style.display = 'none';

        if (cfs_per_beat_element.style.display === "none") {
            cfs_per_beat_element.style.display = 'block';
        }
    } else if (beat_creation_method_element.value === 'NUMBER_ZONES_AND_ATTRIBUTE') {
        cfs_per_beat_element.style.display = 'none';

        if (number_of_beats_element.style.display === "none") {
            number_of_beats_element.style.display = 'block';
        }
    } else {
        if (cfs_per_beat_element.style.display === "none") {
            cfs_per_beat_element.style.display = 'block';
        }
        if (number_of_beats_element.style.display === "none") {
            number_of_beats_element.style.display = 'block';
        }
    }
}

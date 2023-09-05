function get_album_by_id(list_of_artist_albums, list_of_other_albums, album_id) {
    for (let i = 0; i < list_of_artist_albums; i++) {
        if (list_of_artist_albums[i]["id"] === album_id) {
            return list_of_artist_albums[i];
        }
    }

    for (let i = 0; i < list_of_other_albums; i++) {
        if (list_of_other_albums[i]["id"] === album_id) {
            return list_of_other_albums[i];
        }
    }
}

function get_track_by_id(list_of_tracks, track_id) {
    for (let i = 0; i < list_of_tracks.length; i++) {
        if (list_of_tracks[i]["id"] === track_id) {
            return list_of_tracks[i];
        }
    }
}

function refactorIncrementation(all_div_track) {
    let j = 1;
    for (let i = 0; i < all_div_track.length; i++) {
        let div_track = all_div_track[i];
        if (div_track.style.getPropertyValue("display") !== "none") {
            div_track.childNodes[1].textContent = j;
            j++;
        }
    }
}


/*
 * ###########################################################
 * #                      SEARCH BAR                         #
 * ###########################################################
 */


function search(event, all_div_track, list_of_tracks, search_in_album, listOfValues, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked) {
    let value = event.target.value.toLowerCase();

    if (value === "") {
        /*// Reset the search
        for (let i = 0; i < all_div_track.length; i++) {
            all_div_track[i].style.setProperty("display", "", "important");
        }*/
        allDivTrackModifier(listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked)
    } else {
        // Display only divs track who have value in dataset
        for (let i = 0; i < list_of_tracks.length; i++) {
            let track = list_of_tracks[i];
            let div_track = document.getElementById(track["id"]);
            let track_artists = div_track.getElementsByClassName("div_track_artist")[0].innerText.toLowerCase();

            if (search_in_album && div_track.style.display === "" && (track["name"].toLowerCase().includes(value) || track_artists.includes(value) || track["album"]["name"].toLowerCase().includes(value))) {
                div_track.style.setProperty("display", "", "important");
            } else if (!search_in_album && div_track.style.display === "" && (track["name"].toLowerCase().includes(value) || track_artists.includes(value))) {
                div_track.style.setProperty("display", "", "important");
            } else {
                div_track.style.setProperty("display", "none", "important");
            }
        }
    }

    refactorIncrementation(all_div_track);
}


/*
 * ###########################################################
 * #                          SORTS                          #
 * ###########################################################
 */


function sortTracks(event, current_sort_value, sort_order, list_of_tracks, div_track_list, all_div_track) {
    // Get select option value
    let value = event.target.value;

    // If value is equal to 'ignore' do nothing
    if (value === "ignore") {
        return null;
    }

    // If already selected change sort order
    if (value === current_sort_value) {
        sort_order = (sort_order + 1) % 2;
    } else {
        current_sort_value = value;
        sort_order = 0;

        // Remove the class for the green color and font weight
        for (let i = 0; i < event.target.options.length; i++) {
            event.target.options[i].classList.remove("sortOptionSelected");
            // Delete the arrow of the old selected option
            if (event.target.options[i].text.includes("↑") || event.target.options[i].text.includes("↓")) {
                event.target.options[i].text = event.target.options[i].text.slice(0, -2);
            }
        }

        // Add class to selected option to change text color and weight
        event.target.options[event.target.selectedIndex].classList.add("sortOptionSelected");
    }


    // Sort the list_of_tracks
    let temp;
    for (let i = 0; i < list_of_tracks.length; i++) {
        let swapIndex = i;
        for (let j = i; j < list_of_tracks.length; j++) {
            // Get value
            let swapIndexValue, jValue;
            if (value === "album_name") {
                if (list_of_tracks[swapIndex]["album"]["album_type"].toLowerCase() === "single" && list_of_tracks[swapIndex]["album"]["total_tracks"] === 1) {
                    swapIndexValue = "single";
                } else {
                    swapIndexValue = list_of_tracks[swapIndex]["album"]["name"].toLowerCase();
                }

                if (list_of_tracks[j]["album"]["album_type"].toLowerCase() === "single" && list_of_tracks[j]["album"]["total_tracks"] === 1) {
                    jValue = "single";
                } else {
                    jValue = list_of_tracks[j]["album"]["name"].toLowerCase();
                }
            } else if (value === "release_date") {
                swapIndexValue = list_of_tracks[swapIndex]["album"]["release_date"];
                jValue = list_of_tracks[j]["album"]["release_date"];
            } else if (value === "artist") {
                swapIndexValue = document.getElementById(list_of_tracks[swapIndex]["id"]).getElementsByClassName("div_track_artist")[0].innerText.toLowerCase();
                jValue = document.getElementById(list_of_tracks[j]["id"]).getElementsByClassName("div_track_artist")[0].innerText.toLowerCase();
            } else {
                swapIndexValue = list_of_tracks[swapIndex][value];
                jValue = list_of_tracks[j][value];

                if (typeof (swapIndexValue) === "string") {
                    swapIndexValue = swapIndexValue.toLowerCase();
                    jValue = jValue.toLowerCase();
                }
            }

            if (swapIndexValue > jValue) {
                swapIndex = j;
            } else if (swapIndexValue === jValue) {
                // If same value sort by init value
                if (list_of_tracks[swapIndex]["init"] > list_of_tracks[j]["init"]) {
                    swapIndex = j;
                }
            }
        }

        temp = list_of_tracks[swapIndex];
        list_of_tracks[swapIndex] = list_of_tracks[i];
        list_of_tracks[i] = temp;
    }

    let sort = []
    for (let i = 0; i < list_of_tracks.length; i++) {
        sort.push(document.getElementById(list_of_tracks[i]["id"]));
    }

    // Clear div track list
    div_track_list.replaceChildren();

    // If sort order is equal to 0 sort by croissant order else inverse order
    if (sort_order === 0) {
        for (let i = 0; i < sort.length; i++) {
            div_track_list.appendChild(sort[i]);
        }
    } else {
        for (let i = sort.length - 1; i >= 0; i--) {
            div_track_list.appendChild(sort[i]);
        }
    }

    refactorIncrementation(all_div_track);

    // Delete the arrow at the end of the selected option
    if (event.target.options[event.target.selectedIndex].text.includes("↑") || event.target.options[event.target.selectedIndex].text.includes("↓")) {
        event.target.options[event.target.selectedIndex].text = event.target.options[event.target.selectedIndex].text.slice(0, -2);
    }

    // Add arrow at the end of the selected option
    if (sort_order === 0) {
        event.target.options[event.target.selectedIndex].text = event.target.options[event.target.selectedIndex].text + " ↑";
    } else {
        event.target.options[event.target.selectedIndex].text = event.target.options[event.target.selectedIndex].text + " ↓"
    }

    // Change the "Sort by :" text and the selected value
    event.target.options[event.target.options.length - 1].text = "Sort by : " + event.target.options[event.target.selectedIndex].text;
    event.target.options[event.target.options.length - 1].selected = "selected";

    return [current_sort_value, sort_order];
}


/*
 * ###########################################################
 * #                        FILTERS                          #
 * ###########################################################
 */


function filterTracks(event, listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked) {
    // Get filter option value
    let value = event.target.value;

    // If value is equal to 'ignore' do nothing
    if (value === "ignore") {
        return null;
    }

    if (listOfValues.includes(value)) {
        // Remove value from the list
        listOfValues.splice(listOfValues.indexOf(value), 1);
        event.target.options[event.target.selectedIndex].classList.remove("filterOptionSelected");
    } else {
        // Add value to the list
        listOfValues.push(value);
        event.target.options[event.target.selectedIndex].classList.add("filterOptionSelected");
    }

    verifListOfValues(listOfValues);
    allDivTrackModifier(listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked);
    refactorIncrementation(all_div_track);

    event.target.options[event.target.options.length - 1].selected = "selected";
}

// Fill if the list of values is empty
function verifListOfValues(listOfValues) {
    if (listOfValues.length === 0) {
        for (let i = 1; i < selectFilter.options.length - 1; i++) {
            listOfValues.push(selectFilter.options[i].value);
            selectFilter.options[i].classList.add("filterOptionSelected");
        }
    }
}

function allDivTrackModifier(listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked) {
    // Hide all div tracks
    for (let i = 0; i < list_of_tracks.length; i++) {
        let track = list_of_tracks[i];
        let div_track = document.getElementById(track["id"])
        div_track.style.setProperty("display", "none", "important");
    }

    // Show div tracks corresponding to values in the list of values
    for (let i = 0; i < listOfValues.length; i++) {
        let value = listOfValues[i];
        let list = [];
        if (value === "album") {
            list = tracks_from_album;
        } else if (value === "non_album") {
            list = tracks_from_other;
        } else if (value === "featuring") {
            list = tracks_featuring;
        }

        for (let j = 0; j < list.length; j++) {
            let track_id = list[j];
            let track = get_track_by_id(list_of_tracks, track_id);
            let div_track = document.getElementById(track_id);

            if (isShowCopyChecked) {
                div_track.style.setProperty("display", "", "important");
            } else {
                if (!track["is_copy"]) {
                    div_track.style.setProperty("display", "", "important");
                }
            }
        }
    }
}

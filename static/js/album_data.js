const tracks_from_album = [];
const tracks_from_other = [];
const tracks_featuring = [];

const div_track_list = document.getElementById("div_track_list");
const all_div_track = div_track_list.children;

for (let i = 0; i < list_of_tracks.length; i++) {
    let track = list_of_tracks[i];
    track["init"] = i;
    track["album"] = album;

    if (track["artists"].length > 1) {
        tracks_featuring.push(track["id"]);
    } else {
        tracks_from_album.push(track["id"]);
    }
}

const searchBar = document.getElementById("searchBar");
searchBar.addEventListener("input", function () {
    search(event, all_div_track, list_of_tracks, false, listOfValues, tracks_from_album, tracks_from_other, tracks_featuring, true);
});

/*
 * ###########################################################
 * #                          SORTS                          #
 * ###########################################################
 */

const sortSelector = document.getElementById("selectSort");
let current_sort_value = "init";
let sort_order = 0;
sortSelector.options[1].classList.add("sortOptionSelected");
sortSelector.options[1].text += " ↑";
sortSelector.options[sortSelector.options.length - 1].text = "Sort by : " + sortSelector.options[1].text;
sortSelector.options[sortSelector.options.length - 1].selected = "selected";


sortSelector.addEventListener("change", function () {
    [current_sort_value, sort_order] = sortTracks(event, current_sort_value, sort_order, list_of_tracks, div_track_list, all_div_track);
});


/*
 * ###########################################################
 * #                        FILTERS                          #
 * ###########################################################
 */


const selectFilter = document.getElementById("selectFilter");
let listOfValues = [];
verifListOfValues(listOfValues);
let count = 0;

selectFilter.addEventListener("change", function () {
    listOfValues.push("featuring");
    if (count % 2 === 1) {
        listOfValues.push("album");
    }
    filterTracks(event, listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, true);

    count++;
});


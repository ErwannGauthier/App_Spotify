/*
 * ###########################################################
 * #                    INITIALISATION                       #
 * #                     OF VARIABLES                        #
 * ###########################################################
 */

const tracks_from_album = [];
const tracks_from_other = [];
const tracks_featuring = [];
const div_track_list = document.getElementById("div_track_list");
const all_div_track = div_track_list.children;
const length_wo_copy = document.getElementById("length_wo_copy");
let count_copy = 0

for (let i = 0; i < list_of_tracks.length; i++) {
    let track = list_of_tracks[i];
    track["init"] = i;


    if (!track["is_copy"]) {
        count_copy++;
    }

    if (track["artists"].length > 1) {
        tracks_featuring.push(track["id"]);
    }

    let j = 0;
    let found = false;
    while (j < list_of_artist_albums.length && !found) {
        let album = list_of_artist_albums[j];
        if (album["id"] === track["album"]) {
            tracks_from_album.push(track["id"]);
            track["album"] = album;
            found = true;
        }
        j++;
    }

    j = 0;
    while (j < list_of_other_albums.length && !found) {
        let album = list_of_other_albums[j];
        if (album["id"] === track["album"]) {
            tracks_from_other.push(track["id"]);
            track["album"] = album;
            found = true;
        }
        j++;
    }
}

length_wo_copy.innerText = count_copy;


/*
 * ###########################################################
 * #                      SEARCH BAR                         #
 * ###########################################################
 */


const searchBar = document.getElementById("searchBar");
searchBar.addEventListener("input", function () {
    search(event, all_div_track, list_of_tracks, true, listOfValues, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked());
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


sortSelector.addEventListener("change", function (){
    [current_sort_value, sort_order] = sortTracks(event, current_sort_value, sort_order, list_of_tracks, div_track_list, all_div_track);
});


/*
 * ###########################################################
 * #                        FILTERS                          #
 * ###########################################################
 */


const selectFilter = document.getElementById("selectFilter");
selectFilter.addEventListener("change", function(){
    filterTracks(event, listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked());
});

let listOfValues = [];
verifListOfValues(listOfValues);


/*
 * ###########################################################
 * #                        SHOW COPY                        #
 * ###########################################################
 */


let showIsCopy = document.getElementById("showIsCopy");
showIsCopy.addEventListener("change", showCopy);

function isShowCopyChecked() {
    return showIsCopy.checked;
}

function showCopy(event) {
    allDivTrackModifier(listOfValues, list_of_tracks, tracks_from_album, tracks_from_other, tracks_featuring, isShowCopyChecked());
    refactorIncrementation(all_div_track);
}
function to_random() {
    var all = document.getElementById("entries");
    var randel = all.children[Math.floor(Math.random()*all.children.length)];
    window.location.hash = "#"+randel.id;
}

function to_top() {
    window.location.hash = "";
    window.scroll(0,0);
}

function to_bottom() {
    window.location.hash = "";
    window.scroll(0,99999999);
}

function on_hash_change() {
    try {
        window.scrollBy(0,-document.getElementById("sticky").offsetHeight-5);
    } catch (err) {

    }
}

window.onhashchange = function() {
    on_hash_change();
};

function change_votes(id, val) {
    if(true) {
        var el = document.getElementById(id);
        for(var i = 0; i < el.children.length; i++) {
            var cur = el.children[i];
            if(cur.className === "points") {
                var value = parseInt(cur.innerHTML);
                cur.innerHTML = value+val;
            }
        }
    }
}
var fv = true;
function firstvote() {
    if(fv===true) {
        alert("Näitä ei sitten tallenneta vielä.");
        fv = false;
    }
}
function upvote(id) {
    firstvote();
    change_votes(id, 1);
}
function downvote(id) {
    firstvote();
    change_votes(id, -1);
}

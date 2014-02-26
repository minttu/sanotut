function unhide(id) {
    var el = document.getElementById(id);
    for(var i = 0; i < el.children.length; i++) {
        var cur = el.children[i];
        if(cur.className === "hidden") {
            cur.className = "";
        }
    }
}

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

function change_votes(id, meth) {
    post("/onvote", meth+":"+id, function(data) {
        if(data.indexOf("error") !== -1) {
            alert(data);
        }else if(data.indexOf("success") !== -1) {
            var spl = data.split(":");
            var meth = spl[1];
            var id = spl[2];
            var el = document.getElementById(id);
            for(var i = 0; i < el.children.length; i++) {
                var cur = el.children[i];
                if(cur.className === "points") {
                    var value = parseInt(cur.innerHTML);
                    cur.innerHTML = value+(meth==="up"?1:-1);
                }
            }
        }
    });
}

function upvote(id) {
    change_votes(id, "up");
}
function downvote(id) {
    change_votes(id, "down");
}

function post(url, data, cb) {
    var httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      return false;
    }

    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200 || httpRequest.status === 400) {
                cb(httpRequest.responseText);
            }
        }
    };

    httpRequest.open('POST', url, true);
    httpRequest.send(data);
}

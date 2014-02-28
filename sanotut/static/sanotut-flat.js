var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;

$(function() {
    $(".upvote").on("click", function() {
        var id = this[0].parentNode.parentNode.id.split("E")[1];
        $.request('post', '/vote', "up:"+id)
        .then(function success(txt) {
            if($("#E"+id+" .downvote")[0].className.indexOf("voted") !== -1) {
                $("#E"+id+" .downvote").set("$", "-voted");
                $("#E"+id+" .points").set("$", "-downvoted")
            }else{
                $("#E"+id+" .upvote").set("$", "+voted");
                $("#E"+id+" .points").set("$", "+upvoted");
            }
            $("#E"+id+" .points").ht(parseInt($("#E"+id+" .points").text()) + 1);
        },function error(status, statusText, responseText) {

        });
    });
    $(".downvote").on("click", function() {
        var id = this[0].parentNode.parentNode.id.split("E")[1];
        $.request('post', '/vote', "down:"+id)
        .then(function success(txt) {
            if($("#E"+id+" .upvote")[0].className.indexOf("voted") !== -1) {
                $("#E"+id+" .upvote").set("$", "-voted");
                $("#E"+id+" .points").set("$", "-upvoted")
            }else{
                $("#E"+id+" .downvote").set("$", "+voted");
                $("#E"+id+" .points").set("$", "+downvoted");
            }
            $("#E"+id+" .points").ht(parseInt($("#E"+id+" .points").text()) - 1);
        },function error(status, statusText, responseText) {

        });
    });
    $(".show").on("click", function() {
        var id = this[0].parentNode.parentNode.id.split("E")[1];
        $("#E"+id+" pre").set("$", "-hidden");
        $(this).remove();
    });
});

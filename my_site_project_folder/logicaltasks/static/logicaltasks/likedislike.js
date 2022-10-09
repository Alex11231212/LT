function like()
{
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    $.ajax({
        url : "/lt/" + type + "/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            $("#task_reaction_id").find("[data-count='like']").text(json.like_count);
            $("#task_reaction_id").find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}

function dislike()
{
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url : "/lt/" + type + "/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            $("#task_reaction_id").find("[data-count='dislike']").text(json.dislike_count);
            $("#task_reaction_id").find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

function comment_like()
{
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    $.ajax({
        url : "/lt/" + type + "/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            $("#comment_reaction_id").find(`button[data-id="${pk}"]`).find("[data-count='like']").text(json.like_count);
            $("#comment_reaction_id").find(`button[data-id="${pk}"]`).find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}

function comment_dislike()
{
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url : "/lt/" + type + "/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            $("#comment_reaction_id").find(`button[data-id="${pk}"]`).find("[data-count='dislike']").text(json.dislike_count);
            $("#comment_reaction_id").find(`button[data-id="${pk}"]`).find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

// Connecting Handlers
$(function() {
    $("#task_reaction_id").find('[data-action="like"]').click(like);
    $("#task_reaction_id").find('[data-action="dislike"]').click(dislike);
    $("#comment_reaction_id").find('[data-action="like"]').click(comment_like);
    $("#comment_reaction_id").find('[data-action="dislike"]').click(comment_dislike);
});
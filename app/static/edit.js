var minor_edit = false;

//TODO: Flashcard deletion needs to be easier.

$(function() {
    tinymce.init({
        plugins: "code",
        menubar : false,
        valid_elements : "*[*]",
        statusbar : false,
        selector: "#front_editor",
        toolbar: "undo redo | code | styleselect | bold italic | link image",
        setup: function(editor) {
            editor.on('change', function(e) {
                $("#front_preview").html(tinymce.get("front_editor").getContent());
                hljs.initHighlighting.called = false;
                hljs.initHighlighting();
            });
        }
    });

    tinymce.init({
        plugins: "code",
        menubar : false,
        valid_elements : "*[*]",
        selector: "#back_editor",
        toolbar: "undo redo | code | styleselect | bold italic | link image",
        setup: function(editor) {
            editor.on('change', function(e) {
                $("#back_preview").html(tinymce.get("back_editor").getContent());
                hljs.initHighlighting.called = false;
                hljs.initHighlighting();
            });
        }
    });



    $("#save_edit_btn").click(function() {
        var card_type = 0;
        if($("#draw_check").prop("checked")) {
            card_type += 1;
            console.log("draw checked");
        }
        if($("#back_sound_check").prop("checked")) {
            card_type += 20;
            console.log("back sound checked");
        }
        if($("#front_sound_check").prop("checked")) {
            card_type += 300;
            console.log("front sound checked");
        }

        if($("#minor_check").prop("checked")) {
            minor_edit = true;
        }

        var send_data = {
            minor_edit: minor_edit,
            card_type: card_type,
            old_front: old_front,
            new_front: tinymce.get("front_editor").getContent(), 
            new_back: tinymce.get("back_editor").getContent(),
            deck_name: deck_name,
            sound_back: $("#back_sound_input").val(),
            sound_front: $("#front_sound_input").val()
        }

        console.log(send_data);

        $.ajax({
            type: "POST",
            url: "../../ajax/editcard",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(send_data),
            success: function(newData) {
                if(newData.error === true) {
                    console.log(newData.error_msg)
                }
                else {
                    location.reload();
                }
            },
            error: function() {
                alert("Something went wrong!")
            }
        });
    });

    $("#cancel_edit_btn").click(function() {
        if(confirm("Are you sure you want to go back? Any changes made will be lost.")) {
            $("#editarea").addClass("hide");
            $("#mainarea").removeClass("hide");
        }
    });

    $("#new_card_btn").click(function() {
        $("#draw_check").prop("checked", false);
        $("#back_sound_check").prop("checked", false);
        $("#front_sound_check").prop("checked", false);

        old_front = "";

        tinymce.get("front_editor").setContent("");
        tinymce.get("back_editor").setContent("");

        $("#editarea").removeClass("hide");
        $("#mainarea").addClass("hide");
    });
});

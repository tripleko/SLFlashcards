$(document).ready(function() {
    function getData(handleData) {
        $.ajax({
            url:"../../ajax/nextcard",  
            success:function(data) {
                return data;
            }
        });
    }

    $("#show_ans_btn").click(function() {
        $("#back_panel").removeClass("hide").slideDown(450);
        $("#correct_btn").removeClass("hide");
        $("#wrong_btn").removeClass("hide");

        $("#show_ans_btn").addClass("hide");
    });

    $("#correct_btn").click(function() {
        $("#back_panel").addClass("hide").slideUp(450);
        $("#correct_btn").addClass("hide");
        $("#wrong_btn").addClass("hide");

        prev_front = card_front;
        prev_back = card_back;
        prev_interval = interval;
        prev_studied = last_studied;

        if(interval < 35) {
            interval += 1;
        }

        var flash_data = {
            deck_name: deck_name,
            front: card_front,
            interval: interval,
            last_studied: 0 //0 indicates that the time should be set to datetime.now()
        };

        $.ajax({
            type: "POST",
            url: "../../ajax/updatecard",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(flash_data),
            success: function(newData) {
                console.log(newData);
                location.reload();
                /*
                if(newData["interval"] === -1) {
                    //$("#show_ans_btn").addClass("hide");
                    $("#front_body").text("Looks like we're all out of cards for this deck!");
                    location.reload();
                }
                else {
                    card_front = newData["card_front"];
                    card_back = newData["card_back"];
                    last_studied = newData["last_studied"];
                    interval = newData["interval"];

                    $("#front_body").text(newData["card_front"]);
                    $("#back_body").text(newData["card_back"]);

                    $("#show_ans_btn").removeClass("hide");
                    location.reload();
                }
                */
                //TODO: Add error handling in the event that there are no new cards remaining.
            },
            error: function() {
                alert("Something went wrong!")
            }
        });
    });

    $("#wrong_btn").click(function() {
        $("#back_panel").addClass("hide").slideUp(450);
        $("#correct_btn").addClass("hide");
        $("#wrong_btn").addClass("hide");

        prev_front = card_front;
        prev_back = card_back;
        prev_interval = interval;
        prev_studied = last_studied;

        interval = 0;

        var flash_data = {
            deck_name: deck_name,
            front: card_front,
            interval: interval,
            last_studied: 0 //0 indicates that the time should be set to datetime.now()
        };

        $.ajax({
            type: "POST",
            url: "../../ajax/updatecard",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(flash_data),
            success: function(newData) {
                console.log(newData);
                location.reload();
                /*if(newData["interval"] === -1) {
                    //$("#show_ans_btn").addClass("hide");
                    $("#front_body").text("Looks like we're all out of cards for this deck!");
                }
                else {
                    card_front = newData["card_front"];
                    card_back = newData["card_back"];
                    last_studied = newData["last_studied"];
                    interval = newData["interval"];

                    $("#front_body").text(newData["card_front"]);
                    $("#back_body").text(newData["card_back"]);

                    $("#show_ans_btn").removeClass("hide");
                }*/
                //TODO: Add error handling in the event that there are no new cards remaining.
            },
            error: function() {
                alert("Something went wrong!")
            }
        });
    });
});
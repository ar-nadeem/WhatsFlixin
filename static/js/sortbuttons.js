

    $(document).on('click',".rank_button" ,function (e) {

        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                button_post: $("#rank_button").val(),

                arrow: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {

                $('body').html(data);
            },
        });
        return false;


    });

    $(document).on('click',".avail_button",function (e) {

        e.preventDefault();
       $.get("https://ip-api.com/json", function(response) {console.log(response.country);

        $.ajax({
            type: 'POST',
            data: {
                button_post: $("#avail_button").val(),

                arrow: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),
                country: response.country,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {
                $('body').html(data);
            },
        });
    });


    });


    $(document).on('click',".reldate_button",function (e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                button_post: $("#reldate_button").val(),

                arrow: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {

                $('body').html(data);
            },
        });
        return false;


    });

        $(document).on('click',".arrow_button",function (e) {

        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                arrow_post: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),

                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {

                $('body').html(data);
            },
        });
        return false;


    });


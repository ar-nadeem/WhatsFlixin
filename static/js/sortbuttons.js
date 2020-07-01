
    function loading_on() {
        document.getElementById("overlay").style.display = "block";
    }

    function loading_off() {

        document.getElementById("overlay").style.display = "none";
    }

    $("#rank_button").on("click", function (e) {
        loading_on()
        e.preventDefault();

        $.ajax({
            type: 'POST',
            data: {
                button_post: $("#rank_button").val(),

                arrow: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),
                csrfmiddlewaretoken: "{{ csrf_token }}",

                action: 'post'
            },
            success: function (data) {
                loading_off()
                $("body").html(data);
            },
        });
        return false;


    });


    $("#reldate_button").on("click", function (e) {
        loading_on()
        e.preventDefault();

        $.ajax({
            type: 'POST',
            data: {
                button_post: $("#reldate_button").val(),

                arrow: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),
                csrfmiddlewaretoken: "{{ csrf_token }}",
                action: 'post'
            },
            success: function (data) {
                loading_off()
                $("body").html(data);
            },
        });
        return false;
    });

    $("#avail_button").on("click", function (e) {
        loading_on()
        e.preventDefault();
        $.getJSON('https://api.ipify.org?format=jsonp&callback=?', function (data) {

            console.log(JSON.stringify(data, null, 2).ip);
            var ip = jQuery.parseJSON(JSON.stringify(data, null, 2))
            var ip = ip.ip
            console.log(ip)


            $.getJSON("https://cors-anywhere.herokuapp.com/http://www.geoplugin.net/json.gp?ip=" + ip, function (response) {
                console.log(response.geoplugin_countryName);
                $.ajax({
                    type: 'POST',
                    data: {
                        button_post: $("#avail_button").val(),

                        arrow: $("#arrow_button").val(),
                        reldate: $("#reldate_button").attr("class"),
                        avail: $("#avail_button").attr("class"),
                        rank: $("#rank_button").attr("class"),
                        country: response.geoplugin_countryName,
                        csrfmiddlewaretoken: "{{ csrf_token }}",

                        action: 'post'
                    },
                    success: function (data) {
                        loading_off()
                        $("body").html(data);
                    },
                });
            });
        });
        return false;

    });

    $("#arrow_button").on("click", function (e) {
        loading_on()
        e.preventDefault();

        $.ajax({
            type: 'POST',
            data: {
                arrow_post: $("#arrow_button").val(),
                reldate: $("#reldate_button").attr("class"),
                avail: $("#avail_button").attr("class"),
                rank: $("#rank_button").attr("class"),
                csrfmiddlewaretoken: "{{ csrf_token }}",
                country: "{{ country }}",
                action: 'post',

            },
            success: function (data) {
                $("body").html(data);
                loading_off()

            },
        });
        return false;


    });





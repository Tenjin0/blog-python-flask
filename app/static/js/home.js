(function() {
    window.onload = function() {
        var timer = null;
        var controller = null;
        var popups = document.querySelectorAll(".user_popup");
        for (var i = 0; i < popups.length; i++) {
            var popup = popups[i];
            popup.addEventListener("mouseover", function(event) {
                controller = new AbortController();
                const signal = controller.signal;
                timer = setTimeout(() => {
                    timer = null;
                    fetch("/user/" + this.dataset.id + "/popup", {
                        method: "get",
                        credentials: "same-origin",
                        signal
                    })
                        .then(response => {
                            controller = null;
                            if (response.ok) {
                                response
                                    .text()
                                    .then(content => {
                                        console.log(this);
                                        $(this)
                                            .popover({
                                                trigger: "manual",
                                                html: true,
                                                animation: true,
                                                container: this,
                                                content
                                            })
                                            .popover("show");
                                        flask_moment_render_all();
                                    })
                                    .catch(e => console.log(e.message));
                            } else {
                                console.log("response not ok");
                            }
                        })
                        .catch(function(error) {
                            console.log(error.message);
                            timer = null;
                            controller = null;
                        });
                    // popup logic goes here
                }, 1000);
            });
            popup.addEventListener("mouseout", function(event) {
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                } else if (controller) {
                    controller.abort();
                    controller = null;
                } else {
                    $(this).popover("dispose");
                }
            });
        }
    };
})();

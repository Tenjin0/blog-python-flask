(function() {
    function set_message_count(n) {
        document.getElementById("message_count").innerHTML = n;
        document.getElementById("message_count").style.visibility,
            n ? "visible" : "hidden";
    }
    window.onload = function() {
        var namespace = "/notifications";
        var socket = io.connect(
            "http://" + document.domain + ":" + location.port + namespace
        );
        socket.on("connect", function() {
            console.log("connected");
            socket.emit("my event", { data: "I'm connected!" });
        });

        socket.on('task_update', function(msg){
            console.log(msg)
            var taskProgress = document.getElementById(msg.id + '-progress')
            taskProgress.innerHTML = msg.progress
            if (msg.progress === 100) {
                console.log('remove display none and delete task')
            }
        })
        var since = 0;
        this.setInterval(function() {
            fetch("/notifications?since=" + since, {
                method: "get",
                credentials: "same-origin"
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                })
                .then(notifications => {
                    for (var i = 0; i < notifications.length; i++) {
                        if (notifications[i].name === "unread_message_count") {
                            set_message_count(notifications[i].data);
                        }
                        since = notifications[i].timestamp;
                    }
                })
                .catch(e => {
                    console.log(e.message);
                });
        }, 10000);
    };
})();

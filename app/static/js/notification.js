(function () {
    function set_message_count(n) {
        document.getElementById('message_count').innerHTML = n;
        document.getElementById('message_count').style.visibility, n ? "visible" : 'hidden'
    }
    window.onload = function () {
        var namespace = '/notifications'
        var socket = io.connect(this.location.protocol + "//" + this.location.host + namespace, {
            reconnection: false
        })
        socket.on('connect', function() {
            console.log('connect with websocket')
        })

        socket.on('response', function(msg) {
            console.log(msg.meta);
        })
        var since = 0;
        this.setInterval(function () {
            fetch("/notifications?since=" + since, {
                method: "get",
                credentials: "same-origin"
            }).then((response) => {
                if (response.ok) {
                    return response.json()
                }
            }).then((notifications) => {
                for (var i = 0; i < notifications.length; i++) {
                    if (notifications[i].name === 'unread_message_count') {
                        set_message_count(notifications[i].data)
                    }
                    since = notifications[i].timestamp
                }
            }).catch((e) => {
                console.log(e.message)
            })
        }, 10000)
    }
}())
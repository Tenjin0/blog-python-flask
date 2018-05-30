(function(){
    function set_message_count(n) {
        document.getElementById('message_count').innerHTML = n;
        document.getElementById('message_count').style.visibility, n ? "visible" : 'hidden'
    }
    window.onload = function() {
        var since = 0;
        this.setInterval(function(){
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
            }).catch(() => {

            })
        }, 10000)
    }
}())
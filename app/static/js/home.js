(function() {
    window.onload = function() {
        var popups = document.querySelectorAll('.user_popup');
        console.log(popups);
        for (var i = 0; i < popups.length; i++) {
            var popup = popups[i];
            popup.addEventListener("mouseover", function(event) {
                console.log('toto', event)
            })
            popup.addEventListener("mouseout", function(event) {
                console.log('titi', event)
            })
        }
    };
})();

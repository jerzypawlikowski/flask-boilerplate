document.addEventListener("DOMContentLoaded", function() {
    debugger
    fetch('/api/hello').then(function(response) {
        debugger
        return response.json();
    }).then(function(response_data) {
        debugger
        if(response_data.success === true) {
            var container = document.getElementById('main-container');
            container.innerHTML = response_data.data;
        }
    }).catch(function(err) {
        debugger
    });
});

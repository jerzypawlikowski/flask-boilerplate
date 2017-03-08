document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/hello').then(function(response) {
        return response.json();
    }).then(function(response_data) {
        if(response_data.success === true) {
            var container = document.getElementById('main-container');
            container.innerHTML = response_data.data;
        }
    }).catch(function(err) {
        alert("Oh dear! An error occurred!")
    });
});

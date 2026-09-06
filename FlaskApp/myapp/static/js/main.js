//main.js javascript file for the FlaskApp project

function goTo(url){
    window.location.href = url;
}

document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('.delete-link');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            const confirmDelete = confirm('Are you sure you want to delete this item?');
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });
}); 
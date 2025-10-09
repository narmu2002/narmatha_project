function myfun(event) {
    // Prevent the default link navigation for now
    event.preventDefault();

    // Run your custom logic (e.g., show an alert)
    alert("Password generated!");

    window.location = event.target.href; 
    }
$(document).ready(function() {
    // define fields as variables
    var submit_button = $('input#submit');
    var form = $('form');
    // on submit, disable submit button
    form.submit(function() {
        if (form) {
            submit_button.prop('disabled', true);
        }
    });
});
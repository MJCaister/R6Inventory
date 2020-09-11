$(document).ready(function() {
    // define fields as variables
    var submit_button = $('#submit');
    // on submit, disable submit button
    submit_button.onclick(function() {
        submit_button.prop('disabled', true);
    });
});
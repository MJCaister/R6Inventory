$(document).ready(function() {
    // define fields as variables
    var submit_button = $('button#submit');
    // on submit, disable submit button
    submit_button.submit(function() {
        submit_button.prop('disabled', true);
    });
});
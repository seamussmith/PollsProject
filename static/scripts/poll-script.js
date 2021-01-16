// Function called by every vote button when clicked
// Sends a vote to the server via AJAX
function SendVote(self) {
    // Convert button and form to JQuery object
    let $self = $(self);
    let $form = $(self.parentElement);
    // Send Ajax request
    $.ajax({
        method: $form.attr("method"),
        // Serialize hidden inputs in form and add the vote to the data sent
        // NOTE: The data for the button selected by the user is not serialized by $form.serialize(),
        // NOTE: so you have to manually add the data attributed to the button clicked to the data sent.
        data: `${$form.serialize()}&${$self.attr("name")}=${$self.attr("value")}`,
        url: $form.attr("action")
    })
        .done((result) => {
        $form.children().prop("disabled", false); // Re-enable form children
        let data = JSON.parse(result); // Parse JSON sent by server, interface data with Poll interface
        console.log(data);
        // Update every poll button's data with data sent by server
        $form.find(".poll__choice").each((i, $choice) => {
            let votes = data.choices[parseInt($choice.value)].votes;
            $choice.dataset.votes = votes.toString();
            $choice.dataset.votesFormatted = votes.toLocaleString();
        });
        $form.addClass("poll__form--voted");
        $self.addClass("poll__choice--selected");
    })
        .fail((e) => {
        // Alert user with alert prompt
        alert(e); // FIXME: Apparently 'e' is not the error object...
        $form.children().prop("disabled", false); // Re-enable voting of poll
    });
    $form.children().prop("disabled", true); // After sending vote request, disable the form to prevent duplicate votes
}
function TogglePollVisibility(poll) {
    $(poll).toggleClass("poll--visible");
}

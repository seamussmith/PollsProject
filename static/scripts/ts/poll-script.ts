
interface IPoll // Interface for Poll object recieved by server
{
    question: string
    choices: Array<{
        name: string
        poll_uuid: string
        uuid: string
        votes: number
    }>
    uuid: string
    pub_date: string // ISO-8601 timestamp
}

// Function called by every vote button when clicked
// Sends a vote to the server via AJAX
function SendVote(self: HTMLElement): void
{
    // Convert button and form to JQuery object
    let $self = $(self)
    let $form = $(self.parentElement)
    // Send Ajax request
    $.ajax({
        method: $form.attr("method"),
        // Serialize hidden inputs in form and add the vote to the data sent
        // NOTE: The data for the button selected by the user is not serialized by $form.serialize(),
        // NOTE: so you have to manually add the data attributed to the button clicked to the data sent.
        data: `${$form.serialize()}&${$self.attr("name")}=${$self.attr("value")}`,
        url: $form.attr("action")
    })
    .done((data: IPoll) => { // On a successful vote...
        $form.children().prop("disabled", false) // Re-enable form children
        let $prev = $form.children(".poll__choice--selected")
                        .toggleClass("poll__choice--selected")
        if ($self.attr("value") !== $prev.attr("value")) // Vote highlight switching thing
            $self.toggleClass("poll__choice--selected")
        let totalVotes = data.choices.reduce((val, choice) => val + choice.votes, 0) || 1 // Calculate the total amount of votes.
        // Update every poll button's data with data sent by server                       // If 0, set to 1 to prevent division by 0
        $form.find(".poll__choice").each((i, $choice: HTMLInputElement) => {
            let choice = data.choices.find((e) => e.uuid === $choice.value) 
            let votes = choice.votes
            let precentage = votes/totalVotes * 100
            $choice.dataset.votes = votes.toString()
            $choice.dataset.votesFormatted = `(${Math.round(precentage)}%) ${votes.toLocaleString()}`
            $choice.style.setProperty("--precentage", `${precentage}%`)
        })
        $form.addClass("poll__form--voted")
    })
    .fail((response, err, e) => { // On fail...
        // Alert user with alert prompt
        alert(`A server error has occured in the process of handling your vote.\nServer Response Code: ${response.status} ${response.statusText}\nPlease try again`)
        $form.children().prop("disabled", false) // Re-enable voting of poll
    })
    $form.children().prop("disabled", true) // After sending vote request, disable the form to prevent duplicate votes
}

function GrabMorePolls(self: HTMLInputElement)
{
    let $self: JQuery = $(self)
    let next = $self.data("next")
    $.ajax({
        method: "GET",
        url: `${$self.data("url")}?next=${next}`
    }).done((result) => {
        console.log(result)
        $(".poll-container").eq(0).append(result)
        $self.data("next", $(".poll-container").children().length)
    })
}

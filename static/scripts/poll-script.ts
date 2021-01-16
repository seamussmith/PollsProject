
function SendVote(self: HTMLElement): void
{
    let $self = $(self)
    let $form = $(self.parentElement)
    $.ajax({
        method: $form.attr("method"),
        data: `${$form.serialize()}&${$self.attr("name")}=${$self.attr("value")}`,
        url: $form.attr("action")
    })
    .done((result) => {
        console.log(result);
        $form.children().prop("disabled", false)
        let data = JSON.parse(result)
        $form.find(".poll__choice").each((i, $choice: HTMLInputElement) => {
            let votes = data.choices[parseInt($choice.value)].votes
            $choice.dataset.votes = votes
            $choice.dataset.votesFormatted = votes.toLocaleString()
        })
    })
    .fail((e) => {
        alert(e)
        $form.children().prop("disabled", false)
    })
    $form.children().prop("disabled", true)
}

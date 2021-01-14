
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
    })
    .fail((e) => {
        alert(e)
    })
    $form.children().prop("disabled", true)
}

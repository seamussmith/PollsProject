
function SendVote(self)
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
    })
}

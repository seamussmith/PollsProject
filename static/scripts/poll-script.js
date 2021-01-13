
function PollVote(self)
{
    console.log(self)
    let $form = $(self)
    $.ajax({
        url: "/pollapp/",
        data: $form.serialize(),
        method: $form.attr("method")
    })
    .done((res) => {
        console.log("Got result", res)
    })
    return false;
}

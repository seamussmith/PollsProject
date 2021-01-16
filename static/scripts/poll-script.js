function SendVote(self) {
    let $self = $(self);
    let $form = $(self.parentElement);
    $.ajax({
        method: $form.attr("method"),
        data: `${$form.serialize()}&${$self.attr("name")}=${$self.attr("value")}`,
        url: $form.attr("action")
    })
        .done((result) => {
        $form.children().prop("disabled", false);
        let data = JSON.parse(result);
        console.log(data);
        $form.find(".poll__choice").each((i, $choice) => {
            let votes = data.choices[parseInt($choice.value)].votes;
            $choice.dataset.votes = votes;
            $choice.dataset.votesFormatted = votes.toLocaleString();
        });
    })
        .fail((e) => {
        alert(e);
        $form.children().prop("disabled", false);
    });
    $form.children().prop("disabled", true);
}

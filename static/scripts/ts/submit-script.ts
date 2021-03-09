
function AddChoice(self: HTMLElement)
{
    if ($(`input[type="text"]`).length < 6)
        $(self).before(`<input type="text" name="choice[]" maxlength="20">`)
    if ($(`input[type="text"]`).length === 6)
        $(self).prop("disabled", true)
}

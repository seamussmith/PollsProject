function AddChoice(self) {
    if ($(`input[type="text"]`).length < 6)
        $(self).before(`<input type="text" name="choice[]" maxlength="20">`);
}

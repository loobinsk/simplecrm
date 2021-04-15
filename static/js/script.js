$(selector).multiDatesPicker(options_for_datepicker_and_mdp);

function onDivClick(elem) {
	var a = `<input class="my-form" name='data' onblur="document.getElementById('form-id').submit();" id='input' value="${elem.textContent}">`
	elem.outerHTML = a
	let input = document.querySelector('#input');
	input.focus()
}
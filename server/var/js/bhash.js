function hashify(candidate) {
	return '#' + candidate;
}

function loadPosts(target) {
    $('#inputHash').val(target);
    $('#formHash').submit();
}

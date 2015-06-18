$(document).ready(function(){
	$(".delete_item").click(function(event){
		var chk = confirm("Are you sure?")
		if (chk == false) {
			event.preventDefault();
		}
	});
});
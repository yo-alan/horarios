$(function(){
	
	var form = $("#addForm");
	
	form.submit(function (ev){
		
		ev.preventDefault();
		
		$("#" + form.attr('id') + " button[type=submit]").button('loading');
		
		$.ajax({
			url: form.attr('action'),
			type: form.attr('method'),
			data: form.serialize(),
			success: function (response){
				
				$("#" + form.attr('id') + " button[type=submit]").button('reset');
				
				$(".form-group").attr('class', "form-group");
				
				if(response.error){
					
					if(response.campo){
						$("#"+ response.campo).parent().parent().attr('class', "form-group has-error");
						$("#"+ response.campo).focus();
					}
					
					$("#" + form.attr('id') + " .alert").attr('class', "alert alert-dismissable alert-danger");
					$("#" + form.attr('id') + " .alert p").html(response.error);
					return;
				}
				
				alert(response.mensaje);
				window.location.href = onsuccess;
			}
		});
	});
});

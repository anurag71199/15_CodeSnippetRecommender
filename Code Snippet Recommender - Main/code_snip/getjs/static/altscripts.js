$("form[name=signup_form").submit(function (e) {

	var $form = $(this);
	var $error = $form.find(".error");
	var data = $form.serialize();

	$.ajax({
		url: "/register",
		type: "POST",
		data: data,
		dataType: "json",
		success: function (resp) {
			window.location.href = "/";
		},
		error: function (resp) {
			$error.text(resp.responseJSON.error).removeClass("error--hidden");
		}
	});

	e.preventDefault();
});

$("form[name=login_form").submit(function (e) {
	var $form = $(this);
	var $error = $form.find(".error");
	var data = $form.serialize();
	console.log('scripts.js:data=', data);

	$.ajax({
		url: "/login",
		type: "POST",
		data: data,
		dataType: "json",
		success: function (resp) {
			window.location.href = "/userhome";
		},
		error: function (resp) {
			$error.text(resp.responseJSON.error).removeClass("error--hidden");
		}
	});

	e.preventDefault();
});


$("form[name=upload_form").submit(function (e) {

	var $form = $(this);
	var $error = $form.find(".error");
	var data = $form.serialize();

	$.ajax({
		url: "/uploadsnip",
		type: "POST",
		data: data,
		dataType: "json",
		success: function (resp) {
			window.location.href = "/userhome";
		},
		error: function (resp) {
			$error.text(resp.responseJSON.error).removeClass("error--hidden");
		}
	});

	e.preventDefault();
});

$("form[name=index_form").submit(function (e){

	var $form = $(this);
	var $error = $form.find(".error");
	var data = $form.serialize();

	$.ajax({
		url: "/",
		type: "POST",
		data: data,
		dataType: "json",
		success: function (resp){
			window.location.href = "/searchsnippet";
		},
		error: function (resp){
			$error.text(resp.responseJSON.error).removeClass("error-hidden");
		}
	});

	e.preventDefault();
});

$("form[name=logsearch_form").submit(function (e){

	var $form = $(this);
	var $error = $form.find(".error");
	var data = $form.serialize();

	$.ajax({
		url: "/userhome",
		type: "POST",
		data: data,
		dataType: "json",
		success: function (resp){
			window.location.href = "/logsearchsnippet";
		},
		error: function (resp){
			$error.text(resp.responseJSON.error).removeClass("error-hidden");
		}
	});

	e.preventDefault();
});

$(document).ready(function(){
	$('.qtemp').on('click',function(){
	 var layout = $(this).data('rep');
	 console.log(layout)
	  $.ajax({
	   url: "/vote",
	   type: "get",
	   data: {layout: layout},
	   success: function(response) {
		window.location.href = "/logsearchsnippet";
	   },
	  });     
   });
 });
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="/static/css/search.css">
	<title>Поиск по фильмам</title>
	<link rel="stylesheet" href="download/jquery-ui-1.12.1/jquery-ui.css">
<!--[if lt IE 9]>
<script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
<![endif]-->
</head>
<body>

	<div class="container content">
<form class="form-horizontal" method="post" id="form">
	<div class="form-group">
		<div class="col-sm-6">
			<input type="text" class="form-control" id="search" name="search" placeholder="Поиск...">
		</div>
	</div>
	<div class="form-group">
		<div class="col-sm-offset-2 col-sm-6">
			<button type="submit" id="submit" class="btn btn-primary"><img src="/static/img/film_search.png" style="width:100%;"></button>
			<div></div>
		</div>
	</div>
</form>
	</div>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
	<!-- JavaScript Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
	<script src="/download/jquery-ui-1.12.1/jquery-ui.js"></script>

	<script>
$(function(){
 $("#search").autocomplete({
 source: ajaxCall,
 create: function() {
      $(this).data('ui-autocomplete')._renderItem = function(ul, item) {
        return $('<li>')
          .append('<a href="' + item.film_url + '"><img class="icon" src="' + item.icon + '" />'  + item.label + '</span>' + '<br>'  + '</a>')
          .appendTo(ul);
      };
    }
 });
});

function ajaxCall(request, response) {
$.getJSON('/load_films/' + document.getElementById("search").value.split(' ').join('_'),
        function(data) {
        var films = [];
        response($.map(data, function(item) {
        return {'label': item.title, 'value': item.title, 'icon': item.image_url, 'film_url': item.url}
        }));
    });
};

	</script>

</body>
</html>
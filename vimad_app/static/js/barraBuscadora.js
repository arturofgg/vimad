$(document).ready(function() {
    $('#buscar-btn').click(function() {
      var query = $('#buscar-input').val();
  
      $.ajax({
        url: '/buscar/',
        data: {
          'q': query
        },
        dataType: 'json',
        success: function(data) {
          $('#resultados-busqueda').empty();
  
          if (data.cortos.length == 0) {
            $('#resultados-busqueda').append('<h1 style="color: white;">No se encontraron resultados.</h1>');
          } else {
            $.each(data.cortos, function(index, corto) {
              var urlFicha = '/ficha/' + corto.slug;
              $('#resultados-busqueda').append('<a href="' + urlFicha + '" class="list-group-item list-group-item-action"><img src="' + corto.imagen + '" alt="Imagen del corto" width="300px"><h5 class="mb-1">' + corto.titulo + '</h5><p class="mb-1">' + corto.genero + ', ' + corto.idioma + ', ' + corto.pais + '</p></a>');
            });
          }
        }
      });
    });
  });
  
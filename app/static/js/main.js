$(document).ready(function () {

  $("#menu-toggle").click(function (e) {
    e.preventDefault();
    if ($("#wrapper").hasClass('toggled')) {
      $('#menu-toggle > span').addClass('fa-times')
      $('#menu-toggle > span').removeClass('fa-bars')
      $('#navbarToggler > ul > li:nth-child(2) > a').html('Home <span class="sr-only">(current)</span>')
    } else {
      $('#menu-toggle > span').removeClass('fa-times')
      $('#menu-toggle > span').addClass('fa-bars')
      $('#navbarToggler > ul > li:nth-child(2) > a').html('<i class="fa fa-bicycle" aria-hidden="true"></i> PEDAL')
    }
    $("#wrapper").toggleClass("toggled");
  });


  //get latitude and longitude
  let lat = long = 0;
  navigator.geolocation.getCurrentPosition(function (position) {
    let curlat = position.coords.latitude;
    let curlong = position.coords.longitude;
    if ($('#mapid').length > 0) {
      buildMap(curlat, curlong);
    }
  });

  //register map with user events
  function buildMap(curlat, curlong) {

    var mymap = L.map('mapid').setView([curlat, curlong], 16);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 18,
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1
    }).addTo(mymap);

    var marker = L.marker([curlat, curlong]).addTo(mymap);

    var popup = L.popup();

    function onCircleMarkerClick(e) {
      $('#locationsearch').val(this.loc.location);
      $('#hiddenLocation').val(this.loc.id);
    }
    $.ajax({
      url: rootPath + '/api/bike/markerlist',
      type: 'GET',
      success: function (response) {
        console.log('success');
      },
      error: function (response) {
        console.error(response);
      }
    }).done(function (data) {
      console.log("Data:", data);
      for (var loc in data) {
        console.log(data[loc])
        data[loc].location=loc
        latlong = data[loc].current_location_latlong.replace('(', '').replace(')', '').split(',')
        var circle = L.circle([latlong[0], latlong[1]], {
          color: 'red',
          fillColor: '#f03',
          fillOpacity: 0.5,
          radius: 18
        }).addTo(mymap).on('click',onCircleMarkerClick,{'loc':data[loc]});
        circle.bindPopup(loc + " bike station: " + data[loc].count + " cycles");
      }
    });
  }

  $('#navbarToggler > ul.navbar-nav.mr-auto.mt-2.mt-lg-0 > li.nav-item').click((e) => {
    $(e.target).parent().parent().find('li').removeClass('active');
    $(e.target).parent().addClass('active');
  })

  $.ajax({
    url: rootPath + '/api/bike/manager/charts/data',
    type: 'GET',
    success: function (response) {
      console.log('success');
    },
    error: function (response) {
      console.error(response);
    }
  }).done(function (data) {
    console.log("Data:", data);
    Plotly.newPlot('chart1', data[1].data);
    $('#chart1').parent().parent().find('.card-header').text(data[1].name)
    Plotly.newPlot('chart2', data[2].data);
    $('#chart2').parent().parent().find('.card-header').text(data[2].name)
    Plotly.newPlot('chart3', data[3].data, data[3].layout);
    $('#chart3').parent().parent().find('.card-header').text(data[3].name)
    Plotly.newPlot('chart4', data[4].data, data[4].layout);
    $('#chart4').parent().parent().find('.card-header').text(data[4].name)
    Plotly.newPlot('chart5', data[5].data, data[5].layout);
    $('#chart5').parent().parent().find('.card-header').text(data[5].name)
  });

});
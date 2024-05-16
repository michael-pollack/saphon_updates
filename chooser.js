

const langset = new Set();

$(document).ready( function() {
  
  $('#languages tr').each( function() {
    this.faults = 0;
  });

  $('#chooser span').attr( 'unselectable', 'on');

  $('#chooser span[f="-3"]').hide();
  $('#chooser span.rare').hide();

  $('#scroller').click( function() {
    $('html, body').animate({
      scrollTop: $('#chooser').offset().top
    }, 500);
  });

  function handle_click( span) {
    if( span != null) {
      var o = $(span);
      var oi = o.attr( 'f');
      if( oi == '-1') {  // reset
        $('#languages tr').each( function() {
          this.faults = 0;
        });
        $('#chooser span').each( function() {
          $(this).removeClass("yes no");
        });
      } else if( oi == '-2') {  // toggle rare phonemes
        $('#chooser span[f="-2"]').hide();
        $('#chooser span[f="-3"]').show();
        $('#chooser span.rare').show();
      } else if( oi == '-3') {  // toggle rare phonemes
        $('#chooser span[f="-3"]').hide();
        $('#chooser span[f="-2"]').show();
        $('#chooser span.rare').hide();
        $('#chooser span.rare').each( function() {
          var o = $(this)
          var oi = o.attr( 'f');
          if( o.hasClass( 'yes')) {
            o.removeClass( 'yes')
            $('#languages tr').each( function() {
              if( $(this).attr( 'f'+oi) == undefined) {
                this.faults -= 1;
              }
            });
          } else if( o.hasClass( 'no')) {
            o.removeClass( 'no')
            $('#languages tr').each( function() {
              if( $(this).attr( 'f'+oi) != undefined) {
                this.faults -= 1;
              }
            });
          }
        });
      } else if( o.hasClass( 'no')) {
        o.removeClass( 'no');

        $('#languages tr').each( function() {
          if( $(this).attr( 'f'+oi) != undefined) {
            this.faults -= 1;
          }
        });
      } else if( o.hasClass( 'yes')) {
        o.removeClass( 'yes');
        o.addClass( 'no');

        $('#languages tr').each( function() {
          if( $(this).attr( 'f'+oi) == undefined) {
            this.faults -= 1;
          } else {
            this.faults += 1;
          }
        });
      } else {
        o.addClass( 'yes');
        $('#languages tr').each( function() {
          if( $(this).attr( 'f'+oi) == undefined) {
            this.faults += 1;
          }
        });
      }
    }

    /*
    $('div#selections').html(
      $('#chooser span.yes').map( function() {
	return $(this).attr( 'f');
      }).get().join(",") + ';' +
      $('#chooser span.no').map( function() {
	return $(this).attr( 'f');
      }).get().join(",") + ';' +
      $('#languages div').map( function() {
	return '' + this.faults;
      }).get().join(",")
    );
    */

    var matches = 0;
    langset.clear()
    $('#languages tr').each( function() {
      if( this.faults == 0) {
        $(this).css('display', 'block')
        langset.add(this.innerText)
        matches += 1;
      } else {
        $(this).css('display', 'none')
      }
    });
    initialize();
    $('#matches span.key').html( '' + matches)
  }

  $('#chooser span').click( function( e) { 
    handle_click( this); 
    // e.stopPropagation();
  });
  handle_click( null);
  
});

// Hack for accessing the state of meta and ctrl key from
// inside map event handler.
var metadown = false;

$(window).bind('keydown keyup focusin mouseenter', function(evtobj) {
  metadown = evtobj.metaKey || evtobj.ctrlKey;
});

$(window).bind('focusout mouseleave', function(evtobj) {
  metadown = false;
});

//Somedot Route
var icons = {
  'Tupi' : ['#FF0000', '#808080'],     // Red & Gray
  'Tupí' : ['#FF0000', '#808080'],     // Red & Gray
  'Arawak' : ['#00FF00', '#808080'],   // Green & Gray
  'Carib' : ['#0000FF', '#808080'],    // Blue & Gray
  'Macro-Ge' : ['#FFFF00', '#808080'], // Yellow & Gray
  'Quechua' : ['#00FFFF', '#808080'],  // Cyan & Gray
  'Panoan' : ['#FF00FF', '#808080'],   // Magenta & Gray
  'Tucanoan' : ['#FFA500', '#808080'], // Orange & Gray
  'Arawan' : ['#800080', '#808080'],   // Purple & Gray
  'Chibchan' : ['#FFD700', '#808080'], // Gold & Gray
  'Guaicuru' : ['#00CED1', '#00CED1'], // DarkTurquoise & DarkTurquoise 
  'Mataco' : ['#008080', '#008080'],   // Teal & Teal
  'Jivaroan' : ['#2E8B57', '#2E8B57'], // Sea Green & Sea Green
  'Witotoan' : ['#FF6347', '#FF6347'], // Tomato & Tomato
  'Barbacoan' : ['#800000', '#800000'], // Maroon & Maroon
  'Chapakuran' : ['#8A2BE2', '#8A2BE2'], // BlueViolet & BlueViolet
  'Choco' : ['#4B0082', '#4B0082'],    // Indigo & Indigo
  'Guahiban' : ['#FF4500', '#FF4500'], // OrangeRed & OrangeRed
  'Nadahup' : ['#20B2AA', '#20B2AA'],  // LightSeaGreen & LightSeaGreen
  'Nambiquaran' : ['#4682B4', '#4682B4'], // SteelBlue & SteelBlue
  'Tacanan' : ['#3CB371', '#808080'],  // MediumSeaGreen & MediumSeaGreen
  'Yanomam' : ['#87CEEB', '#87CEEB'],  // SkyBlue & SkyBlue
  'Zaparoan' : ['#8B008B', '#8B008B'], // DarkMagenta & DarkMagenta
  'Chon' : ['#8B008B', '#808080'],     // Gray & Gray
  'Other' : ['#D3D3D3', '#D3D3D3']     // Gray & White
};

//Maxdif Nodot route
// const icons = {
// 'Tupi' : ['#FF0000', '#FF0000'],     // Red & Red
// 'Tupí' : ['#FF0000', '#FF0000'],     // Red & Red
// 'Arawak' : ['#0000FF', '#0000FF'],   // Blue & Blue
// 'Carib' : ['#FFFF00', '#FFFF00'],    // Yellow & Yellow
// 'Macro-Ge' : ['#00FFFF', '#00FFFF'], // Cyan & Cyan
// 'Quechua' : ['#FF00FF', '#FF00FF'],  // Magenta & Magenta
// 'Panoan' : ['#FFA500', '#FFA500'],   // Orange & Orange
// 'Tucanoan' : ['#800080', '#800080'], // Purple & Purple
// 'Arawan' : ['#FFD700', '#FFD700'],   // Gold & Gold
// 'Chibchan' : ['#FF4500', '#FF4500'], // OrangeRed & OrangeRed
// 'Guaicuru' : ['#008080', '#008080'], // Teal & Teal
// 'Mataco' : ['#2E8B57', '#2E8B57'],   // Sea Green & Sea Green
// 'Jivaroan' : ['#FF6347', '#FF6347'], // Tomato & Tomato
// 'Witotoan' : ['#800000', '#800000'], // Maroon & Maroon
// 'Barbacoan' : ['#8A2BE2', '#8A2BE2'], // BlueViolet & BlueViolet
// 'Chapakuran' : ['#4B0082', '#4B0082'], // Indigo & Indigo
// 'Choco' : ['#00CED1', '#00CED1'],    // DarkTurquoise & DarkTurquoise
// 'Guahiban' : ['#20B2AA', '#20B2AA'],  // LightSeaGreen & LightSeaGreen
// 'Nadahup' : ['#4682B4', '#4682B4'],   // SteelBlue & SteelBlue
// 'Nambiquaran' : ['#3CB371', '#3CB371'], // MediumSeaGreen & MediumSeaGreen
// 'Tacanan' : ['#87CEEB', '#87CEEB'],   // SkyBlue & SkyBlue
// 'Yanomam' : ['#8B008B', '#8B008B'],  // DarkMagenta & DarkMagenta
// 'Zaparoan' : ['#00FF00', '#00FF00'], // Gray & Gray
// 'Chon' : ['#D3D3D3', '#D3D3D3'],     // LightGray & LightGray
// 'Other' : ['#808080', '#FFFFFF']     // Gray & White
// };
 
function get_pos(el) {
  for (var lx=0, ly=0;
   el != null;
   lx += el.offsetLeft, ly += el.offsetTop, el = el.offsetParent);
  return {x: lx,y: ly};
}

async function initialize() { 
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
  var myLatlng = new google.maps.LatLng(-4.669119, -60.829511);
  var myOptions = {
    zoom: 5,
    center: myLatlng,
    mapTypeControl: false,
    zoomControl: true,
    panControl: false,
    scaleControl: true,
    streetViewControl: false,
    mapTypeId: 'terrain',
    mapId: 'DEMO_MAP_ID'
    //mapID: 'f4dcb8b48ec1a463'
  }
  var map_div = document.getElementById("pmap")
  var map_pos = get_pos( map_div)
  const map = new Map(map_div, myOptions);
  var overlay = new google.maps.OverlayView();
  overlay.draw = function() {};
  overlay.setMap( map);
  var langinfo = document.getElementById("langinfo");
  var tooltip = document.getElementById("tooltip");

  // get URL parameter c
  var parm_c = decodeURIComponent((new RegExp('[?|&]c=' + '([^&;]+?)(&|#|;|$)')
    .exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;

  downloadUrl("../lang.xml", function(data) {
    var xml = parseXml(data); 
    var langs = xml.documentElement.getElementsByTagName("marker"); 
    for (var i = 0; i < langs.length; i++) (function( lang){ 
        var title = lang.getAttribute("title"); 
        if (langset.has(title)) {
          var iso_code = lang.getAttribute("iso_code"); 
          var family = lang.getAttribute("family");
          var link = lang.getAttribute("link");
          var type = lang.getAttribute("labeltype"); 
          var point = new google.maps.LatLng( 
              parseFloat(lang.getAttribute("lat")), 
              parseFloat(lang.getAttribute("lng"))); 
          var bubble = title + " (" + iso_code + ") <br/> Family: " + family;
          if (!(family in icons)){
            family = 'Other'
          }
          const pin = new PinElement({
            background: icons[family][0],
            glyphColor: icons[family][1],
            borderColor: '#000000',
            scale: 0.75
          })
          const marker = new AdvancedMarkerElement({
            map: map,
            position: point,
            content: pin.element,
          });

          marker.content.addEventListener('mouseenter', function() {
              langinfo.innerHTML = "<span class=key>Language:</span> <b>" + title + "</b> <span class=key>Code:</span> <b>" + iso_code + "</b> <span class=key>Family:</span> <b>" + family + "</b>"; 
              var projection = overlay.getProjection(); 
              var pixel = projection.fromLatLngToContainerPixel(point);
              tooltip.style.top = (map_pos.y + pixel.y - 60) + "px";
              tooltip.style.left = (map_pos.x + pixel.x - 11) + "px";
              tooltip.style.padding = "1px 2px"
                  tooltip.innerHTML = title;
          });

          marker.content.addEventListener('mouseleave', function() {
                  langinfo.innerHTML = ""
                  tooltip.innerHTML = ""
              tooltip.style.padding = "0"
          });

          // google.maps.event.addListener(marker, 'click', function(event) {
          //         if( metadown) {
          //         window.open(link);
          //         } else {
          //         window.location.href = link;
          //         }
          // });   
          }
    })( langs[i]);
  });        

  function downloadUrl(url, callback) { 
    var request = window.ActiveXObject ? 
  new ActiveXObject('Microsoft.XMLHTTP') : 
  new XMLHttpRequest; 

    request.onreadystatechange = function() { 
  if (request.readyState == 4) { 
    request.onreadystatechange = doNothing; 
    callback(request.responseText, request.status); 
  }
    }; 

    request.open('GET', url, true); 
    request.send(null); 
  } 

  function parseXml(str) { 
    if (window.ActiveXObject) { 
  var doc = new ActiveXObject('Microsoft.XMLDOM'); 
  doc.loadXML(str); 
  return doc; 
    } else if (window.DOMParser) { 
  return (new DOMParser).parseFromString(str, 'text/xml'); 
    } 
  } 
    
  function doNothing() {} 
}

function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
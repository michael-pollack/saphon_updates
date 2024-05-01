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

var icons = {
  'Tupi' : '#2f0',
  'Tupí' : '#2f0',
  'Arawak' : '#f00',
  'Carib' : '#f80', 
  'Macro-Ge' : '#ff0',
  'Quechua' : '#cf4',
  'Panoan' : '#08f',
  'Tucanoan' : '#00f',
  'Arawan' : '#f08',
  'Chibchan' : '#faa',
  'Guaicuru' : '#a42',
  'Mataco' : '#26c',
  'Jivaroan' : '#2aa',
  'Witotoan' : '#999',
  'Barbacoan' : '#c48',
  'Chapakuran' : '#088',
  'Choco' : '#a80',
  'Guahiban' : '#4cf',
  'Nadahup' : '#4fc',
  'Nambiquaran' : '#4a2',
  'Tacanan' : '#c4f',
  'Yanomam' : '#80c',
  'Zaparoan' : '#fc4',
  'Chon' : '#fef',
  'Other' : '#ccd',
};
 
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
          const pin = new PinElement({
            background: icons[family],
            borderColor: '#000000',
            glyph: ""
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
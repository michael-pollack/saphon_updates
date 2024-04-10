const langset = new Set();

function handle_click( span) {
  downloadUrl("../langs.json", function(langs) {
    if( span != null) {
      var o = $(span);
      var oi = o.attr( 'f');
      if( oi == '-1') {  // reset

        for (let i = 0; i < langs.length; i++) {
          langs[i].faults = 0;
        }

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

            for (let i = 0; i < langs.length; i++) {
              let code = 'f' + oi;
              if (code in langs[i].codes) {
                langs[i].faults -= 1;
              }
            }

            $('#languages tr').each( function() {
              if( $(this).attr( 'f'+oi) == undefined) {
                this.faults -= 1;
              }
            });
          } else if( o.hasClass( 'no')) {
            o.removeClass( 'no')

            for (let i = 0; i < langs.length; i++) {
              let code = 'f' + oi;
              if (!(code in langs[i].codes)) {
                langs[i].faults -= 1;
              }
            }

            $('#languages tr').each( function() {
              if( $(this).attr( 'f'+oi) != undefined) {
                this.faults -= 1;
              }
            });
          }
        });
      } else if( o.hasClass( 'no')) {
        o.removeClass( 'no');

        for (let i = 0; i < langs.length; i++) {
          let code = 'f' + oi;
          if (code in langs[i].codes) {
            langs[i].faults -= 1;
          }
        }

        $('#languages tr').each( function() {
          if( $(this).attr( 'f'+oi) != undefined) {
            this.faults -= 1;
          }
        });
      } else if( o.hasClass( 'yes')) {
        o.removeClass( 'yes');
        o.addClass( 'no');

        for (let i = 0; i < langs.length; i++) {
          let code = 'f' + oi
          if (!(code in langs[i].codes)) {
            langs[i].faults -= 1;
          } else {
            langs[i].faults += 1;
          }
        }

        $('#languages tr').each( function() {
          if( $(this).attr( 'f'+oi) == undefined) {
            this.faults -= 1;
          } else {
            this.faults += 1;
          }
        });
      } else {
        o.addClass( 'yes');

        for (let i = 0; i < langs.length; i++) {
          let code = 'f' + oi
          if (!(code in langs[i].codes)) {
            langs[i].faults += 1;
          }
        }

        $('#languages tr').each( function() {
          if( $(this).attr( 'f'+oi) == undefined) {
            this.faults += 1;
          }
        });
      }
    }

    var matches = 0;
    langset.clear()
    tableBody.innerHTML = '';
    const rowMax = 20;
    var maxHit = false;
    var rowIndex = 0;
    var cellIndex = 0;

    langs.forEach(function (item) {
      if (item.faults == 0) {
        matches += 1;
        if (!maxHit && rowIndex < rowMax) {
          var row = tableBody.insertRow();
          rowIndex += 1;
        } else if (rowIndex == rowMax) {
          var row = tableBody.rows[0]
          rowIndex = 1;
          cellIndex += 1;
          maxHit = true;
        } else {
          var row = tableBody.rows[rowIndex]
          rowIndex += 1;
        }

        console.log(cellIndex)
        var cell1 = row.insertCell(cellIndex);

        // Check if the link is not equal to 0 before creating the hyperlink

        // Create a hyperlink with the name and link
        var link = document.createElement("a");
        link.href = item.link;
        link.textContent = item.title;
        langset.add(item.title);

        // Append the hyperlink to the cell
        cell1.appendChild(link);

        // Display the link in the second cell
      }
    });

    $('#languages tr').each( function() {
      if( this.faults == 0) {
        $(this).css('display', 'block')
        langset.add(this.innerText)
      } else {
        $(this).css('display', 'none')
      }
    });
    initialize();
    $('#matches span.key').html( '' + matches)
  });
}
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

function getIcon( color, text) {
  return new StyledIcon( StyledIconTypes.MARKER, {
      color: color,
      text: text})
}

var icons = {
  'Tupi' : getIcon( '#2f0', 'T'),
  'Tupí' : getIcon( '#2f0', 'T'),
  'Arawak' : getIcon( '#f00', 'A'),
  'Carib' : getIcon( '#f80', 'C'),
  'Macro-Ge' : getIcon( '#ff0', 'M'),
  'Quechua' : getIcon( '#cf4', 'Q'),
  'Panoan' : getIcon( '#08f', 'P'),
  'Tucanoan' : getIcon( '#00f', 'Tu'),
  'Arawan' : getIcon( '#f08', 'An'),
  'Chibchan' : getIcon( '#faa', 'Cb'),
  'Guaicuru' : getIcon( '#a42', 'G'),
  'Mataco' : getIcon( '#26c', 'Mt'),
  'Jivaroan' : getIcon( '#2aa', 'J'),
  'Witotoan' : getIcon( '#999', 'W'),
  'Barbacoan' : getIcon( '#c48', 'B'),
  'Chapakuran' : getIcon( '#088', 'Cp'),
  'Choco' : getIcon( '#a80', 'Cc'),
  'Guahiban' : getIcon( '#4cf', 'Gh'),
  'Nadahup' : getIcon( '#4fc', 'N'),
  'Nambiquaran' : getIcon( '#4a2', 'Nm'),
  'Tacanan' : getIcon( '#c4f', 'Tn'),
  'Yanomam' : getIcon( '#80c', 'Y'),
  'Zaparoan' : getIcon( '#fc4', 'Z'),
  'Chon' : getIcon( '#fef', 'Ch'),
  'Other' : getIcon( '#ccd', ''),
  'TODO' : getIcon( '#ccd', '')
};
 
function get_pos(el) {
  for (var lx=0, ly=0;
   el != null;
   lx += el.offsetLeft, ly += el.offsetTop, el = el.offsetParent);
  return {x: lx,y: ly};
}

function initialize() { 
  var myLatlng = new google.maps.LatLng(-4.669119, -60.829511);
  var myOptions = {
    zoom: 5,
    center: myLatlng,
    mapTypeControl: false,
    zoomControl: true,
    panControl: false,
    scaleControl: true,
    streetViewControl: false,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  }
  var map_div = document.getElementById("pmap")
  var map_pos = get_pos( map_div)
  var map = new google.maps.Map( map_div, myOptions);
  var overlay = new google.maps.OverlayView();
  overlay.draw = function() {};
  overlay.setMap( map);
  var langinfo = document.getElementById("langinfo");
  var tooltip = document.getElementById("tooltip");

  // get URL parameter c
  // var parm_c = decodeURIComponent((new RegExp('[?|&]c=' + '([^&;]+?)(&|#|;|$)')
  //   .exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;

  downloadUrl("../langs.json", function(langs) {
    langs.forEach(function (lang){ 
      var title = lang.title; 
      if (langset.has(title)) {
        var family = lang.family;
        var link = lang.link;

        //needs to be iterative
        //var iso_code = lang.iso_code; 

        var iso_codes = "";
        for(var i = 0; i < lang.iso_code.length; i++) {
          if (i > 0) {
            iso_codes = iso_codes + ", "
          }
          iso_codes = iso_codes + lang.iso_code[i]
        }

        //Needs to be iterative
        for(var j = 0; j < lang.coordinates.length; j++) {
          var coord = lang.coordinates[j];
          var point = new google.maps.LatLng( 
              parseFloat(coord.latitude), 
              parseFloat(coord.longitude)); 
          var marker = 
              new StyledMarker({
              map: map, 
              position: point,
                  styleIcon: (family in icons ? icons[family] : icons.Other)
              })
              //may not need this
              // if( parm_c != null && parm_c == iso_code) {
              //     map.panTo( point);
              //     map.setZoom( 9);
              // }
          google.maps.event.addListener(marker, 'mouseover', function() {
                  langinfo.innerHTML = "<span class=key>Language:</span> <b>" + title 
                  + "</b> <span class=key>Code:</span> <b>" + iso_codes 
                  + "</b> <span class=key>Family:</span> <b>" + family + "</b>"; 
              var projection = overlay.getProjection(); 
              var pixel = projection.fromLatLngToContainerPixel( 
                  marker.getPosition());
              tooltip.style.top = (map_pos.y + pixel.y - 60) + "px";
              tooltip.style.left = (map_pos.x + pixel.x - 11) + "px";
              tooltip.style.padding = "1px 2px"
                  tooltip.innerHTML = title;
          });

          google.maps.event.addListener(marker, 'mouseout', function() {
                  langinfo.innerHTML = ""
                  tooltip.innerHTML = ""
              tooltip.style.padding = "0"
          });

          google.maps.event.addListener(marker, 'click', function( event) {
                  if( metadown) {
                  window.open(link);
                  } else {
                  window.location.href = link;
                  }
          });   
        }
      }
  });
  })
}

function downloadUrl(url, callback) {
  var request = window.ActiveXObject ? new ActiveXObject('Microsoft.XMLHTTP') : new XMLHttpRequest;

  request.onreadystatechange = function () {
      if (request.readyState == 4) {
          request.onreadystatechange = doNothing;
          if (request.status === 200) {
              var responseData = JSON.parse(request.responseText);
              callback(responseData, request.status);
          } else {
              // Handle error cases if needed
              callback(null, request.status);
          }
      }
  };

  request.open('GET', url, true);
  request.send(null);
}
 
function doNothing() {}

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
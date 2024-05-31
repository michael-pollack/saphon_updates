var metadown = false;

$(window).bind('keydown keyup focusin mouseenter', function(evtobj) {
metadown = evtobj.metaKey || evtobj.ctrlKey;
});

$(window).bind('focusout mouseleave', function(evtobj) {
metadown = false;
});

var icons = {
  'Alacalufan' : ['#00FF00', '#000000'], // Green & Black
  'Arawak' : ['#0000FF', '#FFFFFF'],     // Blue & White
  'Arawan' : ['#FFFF00', '#000000'],     // Yellow & Black
  'Araucanian' : ['#FF00FF', '#000000'], // Magenta & Black
  'Aymaran' : ['#00FFFF', '#000000'],    // Cyan & Black
  'Barbacoan' : ['#800000', '#FFFFFF'],  // Maroon & White
  'Boran' : ['#008000', '#FFFFFF'],      // Green & White
  'Cahuapanan' : ['#000080', '#FFFFFF'], // Navy & White
  'Carib' : ['#808000', '#000000'],      // Olive & Black
  'Chapakuran' : ['#800080', '#FFFFFF'], // Purple & White
  'Charruan' : ['#008080', '#FFFFFF'],   // Teal & White
  'Chibchan' : ['#FFA500', '#000000'],   // Orange & Black
  'Choco' : ['#A52A2A', '#FFFFFF'],      // Brown & White
  'Chon' : ['#D2691E', '#FFFFFF'],       // Chocolate & White
  'Guaicuru' : ['#FF4500', '#000000'],   // OrangeRed & Black
  'Guahiban' : ['#2E8B57', '#000000'],   // SeaGreen & Black
  'Harakmbet' : ['#ADFF2F', '#000000'],  // GreenYellow & Black
  'Hibito-Cholon' : ['#7FFF00', '#000000'], // Chartreuse & Black
  'Isolate' : ['#FFFFFF', '#000000'],    // White & Black
  'Jivaroan' : ['#4B0082', '#FFFFFF'],   // Indigo & White
  'Kakua-Nukak' : ['#6A5ACD', '#FFFFFF'], // SlateBlue & White
  'Katukinan' : ['#FF6347', '#000000'],  // Tomato & Black
  'Macro-Ge' : ['#FFD700', '#000000'],   // Gold & Black
  'Mataco' : ['#8A2BE2', '#FFFFFF'],     // BlueViolet & White
  'Mixed' : ['#1E90FF', '#000000'],      // DodgerBlue & Black
  'Mosetenan' : ['#FF1493', '#000000'],  // DeepPink & Black
  'Mura' : ['#00FF7F', '#000000'],       // SpringGreen & Black
  'Nadahup' : ['#20B2AA', '#000000'],    // LightSeaGreen & Black
  'Nambiquaran' : ['#FF8C00', '#000000'], // DarkOrange & Black
  'Other' : ['#D3D3D3', '#000000'],      // LightGray & Black
  'Panoan' : ['#FF69B4', '#000000'],     // HotPink & Black
  'Peba-Yaguan' : ['#98FB98', '#000000'], // PaleGreen & Black
  'Quechua' : ['#DB7093', '#000000'],    // PaleVioletRed & Black
  'Salivan' : ['#AFEEEE', '#000000'],    // PaleTurquoise & Black
  'Tacanan' : ['#4682B4', '#000000'],    // SteelBlue & Black
  'Tucanoan' : ['#40E0D0', '#000000'],   // Turquoise & Black
  'Tupi' : ['#FF0000', '#000000'],       // Red & Black
  'Tupí' : ['#FF0000', '#000000'],       // Coral & Black
  'Uru-Chipaya' : ['#8B4513', '#FFFFFF'], // SaddleBrown & White
  'Witotoan' : ['#9ACD32', '#000000'],   // YellowGreen & Black
  'Yanomam' : ['#87CEEB', '#000000'],    // SkyBlue & Black
  'Zaparoan' : ['#8B008B', '#FFFFFF'],   // DarkMagenta & White
  'Zamucoan' : ['#556B2F', '#FFFFFF']    // DarkOliveGreen & White
};




function get_pos(el) {
for (var lx=0, ly=0;
 el != null;
 lx += el.offsetLeft, ly += el.offsetTop, el = el.offsetParent);
return {x: lx,y: ly};
}

async function initialize(pglang) {
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
    mapId: 'DEMO_MAP_ID',
    options: {
      gestureHandling: 'greedy'
    }
    //mapID: 'f4dcb8b48ec1a463'
  }
  var map_div = document.getElementById("map")
  var map_pos = get_pos( map_div)
  const map = new Map(map_div, myOptions);
  var langinfo = document.getElementById("langinfo");
  var tooltip = document.getElementById("tooltip");
  otherfamilies = {}

  downloadUrl("../lang.xml", function(data) {
    var xml = parseXml(data); 
    var langs = xml.documentElement.getElementsByTagName("marker"); 
    for (var i = 0; i < langs.length; i++) (function( lang){ 
        var title = lang.getAttribute("title"); 
        var iso_code = lang.getAttribute("iso_code"); 
        var family = lang.getAttribute("family");
        var link = lang.getAttribute("link");
        var type = lang.getAttribute("labeltype"); 
        var point = new google.maps.LatLng( 
            parseFloat(lang.getAttribute("lat")), 
            parseFloat(lang.getAttribute("lng"))); 
        var bubble = title + " (" + iso_code + `) <br/> ${pglang["family"]}: ` + family;
        const newPin = document.createElement("div");
        if (!(family in icons)){
          family = 'Other'
          newPin.textContent = iso_code.substring(0, 3);
        } else {
          newPin.textContent = family[0];
        }
        newPin.textContent = family[0];
        newPin.className = "price-tag";
        newPin.style.setProperty("--color", icons[family][0]);
        newPin.style.setProperty("--font_color", icons[family][1]);
        newPin.addEventListener('mouseover', () => {
          langinfo.innerHTML = "<span class=key>Language:</span> <b>" + title + "</b> <span class=key>Code:</span> <b>" + iso_code + "</b> <span class=key>Family:</span> <b>" + family + "</b>"; 
          tooltip.innerHTML = title;
          newPin.style.setProperty("--size", "30px");
          newPin.style.setProperty("--font_size", "28px");
        });
        newPin.addEventListener('mouseleave', function() {
          langinfo.innerHTML = ""
          tooltip.innerHTML = ""
          tooltip.style.padding = "0"
          newPin.style.setProperty("--size", "15px");
          newPin.style.setProperty("--font_size", "14px");
        });
        const marker = new AdvancedMarkerElement({
          map: map,
          position: point,
          content: newPin,
        });
        marker.addListener('click', () => {
          if(metadown) {
              window.open(link);
          } else {
              window.location.href = link;
          }
        });
    })( langs[i]);
  }); 
  console.log(otherfamilies)
  // new MarkerClusterer({map, markers});

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


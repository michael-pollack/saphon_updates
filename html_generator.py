import json
import os
import uuid
from IPAio import normalizeIPA

with open("ipa.json", 'r', encoding='utf-8') as ipa_file:
    ipa = json.load(ipa_file)

#Generates a dictionary that maps phonemes to their category codes for easy access
def flip_ipa(ipa):
    new_map = {}
    scraped_order = []
    for category in ipa:
        for symbol in category["symbols"]:
            new_map[symbol["symbol"]] = category["category"]
            scraped_order.append(symbol["symbol"])
    return new_map, scraped_order

#Dictionary flipper to ensure mappings only have to be done once
def flip_dict(original_dict):
    flipped_dict = {}
    for key, value in original_dict.items():
        flipped_dict[value] = key    
    return flipped_dict

places = {
    "Bilabial": "b",
    "Labiodental": "l",
    "Dental": "d",
    "Alveolar": "a",
    "Postalveolar": "o",
    "Retroflex": "r",
    "Palatal": "p",
    "Velar": "v",
    "Uvular": "u",
    "Pharyngeal": "f",
    "Glottal": "g",
    "Other": "q",
    "Special": "x"
    }

manners = {
    "Stop": "s",
    "Aspirated stop": "a",
    "Fricative": "f",
    "Affricate": "aff",
    "Nasal": "n",
    "Nasal compound": "p",
    "Trill": "r",
    "Tap, Flap": "t",
    "Lateral": "l",
    "Approximant": "x",
    "Implosive": "i",
    "Extra": "e"
}

heights = {
    "High": "7",
    "Low-High": "6",
    "High-Mid": "5",
    "Mid": "4",
    "Low-Mid": "3",
    "High-Low": "2",
    "Low": "1",
}

backness = {
    "Front": "f",
    "Center": "c",
    "Back": "b"
}

abbreviations = {
    "BN": "Nasal Boundary",
    "BO": "Oral Boundary",
    "LDNH": "Long Distance Nasal Harmony",
    "LDOH": "Long Distance Oral Harmony",
    "LN": "Local Nasalization",
    "LNsyll": "Long Distance Nasal Assimilation",
    "LO": "Local Oralization",
    "PNV": "Post Nasal Voicing"
}

ipa_flipped, scraped_order = flip_ipa(ipa)
places_flipped = flip_dict(places)
manners_flipped = flip_dict(manners)
heights_flipped = flip_dict(heights)
backness_flipped = flip_dict(backness)
lost_phonemes = set()

def generate_ipa_subsets(phonemes):
    consonant_subset = {
        "manners": {},
        "places": {}
    }
    vowels_subset = {
        "heights": {},
        "backness": {}
    }
    category_set = set()
    for phoneme in phonemes:
        if phoneme in ipa_flipped:
            category_set.add(ipa_flipped[phoneme])
        else:
            normalized_phoneme = normalizeIPA(phoneme)
            if normalized_phoneme in ipa_flipped:
                category_set.add(ipa_flipped[normalized_phoneme])
            else:
                lost_phonemes.add(phoneme)

    #Determines the rows and columns needed for this table
    for cat in category_set:

        #Other Consonants
        if cat[0] == "c":
            if len(cat) > 4:
                manner_name = "Affricate"
            else:
                manner_name = manners_flipped[cat[1]]
            place_name = places_flipped[cat[2]]
            consonant_subset["manners"][manner_name] = set()
            consonant_subset["places"][place_name] = set()
        
        #Vowels
        elif cat[0] == "v":
            height_name = heights_flipped[cat[1]]
            backness_name = backness_flipped[cat[2]]
            vowels_subset["heights"][height_name] = set()
            vowels_subset["backness"][backness_name] = set()
    
    #Creates the sets used to map each phoneme to a cell
    these_lost_phonemes = set()
    for phoneme in phonemes:
        if phoneme not in ipa_flipped:
            normalized_phoneme = normalizeIPA(phoneme)
            if normalized_phoneme in ipa_flipped:
                this_cat = ipa_flipped[normalized_phoneme]
            else:

                #TODO: Handle lost phonemes
                these_lost_phonemes.add(phoneme)
                continue

        else:
            this_cat = ipa_flipped[phoneme]
        if this_cat[0] == "c":
            if len(this_cat) > 4:
                consonant_subset["manners"]["Affricate"].add(phoneme)
            else:  
                consonant_subset["manners"][manners_flipped[this_cat[1]]].add(phoneme)
            consonant_subset["places"][places_flipped[this_cat[2]]].add(phoneme)
        elif this_cat[0] == "v":
            vowels_subset["heights"][heights_flipped[this_cat[1]]].add(phoneme)
            vowels_subset["backness"][backness_flipped[this_cat[2]]].add(phoneme)

    return consonant_subset, vowels_subset, these_lost_phonemes

def generate_ipa_chart(phonemes: set, allophones: dict, subset: dict, consonant: bool):
    if consonant:
        title = "Consonants"
        col, subCol = places, "places"
        row, subRow = manners, "manners"
    else:
        title = "Vowels"
        col, subCol = backness, "backness"
        row, subRow = heights, "heights"
    html = f"<h2>{title}</h2><table>"
    html += "<tr><th></th>" + "".join(f"<th>{x}</th>" for x in col if x in subset[subCol]) + "</tr>"
    pure_allophones = set(allophones.keys()) - phonemes
    for y in row: 
        if y in subset[subRow]:
            html += f"""
            <tr id="{y}"><th>{y}</th>
            """
            for x in col:
                if x in subset[subCol]:
                    html += f"<td>"
                    these_symbols = subset[subRow][y] & subset[subCol][x]
                    voiced, unvoiced = [], []
                    for symbol in these_symbols:

                        #TODO: Handle lost phonemes
                        if symbol in ipa_flipped:
                            normalized_symbol = symbol

                        else:
                            normalized_symbol = normalizeIPA(symbol)
                        if ipa_flipped[normalized_symbol][3] == "u":
                            unvoiced.append(symbol)
                        else:
                            voiced.append(symbol)
                    ordered = unvoiced + voiced
                    for symbol in ordered:
                        if symbol in pure_allophones:
                            html += f"""
                            <span id="{symbol}" class="visible-allophone"> {symbol} </span>
                            """
                        else: 
                            html += f"""
                            <span id="{symbol}" class="visible-phoneme"> {symbol} </span>
                            """
                    html += f"</td>"
            html += "</tr>"
    html += "</table>"
    return html

def generate_html_body(template, processes, process_map, phonemes, allophones, num_references=0):
    name = template.get("name", "")
    family = template.get("family", "")
    if (type(template.get("iso_codes", [""])) == list and len(template.get("iso_codes", [""])) != 0):
        iso_code = template.get("iso_codes", [""])[0]
    else:
        iso_code = "N/A"
    coordinates = template.get("coordinates", [{}])[0]
    if (type(coordinates) == list and len(coordinates) != 0):
        latitude = coordinates.get("latitude", 0.0)
        longitude = coordinates.get("longitude", 0.0)
    else: 
        latitude, longitude = "N/A", "N/A"
    synthesis_notes = template.get("synthesis", "")
    consonant_subset, vowel_subset, these_lost_phonemes = generate_ipa_subsets(phonemes | set(allophones.keys()))
    html_content = f"""
    <div class=entry>
    """
    if num_references != 0:
        html_content += f"""
        <hr>
        <h1>Document</h1>
        """
    html_content += f"""
    <h1>{name}</h1>
    <div class=field><div class=key>Language code</div><div class=value>{iso_code}</div></div>
    <div class=field><div class=key>Location</div><div class=value>{latitude}° {longitude}°</div></div>
    <div class=field><div class=key>Family</div><div class=value>{family}</div></div>
    """
    html_content += generate_ipa_chart(phonemes, allophones, consonant_subset, True)
    html_content += generate_ipa_chart(phonemes, allophones, vowel_subset, False)

    #TODO: Handle Lost Phonemes
    if len(these_lost_phonemes) != 0:
        html_content += f"""
        <div class=field><h2>Lost Phonemes</h2>{these_lost_phonemes}</div>
        """

    html_content += f"""
    <div class=field><h2>Processes</h2>{processes}</div>
    <div class=field><h2>Process Details</h2>{process_detail_scraper(template.get("processdetails", []), process_map)}</div>
    """
    if synthesis_notes == "":
        synthesis_notes = "N/A"
    html_content += f"""
    <div class=field><h2>Synthesis Notes</h2><p>{synthesis_notes}</p></div>
    """
    return html_content

def generate_html(template, filename):
    if type(template) != list:
        process_map = generate_process_map(template.get("processdetails", []))
        processes, phonemes, allophones = process_scraper(template.get("phonemes", []), process_map)
        html_content = f"""
        <html>
        <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" type="text/css" href="../../lang_info.css" />
        <script type="text/javascript"> {initialize_script(allophones)} </script>
        </head>
        <body onload="initialize()">
        """
        html_content = html_content + generate_html_body(template, processes, process_map, phonemes, allophones)
        html_content += f"""
        <div class=field><h2><a href="/en/ref_inv/{filename}">References</h2></div>
        """
    else:
        #TODO: Make allophones work here
        allophones = {}
        html_content = f"""
        <html>
        <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" type="text/css" href="../../lang_info.css" />
        <script type="text/javascript"> {initialize_script(allophones)} </script>
        <h1>Reference Documents: {template[0].get("name", "")}</h1>
        """
        for ref in template:
            process_map = generate_process_map(ref.get("processdetails", []))
            processes, phonemes, allophones = process_scraper(ref.get("phonemes", []), process_map)
            html_content += f"""
            </head>
            <body>
            """
            html_content = html_content + generate_html_body(ref, processes, process_map, phonemes, allophones, True)
        
    html_content += f"""
    </div>
    </body>
    </html>
    """
    return html_content

def highlight_phonemes_script(allophones):
    json_friendly = {allophone: list(phonemes) for allophone, phonemes in allophones.items()}
    json_allophones = json.dumps(json_friendly)
    html_content = """
    function highlight_phonemes() {
    """
    html_content += f"""
        allophones = {json_allophones};
    """
    #TODO: figure out why background-color doesn't come through in 'highlight' class
    html_content += """ 
        Object.keys(allophones).forEach(id => {
            const span = document.getElementById(id);
            if (span != null) {
                span.addEventListener('mouseover', function () {
                    allophones[id].forEach(associatedId => {
                        document.getElementById(associatedId).classList.add('highlight');
                    });
                });
                span.addEventListener('mouseout', function () {
                    allophones[id].forEach(associatedId => {
                        document.getElementById(associatedId).classList.remove('highlight');
                    });
                });
            }
        });
    }
    """
    return html_content

def dropdown_script():
    process_hider = """
    function dropdown() {
        const process_indices_span = document.getElementById("processIndexCount");
        const process_indices_raw = process_indices_span.getAttribute("data-set");
        console.log(process_indices_raw);
        const process_indices_array = JSON.parse(process_indices_raw);
        const process_subsections_list = ["undergoers", "triggers", "transparent", "opaque"];
        const process_subsections_count_span = document.getElementById("processSubsectionCount");
        const process_subsections_count = process_subsections_count_span.textContent;
        for (var i = 0; i < process_indices_array.length; i += 1) {
            let this_process = "process-" + process_indices_array[i];
            let this_name = "process-name-" + process_indices_array[i];
            let process_span = document.getElementById(this_process);
            let name_span = document.getElementById(this_name);
            process_span.addEventListener("click", function () {
                if (name_span.style.display === "none" || name_span.style.display === "") {
                    name_span.style.display = "inline";
                } else {
                    name_span.style.display = "none";
                }
            });
        }


        
        for (var j = 0; j <= process_subsections_count; j += 1) {
            for (var k = 0; k < process_subsections_list.length; k += 1) {
                let this_process_title = process_subsections_list[k] + j;
                let this_process_sub =  process_subsections_list[k] + "-sub" + j;
                let process_title_span = document.getElementById(this_process_title);
                let process_sub_span = document.getElementById(this_process_sub);
                if (process_title_span != null && process_sub_span != null) {
                    process_title_span.addEventListener("click", function () {
                        if (process_sub_span.style.display === "none" || process_sub_span.style.display === "") {
                            process_sub_span.style.display = "inline";
                            process_title_span.style.transform = "rotate(180deg)";
                        } else {
                            process_sub_span.style.display = "none";
                            process_title_span.style.transform = "rotate(0deg)";
                        }
                    });
                }
            }
        }
    }
    """
    return process_hider

def initialize_script(allophones):
    html_content = dropdown_script()
    html_content += highlight_phonemes_script(allophones)
    html_content += """
    function initialize() {
        dropdown();
        highlight_phonemes();
    }
    """
    return html_content

def process_scraper(phonemes, process_map):
    phoneme_set = set()
    allophone_map = {}
    mappings =  {}
    process_index = 0
    process_indices = set()
    for phoneme in phonemes:
        this_phoneme = phoneme["phoneme"]
        phoneme_set.add(this_phoneme)
        mappings[this_phoneme] = []
        for environment in phoneme["environments"]:
            if type(environment) == dict:
                for allophone in environment["allophones"]:
                    this_allophone = allophone["allophone"]
                    if this_allophone != this_phoneme:
                        index_hash = str(uuid.uuid4())
                        process_indices.add(index_hash)
                        process_id = "process-" + index_hash
                        process_name_id = "process-name-" + index_hash
                        process_index += 1
                        if this_allophone in allophone_map:
                            allophone_map[this_allophone].add(this_phoneme)
                        else:
                            allophone_map[this_allophone] = {this_phoneme}
                        processes = ""
                        for k in range(len(allophone["processnames"])):
                            this_process = allophone["processnames"][k]
                            if this_process in process_map:
                                this_process = process_map[this_process]
                            processes += this_process
                        process = f"""
                        <span class="process" id="{process_id}">/{this_phoneme}/ &#8594; [{this_allophone}] / {environment["preceding"]}_{environment["following"]} </span> <span class="processname" id="{process_name_id}"> <br> {processes} </span>
                        """
                        mappings[this_phoneme].append(process)
    html_content = f"""
    <div class="processtable"><table><tr><th>Phoneme</th><th>Processes</th></tr>
    """
    for mapping in scraped_order:
        if mapping in mappings and mappings[mapping] != []:
            html_content += f"""
            <tr><th> /{mapping}/ </th><td>
            """
            for index, process in enumerate(mappings[mapping]):
                html_content += f"""
                {process} <br>
                """
                if index != len(mappings[mapping]) - 1:
                    html_content += "<br>"
            
            html_content = html_content[:-4]
            html_content += f"""
            </td></tr>
            """
    json_ready = json.dumps(list(process_indices))
    print(json_ready)
    html_content += f"""
    </table></div>
    <span class="hidden" id="processIndexCount" data-set='{json_ready}'></span>
    """
    return html_content, phoneme_set, allophone_map


def segments_morphemes_and_other_fun(category):
    segNA = False
    morphNA = False
    segments = category["segments"]
    if type(segments) != list:
        segments = [segments]
    morphemes = category["morphemes"]  
    if type(morphemes) != list:
        morphemes = [morphemes]
    segment_units = ""
    morpheme_units = ""
    html_content = f"""
    <span class="process-descriptor-sub">Segments: </span>
    """
    if segments == [] or (len(segments) == 1 and ((segments[0]["units"] == [] or segments[0]["units"] == ["NA"] or segments[0]["units"] == [""]) and (segments[0]["positional_restrictions"] == "" or segments[0]["positional_restrictions"] == "NA"))):
        segNA = True
        html_content += f"""
        <span class="process-descriptor-sub">NA</span><br><br>
        """
    else: 
        html_content += "<br>"
        for segment in segments:
            seg_u_list = segment["units"]
            pos_res_list = segment["positional_restrictions"]
            if len(seg_u_list) > 1:
                segment_units += "{"
            for i in range(len(seg_u_list)):
                segment_units += seg_u_list[i]
                if i < len(seg_u_list) - 1:
                    segment_units += ", "
            if len(seg_u_list) > 1:
                segment_units += "}"
            html_content += f"""
            <span class="process-descriptor-sub">&nbsp;&nbsp;&nbsp;&nbsp;-Units: </span><span class="process-description"> {segment_units} </span><br>
            <span class="process-descriptor-sub">&nbsp;&nbsp;&nbsp;&nbsp;-Positional Restrictions: </span><span class="process-description"> {pos_res_list} </span><br><br>
            """
    html_content += f"""
    <span class="process-descriptor-sub">Morphemes: </span>
    """
    if morphemes == [] or (len(morphemes) == 1 and ((morphemes[0]["units"] == [] or morphemes[0]["units"] == ["NA"] or morphemes[0]["units"] == [""]) and (morphemes[0]["positional_restrictions"] == "" or morphemes[0]["positional_restrictions"] == "NA"))):
        morphNA = True
        html_content += f"""
        <span class="process-descriptor-sub">NA</span><br><br>
        """
    else:
        html_content += "<br>"
        for morpheme in morphemes:
            morph_u_list = morpheme["units"]
            pos_res_list = morpheme["positional_restrictions"]
            for i in range(len(morph_u_list)):
                morpheme_units += morph_u_list[i]
                if i < len(morph_u_list) - 1:
                    morpheme_units += ", "
            html_content += f"""
            <span class="process-descriptor-sub">&nbsp;&nbsp;&nbsp;&nbsp;-Units: </span><span class="process-description"> {morpheme_units} </span><br>
            <span class="process-descriptor-sub">&nbsp;&nbsp;&nbsp;&nbsp;-Positional Restrictions: </span><span class="process-description"> {morpheme["positional_restrictions"]} </span><br><br>
            """
    if segNA and morphNA:
        return "NA"
    else:
        return html_content
    
def generate_process_map(processes):
    process_map = {}
    prefix_count = {}
    for process in processes:
        process_name = process["processname"]
        process_prefix = process_name[:process_name.find(":")] if process_name.find(":") != -1 else process_name
        simple_name = abbreviations[process_prefix] if process_prefix in abbreviations else process_name
        this_count = prefix_count[process_prefix] + 1 if process_prefix in prefix_count else 1
        prefix_count[process_prefix] = this_count
        simple_name += " " + str(this_count)
        process_map[process_name] = simple_name
    return process_map

def process_detail_scraper(processes, process_map):
    html_content = ""
    process_index = 0
    for process in processes:
        process_name = process["processname"]
        simple_name = process_map[process_name]
        process_type = process["processtype"]
        description = process["description"]
        optionality = process["optionality"]
        directionality = process["directionality"]
        alternation_type = process["alternation_type"]
        domain = process["domain"]
        undergoers = segments_morphemes_and_other_fun(process["undergoers"])
        triggers = segments_morphemes_and_other_fun(process["triggers"])
        transparent = segments_morphemes_and_other_fun(process["transparent"])
        opaque = segments_morphemes_and_other_fun(process["opaque"])
        html_content += f"""
        <span class="process-title">{simple_name}</span>
        <div><table class="processDescTable">
        <tr><th><span class="process-descriptor">Abbreviation: </span></th><td><span class="process-description"> {process_name} </span></td></tr>
        <tr><th><span class="process-descriptor">Type: </span></th><td><span class="process-description"> {process_type} </span></td></tr>
        <tr><th><span class="process-descriptor">Description: </span></th><td><span class="process-description"> {description} </span></td></tr>
        <tr><th><span class="process-descriptor">Optionality: </span></th><td><span class="process-description"> {optionality} </span></td></tr>
        <tr><th><span class="process-descriptor">Directionality: </span></th><td><span class="process-description"> {directionality} </span></td></tr>
        <tr><th><span class="process-descriptor">Alternation Type: </span></th><td><span class="process-description"> {alternation_type} </span></td></tr>
        <tr><th><span class="process-descriptor">Domain: </span></th><td><span class="process-description"> {domain} </span></td></tr>
        <tr><th><span class="process-descriptor">Undergoers: </span></th><td>
        """
        if undergoers != "NA":
            html_content += f"""
            <button class="dropdown-button" id={"undergoers" + str(process_index)}> &#9660 </button>
            <span class="pd-subsection" id={"undergoers-sub" + str(process_index)}> {undergoers} </span></td></tr>
            """
        else: 
            html_content += f"""
            <span class="na"> NA </span></td></tr>
            """
        html_content += f"""
        <tr><th><span class="process-descriptor">Triggers: </span></th><td>
        """
        if triggers != "NA":
            html_content += f"""
            <button class="dropdown-button" id={"triggers" + str(process_index)}> &#9660 </button>
            <span class="pd-subsection" id={"triggers-sub" + str(process_index)}> {triggers} </span></td></tr>
            """
        else: 
            html_content += f"""
            <span class="na"> NA </span><br></td></tr>
            """
        html_content += f"""
        <tr><th><span class="process-descriptor">Transparent: </span></th><td>
        """
        if transparent != "NA":
            html_content += f"""
            <button class="dropdown-button" id={"transparent" + str(process_index)}> &#9660 </button>
            <span class="pd-subsection" id={"transparent-sub" + str(process_index)}> {transparent} </span></td></tr>
            """
        else: 
            html_content += f"""
            <span class="na"> NA </span></td></tr>
            """
        html_content += f"""
        <tr><th><span class="process-descriptor">Opaque: </span></th><td>
        """
        if opaque != "NA":
            html_content += f"""
            <button class="dropdown-button" id={"opaque" + str(process_index)}> &#9660 </button>
            <span class="pd-subsection" id={"opaque-sub" + str(process_index)}> {opaque} </span></td></tr>
            """
        else: 
            html_content += f"""
            <span class="na"> NA </span></td></tr>
            """
        html_content += f"""
        </table></div>
        <br><br>
        """
        process_index += 1
    html_content += f"""
    <span class="hidden" id="processSubsectionCount">{process_index - 1}</span>
    """
    return html_content

def process_templates_from_folder(input_folder, synth_output_folder, ref_output_folder):
    if not os.path.exists(synth_output_folder):
        os.makedirs(synth_output_folder)

    if not os.path.exists(ref_output_folder):
        os.makedirs(ref_output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            template_path = os.path.join(input_folder, filename)
            with open(template_path, 'r', encoding='utf-8') as file:
                templates = json.load(file)
                ref_templates = []
                if type(templates) == list:
                    for template in templates:
                        doctype = template.get("doctype", "")
                        output_file = f"{filename.replace('.json', '.html')}"
                        if doctype == "synthesis":
                            html_content = generate_html(template, output_file)
                            output_path = os.path.join(synth_output_folder, output_file)
                        elif doctype == "reference":
                            ref_templates.append(template)
                        else:
                            raise ValueError("Invalid Doctype")
                        with open(output_path, 'w', encoding='utf-8') as html_file:
                            html_file.write(html_content)
                        print(f"Generated Synthesis HTML file: {output_path}")
                    if ref_templates != []:
                        ref_html_content = generate_html(ref_templates, output_file)
                        ref_output_path = os.path.join(ref_output_folder, output_file)
                        with open(ref_output_path, 'w', encoding='utf-8') as ref_html_file:
                            ref_html_file.write(ref_html_content)
                        print(f"Generated Reference HTML file: {ref_output_path}")
                else:
                    print(filename + " skipped, files must be a list")
    print(lost_phonemes)

# Specify the folder containing template files and the output folder for HTML files
input_folder = "new_json"
synth_output_folder = "en/synth_inv"
ref_output_folder = "en/ref_inv"
# Run the script to process all template files in the specified folder and save the HTML files in the output folder
process_templates_from_folder(input_folder, synth_output_folder, ref_output_folder)

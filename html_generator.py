import json
import os

with open("ipa.json", 'r', encoding='utf-8') as ipa_file:
    ipa = json.load(ipa_file)

places = {
    "bilabial": "b",
    "labiodental": "d",
    "dental": "d",
    "alveolar": "a",
    "postalveolar": "o",
    "retroflex": "r",
    "palatal": "p",
    "velar": "v",
    "uvular": "u",
    "pharyngeal": "f",
    "glottal": "g",
    "other": "q",
    "special": "x"
    }

manners = {
    "stop": "s",
    "aspirated stop": "a",
    "fricative": "f",
    "nasal": "n",
    "nasal compound": "p",
    "trill": "r",
    "tap, flap": "t",
    "lateral": "l",
    "approximant": "x",
    "implosive": "i",
    "extra": "e"
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

def flip_ipa(ipa):
    new_map = {}
    for category in ipa:
        for symbol in category["symbols"]:
            new_map[symbol["symbol"]] = category["category"]
    return new_map

print(flip_ipa(ipa))

def generate_base_consonant_chart(ipa):
    html = "<html><head><style>table, th, td { border: 1px solid black; border-collapse: collapse; padding: 5px; }</style></head><body>"
    # Generate consonant table
    html += "<h2>Consonants</h2><table>"
    html += "<tr><th></th>" + "".join(f"<th>{place}</th>" for place in places) + "</tr>"
    iterations = 0
    for manner in manners:
        manner_prefix = "c" + manners[manner]
        html += f"""
        <tr id="{manner}"><th>{manner}</th>
        """
        for place in places:
            place_prefix = manner_prefix + places[place]
            voiced_cat_id, unvoiced_cat_id = place_prefix + "v", place_prefix + "u"
            voiced_cats = [cat for cat in ipa if cat.get("category") == voiced_cat_id]
            unvoiced_cats = [cat for cat in ipa if cat.get("category") == unvoiced_cat_id]
            if voiced_cats != []:
                voiced_cats = voiced_cats[0]["symbols"]
            if unvoiced_cats != []:
                unvoiced_cats = unvoiced_cats[0]["symbols"]
            cell_content = [symbol["symbol"] for symbol in voiced_cats] + [symbol["symbol"] for symbol in unvoiced_cats]
            html += f"<td>"
            for phoneme in cell_content:
                html += f"""
                <span id="{phoneme}" class="hidden"> {phoneme} </span>
                """
            html += f"</td>"
            iterations += 1
        html += "</tr>"
    html += "</table>"
    print(iterations)
    return html

def generate_base_vowel_chart(ipa):
    html = "<html><head><style>table, th, td { border: 1px solid black; border-collapse: collapse; padding: 5px; }</style></head><body>"
    # Generate consonant table
    html += "<h2>Vowels</h2><table>"
    html += "<tr><th></th>" + "".join(f"<th>{depth}</th>" for depth in backness) + "</tr>"
    iterations = 0
    for height in heights:
        height_prefix = "v" + heights[height]
        html += f"<tr><th>{height}</th>"
        for depth in backness:
            depth_prefix = height_prefix + backness[depth]
            rounded_cat_id, unrounded_cat_id = depth_prefix + "r", depth_prefix + "u"
            rounded_cats = [cat for cat in ipa if cat.get("category") == rounded_cat_id]
            unrounded_cats = [cat for cat in ipa if cat.get("category") == unrounded_cat_id]
            if rounded_cats != []:
                rounded_cats = rounded_cats[0]["symbols"]
            if unrounded_cats != []:
                unrounded_cats = unrounded_cats[0]["symbols"]
            cell_content = [symbol["symbol"] for symbol in rounded_cats] + [symbol["symbol"] for symbol in unrounded_cats]
            html += f"<td>"
            for phoneme in cell_content:
                html += f"""
                <span id="{phoneme}" class="hidden"> {phoneme} </span>
                """
            html += f"</td>"
            iterations += 1
        html += "</tr>"
    html += "</table>"
    print(iterations)
    return html

base_consonant_chart = generate_base_consonant_chart(ipa)
base_vowel_chart = generate_base_vowel_chart(ipa)

#Generates JavaScript that can be imbedded in the HTML file. 
def generate_phoneme_script(phonemes, allophones):
    phoneme_script = """
    function writePhonemes() {
        const phonemes = """
    
    phoneme_script += str(phonemes) + ";"

    phoneme_script += """
        const allophones = """
    
    phoneme_script += str(allophones) + ";"

    phoneme_script += """
        const phonSet = new Set()
        for (var i = 0; i < phonemes.length; i += 1) {
            this_phon = document.getElementById(phonemes[i])
            if(this_phon != null) {
                this_phon.classList.toggle("visible-phoneme")
                phonSet.add(this_phon)
            }
        }
        for (var i = 0; i < allophones.length; i += 1) {
            this_aphon = document.getElementById(allophones[i])
            if(this_aphon != null && !phonSet.has(this_aphon)) {
                this_aphon.classList.toggle("visible-allophone")
            }
        }
    }
    """
    return phoneme_script

def generate_html_body(template, processes):
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
    html_content = f"""
    <div class=entry>
    <h1>{name}</h1>
    <div class=field><div class=key>Language code</div><div class=value>{iso_code}</div></div>
    <div class=field><div class=key>Location</div><div class=value>{latitude}° {longitude}°</div></div>
    <div class=field><div class=key>Family</div><div class=value>{family}</div></div>
    <div class=field><table class=inv>
    """
    html_content += base_consonant_chart
    html_content += base_vowel_chart
    html_content += f"""
    <div class=field><h2>Synthesis Notes</h2><p>{synthesis_notes}</p></div>
    <div class=field><h2>Processes</h2>{processes}</div>
    <div class=field><h2>References</h2></div>
    """
    return html_content

def generate_html(template):
    phonemes = []
    processes = ""
    allophones = []
    if type(template) != list:
        processes, phonemes, allophones = process_scraper(template.get("phonemes", []))
        html_content = f"""
        <html>
        <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" type="text/css" href="../../lang_info.css" />
        <script type="text/javascript">{generate_phoneme_script(phonemes, allophones)}</script>
        </head>
        <body onload="writePhonemes()">
        """
        html_content = html_content + generate_html_body(template, processes)
    else:
        html_content = f"""
        <html>
        <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" type="text/css" href="../../lang_info.css" />
        <h1>Reference Documents: {template[0].get("name", "")}</h1>
        """
        for ref in template:
            processes, phonemes, allophones = process_scraper(ref.get("phonemes", []))
            html_content += f"""
            <script type="text/javascript">{generate_phoneme_script(phonemes, allophones)}</script>
            </head>
            <body onload="writePhonemes()">
            """
            html_content = html_content + generate_html_body(ref, processes)
        
    html_content += f"""
    </div>
    </body>
    </html>
    """
    return html_content

def process_scraper(phonemes):
    phoneme_list = []
    allophone_list = []
    mappings =  {}
    for phoneme in phonemes:
        phoneme_list.append(phoneme["phoneme"])
        mappings[phoneme["phoneme"]] = []
        for environment in phoneme["environments"]:
            if type(environment) == dict:
                for allophone in environment["allophones"]:
                    if allophone["allophone"] != phoneme["phoneme"]:
                        allophone_list.append(allophone["allophone"])
                        processes = ""
                        for k in range(len(allophone["processnames"])):
                            if k != 0:
                                processes += " ,"
                            processes +=  allophone["processnames"][k]
                            if k == len(allophone["processnames"]) - 1:
                                processes += ": "
                        process = f"""
                        <span class="processname"> {processes} </span> <br> <span class="process">/{phoneme["phoneme"]}/ -> [{allophone["allophone"]}] / {environment["preceding"]}_{environment["following"]} </span>
                        """
                        mappings[phoneme["phoneme"]].append(process)

    html_content = f"""
    <div class="processtable"><table><tr><th>Phoneme</th><th>Processes</th></tr>
    """
    for mapping in mappings:
        if mappings[mapping] != []:
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
    html_content += f"""
    </table></div>
    """
    return html_content, phoneme_list, allophone_list

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
                            html_content = generate_html(template)
                            output_path = os.path.join(synth_output_folder, output_file)
                        elif doctype == "reference":
                            ref_templates.append(template)
                        else:
                            raise ValueError("Invalid Doctype")
                        with open(output_path, 'w', encoding='utf-8') as html_file:
                            html_file.write(html_content)
                        print(f"Generated Synthesis HTML file: {output_path}")
                    if ref_templates != []:
                        ref_html_content = generate_html(ref_templates)
                        ref_output_path = os.path.join(ref_output_folder, output_file)
                        with open(ref_output_path, 'w', encoding='utf-8') as ref_html_file:
                            ref_html_file.write(ref_html_content)
                        print(f"Generated Reference HTML file: {ref_output_path}")
                else:
                    print(filename + " skipped, files must be a list")

# Specify the folder containing template files and the output folder for HTML files
input_folder = "new_json"
synth_output_folder = "en/synth_inv"
ref_output_folder = "en/ref_inv"
# Run the script to process all template files in the specified folder and save the HTML files in the output folder
process_templates_from_folder(input_folder, synth_output_folder, ref_output_folder)

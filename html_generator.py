import json
import os

with open("ipa.json", 'r', encoding='utf-8') as ipa_file:
    ipa = json.load(ipa_file)

#Generates a dictionary that maps phonemes to their category codes for easy access
def flip_ipa(ipa):
    new_map = {}
    for category in ipa:
        for symbol in category["symbols"]:
            new_map[symbol["symbol"]] = category["category"]
    return new_map

ipa_flipped = flip_ipa(ipa)

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
            lost_phonemes.add(phoneme)
    #category_set = set([ipa_flipped[phoneme] for phoneme in phonemes])

    #Determines the rows and columns needed for this table
    for cat in category_set:
        if cat[0] == "c":
            manner_name = manners_flipped[cat[1]]
            place_name = places_flipped[cat[2]]
            consonant_subset["manners"][manner_name] = set()
            consonant_subset["places"][place_name] = set()
        elif cat[0] == "v":
            height_name = heights_flipped[cat[1]]
            backness_name = backness_flipped[cat[2]]
            vowels_subset["heights"][height_name] = set()
            vowels_subset["backness"][backness_name] = set()
    
    #Creates the sets used to map each phoneme to a cell
    for phoneme in phonemes:
        if phoneme in ipa_flipped:
            this_cat = ipa_flipped[phoneme]
            if this_cat[0] == "c":
                consonant_subset["manners"][manners_flipped[this_cat[1]]].add(phoneme)
                consonant_subset["places"][places_flipped[this_cat[2]]].add(phoneme)
            elif this_cat[0] == "v":
                vowels_subset["heights"][heights_flipped[this_cat[1]]].add(phoneme)
                vowels_subset["backness"][backness_flipped[this_cat[2]]].add(phoneme)

    return consonant_subset, vowels_subset

def generate_ipa_chart(phonemes: set, allophones: set, subset: dict, consonant: bool):
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
    pure_allophones = allophones - phonemes
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
                        if ipa_flipped[symbol][3] == "u":
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

#Generates JavaScript that can be imbedded in the HTML file. 
# def generate_phoneme_script(phonemes, allophones):
#     phoneme_script = """
#     function writePhonemes() {
#         const phonemes = """
    
#     phoneme_script += str(phonemes) + ";"

#     phoneme_script += """
#         const allophones = """
    
#     phoneme_script += str(allophones) + ";"

#     phoneme_script += """
#         const phonSet = new Set()
#         for (var i = 0; i < phonemes.length; i += 1) {
#             this_phon = document.getElementById(phonemes[i])
#             if(this_phon != null) {
#                 this_phon.classList.toggle("visible-phoneme")
#                 phonSet.add(this_phon)
#             }
#         }
#         for (var i = 0; i < allophones.length; i += 1) {
#             this_aphon = document.getElementById(allophones[i])
#             if(this_aphon != null && !phonSet.has(this_aphon)) {
#                 this_aphon.classList.toggle("visible-allophone")
#             }
#         }
#     }
#     """
#     return phoneme_script

def generate_html_body(template, processes, phonemes, allophones):
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
    consonant_subset, vowel_subset = generate_ipa_subsets(phonemes | allophones)
    html_content = f"""
    <div class=entry>
    <h1>{name}</h1>
    <div class=field><div class=key>Language code</div><div class=value>{iso_code}</div></div>
    <div class=field><div class=key>Location</div><div class=value>{latitude}° {longitude}°</div></div>
    <div class=field><div class=key>Family</div><div class=value>{family}</div></div>
    <div class=field><table class=inv>
    """
    html_content += generate_ipa_chart(phonemes, allophones, consonant_subset, True)
    html_content += generate_ipa_chart(phonemes, allophones, vowel_subset, False)
    html_content += f"""
    <div class=field><h2>Synthesis Notes</h2><p>{synthesis_notes}</p></div>
    <div class=field><h2>Processes</h2>{processes}</div>
    <div class=field><h2>References</h2></div>
    """
    return html_content

def generate_html(template):
    if type(template) != list:
        processes, phonemes, allophones = process_scraper(template.get("phonemes", []))
        html_content = f"""
        <html>
        <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" type="text/css" href="../../lang_info.css" />
        </head>
        <body>
        """
        html_content = html_content + generate_html_body(template, processes, phonemes, allophones)
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
            </head>
            <body>
            """
            html_content = html_content + generate_html_body(ref, processes, phonemes, allophones)
        
    html_content += f"""
    </div>
    </body>
    </html>
    """
    return html_content

def process_scraper(phonemes):
    phoneme_set = set()
    allophone_set = set()
    mappings =  {}
    for phoneme in phonemes:
        phoneme_set.add(phoneme["phoneme"])
        mappings[phoneme["phoneme"]] = []
        for environment in phoneme["environments"]:
            if type(environment) == dict:
                for allophone in environment["allophones"]:
                    if allophone["allophone"] != phoneme["phoneme"]:
                        allophone_set.add(allophone["allophone"])
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
    return html_content, phoneme_set, allophone_set

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
    print(lost_phonemes)

# Specify the folder containing template files and the output folder for HTML files
input_folder = "new_json"
synth_output_folder = "en/synth_inv"
ref_output_folder = "en/ref_inv"
# Run the script to process all template files in the specified folder and save the HTML files in the output folder
process_templates_from_folder(input_folder, synth_output_folder, ref_output_folder)

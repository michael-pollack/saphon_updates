import json
import os

ipa_consonants = {
    "p": ("bilabial", "plosive", "voiceless"),
    "b": ("bilabial", "plosive", "voiced"),
    "t": ("alveolar", "plosive", "voiceless"),
    "d": ("alveolar", "plosive", "voiced"),
    "k": ("velar", "plosive", "voiceless"),
    "g": ("velar", "plosive", "voiced"),
    "ʔ": ("glottal", "plosive", "voiceless"),
    "m": ("bilabial", "nasal", "voiced"),
    "n": ("alveolar", "nasal", "voiced"),
    "ŋ": ("velar", "nasal", "voiced"),
    "ɱ": ("labiodental", "nasal", "voiced"),
    "ɳ": ("retroflex", "nasal", "voiced"),
    "ɲ": ("palatal", "nasal", "voiced"),
    "ɴ": ("uvular", "nasal", "voiced"),
    "ʙ": ("bilabial", "trill", "voiced"),
    "r": ("alveolar", "trill", "voiced"),
    "ʀ": ("uvular", "trill", "voiced"),
    "ɾ": ("alveolar", "tap", "voiced"),
    "ɽ": ("retroflex", "tap", "voiced"),
    "ɸ": ("bilabial", "fricative", "voiceless"),
    "β": ("bilabial", "fricative", "voiced"),
    "f": ("labiodental", "fricative", "voiceless"),
    "v": ("labiodental", "fricative", "voiced"),
    "θ": ("dental", "fricative", "voiceless"),
    "ð": ("dental", "fricative", "voiced"),
    "s": ("alveolar", "fricative", "voiceless"),
    "z": ("alveolar", "fricative", "voiced"),
    "ʃ": ("postalveolar", "fricative", "voiceless"),
    "ʒ": ("postalveolar", "fricative", "voiced"),
    "ʂ": ("retroflex", "fricative", "voiceless"),
    "ʐ": ("retroflex", "fricative", "voiced"),
    "ç": ("palatal", "fricative", "voiceless"),
    "ʝ": ("palatal", "fricative", "voiced"),
    "x": ("velar", "fricative", "voiceless"),
    "ɣ": ("velar", "fricative", "voiced"),
    "χ": ("uvular", "fricative", "voiceless"),
    "ʁ": ("uvular", "fricative", "voiced"),
    "ħ": ("pharyngeal", "fricative", "voiceless"),
    "ʕ": ("pharyngeal", "fricative", "voiced"),
    "h": ("glottal", "fricative", "voiceless"),
    "ɦ": ("glottal", "fricative", "voiced"),
    "ʋ": ("labiodental", "approximant", "voiced"),
    "ɹ": ("alveolar", "approximant", "voiced"),
    "ɻ": ("retroflex", "approximant", "voiced"),
    "j": ("palatal", "approximant", "voiced"),
    "ɰ": ("velar", "approximant", "voiced"),
    "l": ("alveolar", "lateral approximant", "voiced"),
    "ɭ": ("retroflex", "lateral approximant", "voiced"),
    "ʎ": ("palatal", "lateral approximant", "voiced"),
    "ʟ": ("velar", "lateral approximant", "voiced"),
    "ɬ": ("alveolar", "lateral fricative", "voiceless"),
    "ɮ": ("alveolar", "lateral fricative", "voiced"),
    "ɺ": ("alveolar", "lateral flap", "voiced"),
    "ɕ": ("alveolo-palatal", "fricative", "voiceless"),
    "ʑ": ("alveolo-palatal", "fricative", "voiced"),
    "ɧ": ("simultaneous postalveolar and velar", "fricative", "voiceless")
}

ipa_vowels = {
    "i": ("high", "front"),
    "y": ("high", "front"),
    "ɨ": ("high", "central"),
    "ʉ": ("high", "central"),
    "ɯ": ("high", "back"),
    "u": ("high", "back"),
    "ɪ": ("near-high", "front"),
    "ʏ": ("near-high", "front"),
    "ʊ": ("near-high", "back"),
    "e": ("close-mid", "front"),
    "ø": ("close-mid", "front"),
    "ɘ": ("close-mid", "central"),
    "ɵ": ("close-mid", "central"),
    "ɤ": ("close-mid", "back"),
    "o": ("close-mid", "back"),
    "ə": ("mid", "central"),
    "ɛ": ("open-mid", "front"),
    "œ": ("open-mid", "front"),
    "ɜ": ("open-mid", "central"),
    "ɞ": ("open-mid", "central"),
    "ʌ": ("open-mid", "back"),
    "ɔ": ("open-mid", "back"),
    "æ": ("near-open", "front"),
    "ɐ": ("near-open", "central"),
    "a": ("open", "front"),
    "ɶ": ("open", "front"),
    "ɑ": ("open", "back"),
    "ɒ": ("open", "back")
}

lost_phonemes = {"a"}

def generate_html(template):
    name = template.get("name", "")
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
    family = template.get("family", "")
    phonemes = template.get("phonemes", [])
    processes = process_scraper(phonemes)
    synthesis_notes = template.get("synthesis", "")
    html_content = f"""
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link rel="stylesheet" type="text/css" href="../../inv.css" />
    </head>
    <body>
    <div class=entry>
    <h1>{name}</h1>
    <div class=field><div class=key>Language code</div><div class=value>{iso_code}</div></div>
    <div class=field><div class=key>Location</div><div class=value>{latitude}° {longitude}°</div></div>
    <div class=field><div class=key>Family</div><div class=value>{family}</div></div>
    <div class=field><table class=inv>
    """
    html_content += generate_ipa_html_table([phon["phoneme"] for phon in phonemes])
    html_content += f"""
    <div class=field><h2>Synthesis Notes</h2><p>{synthesis_notes}</p></div>
    <div class=field><h2>Processes</h2>{processes}</div>
    <div class=field><h2>References</h2></div>
    </div>
    </body>
    </html>
    """
    
    return html_content

def process_scraper(phonemes):
    mappings =  {}
    for phoneme in phonemes:
        mappings[phoneme["phoneme"]] = []
        for environment in phoneme["environments"]:
            for allophone in environment["allophones"]:
                if allophone["allophone"] != phoneme["phoneme"]:
                    process = "/" + phoneme["phoneme"] + "/ -> [" + allophone["allophone"] + "] / " + environment["preceding"] + "_" + environment["following"]
                    mappings[phoneme["phoneme"]].append(process)

    html_content = f"""
    <div><table><tr><th>Phoneme</th><th>Processes</th></tr>
    """
    for mapping in mappings:
        if mappings[mapping] != []:
            html_content += f"""
            <tr><th> /{mapping}/ </th><td>
            """
            for process in mappings[mapping]:
                html_content += f"""
                {process} <br>
                """
            html_content += f"""
            </td></tr>
            """
    html_content += f"""
    </table></div>
    """
    return html_content

def generate_ipa_html_table(phonemes):
    # Consonant categories
    places = ["bilabial", "labiodental", "dental", "alveolar", "postalveolar", "retroflex", "palatal", "velar", "uvular", "pharyngeal", "glottal"]
    manners = ["plosive", "nasal", "trill", "tap", "fricative", "lateral fricative", "approximant", "lateral approximant"]

    # Vowel categories
    heights = ["high", "near-high", "close-mid", "mid", "open-mid", "near-open", "open"]
    backness = ["front", "central", "back"]

    # Initialize HTML table structure
    html = "<html><head><style>table, th, td { border: 1px solid black; border-collapse: collapse; padding: 5px; }</style></head><body>"

    # Generate consonant table
    html += "<h2>Consonants</h2><table>"
    html += "<tr><th></th>" + "".join(f"<th>{place}</th>" for place in places) + "</tr>"
    for manner in manners:
        html += f"<tr><th>{manner}</th>"
        for place in places:
            cell_content = [phoneme for phoneme in phonemes if phoneme in ipa_consonants and ipa_consonants[phoneme][:2] == (place, manner)]
            for phoneme in phonemes:
                if phoneme not in ipa_consonants:
                    lost_phonemes.add(phoneme)
            html += f"<td>{' '.join(cell_content)}</td>"
        html += "</tr>"
    html += "</table>"

    # Generate vowel table
    html += "<h2>Vowels</h2><table>"
    html += "<tr><th></th>" + "".join(f"<th>{back}</th>" for back in backness) + "</tr>"
    for height in heights:
        html += f"<tr><th>{height}</th>"
        for back in backness:
            cell_content = [phoneme for phoneme in phonemes if phoneme in ipa_vowels and ipa_vowels[phoneme] == (height, back)]
            html += f"<td>{' '.join(cell_content)}</td>"
        html += "</tr>"
    html += "</table>"

    # Close HTML structure
    html += "</body></html>"
    return html

def process_templates_from_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            template_path = os.path.join(input_folder, filename)
            with open(template_path, 'r', encoding='utf-8') as file:
                template = json.load(file)
                doctype = template.get("doctype", "")
                html_content = generate_html(template)
                output_file = f"{template['name'].replace(' ', '_').replace(',', '').replace(':', '')}.html"
                output_path = os.path.join(output_folder, output_file)
                with open(output_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_content)
                print(f"Generated HTML file: {output_path}")
    print(lost_phonemes)

# Specify the folder containing template files and the output folder for HTML files
input_folder = "json"
output_folder = "en/new_inv"
# Run the script to process all template files in the specified folder and save the HTML files in the output folder
process_templates_from_folder(input_folder, output_folder)

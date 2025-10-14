import csv
import xml.etree.ElementTree as ET
import pandas as pd

# Configuration
xml_file = "microfilm.xml"
template_csv = "template.csv"
output_csv = "output.csv"

# Parse XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Read csv template headers
with open(template_csv, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

# List for output rows
output_rows = []

# Helper function to append or create value
def append_value(current, new_value):
    if not new_value:
        return current
    if current:
        return f"{current}; {new_value}"
    return new_value

# Iterate through each record in XML
for record in root.findall("Microfilm_x0020_List"):
    data = {}

    # Extract XML field values
    fields = {child.tag: child.text.strip() if child.text else "" for child in record}

    # Filter for microfilm only records
    if fields.get("ACCESSNUM", "").strip() != "MFO":
        continue

    # get values from NEGATIVE
    if fields.get("NEGATIVE") == "Y":
        data["accession_content_description"] = "Negatives"

    # get values from TARGETBY
    if fields.get("TARGETBY"):
        data["accession_general_note"] = append_value(data.get("accession_general_note"), f"Processed by {fields['TARGETBY']}.")

    # get values from CATALOG
    if fields.get("CATALOG"):
        data["accession_general_note"] = append_value(data.get("accession_general_note"), f"Cataloged by {fields['CATALOG']}.")

    # get values from THS
    if fields.get("THS") == "Y":
        data["accession_provenance"] = append_value(data.get("accession_provenance"), "Acquired from THS.")

    # get values from ACQUIS
    acquis_value = fields.get("ACQUIS", "").strip()
    if acquis_value == "L":
        data["accession_acquisition_type"] = "Loan"
    elif acquis_value == "P":
        data["accession_acquisition_type"] = "Purchase"
    elif acquis_value == "O":
        data["accession_acquisition_type"] = "Originals"

    # get values from SIZE
    size_value = fields.get("SIZE", "").strip()
    if size_value == "35":
        data["extent_type"] = "microfilm reel(s)"
        data["extent_container_summary"] = "35 mm"
    elif size_value == "16":
        data["extent_type"] = "microfilm reel(s)"
        data["extent_container_summary"] = "16 mm"
    elif size_value == "":
        data["extent_type"] = "microfilm reel(s)"

    # get values from RESTRICTED
    restricted_value = fields.get("RESTRICTED", "").strip()
    if restricted_value == "":
        data["accession_access_restrictions"] = "0"
    elif restricted_value == "Y":
        data["accession_access_restrictions"] = "1"
        data["accession_access_restrictions_note"] = "Some materials in this accession are restricted."

    # get values from DATE_ASSIGNED
    if fields.get("DATE_ASSIGNED"):
        date_clean = fields["DATE_ASSIGNED"].split("T")[0]
        data["date_1_begin"] = date_clean
        data["date_1_type"] = "single"

    # Direct mappings
    if fields.get("COLLECTION"):
        data["accession_title"] = fields["COLLECTION"]
    if fields.get("MFNUMBER"):
        data["accession_number_1"] = fields["MFNUMBER"]
    if fields.get("REELS"):
        data["extent_number"] = fields["REELS"]


    # Fill missing template fields with blanks
    row = {col: data.get(col, "") for col in fieldnames}
    output_rows.append(row)

# Convert to DataFrame for date formatting
df = pd.DataFrame(output_rows)

# Convert dates from mm/dd/yyyy to yyyy-mm-dd
if "date_1_begin" in df.columns:
    df["date_1_begin"] = pd.to_datetime(
        df["date_1_begin"], errors="coerce", infer_datetime_format=True
    ).dt.strftime("%Y-%m-%d")

# Write to csv
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

print(f"✅ Done! Wrote {len(df)} rows to {output_csv}")
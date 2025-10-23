# 🎞️ Microfilm XML to ArchivesSpace CSV Converter

## 📘 Overview
This Python script parses a Microsoft Access **XML export** containing microfilm accession records, and transforms it into a **CSV file** formatted for **ArchivesSpace bulk accessions**.  
It automatically maps XML fields to ArchivesSpace CSV fields, applies conditional logic, and reformats dates for consistency. The fields and code can be modified as needed to accomodate an institution's unique XML schema.

---

## ⚙️ Features
✅ Converts XML records into an ArchivesSpace-compatible CSV  
✅ Applies conditional logic for fields like restrictions, acquisition type, and extent  
✅ Reformats dates from `mm/dd/yyyy` → `yyyy-mm-dd`  
✅ Adds standardized language and script values (`eng`, `Latn`)  
✅ Detects resource type keywords (`papers`, `records`, `collection`)  
✅ Fills missing fields using a template CSV  
✅ Outputs a clean, UTF-8 encoded CSV file ready for import into ArchivesSpace  

---

## 🧩 Field Mapping Summary / Metadata Application Profile

| XML Field | CSV Field | Logic |
|------------|------------|-------|
| `ACCESSNUM` | Used to filter only records with value `"MFO"` | Extract data only from microfilm only (MFO) collections |
| `NEGATIVE` | `accession_content_description` | `"Y"` → `"Negatives"` |
| `TARGETBY` | `accession_processors` |
| `NOTES` | `accession_provenance` | Appended to provenance |
| `CATALOGED_x003F_` | `accession_cataloged` | `"YES"` → `1`, `"NO"` → `0` |
| `THS` | `accession_provenance` | `"Y"` → `"Acquired from THS."` |
| `ACQUIS` | `accession_acquisition_type` | `"L"` → Loan, `"P"` → Purchase, `"O"` → Originals |
| `SIZE` | `extent_type`, `extent_container_summary` | `"35"` → `35 mm`, `"16"` → `16 mm`, default = `"microfilm reel(s)"` |
| `RESTRICTED` | `accession_restrictions_apply`, `accession_access_restrictions_note` | `"Y"` → restricted note, `"N"` or blank → unrestricted |
| `DATE_ASSIGNED` | `date_1_begin`, `date_1_type`, `date_1_label` | Reformatted to `yyyy-mm-dd`, type = `"single"`, label = `"Targeted"` |
| `COLLECTION` | `accession_title` | Directly mapped |
| `COLLECTION` | `date_2_begin`, `date_2_end`, `date_2_label` | Extracts collection dates from collection title |
| *(analyzed from title)* | `accession_resource_type` | `"papers"`, `"records"`, `"collection"` keyword detection; default = `"collection"` |
| `MFNUMBER` | `accession_number_1` | Prepends `"MF. "` |
| `REELS` | `extent_number` | Direct mapping |

---

## 🌍 Default Values Added to Every Record

| Field | Value |
|--------|--------|
| `accession_language` | `eng` |
| `accession_script` | `Latn` |
| `lang_material_language` | `eng` |
| `lang_material_script` | `Latn` |

---

## 🧮 Date Handling
Dates from the XML (`DATE_ASSIGNED`) are expected in `mm/dd/yyyy` format.  
They are automatically converted to ISO `yyyy-mm-dd` format using `pandas`.

---

## 📂 File Inputs & Outputs
**Inputs**
- `microfilm.xml` → The XML source file.
- `template.csv` → The ArchivesSpace bulk accession import template (ArchivesSpace users can download the CSV template by clicking on the dropdown menu with the gear icon and navigating to Bulk Import Templates)

**Output**
- `output.csv` → A fully populated, UTF-8 encoded CSV ready for import.

---

## 🧾 Notes
The script only works as well as your data is cleaned. If your institution has not stored data in a standardized format, parts of the spreadsheet may have to be completed by hand (For example, in my case, our institution included the microfilm reel count for most of the collections, but not all. I had to go to the microfilm room and count the number of reels for the ~10 collections that were missing that information).
* The script assumes the XML export uses consistent element names.
* Missing fields are filled with blanks to preserve CSV structure.
* The resulting CSV can be validated or modified in Excel before importing into ArchivesSpace.
* If you need to adapt this for non-microfilm only accessions, adjust the filter condition (ACCESSNUM = "MFO") in the code.
* If DATE_ASSIGNED is missing, the record will still be included (without date fields).
* Dates that cannot be parsed will appear as blank.
---

## 🚀 How to Run

### 1️⃣ Install Dependencies
Make sure you have Python 3 and the required libraries installed:
```bash
pip install pandas
```

### 2️⃣ Place Files in the Same Folder
```pgsql
microfilm.xml
template.csv
db_migration.py (whatever your Python script is named)
```

### 3️⃣ Run the Script
Run the script from your terminal or command prompt:
```bash
python db_migration.py
```
When finished, you'll see:
```pgsql
✅ Done! Wrote X rows to output.csv
```

---

✍️ Created with care to streamline archival data cleanup and migration workflows.

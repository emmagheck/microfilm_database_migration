# Microfilm Accessions Migration Script

This Python script migrates microfilm-only **accession records** from a **Microsoft Access export (in XML format)** to a **CSV file** formatted for import into [ArchivesSpace](https://archivesspace.org/).

It filters and transforms relevant data fields from the XML export, applies consistent data mapping and formatting, and outputs a ready-to-import CSV using a provided ArchivesSpace CSV template.

---

## 🧩 Features

- Filters **microfilm-only** accessions (`ACCESSNUM = "MFO"`)
- Maps key fields from the Access XML export to ArchivesSpace accession CSV fields
- Handles conditional logic for provenance, restrictions, dates, and extent information
- Converts date formats to ISO (`YYYY-MM-DD`)
- Preserves existing ArchivesSpace CSV template headers
- Outputs a UTF-8 encoded, ready-to-import CSV

---

## 🗂️ Input Files

### 1. `microfilm.xml`
An XML file exported from Microsoft Access containing microfilm accession data.  
Each record should be wrapped in a `<Microfilm_x0020_List>` element.

### 2. `template.csv`
A CSV file containing **ArchivesSpace accession import headers**.  
This ensures the output CSV matches the expected field structure for ArchivesSpace.

---

## 💾 Output

### `output.csv`
A new CSV file containing transformed and standardized accession data ready for import into ArchivesSpace.

---

## ⚙️ Configuration
File paths for input and output files are defined at the top of the script. Edit these values to match your local setup.

```python
xml_file = "microfilm.xml"
template_csv = "template.csv"
output_csv = "output.csv"
```
---

## 🧠 Field Mapping Overview

| Source Field (Access XML) | ArchivesSpace Field                                                   | Transformation / Logic                                                   |
| ------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `ACCESSNUM`               | *(filter)*                                                            | Only include records where `ACCESSNUM = "MFO"`                           |
| `MFNUMBER`                | `accession_number_1`                                                  | Direct copy                                                              |
| `COLLECTION`              | `accession_title`                                                     | Direct copy                                                              |
| `REELS`                   | `extent_number`                                                       | Direct copy                                                              |
| `SIZE`                    | `extent_type`, `extent_container_summary`                             | `35` → “microfilm reel(s)”, “35 mm”; `16` → “microfilm reel(s)”, “16 mm” |
| `RESTRICTED`              | `accession_access_restrictions`, `accession_access_restrictions_note` | Blank = `0`; `Y` = `1` and note added                                    |
| `NEGATIVE`                | `accession_content_description`                                       | `Y` → “Negatives”                                                        |
| `TARGETBY`, `CATALOG`     | `accession_general_note`                                              | Appends “Processed by…” or “Cataloged by…”                               |
| `THS`                     | `accession_provenance`                                                | `Y` → “Acquired from THS.”                                               |
| `ACQUIS`                  | `accession_acquisition_type`                                          | `L` = Loan; `P` = Purchase; `O` = Originals                              |
| `DATE_ASSIGNED`           | `date_1_begin`, `date_1_type`                                         | Converts to ISO format; type = “single”                                  |

---

## 🧰 Requirements

* Python 3.8+
* Libraries:
  * pandas
  * Standard libraries: csv, xml.etree.ElementTree
    
Install dependencies (if not already installed):
```python
pip install pandas
```

---

## 🚀 Usage
1. Place microfilm.xml and template.csv in the same directory as the script.
2. Run the script:
```python
python db_migration.py
```
3. The script will create output.csv in the same directory and print a summary message to the console, e.g.:
```python
✅ Done! Wrote 152 rows to output.csv
```

---

## 🧾 Notes
* The script assumes the XML export uses consistent element names.
* Missing fields are filled with blanks to preserve CSV structure.
* The resulting CSV can be validated or modified in Excel before importing into ArchivesSpace.
* If you need to adapt this for non-microfilm only accessions, adjust the filter condition (ACCESSNUM = "MFO") in the code.

# 🎞️ Microfilm XML to ArchivesSpace CSV Converter

## 📘 Overview
This Python script parses a **microfilm XML export** and transforms it into a **CSV file** formatted for **ArchivesSpace accessions**.  
It automatically maps XML fields to ArchivesSpace CSV fields, applies conditional logic, and reformats dates for consistency.

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

## 🧩 Field Mapping Summary

| XML Field | CSV Field | Logic |
|------------|------------|-------|
| `ACCESSNUM` | Used to filter only records with value `"MFO"` |
| `NEGATIVE` | `accession_content_description` | `"Y"` → `"Negatives"` |
| `TARGETBY` | `accession_processors` | Adds `"Processed by <TARGETBY>."` |
| `NOTES` | `accession_provenance` | Appended to provenance |
| `CATALOG` | `accession_cataloged` | `"YES"` → `1`, `"NO"` → `0` |
| `THS` | `accession_provenance` | `"Y"` → `"Acquired from THS."` |
| `ACQUIS` | `accession_acquisition_type` | `"L"` → Loan, `"P"` → Purchase, `"O"` → Originals |
| `SIZE` | `extent_type`, `extent_container_summary` | `"35"` → `35 mm`, `"16"` → `16 mm`, default = `"microfilm reel(s)"` |
| `RESTRICTED` | `accession_restrictions_apply`, `accession_access_restrictions_note` | `"Y"` → restricted note, `"N"` or blank → unrestricted |
| `DATE_ASSIGNED` | `date_1_begin`, `date_1_type`, `date_1_label` | Reformatted to `yyyy-mm-dd`, type = `"single"`, label = `"Targeted"` |
| `COLLECTION` | `accession_title` | Directly mapped |
| `COLLECTION` | `date_2_begin`, `date_2_end`, 'date_2_label' | Extracts collection dates from collection title |
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
- `template.csv` → A CSV template containing the expected ArchivesSpace headers.

**Output**
- `output.csv` → A fully populated, UTF-8 encoded CSV ready for import.

---

## 🚀 How to Run

### 1️⃣ Install Dependencies
Make sure you have Python 3 and the required libraries installed:
```bash
pip install pandas

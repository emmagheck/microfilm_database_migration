# Microfilm Accessions Migration Script

This Python script migrates **microfilm-only accession records** from a **Microsoft Access export (in XML format)** to a **CSV file** formatted for import into [ArchivesSpace](https://archivesspace.org/).

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

File paths are defined at the top of the script:

```python
xml_file = "microfilm.xml"
template_csv = "template.csv"
output_csv = "output.csv"

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


# Microfilm Accession Record Database Migration
## ArchivesSpace Metadata Cleanup Project
This respository is part of Phase 2 of TSLA's ArchivesSpace Metadata Cleanup Project. The Tennessee State Library and Archives has historically stored microfilm accession records in a Microsoft Access Database, but needed to migrate them to ArchivesSpace as part of the  metadata cleanup. This code shows the process of migrating records from XML to CSV format.

## ArchivesSpace Requirements
ArchivesSpace provides Bulk Import spreadsheets for users, so rather than creating an accession record for all 1475 records, we are able to upload them all at once. However, 

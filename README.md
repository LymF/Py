# Py — Python Bioinformatics Scripts

A curated collection of Python scripts for bioinformatics data processing, organized by functional category. Scripts cover sequence manipulation, homology search, RNA-seq analysis, ortholog identification, and general data utilities — primarily developed for viral metagenomics and transcriptomics workflows.

## Repository structure

```
Py/
├── blast/       # NCBI BLAST searches and output parsing
├── diamond/     # DIAMOND protein searches and tabular output filtering
├── fasta/       # FASTA file manipulation and format conversion
├── eves/        # Endogenous Viral Element (EVE) identification and context
├── rna/         # RNA-seq read counting and quantification utilities
└── utils/       # General-purpose bioinformatics utilities
```

---

## blast/

Scripts for running and processing NCBI BLAST searches.

| Script | Description |
|---|---|
| `blastn.py` | Runs BLASTn searches against a local nucleotide database; accepts FASTA input and outputs tabular results |
| `blastx.py` | Runs BLASTx (translated nucleotide vs. protein) against a local database |
| `blast_api_online.py` | Submits BLAST queries to the NCBI online API via Biopython `NCBIWWW`; suitable for small query sets |
| `blastn_15nt_alignment.py` | BLASTn optimized for short (15 nt) query alignment, useful for small RNA mapping to reference sequences |

**Dependencies:** BLAST+ suite, Biopython

---

## diamond/

Scripts for running DIAMOND blastx searches and filtering tabular outputs.

| Script | Description |
|---|---|
| `diamond_filtering.py` | Parses DIAMOND tabular output, applies e-value and identity filters, and extracts high-confidence hits |
| `diamond_filter_all_tabular.py` | Applies filtering criteria across all DIAMOND tabular files in a directory |
| `diamond_filter_per_file.py` | Filters a single DIAMOND tabular file with customizable thresholds |
| `diamond_to_fasta.py` | Converts DIAMOND hit sequences from tabular format back to FASTA |
| `diamond_redundancy.py` | Identifies and removes redundant hits from DIAMOND output based on query-subject overlap |

**Dependencies:** DIAMOND, pandas

---

## fasta/

Utilities for FASTA file processing, deduplication, and format conversion.

| Script | Description |
|---|---|
| `split_fasta.py` | Splits a multi-FASTA file into individual files or fixed-size chunks |
| `deduplicate_fasta.py` | Removes duplicate sequences from a FASTA file based on exact sequence match |
| `remove_duplicate_sequences_fasta.py` | Alternative deduplication approach using sequence headers and content |
| `merge_contigs_singles_fasta.py` | Merges CAP3 contigs and singlets into a single FASTA file |
| `xlsx_to_fasta.py` | Converts an Excel spreadsheet with ID and sequence columns to FASTA format |
| `extract_family_taxon_fasta.py` | Extracts sequences from a FASTA file filtered by taxonomic family annotation in the header |

**Dependencies:** Biopython, openpyxl

---

## eves/

Scripts for identification and genomic context analysis of Endogenous Viral Elements (EVEs).

| Script | Description |
|---|---|
| `eves_identification.py` | Screens DIAMOND/BLAST results to identify putative EVE integrations based on hit criteria and host genomic origin |
| `eves_complete_analysis.py` | Extended EVE analysis pipeline — integrates hit filtering, taxonomic annotation, and summary table generation |
| `genome_context.py` | Extracts genomic flanking regions around EVE insertions from a reference genome; useful for characterizing insertion sites |

**Dependencies:** Biopython, pandas

---

## rna/

Utilities for RNA-seq quantification processing and mapping statistics.

| Script | Description |
|---|---|
| `count_reads.py` | Counts reads per feature from a SAM/BAM-derived table |
| `read_counts.py` | Parses raw count files and produces a consolidated count matrix across samples |
| `transcripts_to_gene.py` | Aggregates transcript-level quantification (e.g., from Salmon) to gene-level counts |
| `extract_quant_sf.py` | Extracts TPM and count values from Salmon `quant.sf` files across multiple samples |
| `reverse_translate_mirnas.py` | Reverse-translates miRNA mature sequences for alignment against coding sequences |
| `parse_bowtie2_stats.py` | Parses Bowtie2 mapping statistics log files and compiles alignment rates across multiple samples |

**Dependencies:** pandas

---

## utils/

General-purpose utilities for data formatting, comparison, and ortholog analysis.

| Script | Description |
|---|---|
| `csv_to_tsv.py` | Converts CSV files to TSV format |
| `tabular_to_tsv.py` | Converts space- or custom-delimited tabular files to standard TSV |
| `compare_excel_columns.py` | Compares two columns across Excel files and reports matches and differences |
| `compare_two_columns.py` | Identifies shared and unique entries between two list-format columns |
| `extract_species.py` | Parses FASTA headers or tabular files to extract species names |
| `filter_by_virus.py` | Filters tabular annotation results to retain only virus-associated entries |
| `remove_duplicate_lines.py` | Removes duplicate lines from a text or tabular file |
| `generate_heatmap.py` | Generates a heatmap from a matrix file using matplotlib/seaborn |
| `dinucleotide_analysis.py` | Calculates dinucleotide frequencies for a set of sequences — useful for viral genome composition analysis |
| `orthologs.py` | Identifies orthologous gene pairs between two species from BLAST reciprocal best hits |
| `orthologs_v2.py` | Updated version of ortholog identification with improved filtering |
| `orthologs_drosophila.py` | Ortholog identification tuned for *Drosophila* genome annotations |
| `pandas_utils.py` | Common pandas data loading, filtering, and export utility functions |

**Dependencies:** pandas, matplotlib, seaborn, openpyxl

---

## General requirements

```bash
pip install biopython pandas matplotlib seaborn openpyxl
```

BLAST+ and DIAMOND must be installed and available in `$PATH`.

## Usage pattern

Most scripts are standalone and accept arguments via command line or by editing input paths at the top of the file. Example:

```bash
python blast/blastn.py -i sequences.fasta -d /path/to/db -o results.tsv -t 8
python fasta/split_fasta.py -i genome.fasta -n 1000 -o split_output/
python utils/csv_to_tsv.py -i data.csv -o data.tsv
```

Refer to each script's `argparse` help for full usage:

```bash
python <script>.py --help
```

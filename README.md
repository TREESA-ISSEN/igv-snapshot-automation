# igv-snapshot-automation
# IGV Snapshot Automation

Automates IGV (Integrative Genomics Viewer) batch snapshot generation 
for multiple BAM files and genomic regions.
Developed at CSIR-IGIB for rare disease WES variant visualization.

---

## What it does
- Reads BAM filenames and genomic regions from a text file
- Generates individual IGV batch scripts (.igv) for each sample
- Runs IGV in batch mode to capture PNG snapshots automatically

---

## Workflow

### Step 1 — Prepare input file
Create `bam_region.txt` (tab or space separated):                 
### Step 2 — Generate IGV scripts
```bash
python generate_igv_script.py \
  -b /path/to/BAMs \
  -s /path/to/snapshots \
  -g /path/to/hg38.fa \
  -r bam_region.txt
```

### Step 3 — Run IGV batch
```bash
./run_igv.sh
```

---

## Arguments

| Argument | Description |
|---|---|
| `-b` | Path to BAM files directory |
| `-s` | Directory to save PNG snapshots |
| `-g` | Path to genome reference (hg38) |
| `-r` | Path to BAM regions file |
| `-d` | Delay in seconds between samples (default: 2) |

---

## Output
- `.igv` batch scripts per sample
- `.png` snapshots saved to snapshot directory

---

## Requirements
- Python 3.8+
- IGV installed and `igv.sh` in PATH

## Tools Used
- IGV (Integrative Genomics Viewer)
- Python 3
- Bash

## Author
Treesa Issen | CSIR-IGIB, New Delhi

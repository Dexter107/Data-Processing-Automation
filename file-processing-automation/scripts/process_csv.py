from pathlib import Path
import csv
from statistics import mean
import logging
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger()

INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
REPORTS_DIR = Path("reports")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

values = []

# 1. Read CSV files
log.info("📊 Scanning for CSV files...")
csv_files = list(INPUT_DIR.glob("*.csv"))

if not csv_files:
    log.error("⚠ No CSV files found in data/input/. Exiting.")
    exit(1)

for csv_file in csv_files:
    log.info(f"   Reading file: {csv_file.name}")
    with csv_file.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "value" in row and row["value"].strip():
                values.append(float(row["value"]))

if not values:
    log.error("⚠ No numeric data found in 'value' column. Exiting.")
    exit(1)

total = sum(values)
average = mean(values)

# 2. Generate CSV report
csv_report = OUTPUT_DIR / "report.csv"
with csv_report.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["total", "average"])
    writer.writerow([total, f"{average:.2f}"])

log.info(f"\n✔ CSV report generated: {csv_report}")

# 3. Generate PDF report
pdf_report = REPORTS_DIR / "report.pdf"
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(str(pdf_report))

story = []
story.append(Paragraph("File Processing Report", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Automated metrics extracted from CSV input files.", styles["Normal"]))
story.append(Spacer(1, 12))
story.append(Paragraph(f"Total: {total}", styles["Heading2"]))
story.append(Paragraph(f"Average: {average:.2f}", styles["Heading2"]))

doc.build(story)

log.info(f"✔ PDF report created: {pdf_report}\n")

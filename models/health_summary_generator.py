from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', 'assets/DejaVuSans.ttf', uni=True)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("DejaVu", size=16)
        self.cell(0, 10, "Health Summary", ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", size=8)
        self.cell(0, 10, f"Page {self.page_no()}", align='C')


def generate_health_summary(patient_id, patient_data):
    try:
        pdf = PDF()
        pdf.add_page()

        # Patient metadata
        metadata = patient_data.get("metadata", {})
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, f"Patient ID: {patient_id}", ln=True)
        pdf.cell(0, 10, f"Name: {metadata.get('name', 'N/A')}", ln=True)
        pdf.cell(0, 10, f"Age: {metadata.get('age', 'N/A')}", ln=True)
        pdf.cell(0, 10, f"Gender: {metadata.get('gender', 'N/A')}", ln=True)

        # Visit Details
        visits = patient_data.get("visits", [])
        pdf.ln(10)
        pdf.set_font("DejaVu", size=14)
        pdf.cell(0, 10, "Visit Details:", ln=True)
        pdf.set_font("DejaVu", size=12)

        for i, visit in enumerate(visits, 1):
            pdf.ln(5)
            pdf.cell(0, 10, f"Visit {i}:", ln=True)
            for key, value in visit.items():
                pdf.cell(0, 10, f"  - {key}: {value}", ln=True)

        # Save PDF
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

        filename = f"{patient_id}_summary.pdf"
        filepath = os.path.join("outputs", filename)
        pdf.output(filepath)

        return filepath, filename

    except Exception as e:
        print("[ERROR] Failed to generate health summary PDF:", e)
        return None, None

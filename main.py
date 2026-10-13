import pytesseract
import re
from datetime import datetime
import streamlit as st
from PIL import Image
import json

import os
import shutil

tesseract_path = shutil.which("tesseract")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    # Optional Windows fallback for local development
    windows_path = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    if os.path.exists(windows_path):
        pytesseract.pytesseract.tesseract_cmd = windows_path

# # Maintain your explicit tesseract configuration execution path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\amrut\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# ----------------- STREAMLIT PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="Enterprise KYC Verification Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM ENTERPRISE CSS STYLING -----------------
st.markdown("""
<style>
    /* Global Page Styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Card Component */
    .card-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    
    /* Custom Primary Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #1d976c, #93f9b9);
        color: #0d3b2e !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        font-size: 16px !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(29, 151, 108, 0.4);
    }

    /* Badges */
    .badge-pass {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    .badge-fail {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# ----------------- OOP CLASS ARCHITECTURE -----------------

class UploadImage:

    def __init__(self, image_path):
        self.image_path = image_path

    def display_image(self):
        pass


class ExtractText(UploadImage):

    def __init__(self, image_path):
        super().__init__(image_path)
        self.text = ""

    def extract_text(self):
        img = Image.open(self.image_path)
        self.text = pytesseract.image_to_string(img)

    def display_text(self):
        pass


class AadhaarDocument(ExtractText):

    def process(self):
        self.display_image()
        self.extract_text()

        # ---------- Extraction ----------
        self.extract_aadhaar_name()
        self.extract_aadhaar_number()
        self.extract_aadhaar_dob()
        self.extract_aadhaar_gender()
        self.extract_aadhaar_address() 
        self.extract_aadhaar_pincode()

        # ---------- Normalization ----------
        self.normalize_aadhaar_name()
        self.normalize_aadhaar_number()
        self.normalize_aadhaar_dob()
        self.normalize_aadhaar_gender()
        self.normalize_aadhaar_address()
        self.normalize_aadhaar_pincode()

        # ---------- Validation ----------
        self.validate_aadhaar_name()
        self.validate_aadhaar_number()
        self.validate_aadhaar_dob()
        self.validate_aadhaar_gender()
        self.validate_aadhaar_address()
        self.validate_aadhaar_pincode()
        

    def extract_aadhaar_name(self):
        lines = self.text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        for i, line in enumerate(lines):
            if "DOB" in line.upper():
                self.aadhaar_name = lines[i - 1]
                return
        self.aadhaar_name = None
    
    def extract_aadhaar_number(self):
        self.aadhaar_num = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", self.text)

    def extract_aadhaar_dob(self):
        self.aadhaar_dob = re.search(r"\d{2}/\d{2}/\d{4}", self.text)
            
    def extract_aadhaar_gender(self):
        self.gender = re.search(r"\b(Male|Female|Transgender)\b", self.text, re.IGNORECASE)

    def extract_aadhaar_address(self):
        lines = self.text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]

        address = []
        after_to = False
        start_collecting = False

        for line in lines:
            if line.upper() == "TO":
                after_to = True
                continue
            if not after_to:
                continue
            if re.fullmatch(r"\d{10}", line):
                break
            if re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", line):
                break
            if re.search(r"\b(S/O|D/O|W/O|C/O)\b", line.upper()):
                continue
            if re.search(r"\d", line):
                start_collecting = True
            if start_collecting:
                address.append(line)

        if address:
            self.aadhaar_address = "\n".join(address)
        else:
            self.aadhaar_address = None

    def extract_aadhaar_pincode(self):
        self.aadhaar_pincode = re.search(r"\b\d{6}\b", self.text)

#-----------------------------------------normalization methods aadhaar------------------------------------
    
    def normalize_aadhaar_name(self):
        if not hasattr(self, "aadhaar_name") or self.aadhaar_name is None:
            return
        self.original_aadhaar_name = self.aadhaar_name
        name = self.aadhaar_name.strip()
        name = re.sub(r"[^\w\s]", "", name)
        self.normalized_aadhaar_name = re.sub(r"\s+", " ", name)

    def normalize_aadhaar_number(self):
        if not self.aadhaar_num:
            return
        self.original_aadhaar_number = self.aadhaar_num.group()
        self.normalized_aadhaar_number = self.original_aadhaar_number.replace(" ", "")

    def normalize_aadhaar_dob(self):
        if not self.aadhaar_dob:
            return
        self.original_aadhaar_dob = self.aadhaar_dob.group()
        self.normalized_aadhaar_dob = re.sub(r"\s+", "", self.original_aadhaar_dob.strip())

    def normalize_aadhaar_gender(self):
        if not self.gender:
            return
        self.original_aadhaar_gender = self.gender.group()
        self.normalized_aadhaar_gender = self.original_aadhaar_gender.strip().title()

    def normalize_aadhaar_address(self):
        if not hasattr(self, "aadhaar_address") or self.aadhaar_address is None:
            return
        self.original_aadhaar_address = self.aadhaar_address
        lines = [line.strip() for line in self.aadhaar_address.split("\n") if line.strip()]
        self.normalized_aadhaar_address = "\n".join(lines)

    def normalize_aadhaar_pincode(self):
        if not self.aadhaar_pincode:
            return
        self.original_aadhaar_pincode = self.aadhaar_pincode.group()
        self.normalized_aadhaar_pincode = self.original_aadhaar_pincode.strip()


#-------------------------------------validation----------------------------------

    def validate_aadhaar_name(self):
        if not hasattr(self, "normalized_aadhaar_name"):
            self.aadhaar_name_valid = False
            return
        name = self.normalized_aadhaar_name
        if len(name) < 3 or not re.fullmatch(r"[A-Za-z ]+", name):
            self.aadhaar_name_valid = False
        else:
            self.aadhaar_name_valid = True

    def validate_aadhaar_number(self):
        if not hasattr(self, "normalized_aadhaar_number"):
            self.aadhaar_number_valid = False
            return
        number = self.normalized_aadhaar_number
        if len(number) != 12 or not number.isdigit():
            self.aadhaar_number_valid = False
        else:
            self.aadhaar_number_valid = True

    def validate_aadhaar_dob(self):
        if not hasattr(self, "normalized_aadhaar_dob"):
            self.aadhaar_dob_valid = False
            return
        try:
            datetime.strptime(self.normalized_aadhaar_dob, "%d/%m/%Y")
            self.aadhaar_dob_valid = True
        except ValueError:
            self.aadhaar_dob_valid = False

    def validate_aadhaar_gender(self):
        if not hasattr(self, "normalized_aadhaar_gender"):
            self.aadhaar_gender_valid = False
            return
        if self.normalized_aadhaar_gender in ["Male", "Female", "Transgender"]:
            self.aadhaar_gender_valid = True
        else:
            self.aadhaar_gender_valid = False

    def validate_aadhaar_address(self):
        if not hasattr(self, "normalized_aadhaar_address"):
            self.aadhaar_address_valid = False
            return
        address = self.normalized_aadhaar_address
        lines = address.split("\n")
        if len(address) < 10 or len(lines) < 2:
            self.aadhaar_address_valid = False
        else:
            self.aadhaar_address_valid = True

    def validate_aadhaar_pincode(self):
        if not hasattr(self, "normalized_aadhaar_pincode"):
            self.aadhaar_pincode_valid = False
            return
        pin = self.normalized_aadhaar_pincode
        if len(pin) != 6 or not pin.isdigit():
            self.aadhaar_pincode_valid = False
        else:
            self.aadhaar_pincode_valid = True


#--------------------------------class pan Document-------------------------------------------
class PanDocument(ExtractText):

    def process(self):
        self.display_image()
        self.extract_text()

        #---------Extraction-------------
        self.extract_pan_name()
        self.extract_father_name()
        self.extract_pan_number()
        self.extract_pan_dob()

        # ---------- Normalization ----------
        self.normalize_pan_name()
        self.normalize_father_name()
        self.normalize_pan_number()
        self.normalize_pan_dob()

        # ---------- Validating ----------
        self.validate_pan_name()
        self.validate_father_name()
        self.validate_pan_number()
        self.validate_pan_dob()
        
    def extract_pan_name(self):
        lines = self.text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        
        class MatchPlaceholder:
            def __init__(self, text):
                self._text = text
            def group(self):
                return self._text

        for i, line in enumerate(lines):
            if "NAME" in line.upper() and len(line) > 5:
                cleaned_line = re.sub(r'(?i)^.*name\s*[:\-]*\s*', '', line).strip()
                if cleaned_line:
                    self.pan_name = MatchPlaceholder(cleaned_line)
                    return

            if "NAME" in line.upper():
                if i + 1 < len(lines):
                    self.pan_name = MatchPlaceholder(lines[i + 1])
                    return
                
        self.pan_name = re.search(r"(?<=Name\n).*", self.text)

    def extract_father_name(self):
        lines = self.text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
    
        for i, line in enumerate(lines):
            if "FATHER" in line.upper():
                if i + 1 < len(lines):
                    self.father_name = lines[i + 1]
                    return
        self.father_name = None

    def extract_pan_number(self):
        self.pan_num = re.search(r"\b[A-Z]{5}\d{4}[A-Z]\b", self.text)

    def extract_pan_dob(self):
        self.pan_dob = re.search(r"\d{2}/\d{2}/\d{4}", self.text)
            
#------------------------------normalization of pan details----------------------------

    def normalize_pan_name(self):
        if not self.pan_name:
            return
        self.original_pan_name = self.pan_name.group()
        name = self.original_pan_name
        name = name.strip()
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", " ", name)
        name = re.sub(r"\d+", " ", name)
        self.normalized_pan_name = name.title()

    def normalize_father_name(self):
        if not hasattr(self, "father_name") or self.father_name is None:
            return
        self.original_father_name = self.father_name
        name = self.original_father_name
        name = name.strip()
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", " ", name)
        name = re.sub(r"\d+", " ", name)
        self.normalized_father_name = name.title()

    def normalize_pan_number(self):
        if not self.pan_num:
            return
        self.original_pan_number = self.pan_num.group()
        pan = self.original_pan_number
        self.normalized_pan_number = pan.strip().upper()

    def normalize_pan_dob(self):
        if not self.pan_dob:
            return
        self.original_pan_dob = self.pan_dob.group()
        dob = self.original_pan_dob
        dob = dob.strip()
        self.normalized_pan_dob = re.sub(r"\s+", "", dob)

#------------------------------Validation of pan details----------------------------

    def validate_pan_name(self):
        if not hasattr(self, "normalized_pan_name"):
            self.pan_name_valid = False
            return
        name = self.normalized_pan_name
        if len(name) < 3 or not re.fullmatch(r"[A-Za-z ]+", name):
            self.pan_name_valid = False
        else:
            self.pan_name_valid = True

    def validate_father_name(self):
        if not hasattr(self, "normalized_father_name"):
            self.father_name_valid = False
            return
        name = self.normalized_father_name
        if len(name) < 3 or not re.fullmatch(r"[A-Za-z ]+", name):
            self.father_name_valid = False
        else:
            self.father_name_valid = True

    def validate_pan_number(self):
        if not hasattr(self, "normalized_pan_number"):
            self.pan_number_valid = False
            return
        pan = self.normalized_pan_number
        if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan):
            self.pan_number_valid = True
        else:
            self.pan_number_valid = False

    def validate_pan_dob(self):
        if not hasattr(self, "normalized_pan_dob"):
            self.pan_dob_valid = False
            return
        dob = self.normalized_pan_dob
        try:
            dob_date = datetime.strptime(dob, "%d/%m/%Y")
            if dob_date > datetime.now():
                self.pan_dob_valid = False
            else:
                self.pan_dob_valid = True
        except ValueError:
            self.pan_dob_valid = False


#---------------------------------KYC VERIFICATION CODE---------------------------------------------------------

class KYCVerification:

    def __init__(self, aadhaar, pan):
        self.aadhaar = aadhaar
        self.pan = pan

    def process(self):
        self.compare_name()
        self.compare_dob()
        self.verify_documents()
        self.generate_report()

    def compare_name(self):
        aadhaar_name = getattr(self.aadhaar, "normalized_aadhaar_name", None)
        pan_name = getattr(self.pan, "normalized_pan_name", None)
        
        if aadhaar_name is None or pan_name is None:
            self.name_match = False
            return
        self.name_match = (aadhaar_name == pan_name)

    def compare_dob(self):
        aadhaar_dob = getattr(self.aadhaar, "normalized_aadhaar_dob", None)
        pan_dob = getattr(self.pan, "normalized_pan_dob", None)

        if aadhaar_dob is None or pan_dob is None:
            self.dob_match = False
            return
        self.dob_match = (aadhaar_dob == pan_dob)

    def verify_documents(self):
        self.aadhaar_document_valid = all([
            getattr(self.aadhaar, "aadhaar_name_valid", False),
            getattr(self.aadhaar, "aadhaar_number_valid", False),
            getattr(self.aadhaar, "aadhaar_dob_valid", False),
            getattr(self.aadhaar, "aadhaar_gender_valid", False),
            getattr(self.aadhaar, "aadhaar_address_valid", False),
            getattr(self.aadhaar, "aadhaar_pincode_valid", False)
        ])

        self.pan_document_valid = all([
            getattr(self.pan, "pan_name_valid", False),
            getattr(self.pan, "father_name_valid", False),
            getattr(self.pan, "pan_number_valid", False),
            getattr(self.pan, "pan_dob_valid", False)
        ])

    def generate_report(self):
        if (self.name_match and self.dob_match and self.aadhaar_document_valid and self.pan_document_valid):
            self.kyc_status = "VERIFIED"
        else:
            self.kyc_status = "REJECTED"


# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.title("⚙️ KYC Engine Settings")
    st.caption("Modular Verification Control System")
    st.divider()

    # 1. System Health Status
    st.subheader("System Health")
    st.markdown("🟢 **Tesseract OCR:** Active")
    st.markdown("🟢 **Validation Engine:** Operational")

    st.divider()

    # 2. Advanced Rule Controls (Expandable & Flexible for future logic)
    st.subheader("Verification Controls")
    mask_aadhaar_ui = st.toggle("Mask Aadhaar in Results Table", value=True)
    strict_exact_match = st.toggle("Require Exact String Matching", value=True)
    
    # Static Placeholder Threshold (Easily convert to dynamic fuzzy ratio matching later)
    match_sensitivity = st.slider("Name Similarity Tolerance", min_value=70, max_value=100, value=90, help="Static threshold parameter for future fuzzy string comparisons.")

    st.divider()

    # 3. Image Preprocessing Extensions (Placeholder for Future OpenCV enhancements)
    with st.expander("🖼️ Image Preprocessing Tools"):
        st.caption("Future OpenCV integration tools:")
        st.checkbox("Auto-Rotate Image", value=False, disabled=True)
        st.checkbox("Contrast Enhancement", value=False, disabled=True)
        st.checkbox("Noise Reduction Filter", value=False, disabled=True)

    st.divider()

    # 4. Quick How-To Guide
    st.subheader("💡 Onboarding Guide")
    st.markdown("""
    1. Upload clear document images.
    2. Click **Extract & Verify Documents**.
    3. Review outputs in summary tabs.
    """)

    st.caption("🔒 *Processed securely in local memory.*")

# ----------------- MAIN HEADER BAR -----------------
st.markdown("""
<div class="header-box">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="margin: 0; padding: 0; font-weight: 700;">Automated KYC Verification Portal</h2>
            <p style="margin: 4px 0 0 0; opacity: 0.85; font-size: 14px;">Automated document parsing and identity verification system.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------- DOCUMENT UPLOAD AREA -----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("📄 Aadhaar Card Document")
    st.caption("Please upload a clear image. avoid blurry, dark, or low-quality image.")
    aadhaar_file = st.file_uploader("Upload Aadhaar", type=["jpeg", "jpg", "png"], key="aadhaar_upload")
    if aadhaar_file:
        st.image(aadhaar_file, caption="Aadhaar Preview", width=220)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("💳 PAN Card Document")
    st.caption("Please upload a clear image. avoid blurry, dark, or low-quality image.")
    pan_file = st.file_uploader("Upload PAN", type=["jpeg", "jpg", "png"], key="pan_upload")
    if pan_file:
        st.image(pan_file, caption="PAN Preview", width=220)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ----------------- EXECUTION TRIGGER -----------------
if st.button("Extract & Verify Documents", use_container_width=True):
    if aadhaar_file is not None and pan_file is not None:
        with st.spinner("Processing document analysis and cross-verification logic..."):
            
            # Instantiate classes and run matching logic pipelines directly
            aadhaar = AadhaarDocument(aadhaar_file)
            aadhaar.process()

            pan = PanDocument(pan_file)
            pan.process()

            kyc = KYCVerification(aadhaar, pan)
            kyc.process()
            
            st.write("")
            
            # ----------------- TABBED ANALYTICS DISPLAY -----------------
            tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🔍 Cross-Verification Metrics", "📑 Document Breakdown Matrix"])

            with tab1:
                st.write("")
                # Final Verdict Headline Card
                if kyc.kyc_status == "VERIFIED":
                    st.success("### Status: VERIFIED ✅\nBoth documents match and all details are valid. Your identity "
                               "verification is complete!"
                               )
                else:
                    st.error("### Status: REJECTED ❌\nThe details on your documents do not match or could not be read clearly."
                             "Please re-upload clear images and try again."
                             )

                # High-level Metrics Dashboard Grid
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Name Match", "PASS" if kyc.name_match else "FAIL")
                m2.metric("DOB Match", "PASS" if kyc.dob_match else "FAIL")
                m3.metric("Aadhaar Details", "VALID" if kyc.aadhaar_document_valid else "INVALID")
                m4.metric("PAN Details", "VALID" if kyc.pan_document_valid else "INVALID")

                # Compliance Export Download Action
                st.write("")
                audit_summary = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "final_status": kyc.kyc_status,
                    "name_match": kyc.name_match,
                    "dob_match": kyc.dob_match,
                    "aadhaar_valid": kyc.aadhaar_document_valid,
                    "pan_valid": kyc.pan_document_valid
                }
                st.download_button(
                    label="📥 Download KYC Audit JSON Report",
                    data=json.dumps(audit_summary, indent=4),
                    file_name="kyc_audit_report.json",
                    mime="application/json"
                )

            with tab2:
                st.write("")
                st.subheader("📋 Cross-Verification Documents")
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown(f"""
                    <div class="card-box">
                        <h4 style="margin-top:0;">Name Verification</h4>
                        <p><b>Aadhaar Name:</b> <code>{getattr(aadhaar, 'normalized_aadhaar_name', 'Not Found')}</code></p>
                        <p><b>PAN Name:</b> <code>{getattr(pan, 'normalized_pan_name', 'Not Found')}</code></p>
                        <p><b>Result:</b> <span class="{'badge-pass' if kyc.name_match else 'badge-fail'}">{'MATCHED' if kyc.name_match else 'MISMATCHED'}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                with res_col2:
                    st.markdown(f"""
                    <div class="card-box">
                        <h4 style="margin-top:0;">Date of Birth Verification</h4>
                        <p><b>Aadhaar DOB:</b> <code>{getattr(aadhaar, 'normalized_aadhaar_dob', 'Not Found')}</code></p>
                        <p><b>PAN DOB:</b> <code>{getattr(pan, 'normalized_pan_dob', 'Not Found')}</code></p>
                        <p><b>Result:</b> <span class="{'badge-pass' if kyc.dob_match else 'badge-fail'}">{'MATCHED' if kyc.dob_match else 'MISMATCHED'}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

            with tab3:
                st.write("")
                view_col1, view_col2 = st.columns(2)
                
                with view_col1:
                    st.subheader("Aadhaar Document Extraction ")
                    st.write("Aadhaar Details :", "VALID ✅" if kyc.aadhaar_document_valid else "INVALID ❌")
                    
                    aadhaar_table_data = {
                        "Field Entity": ["Name", "Aadhaar Number ", "DOB ", "Gender ", "Address ", "Pincode "],
                        "Normalized Value Extracted": [
                            getattr(aadhaar, "normalized_aadhaar_name", "N/A"),
                            getattr(aadhaar, "normalized_aadhaar_number", "N/A"),
                            getattr(aadhaar, "normalized_aadhaar_dob", "N/A"),
                            getattr(aadhaar, "normalized_aadhaar_gender", "N/A"),
                            getattr(aadhaar, "normalized_aadhaar_address", "N/A").replace('\n', ' | ') if getattr(aadhaar, "normalized_aadhaar_address", None) else "N/A",
                            getattr(aadhaar, "normalized_aadhaar_pincode", "N/A")
                        ],
                        "Pattern Validation Status": [
                            "VALID" if getattr(aadhaar, "aadhaar_name_valid", False) else "INVALID",
                            "VALID" if getattr(aadhaar, "aadhaar_number_valid", False) else "INVALID",
                            "VALID" if getattr(aadhaar, "aadhaar_dob_valid", False) else "INVALID",
                            "VALID" if getattr(aadhaar, "aadhaar_gender_valid", False) else "INVALID",
                            "VALID" if getattr(aadhaar, "aadhaar_address_valid", False) else "INVALID",
                            "VALID" if getattr(aadhaar, "aadhaar_pincode_valid", False) else "INVALID",
                        ]
                    }
                    st.table(aadhaar_table_data)

                with view_col2:
                    st.subheader("PAN Document Extraction ")
                    st.write("PAN Details :", "VALID ✅" if kyc.pan_document_valid else "INVALID ❌")

                    pan_table_data = {
                        "Field Entity": ["Name", "Father's Name ", "PAN Number ", "DOB "],
                        "Normalized Value Extracted": [
                            getattr(pan, "normalized_pan_name", "N/A"),
                            getattr(pan, "normalized_father_name", "N/A"),
                            getattr(pan, "normalized_pan_number", "N/A"),
                            getattr(pan, "normalized_pan_dob", "N/A")
                        ],
                        "Pattern Validation Status": [
                            "VALID" if getattr(pan, "pan_name_valid", False) else "INVALID",
                            "VALID" if getattr(pan, "father_name_valid", False) else "INVALID",
                            "VALID" if getattr(pan, "pan_number_valid", False) else "INVALID",
                            "VALID" if getattr(pan, "pan_dob_valid", False) else "INVALID",
                        ]
                    }
                    st.table(pan_table_data)
                
    else:
        st.warning("Please make sure both identity document images are fully uploaded first.")
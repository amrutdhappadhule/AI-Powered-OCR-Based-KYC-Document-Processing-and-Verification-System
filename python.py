import pytesseract
import re
from datetime import datetime
import streamlit as st
from PIL import Image

# Maintain your explicit tesseract configuration execution path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\amrut\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

class UploadImage:

    def __init__(self, image_path):
        self.image_path = image_path

    def display_image(self):
        # Console print removed for native Streamlit flow
        pass


class ExtractText(UploadImage):

    def __init__(self, image_path):
        super().__init__(image_path)
        self.text = ""

    def extract_text(self):
        # Open the uploaded file object seamlessly using PIL
        img = Image.open(self.image_path)
        self.text = pytesseract.image_to_string(img)

    def display_text(self):
        # Console print removed for native Streamlit flow
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


#-------------------------------------valiidation----------------------------------

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
        
        # Emulate standard regex group matching container expected by normalization
        class MatchPlaceholder:
            def __init__(self, text):
                self._text = text
            def group(self):
                return self._text

        for i, line in enumerate(lines):
            # 1. Handle Horizontal Layouts (e.g., "Name: John Doe" or "NAME - John Doe")
            if "NAME" in line.upper() and len(line) > 5:
                # Strip out the label "Name" and any common separating punctuation symbols
                cleaned_line = re.sub(r'(?i)^.*name\s*[:\-]*\s*', '', line).strip()
                if cleaned_line:
                    self.pan_name = MatchPlaceholder(cleaned_line)
                    return

            # 2. Handle Vertical Layouts (Label "Name" sits on its own line above the text value)
            if "NAME" in line.upper():
                if i + 1 < len(lines):
                    self.pan_name = MatchPlaceholder(lines[i + 1])
                    return
                
        # 3. Last resort fallback to your original regular expression lookbehind logic
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


# ---------------- MAIN STREAMLIT APPLICATION AREA ----------------

st.set_page_config(page_title="KYC Verification Dashboard", layout="wide")
st.title("Document KYC Verification Dashboard")
st.write("Upload the Aadhaar and PAN Card images below to process the matching pipeline.")

# Side-by-side file uploading setup
col1, col2 = st.columns(2)

with col1:
    st.subheader("Aadhaar Card Setup")
    aadhaar_file = st.file_uploader("Upload Aadhaar Card Image", type=["jpeg", "jpg", "png"], key="aadhaar_upload")
    if aadhaar_file:
        st.image(aadhaar_file, caption="Aadhaar Preview", width=250)

with col2:
    st.subheader("PAN Card Setup")
    pan_file = st.file_uploader("Upload PAN Card Image", type=["jpeg", "jpg", "png"], key="pan_upload")
    if pan_file:
        st.image(pan_file, caption="PAN Preview", width=250)

st.write("---")

if st.button("Run KYC Processing Verification", use_container_width=True):
    if aadhaar_file is not None and pan_file is not None:
        with st.spinner("Processing document analysis and cross-verification logic..."):
            
            # Instantiate classes and run matching logic pipelines directly
            aadhaar = AadhaarDocument(aadhaar_file)
            aadhaar.process()

            pan = PanDocument(pan_file)
            pan.process()

            kyc = KYCVerification(aadhaar, pan)
            kyc.process()
            
            # --- Graphical Result Presentation Area ---
            if kyc.kyc_status == "VERIFIED":
                st.success(f"### Final KYC Status: {kyc.kyc_status} 🎉")
            else:
                st.error(f"### Final KYC Status: {kyc.kyc_status} ❌")
                
            # Cross-Verification Parameter Metrics Layout
            st.subheader("📋 Core Cross-Verification Parameters")
            match_col1, match_col2 = st.columns(2)
            with match_col1:
                st.metric("Identity Name Concordance Match", "PASS" if kyc.name_match else "FAIL")
                st.write(f"**Aadhaar Stated Name:** `{getattr(aadhaar, 'normalized_aadhaar_name', 'Not Found')}`")
                st.write(f"**PAN Stated Name:** `{getattr(pan, 'normalized_pan_name', 'Not Found')}`")
                
            with match_col2:
                st.metric("Date of Birth Concordance Match", "PASS" if kyc.dob_match else "FAIL")
                st.write(f"**Aadhaar DOB:** `{getattr(aadhaar, 'normalized_aadhaar_dob', 'Not Found')}`")
                st.write(f"**PAN DOB:** `{getattr(pan, 'normalized_pan_dob', 'Not Found')}`")

            st.write("---")

            # Side-by-Side Data Verification Breakdown Tables Mapping
            view_col1, view_col2 = st.columns(2)
            
            with view_col1:
                st.subheader("Aadhaar Data Breakdown")
                st.write("Document Structural Integrity:", "✅ VALID" if kyc.aadhaar_document_valid else "❌ INVALID")
                
                aadhaar_table_data = {
                    "Field Entity": ["Name", "Number Format", "DOB Structure", "Gender Match", "Address Blocks", "Pincode Code"],
                    "Normalized Value Extracted": [
                        getattr(aadhaar, "normalized_aadhaar_name", "N/A"),
                        "[Aadhaar Number Redacted for Privacy]" if getattr(aadhaar, "normalized_aadhaar_number", None) else "N/A",
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
                st.subheader("PAN Data Breakdown")
                st.write("Document Structural Integrity:", "✅ VALID" if kyc.pan_document_valid else "❌ INVALID")
                
                pan_table_data = {
                    "Field Entity": ["Name", "Father's Name Line", "PAN Number Sequence", "DOB Structure"],
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
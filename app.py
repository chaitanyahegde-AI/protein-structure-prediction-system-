
import io
import time
import requests
import streamlit as st
import py3Dmol
import numpy as np

from stmol import showmol
from biotite.structure.io.pdb import PDBFile


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Protein Structure Predictor",
    page_icon="🧬",
    layout="wide"
)

st.title("Protein Structure Prediction")
st.markdown(
    "Predict protein structures from amino acid sequences "
    "and explore their 3D structures interactively."
)

st.divider()


# ==========================================
# API CONFIGURATION
# ==========================================

API_URL = "https://api.esmatlas.com/foldSequence/v1/pdb/"

VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


# ==========================================
# SEQUENCE VALIDATION
# ==========================================

def validate_sequence(sequence):

    sequence = "".join(sequence.split()).upper()

    if not sequence:
        return False, "Please enter an amino acid sequence."

    invalid = sorted(set(sequence) - VALID_AMINO_ACIDS)

    if invalid:
        return (
            False,
            "Invalid amino acid characters: "
            + ", ".join(invalid)
        )

    return True, sequence


# ==========================================
# API REQUEST WITH RETRIES
# ==========================================

def predict_structure(sequence):

    max_attempts = 3
    retryable_statuses = {429, 500, 502, 503, 504}

    for attempt in range(1, max_attempts + 1):

        try:
            response = requests.post(
                API_URL,
                data=sequence,
                headers={
                    "Content-Type": "text/plain",
                    "Accept": "text/plain"
                },
                timeout=(15, 300)
            )

            if response.status_code == 200:

                pdb_data = response.text.strip()

                valid_atom_lines = [
                    line for line in pdb_data.splitlines()
                    if line.startswith(("ATOM  ", "HETATM"))
                ]

                if not valid_atom_lines:
                    return None, (
                        "The API returned no valid atom records. "
                        "The prediction service may have returned "
                        "an error instead of a PDB structure."
                    )

                # Validate that Biotite can parse the PDB.
                try:
                    pdb_file = PDBFile.read(
                        io.StringIO(pdb_data)
                    )
                    structure = pdb_file.get_structure()

                    if structure.array_length() == 0:
                        return None, (
                            "The returned PDB file contains "
                            "no readable atoms."
                        )

                except Exception as error:
                    return None, (
                        f"The API returned an unreadable PDB file: "
                        f"{error}"
                    )

                return pdb_data, None

            if response.status_code in retryable_statuses:

                if attempt < max_attempts:
                    wait_seconds = 2 ** attempt

                    st.warning(
                        f"API returned HTTP {response.status_code}. "
                        f"Retrying in {wait_seconds} seconds "
                        f"(attempt {attempt + 1}/{max_attempts})..."
                    )

                    time.sleep(wait_seconds)
                    continue

                return None, (
                    f"Prediction API returned HTTP "
                    f"{response.status_code} after "
                    f"{max_attempts} attempts. "
                    "The service may be overloaded or unavailable. "
                    "Please try again later."
                )

            return None, (
                f"Prediction API returned HTTP "
                f"{response.status_code}. "
                f"Response: {response.text[:300]}"
            )

        except requests.exceptions.RequestException as error:

            if attempt < max_attempts:

                wait_seconds = 2 ** attempt

                st.warning(
                    f"Connection problem: {error}. "
                    f"Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)
                continue

            return None, (
                f"Could not contact the prediction API after "
                f"{max_attempts} attempts: {error}"
            )

    return None, "Prediction failed unexpectedly."


# ==========================================
# SAVE PDB FILE
# ==========================================

def save_pdb(pdb_data):

    with open(
        "predicted.pdb",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(pdb_data.rstrip() + "\n")


# ==========================================
# CONFIDENCE ANALYSIS
# ==========================================

def calculate_confidence(pdb_data):

    try:
        pdb_file = PDBFile.read(
            io.StringIO(pdb_data)
        )

        structure = pdb_file.get_structure()

        if structure.array_length() == 0:
            return None

        values = np.asarray(
            structure.b_factor,
            dtype=float
        )

        values = values[np.isfinite(values)]

        if len(values) == 0:
            return None

        return float(np.mean(values))

    except Exception:
        return None


# ==========================================
# 3D VISUALIZATION
# ==========================================

def visualize_protein(pdb_data):

    viewer = py3Dmol.view(
        width=900,
        height=600
    )

    viewer.addModel(pdb_data, "pdb")

    viewer.setStyle({
        "cartoon": {
            "color": "spectrum"
        }
    })

    viewer.setBackgroundColor("#111827")
    viewer.zoomTo()

    showmol(
        viewer,
        height=600,
        width=900
    )


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("About the project")

    st.write(
        "This application predicts protein structures "
        "using the ESM Atlas Fold API."
    )

    st.write("Technologies used:")

    st.markdown(
        """
        - Python
        - Streamlit
        - ESM Atlas API
        - Biotite
        - py3Dmol
        - stmol
        - NumPy
        """
    )

    st.caption(
        "Prediction requires an internet connection "
        "and an available external API."
    )


# ==========================================
# MAIN USER INTERFACE
# ==========================================

st.subheader("Enter an amino acid sequence")

sequence = st.text_area(
    "Protein sequence",
    placeholder=(
        "Paste your amino acid sequence here...\n"
        "Example: MKTAYIAKQRQISFVKSHFSRQ"
    ),
    height=180
)

predict_button = st.button(
    "Predict Protein Structure",
    type="primary",
    use_container_width=True
)


# ==========================================
# RUN PREDICTION
# ==========================================

if predict_button:

    is_valid, result = validate_sequence(sequence)

    if not is_valid:

        st.error(result)

    else:

        sequence = result

        st.info(
            f"Sequence length: {len(sequence)} amino acids"
        )

        with st.spinner(
            "Requesting protein structure prediction..."
        ):

            pdb_data, error = predict_structure(sequence)

        if error:

            st.error(error)

            st.info(
                "If HTTP 504 persists after retries, "
                "the prediction server may be unavailable. "
                "Increasing the client timeout cannot fix "
                "a gateway timeout returned by the server."
            )

        else:

            save_pdb(pdb_data)

            st.success(
                "Protein structure prediction completed!"
            )

            st.divider()

            # ----------------------------------
            # 3D VIEWER
            # ----------------------------------

            st.subheader("Interactive 3D Structure")

            st.caption(
                "Rotate and zoom the model to explore "
                "the predicted protein structure."
            )

            try:
                visualize_protein(pdb_data)

            except Exception as error:
                st.error(
                    f"Could not display the 3D structure: {error}"
                )

            st.divider()

            # ----------------------------------
            # CONFIDENCE SCORE
            # ----------------------------------

            st.subheader("Structure Confidence")

            confidence = calculate_confidence(pdb_data)

            if confidence is not None:

                st.metric(
                    "Mean B-factor field",
                    f"{confidence:.2f}"
                )

                st.caption(
                    "ESMFold PDB output commonly stores "
                    "per-residue confidence in the B-factor "
                    "field. Confirm the field's meaning before "
                    "interpreting this value as pLDDT."
                )

            else:

                st.warning(
                    "Confidence information could not "
                    "be extracted from this structure."
                )

            st.divider()

            # ----------------------------------
            # DOWNLOAD PDB
            # ----------------------------------

            st.subheader("Download Structure")

            st.download_button(
                label="Download PDB File",
                data=pdb_data,
                file_name="predicted.pdb",
                mime="chemical/x-pdb",
                use_container_width=True
            )

            st.success(
                "Your predicted structure is ready to download."
            )

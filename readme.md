# Protein Structure Prediction and 3D Visualization

A web-based bioinformatics application that predicts the three-dimensional structure of a protein from its amino acid sequence and visualizes the predicted structure interactively. The application uses the ESM Atlas Fold API for protein structure prediction and Streamlit to provide a simple, user-friendly interface.

## Overview

Proteins perform essential biological functions, and their three-dimensional structures play a significant role in understanding how they work. Experimental structure determination can be expensive and time-consuming. This project provides a convenient way to explore predicted protein structures directly from an amino acid sequence.

Users can enter a protein sequence, generate a predicted structure, view the resulting 3D model, examine confidence-related information, and download the predicted PDB file.

## Features

- **Protein Sequence Input:** Enter an amino acid sequence directly into the application.
- **Sequence Validation:** Check the sequence for valid standard amino acid symbols.
- **AI-Based Structure Prediction:** Submit the sequence to the ESM Atlas Fold API.
- **Interactive 3D Visualization:** Explore the predicted protein structure using py3Dmol and stmol.
- **Structure File Download:** Download the predicted structure in PDB format.
- **Confidence Information:** Calculate a mean value from the PDB B-factor field, which may represent pLDDT-style confidence scores in ESMFold output.
- **Error Handling and Retries:** Handle unsuccessful API responses and retry selected temporary server errors.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application interface |
| ESM Atlas Fold API | Protein structure prediction |
| Requests | HTTP communication with the prediction API |
| Biotite | Reading and processing PDB structure data |
| py3Dmol | Interactive molecular structure visualization |
| stmol | Integrating molecular visualization into Streamlit |
| NumPy | Numerical computing support |

## System Workflow

1. The user enters an amino acid sequence.
2. The application validates the sequence.
3. The sequence is submitted to the ESM Atlas Fold API.
4. The API returns the predicted protein structure in PDB format.
5. The application checks and processes the returned structure.
6. The predicted protein is displayed in an interactive 3D viewer.
7. The user can inspect the structure and download the PDB file.

## Project Structure

```text
protein-structure-prediction/
│
├── app.py
├── requirements.txt
├── README.md
└── predicted.pdb       # Generated after a successful prediction
```

The `predicted.pdb` file is generated during execution and may be excluded from version control if it is only an output file.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

Replace the placeholders with your actual GitHub repository URL and project folder name.

### 2. Create a virtual environment

On Windows:

```bash
py -3.13 -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

If Python 3.13 is not installed, use a Python version supported by all the required dependencies.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open that URL in your browser to use the application.

## Requirements

Your `requirements.txt` should contain:

```text
streamlit
stmol
py3Dmol
requests
biotite
numpy
```

For a reproducible deployment, consider pinning versions after confirming that the application works with the selected Python version.

## Protein Structure Prediction API

This project uses the ESM Atlas Fold API endpoint:

```text
https://api.esmatlas.com/foldSequence/v1/pdb/
```

The application sends an amino acid sequence to the service and processes the returned PDB structure. Prediction availability and response times depend on the external service. Temporary errors such as HTTP 429 or HTTP 504 may occur due to rate limiting, server load, or gateway timeouts.

## Output

A successful prediction produces a protein structure in PDB format. The structure can be:

- Viewed interactively in the application.
- Inspected in a compatible molecular visualization tool.
- Downloaded for further analysis.

The confidence-related value derived from the PDB B-factor field should be interpreted according to the output format and model conventions; it is not automatically a measure of experimental accuracy.

## Limitations

- Structure prediction requires an internet connection and access to the external API.
- Long sequences and temporary service issues may increase prediction time or cause requests to fail.
- Predicted structures are computational models and should not be treated as experimentally verified structures.
- The application depends on compatibility between Python, Biotite, Streamlit, and the molecular visualization libraries.

## Future Enhancements

- Add sequence upload support using FASTA files.
- Display per-residue confidence scores and confidence-colored structures.
- Add secondary structure analysis.
- Support saving and comparing multiple predictions.
- Add prediction history and downloadable reports.
- Improve handling of long-running requests and API failures.
- Deploy the application on a cloud platform.

## Learning Outcomes

This project demonstrates practical experience with:

- Integrating an external machine-learning-based scientific API.
- Developing an interactive application using Streamlit.
- Validating biological sequence data.
- Processing molecular structure files.
- Visualizing scientific data in three dimensions.
- Handling HTTP errors, retries, and external service dependencies.

## Disclaimer

This application is intended for educational and research exploration. Predicted structures and confidence values should be interpreted carefully and independently validated before use in scientific or clinical decision-making.

## Acknowledgements

- ESM Atlas for the protein structure prediction service.
- Streamlit for the web application framework.
- Biotite, py3Dmol, and stmol for molecular structure processing and visualization.

---

**Author:** Chaitanya Hegde  
**Project:** Protein Structure Prediction and 3D Visualization  
**Language:** Python

# AutoPartsAI

AutoPartsAI is a Python/FastAPI prototype that reads vehicle information from registration document images and provides a starting point for spare parts requests.

## Current features

- Attempts to extract the VIN, make, model, model year, engine displacement, and fuel type from a registration image using OCR.
- Chat-style upload interface: `/chat`
- API documentation and interactive page: `/docs`
- Health check: `/health`
- API endpoints that validate vehicle and part-request data

Vehicle and part requests are not stored in a database yet. The parts catalog, pricing, and warehouse integrations have not been implemented. Review OCR results before using them; the VIN in the sample registration image is test data.

## Requirements

- Python 3
- Tesseract OCR
- Tesseract Turkish language data (`tur`)

### macOS

Install Tesseract and its additional language data with Homebrew:

```bash
brew install tesseract tesseract-lang
```

Verify that Tesseract and the Turkish language data are available:

```bash
tesseract --version
tesseract --list-langs
```

The output should include `tur`. The base Homebrew Tesseract package includes English and orientation data; additional languages such as Turkish are provided by `tesseract-lang`. See the [Tesseract formula](https://formulae.brew.sh/formula/tesseract) and [additional language data formula](https://formulae.brew.sh/formula/tesseract-lang).

### Windows

1. Install Tesseract by following the [Windows instructions in the Tesseract installation guide](https://tesseract-ocr.github.io/tessdoc/Installation.html). The executable is commonly located at `C:\Program Files\Tesseract-OCR\tesseract.exe`.
2. If Turkish language data was not included during installation, download `tur.traineddata` from the [Tesseract language data files](https://tesseract-ocr.github.io/tessdoc/Data-Files.html) and place it in Tesseract's `tessdata` folder. This is commonly `C:\Program Files\Tesseract-OCR\tessdata`.
3. Reopen PowerShell and verify the installation:

```powershell
tesseract --version
tesseract --list-langs
```

The output should include `tur`. If the Tesseract installation folder is not on `PATH`, configure the executable path as described below.

## Set up the Python environment

Open Terminal or PowerShell in the `AutoPartsAI` project folder, the folder that contains `requirements.txt`.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, open Command Prompt and run:

```bat
.venv\Scripts\activate.bat
```

## Configure the Tesseract path (if needed)

No `.env` file is needed if `tesseract --version` works in your terminal and Tesseract is available on `PATH`.

If it is not on `PATH`, copy `.env.example` to `.env` and uncomment the `TESSERACT_CMD` line for your operating system. Update the path if Tesseract is installed elsewhere.

To find the Tesseract path on macOS:

```bash
which tesseract
```

Keep `.env` in the project root, next to `requirements.txt`.

## Run the application

With the virtual environment active, run this command from the project folder:

```bash
uvicorn src.api.main:app --reload
```

Open these addresses in your browser:

- Chat interface: <http://127.0.0.1:8000/chat>
- API documentation: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

On the chat page, select a registration image and click **Send**. The extracted vehicle details appear in the conversation. If some fields cannot be read, try a clearer, straight-on image and review the results.

Stop the server with `Ctrl+C` in the terminal.

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | API status message |
| `GET` | `/health` | Health check |
| `GET` | `/chat` | Chat interface |
| `POST` | `/vehicles` | Validates and returns vehicle information |
| `POST` | `/part-requests` | Validates and returns a part request |
| `POST` | `/vehicles/upload-registration` | Processes a registration image with OCR |

See `/docs` for request and response examples.

## Run the tests

Activate the virtual environment first.

**macOS:**

```bash
python3 -m pytest
```

**Windows PowerShell:**

```powershell
python -m pytest
```

## Project structure

```text
config/                  Application configuration
src/api/                 FastAPI endpoints and chat interface
src/models/              Vehicle and part-request models
src/vehicle_detection/   OCR and registration-field parsing
src/parts_lookup/        Parts lookup module (not implemented yet)
src/pricing/             Pricing module (not implemented yet)
src/cross_reference/     Part cross-reference module (not implemented yet)
src/warehouse/           Warehouse module (not implemented yet)
data/                    Local test images (ignored by Git)
tests/                   API and model tests
```

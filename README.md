# BDD Utility
BDD-Utility is a powerful tool that converts various requirement documents (BRD, FRD, User Stories, Test Cases) into Gherkin feature files and generates step definitions in multiple programming languages.

## Features
- Convert requirement documents to Gherkin feature files
- Generate step definitions in multiple programming languages
- Support for various input formats (docx, pdf, txt)
- Web-based interface with real-time preview
- NLP-powered smart conversion

## Setup

### Backend
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm start
```

## Usage
1. Upload your requirement document through the web interface
2. Review and edit the generated feature file
3. Generate step definitions in your preferred programming language
4. Download the generated code

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
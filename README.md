# Flask Multi-Page Website

A Flask site that has every basic input, button, etc that everyone uses

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd just-Flask
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8080
   ```

## Project Structure

```
just-Flask/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css      # Stylesheet
└── templates/
    ├── index.html     # Home page
    ├── page2.html     # Second page
    ├── page3.html     # Third page
    └── logo.html      # Logo display page
```

## Dependencies

- Flask - Web framework

## Contributing

Feel free to submit issues and enhancement requests.


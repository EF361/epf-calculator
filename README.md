# EPF Calculator

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-orange.svg)
![HTML5](https://img.shields.io/badge/Frontend-HTML5-red.svg)
![CSS3](https://img.shields.io/badge/Styling-CSS3-blueviolet.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## Executive Summary
The **EPF Calculator** is a web-based tool that simplifies and ensures the accurate calculation of Malaysian Employees Provident Fund (EPF) contributions. It adheres to statutory regulations by implementing versioned contribution rules, precise rounding policies, and robust financial computations for employers and employees.

## Key Features
- **Version-Controlled Contribution Rules**: Calculates EPF contributions using tables tied to their effective dates, with explicit references to data from the [Official EPF Malaysia Website](https://www.kwsp.gov.my/).
- **Precise Rounding Logic**: Implements and tests statutory rounding rules using decimal and integer-sen arithmetic to ensure accuracy.
- **Boundary-Driven Validation**: Validates inputs and computes results across age groups, salary thresholds, citizenship categories, and effective rule dates.
- **Separation of Concerns**: Decouples calculation logic from Flask routes for modularity and easier testing.
- **Detailed Outputs**: Displays calculation breakdowns, rule versions, effective dates, and legal disclaimers for transparency.
- **Error Handling**: Intuitive error messages for unsupported employee categories, dates, or invalid salary inputs.
- **Table-Driven Testing**: Automatically verifies contributions against boundary values, thresholds, and complex wage scenarios.
- **User-Friendly Interface**: Responsive design with modern HTML5 and CSS3.

## Architecture & Workflow

```mermaid
graph TD
  A[User Input] --> B[Flask Endpoint]
  B --> C[Input Validation]
  C --> D[Calculation Engine]
  D --> E[Versioned Contribution Tables]
  D --> F[Rounding & Threshold Logic]
  E --> G[Calculation Breakdown Generator]
  F --> G
  G --> H[Render Result (Frontend)]
  H --> I[User Output: Breakdown, Disclaimer, Version]
```

1. **User Input**: The user provides salary and employee details via a web form.
2. **Flask Endpoint**: Handles HTTP requests and routes, passing input to the backend processor.
3. **Input Validation**: Ensures salaries, dates, and employee data are valid and supported.
4. **Calculation Engine**: Executes core business logic using modular and versioned contribution tables.
5. **Result Rendering**: Generates a user-friendly breakdown, disclaimer, and calculation result.

The modular structure ensures high maintainability, testability, and adaptability to future EPF changes.

## Tech Stack & Tools
- **Backend**: Python 3.9+, Flask
- **Frontend**: HTML5, CSS3
- **Testing**: Pytest (Including boundary-driven, table-driven unit testing)
- **Data Handling**: Versioned Contribution Tables
- **Tools**:
  - `flask` for serving web requests.
  - `decimal` for precise financial calculations.
  - `pytest` for rigorous validation of contribution rules and edge cases.

## Quickstart / Installation

### Prerequisites
- Python 3.9 or later installed.
- A virtual environment tool (`venv` or `virtualenv`).

### Steps
1. **Clone the Repository**:
   ```
   git clone https://github.com/EF361/epf-calculator.git
   cd epf-calculator
   ```

2. **Set Up a Virtual Environment**:
   ```
   python3 -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```
   flask run
   ```

5. **Access the Application**:
   Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

6. **Run Tests**:
   To verify the application's accuracy, execute:
   ```
   pytest
   ```

## Disclaimer
This tool provides indicative calculations based on official EPF contribution tables from the Malaysian EPF website as of the last effective update. Users are advised to consult with the EPF office or legal professionals for authoritative financial advice.

--- 

Contributed by **Alicia Goh (EF361)**, an AI & Software Engineer committed to building precise, regulatory-compliant financial software.
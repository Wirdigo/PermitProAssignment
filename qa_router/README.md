# QA Router API  
  
A Django REST Framework API that routes natural-language questions to the appropriate data source (geo or regulation).  
  
## Setup  
  
### Prerequisites  
- Python 3.10+  
- Node.js 18+ (optional, for UI)  
  
### Installation  
```bash  
# Clone repository  
git clone <repo-url>  
cd qa_router  
  
# Create virtual environment  
python -m venv .venv  
source .venv/bin/activate  # On Windows: .venv\Scripts\activate  
  
# Install dependencies  
pip install -r requirements.txt  
  
# Run server  
python manage.py runserver  
```  
  
## API Usage  
  
### Endpoint  
```  
POST /api/ask/  
```  
  
### Request Body  
```json  
{  
  "question": "What is the soil type?"}  
```  
  
### Response  
```json  
{  
  "answer": "Found 1 result(s): ...",  "source": "geo"}  
```  
  
### Example curl Commands  
```bash  
# Geo case  
curl -X POST http://localhost:8000/api/ask/ \  
  -H "Content-Type: application/json" \  -d '{"question": "What is the soil type?"}'  
# Regulation case  
curl -X POST http://localhost:8000/api/ask/ \  
  -H "Content-Type: application/json" \  -d '{"question": "What are the building regulations?"}'  
# Unknown case  
curl -X POST http://localhost:8000/api/ask/ \  
  -H "Content-Type: application/json" \  -d '{"question": "Hello, how are you?"}'  
```  
  
## Routing Logic  
  
The system uses keyword matching to determine the data source:  
  
| Source         | Keywords                                                        |
| -------------- | --------------------------------------------------------------- |
| **geo**        | soil, flood, bodem, overstroming, kaart, gebied, natuur...      |
| **regulation** | regulation, rule, artikel, voorschrift, vergunning, bouwlaag... |
| **unknown**    | No matching keywords found                                      |
  
The source with the highest keyword match count is selected.  
  
## Running Tests  
```bash    
python manage.py test 
```
  

## qa_router (Backend API)

The Django REST Framework backend that:
- Receives natural-language questions via `POST /api/ask/`
- Routes questions to the correct data source (geo or regulation)
- Searches mock data files and returns answers
  
## qa_client (Frontend UI)

Optional Next.js chat interface for interacting with the API.

### Quick Start
```bash
cd qa_client
npm install
npm run dev
```

Open http://localhost:3000

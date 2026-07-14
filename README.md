1. Create and Activate a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

### Install dependencies
pip install -r requirements.txt

### 3. Start PostgreSQL (Local Test Database)

This project uses PostgreSQL for integration and end‑to‑end tests.  
You can start a local PostgreSQL instance using Docker:

```bash
docker run -d \
  --name testdb \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=mytestdb \
  -p 5432:5432 \
  postgres:latest


### 4. Set the DATABASE_URL environment variable
export DATABASE_URL=postgresql://user:password@localhost:5432/mytestdb

### 5. Run Test
pytest
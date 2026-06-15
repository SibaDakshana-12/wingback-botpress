from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from app.connector.scanner import BotpressScanner
from app.database import create_db, engine
from app.models import Resource, Scan
import uuid, datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class ResourceCreate(BaseModel):
    account_name: str
    resource_name: str
    webhook_id: str
    encryption_key: str = None
    user_id: str = None
    description: str = None

class PromptItem(BaseModel):
    vulnerability_id: str
    attack_id: str
    test_input: str

class ScanRequest(BaseModel):
    prompts: list[PromptItem]
    reset_conversation: bool = True

# --- Routes ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.post("/api/v1/resources")
def create_resource(body: ResourceCreate):
    with Session(engine) as session:
        resource = Resource(
            id=str(uuid.uuid4()),
            account_name=body.account_name,
            resource_name=body.resource_name,
            webhook_id=body.webhook_id,
            encryption_key=body.encryption_key,
            user_id=body.user_id,
            description=body.description,
            validated=False,
            created_at=datetime.datetime.utcnow()
        )
        session.add(resource)
        session.commit()
        session.refresh(resource)
        return {**resource.dict(), "encryption_key": None}

@app.get("/api/v1/resources")
def list_resources():
    with Session(engine) as session:
        resources = session.exec(select(Resource)).all()
        return [{**r.dict(), "encryption_key": None} for r in resources]

@app.get("/api/v1/resources/{id}")
def get_resource(id: str):
    with Session(engine) as session:
        resource = session.get(Resource, id)
        if not resource:
            raise HTTPException(status_code=404, detail="Not found")
        return {**resource.dict(), "encryption_key": None}

@app.post("/api/v1/resources/{id}/validate")
def validate_resource(id: str):
    with Session(engine) as session:
        resource = session.get(Resource, id)
        if not resource:
            raise HTTPException(status_code=404, detail="Not found")
        scanner = BotpressScanner({"webhook_id": resource.webhook_id})
        ok = scanner.validate_target()
        resource.validated = ok
        session.add(resource)
        session.commit()
        return {"validated": ok}

@app.post("/api/v1/resources/{id}/scan")
def run_scan(id: str, body: ScanRequest):
    with Session(engine) as session:
        resource = session.get(Resource, id)
        if not resource:
            raise HTTPException(status_code=404, detail="Not found")
        scanner = BotpressScanner({"webhook_id": resource.webhook_id})
        results = []
        for p in body.prompts:
            if body.reset_conversation:
                scanner.reset_conversation()
            result = scanner.execute_test(p.vulnerability_id, p.attack_id, p.test_input)
            scan = Scan(
                id=str(uuid.uuid4()),
                resource_id=id,
                vulnerability_id=p.vulnerability_id,
                attack_id=p.attack_id,
                prompt=p.test_input,
                response=result.get("model_response") or "",
                success=result.get("success", False),
                execution_time_ms=result.get("execution_time_ms", 0),
                created_at=datetime.datetime.utcnow()
            )
            session.add(scan)
            session.commit()
            results.append(result)
        return {"resource_id": id, "results": results}

@app.get("/api/v1/resources/{id}/scans")
def list_scans(id: str):
    with Session(engine) as session:
        scans = session.exec(select(Scan).where(Scan.resource_id == id)).all()
        return scans
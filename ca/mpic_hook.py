# mpic_hook.py
from fastapi import FastAPI, Request, HTTPException
import httpx, os, uuid

app = FastAPI()
MPIC_URL = os.getenv("MPIC_COORD", "http://coord.example.com/mpic")

@app.post("/shouldSign")
async def should_sign(req: Request):
    payload = await req.json()
    sans = payload["sans"]           # step‑ca passes parsed SANs
    for domain in sans:
        trace = str(uuid.uuid4())
        mpic_req = {
            "check_type": "dcv",
            "domain_or_ip_target": domain,
            "dcv_check_parameters": {
                "validation_method": "acme-http-01",
                "token": payload["acmeToken"],
                "key_authorization": payload["acmeKeyAuth"]
            },
            "trace_identifier": trace
        }
        r = await httpx.post(MPIC_URL, json=mpic_req, timeout=15)
        data = r.json()
        if not data.get("is_valid"):
            raise HTTPException(status_code=403,
                                detail=f"MPIC failed for {domain}, trace {trace}")
    # all SANs cleared MPIC
    return {"sign": True}
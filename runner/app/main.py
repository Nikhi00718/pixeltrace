"""HTTP API for the C++ runner."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .runner import run_request

app = FastAPI(title="pixeltrace-runner")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOW_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

TOKEN = os.environ.get("RUNNER_TOKEN", "")
# One compile+trace at a time per worker keeps CPU predictable.
SLOTS = asyncio.Semaphore(int(os.environ.get("RUNNER_SLOTS", "2")))


class Spec(BaseModel):
    method: str
    ret: str = "void"
    params: list[list[str]]
    output: str = "return"


class Test(BaseModel):
    args: list[Any]
    expected: Any = None
    has_expected: bool = True


class RunBody(BaseModel):
    code: str = Field(max_length=40000)
    spec: Spec
    tests: list[Test]
    compare: str = "exact"
    trace: int | None = None
    reference: str | None = None


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/run")
async def run(body: RunBody, authorization: str | None = Header(default=None)):
    if TOKEN and authorization != f"Bearer {TOKEN}":
        raise HTTPException(401, "bad token")
    tests = []
    for t in body.tests:
        d = {"args": t.args}
        if t.has_expected:
            d["expected"] = t.expected
        tests.append(d)
    req = {
        "code": body.code,
        "spec": body.spec.model_dump(),
        "tests": tests,
        "compare": body.compare,
        "trace": body.trace,
        "reference": body.reference,
    }
    async with SLOTS:
        return await asyncio.to_thread(run_request, req)

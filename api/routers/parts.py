from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db
import api.cruds.parts as parts_cruds

router = APIRouter()

@router.get("/cpu-all")
def get_cpus(db: Session = Depends(get_db)):
    return parts_cruds.get_cpu_all(db)

@router.get("/cpu-with/{gpu_id}")
def get_cpus_with_gpu(gpu_id: int, db: Session = Depends(get_db)):
    if gpu_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid GPU ID")
    
    return parts_cruds.get_cpu_with_gpu(gpu_id, db)

@router.get("/gpu-all")
def get_gpus(db: Session = Depends(get_db)):
    return parts_cruds.get_gpu_all(db)

@router.get("/gpu-with/{cpu_id}")
def get_gpus_with_cpu(cpu_id: int, db: Session = Depends(get_db)):
    gpus = parts_cruds.get_gpu_with_cpu(cpu_id, db)
    if not gpus:
        raise HTTPException(status_code=404, detail="No GPUs found for the given CPU ID")
    return gpus

@router.get("/memory-all")
def get_memories(db: Session = Depends(get_db)):
    return parts_cruds.get_memory_all(db)

@router.get("/memory-with/{cpu_id}")
def get_memories_with_cpu(cpu_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_memory_with_cpu(cpu_id, db)
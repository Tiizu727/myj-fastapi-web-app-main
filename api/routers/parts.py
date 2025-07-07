from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db
from api.extra_modules.auth.core import get_current_user
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

@router.get("/storage-all")
def get_storages(db: Session = Depends(get_db)):
    return parts_cruds.get_storage_all(db)

@router.get("/motherboard-all")
def get_motherboards(db: Session = Depends(get_db)):
    return parts_cruds.get_motherboard_all(db)

@router.get("/motherboard-with/{cpu_id}/{gpu_id}/{memory_id}/{storage_id}")
def get_motherboard_with(cpu_id: int, gpu_id: int, memory_id: int, storage_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_motherboard_with(cpu_id, gpu_id, memory_id, storage_id, db)

@router.get("/cooler-all")
def get_coolers(db: Session = Depends(get_db)):
    return parts_cruds.get_cooler_all(db)

@router.get("/cooler-with/{cpu_id}")
def get_cooler_with(cpu_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_cooler_with(cpu_id, db)

@router.get("/psu-all")
def get_psu_all(db: Session = Depends(get_db)):
    return parts_cruds.get_psu_all(db)

@router.get("/tdp/{product_id}")
def get_tdp(product_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_tdp(product_id, db)

@router.get("/psu-with/{tdp}")
def get_psu_with(tdp: int, db: Session = Depends(get_db)):
    return parts_cruds.get_psu_with(tdp, db)

@router.get("/case-with/{gpu_id}/{storage_id}/{mb_id}/{cooler_id}/{psu_id}")
def get_case_with(gpu_id: int, storage_id: int, mb_id: int, cooler_id: int, psu_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_case_with(gpu_id, storage_id, mb_id, cooler_id, psu_id, db)

@router.get("/gpu-game/{game_id}")
def get_gpu_game(game_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_gpu_from_gameid(game_id, db)

@router.get("/build/{build_id}")
def get_build(build_id: int, db: Session = Depends(get_db)):
    return parts_cruds.get_build(db, build_id)

@router.post("/build")
def create_build(
    build: dict = Body(), db: Session = Depends(get_db)
):
    return parts_cruds.create_build(build,db)

@router.get("/os")
def get_os(db: Session = Depends(get_db)):
    return parts_cruds.get_os(db)

@router.post("/user-build")
def connect_user_builds(
    user_id: int, build_id: int, db: Session = Depends(get_db)
):
    
    return parts_cruds.connect_user_builds(db, user_id=user_id, build_id=build_id)

@router.get("/builds")
def get_user_builds(
    db: Session = Depends(get_db)
, current_user: dict = Depends(get_current_user)
):
    return parts_cruds.get_user_builds(db, current_user.get("id"))

@router.get("/build/{build_id}")
def get_build_by_id(
    build_id: int, db: Session = Depends(get_db)
):
    return parts_cruds.get_build(db, build_id)

@router.get("/gpu-by-game/{game_id}")
def get_gpu_by_game(
    game_id: int, db: Session = Depends(get_db)
):
    return parts_cruds.get_gpu_by_game(db, game_id)

@router.delete("/build/{build_id}")
def delete_build(
    build_id: int, db: Session = Depends(get_db)
):
    return parts_cruds.delete_build(db, build_id)
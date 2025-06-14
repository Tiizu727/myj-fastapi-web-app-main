from sqlalchemy import text
from sqlalchemy.orm import Session

def get_cpu_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN cpu_specs ON products.chipset_id = cpu_specs.chipset_id
        WHERE products.category = 'CPU'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_cpu_with_gpu(gpu_id: int, db: Session):
    sql = text(
        """
        SELECT 
            p.*, 
            cspecs.*, 
            cspecs.passmark AS cpu_passmark,
            coeff.coefficient,
            LEAST(
                cspecs.passmark / (gspecs.passmark * coeff.coefficient),
                (gspecs.passmark * coeff.coefficient) / cspecs.passmark
            ) AS evaluation
        FROM products p
        INNER JOIN cpu_specs cspecs ON p.chipset_id = cspecs.chipset_id
        INNER JOIN (
            SELECT chipset_id, passmark
            FROM gpu_specs
            WHERE chipset_id = (
                SELECT chipset_id FROM products WHERE id = :gpu_id
            )
        ) gspecs ON 1=1
        INNER JOIN cpu_gpu_coefficients coeff ON cspecs.series = coeff.cpu_model
        WHERE p.category = 'CPU'
        ORDER BY evaluation DESC
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"gpu_id": gpu_id}).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_gpu_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN gpu_specs ON products.chipset_id = gpu_specs.chipset_id
        INNER JOIN gpu_performance ON products.id = gpu_performance.product_id
        WHERE products.category = 'GPU'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_gpu_with_cpu(cpu_id: int, db: Session):
    sql = text(
        """
        SELECT 
            p.*, 
            gspecs.*,
            gperf.*,
            cspecs.passmark AS cpu_passmark,
            coeff.coefficient,
            LEAST(
                cspecs.passmark / (gspecs.passmark * coeff.coefficient),
                (gspecs.passmark * coeff.coefficient) / cspecs.passmark
            ) AS evaluation
        FROM products p
        INNER JOIN gpu_specs gspecs ON p.chipset_id = gspecs.chipset_id
        INNER JOIN gpu_performance gperf ON p.id = gperf.product_id
        INNER JOIN (
            SELECT chipset_id, series, passmark
            FROM cpu_specs
            WHERE chipset_id = (
                SELECT chipset_id FROM products WHERE id = :cpu_id
            )
        ) cspecs ON 1=1
        INNER JOIN cpu_gpu_coefficients coeff ON cspecs.series = coeff.cpu_model
        WHERE p.category = 'GPU'
        ORDER BY evaluation DESC
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"cpu_id": cpu_id}).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_memory_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN memory_specs ON products.id = memory_specs.product_id
        WHERE products.category = 'memory'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_memory_with_cpu(cpu_id: int, db: Session):
    sql = text(
        """
        SELECT 
            p.*, 
            mspecs.*
        FROM products p
        INNER JOIN memory_specs mspecs ON p.id = mspecs.product_id
        WHERE p.category = 'memory'
          AND mspecs.memory_type = (
              SELECT memory_type FROM cpu_specs
              WHERE chipset_id = (
                  SELECT chipset_id FROM products WHERE id = :cpu_id
              )
          )
          AND mspecs.speed_mhz <= (
              SELECT memory_speed FROM cpu_specs
              WHERE chipset_id = (
                  SELECT chipset_id FROM products WHERE id = :cpu_id
              )
          )
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"cpu_id": cpu_id}).mappings().all()
    print(f"DB操作の結果: {result}")

    return result
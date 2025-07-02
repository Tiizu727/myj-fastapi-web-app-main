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

def get_storage_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN storage_specs ON products.id = storage_specs.product_id
        WHERE products.category = 'storage'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_motherboard_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN motherboard_specs ON products.id = motherboard_specs.product_id
        WHERE products.category = 'motherboard'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_motherboard_with(cpu_id: int, gpu_id: int, memory_id: int, storage_id: int, db: Session):
    sql = text(
        """
        SELECT 
            p.*, 
            mb.*, 
            mspecs.*, 
            gspecs.*, 
            sspecs.*
        FROM products p
        INNER JOIN motherboard_specs mb ON p.id = mb.product_id

        -- CPU条件
        INNER JOIN products cpu_prod ON cpu_prod.id = :cpu_id
        INNER JOIN cpu_specs cspecs ON cpu_prod.chipset_id = cspecs.chipset_id
            AND mb.socket_type = cspecs.socket_type

        -- メモリ条件
        INNER JOIN memory_specs mspecs ON mspecs.product_id = :memory_id
            AND mb.memory_type = mspecs.memory_type
            AND mb.max_memory >= (mspecs.capacity_gb * mspecs.module_count)

        -- GPU条件
        INNER JOIN products gpu_prod ON gpu_prod.id = :gpu_id
        INNER JOIN gpu_specs gspecs ON gpu_prod.chipset_id = gspecs.chipset_id

        -- ストレージ条件
        INNER JOIN storage_specs sspecs ON sspecs.product_id = :storage_id

        WHERE
            (
                (gspecs.interface = 'PCI Express 5.0' AND mb.PCIe5x16 >= 1)
                OR
                (gspecs.interface = 'PCI Express 4.0' AND mb.PCIe4x16 >= 1)
            )
            AND (
                (
                    sspecs.storage_type IN ('SSD', 'HDD')
                    AND mb.SATA >= 1
                )
                OR
                (
                    sspecs.storage_type = 'M2'
                    AND EXISTS (
                        SELECT 1 FROM motherboard_M2type m2
                        WHERE m2.type_id = sspecs.interface
                        AND m2.product_id = mb.product_id
                    )
                )
            )
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"cpu_id": cpu_id, "gpu_id": gpu_id, "memory_id": memory_id, "storage_id": storage_id}).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_cooler_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN cooler_specs ON products.id = cooler_specs.product_id
        WHERE products.category = 'cpu_cooler'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_cooler_with(cpu_id: int, db: Session):
    sql = text(
        """
        SELECT 
            p.*, 
            coolers.*
        FROM products p
        INNER JOIN cooler_specs coolers ON p.id = coolers.product_id
        WHERE p.id IN (
            SELECT cs.product_id
            FROM cooler_socket cs
            WHERE cs.socket_type = (
                SELECT cpu_specs.socket_type
                FROM cpu_specs
                WHERE cpu_specs.chipset_id = (
                    SELECT products.chipset_id
                    FROM products
                    WHERE products.id = :cpu_id
                )
                LIMIT 1
            )
        )
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql,{"cpu_id": cpu_id}).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_psu_all(db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN psu_specs ON products.id = psu_specs.product_id
        WHERE products.category = 'powersupply'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_tdp(product_id: int, db: Session):
    chipset_based_specs = {
        "CPU": "cpu_specs",
        "GPU": "gpu_specs"
    }

    presql = text("""
        SELECT category, chipset_id
        FROM products
        WHERE id = :product_id
    """)
    product = db.execute(presql, {"product_id": product_id}).mappings().first()

    category = product["category"]
    chipset_id = product["chipset_id"]

    if category in chipset_based_specs:
        table = chipset_based_specs[category]
        sql = text(f"""
            SELECT tdp FROM {table}
            WHERE chipset_id = :chipset_id
            LIMIT 1
        """)
        result = db.execute(sql, {"chipset_id": chipset_id}).mappings().first()
        return result["tdp"]

    elif category == "memory":
        sql = text("SELECT tdp FROM memory_specs WHERE product_id = :product_id")
        result = db.execute(sql, {"product_id": product_id}).mappings().first()
        return result["tdp"]

    elif category == "storage":
        sql = text("SELECT tdp FROM storage_tdp WHERE storage_type = :storage_type")
        result = db.execute(sql, {"storage_type": chipset_id}).mappings().first()
        return result["tdp"]
    
def get_psu_with(tdp: int, db: Session):
    sql = text(
        """
        SELECT * FROM products
        INNER JOIN psu_specs ON products.id = psu_specs.product_id
        WHERE psu_specs.wattage >= :tdp
        ORDER BY psu_specs.wattage
        """
    )
    
    print(f"SQL: {sql}")
    result = db.execute(sql, {"tdp": tdp}).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_case_with(gpu_id: int, storage_id: int, mb_id: int, cooler_id: int, psu_id: int, db: Session):
    sql = text(
        """
        SELECT 
            p.*, 
            cspecs.*
        FROM products p
        INNER JOIN case_specs cspecs ON p.id = cspecs.product_id

        -- GPU条件
        INNER JOIN gpu_performance gperf ON gperf.product_id = :gpu_id
            AND cspecs.max_gpu_length > gperf.width

        -- PSU条件
        INNER JOIN psu_specs pspecs ON pspecs.product_id = :psu_id
            AND cspecs.max_psu_length > pspecs.most_length

        -- ストレージ条件
        INNER JOIN storage_specs sspecs ON sspecs.product_id = :storage_id
            AND (
                (sspecs.storage_type = 'SSD' AND cspecs.drive25 >= 1)
                OR
                (sspecs.storage_type = 'HDD' AND cspecs.drive35 >= 1)
                OR
                (sspecs.storage_type = 'M2')
            )

        -- クーラー条件
        INNER JOIN cooler_specs coolers ON coolers.product_id = :cooler_id
            AND (
                (coolers.cooler_type = 'air' AND cspecs.max_cooler_height > coolers.size)
                OR
                (coolers.cooler_type = 'liquid' AND EXISTS (
                    SELECT 1 FROM case_radiator cr
                    WHERE cr.radiator_size = coolers.size
                    AND cr.product_id = cspecs.product_id
                ))
            )

        -- マザーボード条件
        INNER JOIN motherboard_specs mb ON mb.product_id = :mb_id
        INNER JOIN case_motherboard cmb ON cmb.formfactor = mb.form_factor
            AND cmb.product_id = cspecs.product_id
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"gpu_id": gpu_id, "storage_id": storage_id, "mb_id": mb_id, "cooler_id": cooler_id, "psu_id": psu_id}).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def get_gpu_from_gameid(gameid: int, db: Session):
    sql = text(
        """
        SELECT p.*
        FROM products p
        INNER JOIN gpu_specs gs ON p.chipset_id = gs.chipset_id
        INNER JOIN gpu_performance gp ON p.id = gp.product_id
        AND p.id IN (
            SELECT p2.id
            FROM products p2
            WHERE p2.chipset_id IN (
                SELECT gs2.chipset_id
                FROM gpu_specs gs2
                WHERE gs2.passmark >= (
                    SELECT gs3.passmark
                    FROM game_gpu gg
                    INNER JOIN gpu_specs gs3 ON gs3.chipset_id = gg.gpu_id
                    WHERE gg.id = :gameid
                )
            )
        )
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"gameid": gameid}).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def create_build(build: dict, db: Session) -> dict:
    sql = text(
        """
        INSERT INTO build(name,cpu,gpu,memory,storage,mb,cooler,psu,`case`,`OS`) VALUES(:name,:cpu,:gpu,:memory,:storage,:mb,:cooler,:psu,:case,:os)
        """
    )

    params = {
        "name": build.get("name"),
        "cpu": build.get("cpu"),
        "gpu": build.get("gpu"),
        "memory": build.get("memory"),
        "storage": build.get("storage"),
        "mb": build.get("mb"),
        "cooler": build.get("cooler"),
        "psu": build.get("psu"),
        "case": build.get("case"),
        "os": build.get("os"),
    }

    print(f"SQL: {sql}")
    result = db.execute(sql, params)
    db.commit()
    new_build_id = result.lastrowid
    if new_build_id is None:
        raise ValueError("ビルドの作成に失敗しました。")
    connect = connect_user_builds(db, user_id=build.get("user_id"), build_id=new_build_id)
    print(f"ユーザーとビルドの接続結果: {connect}")
    new_build = get_build(db, build_id=new_build_id)
    print(f"DB操作結果: {new_build}")

    return result

def get_build(db: Session, build_id: int):
    sql = text(
        """
        SELECT * FROM build WHERE id = :build_id
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"build_id": build_id}).mappings().first()
    print(f"DB操作結果: {result}")

    return result

def get_os(db: Session):
    sql = text(
        """
        SELECT * FROM products
        WHERE products.category = 'OS'
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作結果: {result}")

    return result

def connect_user_builds(db: Session, user_id: int, build_id: int):
    sql = text(
        """
        INSERT INTO user_builds(userid, buildid) VALUES(:user_id, :build_id)
        """
    )

    params = {
        "user_id": user_id,
        "build_id": build_id
    }

    print(f"SQL: {sql}")
    result = db.execute(sql, params)
    db.commit()
    print(f"DB操作結果: {result}")

    return result

def get_user_builds(db: Session, user_id: int):
    sql = text(
        """
        SELECT b.* FROM build b
        INNER JOIN user_builds ub ON b.id = ub.buildid
        WHERE ub.userid = :user_id
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"user_id": user_id}).mappings().all()
    print(f"DB操作結果: {result}")

    return result
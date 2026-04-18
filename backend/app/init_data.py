from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.alert import Alert
from app.core.security import hash_password

# 自动建表
Base.metadata.create_all(bind=engine)

ALERT_SEED_DATA = [
    {"alert_type": "台风", "level": "蓝", "criteria": "预计未来24小时内可能或者已经受热带气旋影响，沿海或者陆地平均风力达6级以上，或者阵风8级以上并可能持续。", "response_guide": "停止露天集体活动和高空等户外危险作业；加固门窗、围板、棚架、广告牌等易被风吹动的搭建物。"},
    {"alert_type": "台风", "level": "黄", "criteria": "预计未来24小时内可能或者已经受热带气旋影响，沿海或者陆地平均风力达8级以上，或者阵风10级以上并可能持续。", "response_guide": "停止室内外大型集会和高空等户外危险作业；加固港口设施，防止船舶走锚、搁浅和碰撞。"},
    {"alert_type": "台风", "level": "橙", "criteria": "预计未来12小时内可能或者已经受热带气旋影响，沿海或者陆地平均风力达10级以上，或者阵风12级以上并可能持续。", "response_guide": "停止集会、停课、停业（除特殊行业外）；回港避风的船舶要视情况采取积极措施，妥善安排人员留守或者转移到安全地带。"},
    {"alert_type": "台风", "level": "红", "criteria": "预计未来6小时内可能或者已经受热带气旋影响，沿海或者陆地平均风力达12级以上，或者阵风14级以上并可能持续。", "response_guide": "停止集会、停课、停业（除特殊行业外）；人员应尽可能待在防风安全的地方，当台风中心经过时风力会减小或者静止一段时间，切记强风将会突然吹袭，应当继续留在安全处避风。"},
    {"alert_type": "暴雨", "level": "蓝", "criteria": "预计未来12小时内降雨量将达50毫米以上，或者已达50毫米以上且降雨可能持续。", "response_guide": "驾驶人员应当注意道路积水和交通阻塞，确保安全；检查城市、农田、鱼塘排水系统，做好排涝准备。"},
    {"alert_type": "暴雨", "level": "黄", "criteria": "预计未来6小时内降雨量将达50毫米以上，或者已达50毫米以上且降雨可能持续。", "response_guide": "交通管理部门应当根据路况在强降雨路段采取交通管制措施，在积水路段实行交通引导；切断低洼地带有危险的室外电源，暂停在空旷地方的户外作业，转移危险地带人员和危房居民到安全场所避雨。"},
    {"alert_type": "暴雨", "level": "橙", "criteria": "预计未来3小时内降雨量将达50毫米以上，或者已达50毫米以上且降雨可能持续。", "response_guide": "切断有危险的室外电源，暂停户外作业；处于危险地带的单位应当停课、停业，采取专门措施保护已到校学生、幼儿和其他上班人员的安全；做好城市、农田的排涝，注意防范可能引发的山洪、滑坡、泥石流等灾害。"},
    {"alert_type": "暴雨", "level": "红", "criteria": "预计未来3小时内降雨量将达100毫米以上，或者已达100毫米以上且降雨可能持续。", "response_guide": "停止集会、停课、停业（除特殊行业外）；做好山洪、滑坡、泥石流等灾害的防御和抢险工作。"},
    {"alert_type": "高温", "level": "黄", "criteria": "连续三天日最高气温将在35℃以上。", "response_guide": "有关部门和单位按照职责做好防暑降温准备工作；午后尽量减少户外活动；对老、弱、病、幼人群提供防暑降温指导。"},
    {"alert_type": "高温", "level": "橙", "criteria": "24小时内最高气温将升至37℃以上。", "response_guide": "有关部门和单位按照职责落实防暑降温保障措施；尽量避免在高温时段进行户外活动，高温条件下作业的人员应当缩短连续工作时间。"},
    {"alert_type": "高温", "level": "红", "criteria": "24小时内最高气温将升至40℃以上。", "response_guide": "有关部门和单位按照职责采取防暑降温应急措施；停止户外露天作业（除特殊行业外）；对老、弱、病、幼人群采取保护措施。"},
]

def init_db():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if not existing:
            user = User(
                username="admin",
                password_hash=hash_password("admin123"),
            )
            db.add(user)
            db.commit()
            print("Default user created: admin / admin123")
        else:
            print("Default user already exists")

        alert_count = db.query(Alert).count()
        if alert_count == 0:
            for data in ALERT_SEED_DATA:
                alert = Alert(**data)
                db.add(alert)
            db.commit()
            print(f"Inserted {len(ALERT_SEED_DATA)} alert records")
        else:
            print(f"Alerts already exist ({alert_count} records)")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

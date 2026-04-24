from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.alert import Alert
from app.models.term import Term
from app.core.security import hash_password

# 自动建表
Base.metadata.create_all(bind=engine)

TERM_SEED_DATA = [
    {"term": "副热带高压", "category": "天气系统", "definition": "位于副热带地区的暖性高压系统，是影响我国夏季天气的重要天气系统，其位置和强度变化直接影响雨带分布和台风路径。", "source": "中国气象局"},
    {"term": "锋面", "category": "天气系统", "definition": "两种不同性质气团（如冷暖气团）之间的过渡地带，锋面附近常伴有云、雨、大风等天气现象。", "source": "中国气象局"},
    {"term": "台风", "category": "灾害性天气", "definition": "发生在热带或副热带洋面上的强烈气旋性涡旋，中心附近最大风力达12级或以上，常伴有暴雨、风暴潮等灾害。", "source": "中国气象局"},
    {"term": "暴雨", "category": "灾害性天气", "definition": "指24小时内降水量达50毫米以上的降雨天气过程，可能引发洪涝、山洪、泥石流等次生灾害。", "source": "中国气象局"},
    {"term": "寒潮", "category": "灾害性天气", "definition": "指来自高纬度地区的强冷空气迅速入侵，造成大范围剧烈降温的天气过程，24小时内降温幅度达8℃以上。", "source": "中国气象局"},
    {"term": "相对湿度", "category": "气象要素", "definition": "空气中实际水汽压与同温度下饱和水汽压的百分比，反映空气的潮湿程度，对人体舒适度和农业生产有重要影响。", "source": "中国气象局"},
    {"term": "能见度", "category": "气象要素", "definition": "视力正常的人在当时天气条件下，能够从天空背景中看到和辨认出目标物的最大水平距离，单位通常为米或公里。", "source": "中国气象局"},
    {"term": "强对流", "category": "灾害性天气", "definition": "指发生突然、移动迅速、天气剧烈、破坏力强的灾害性天气，包括雷暴、短时强降水、冰雹、雷雨大风、龙卷风等。", "source": "中国气象局"},
    {"term": "厄尔尼诺", "category": "气候现象", "definition": "赤道太平洋中东段海水温度异常升高的现象，可引起全球大气环流异常，对全球气候产生显著影响。", "source": "中国气象局"},
    {"term": "拉尼娜", "category": "气候现象", "definition": "赤道太平洋中东段海水温度异常降低的现象，与厄尔尼诺相反，同样会对全球气候产生重要影响。", "source": "中国气象局"},
]

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

        term_count = db.query(Term).count()
        if term_count == 0:
            for data in TERM_SEED_DATA:
                term = Term(**data)
                db.add(term)
            db.commit()
            print(f"Inserted {len(TERM_SEED_DATA)} term records")
        else:
            print(f"Terms already exist ({term_count} records)")

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

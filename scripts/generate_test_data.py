"""生成测试数据脚本"""

import argparse
import random
from datetime import datetime, timedelta

from loguru import logger

from augur_common import logging
from augur_common.db.init_db import create_all_tables
from augur_common.db.models import (
    Entity,
    Lead,
    Pipeline,
    PipelineState,
    RawSignal,
    Relation,
    RelationType,
)
from augur_common.db.models.base import SyncSessionLocal


def generate_leads(count: int = 10) -> list[Lead]:
    """生成测试线索"""
    session = SyncSessionLocal()
    leads = []

    regions = ["china", "europe", "north_america", "mea", "sea", "india"]
    countries = ["中国", "美国", "德国", "日本", "澳大利亚"]
    stages = ["exploration", "feasibility", "tender", "epc", "operation"]
    priorities = ["critical", "high", "medium", "low"]
    statuses = ["new", "reviewing", "accepted", "rejected"]
    technologies = ["锂电池储能", "液流电池", "压缩空气储能", "抽水蓄能", "钠离子电池", "飞轮储能"]

    companies = [
        "阳光电源",
        "宁德时代",
        "比亚迪",
        "隆基绿能",
        "通威股份",
        "华为数字能源",
        "亿纬锂能",
        "中创新航",
        "国轩高科",
        "欣旺达",
    ]

    for i in range(count):
        lead = Lead(
            name=f"{random.choice(regions)} {random.choice(['光伏', '风电', '储能'])}项目 {datetime.now().strftime('%Y%m%d')}-{i + 1}",
            summary=f"这是一个{random.choice(technologies)}项目，预计投资{random.randint(1, 50)}亿元。",
            description=f"项目位于{random.choice(regions)}，总容量{random.randint(100, 1000)}MW/{random.randint(200, 2000)}MWh。",
            type="项目商机",
            source="https://test",
            raw_file="",
            region=random.choice(regions),
            country=random.choice(countries),
            stage=random.choice(stages),
            estimated_value_mw=random.uniform(100, 1000),
            estimated_value_mwh=random.uniform(200, 2000),
            estimated_value_usd=random.uniform(1e8, 5e8),
            technology=random.choice(technologies),
            timing_window=f"{datetime.now().year}-{datetime.now().year + 2}",
            published_at=(datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            developers={"primary": random.choice(companies), "partners": random.sample(companies, k=2)},
            priority=random.choice(priorities),
            overall_score=random.uniform(50, 100),
            status=random.choice(statuses),
        )
        lead.create()
        leads.append(lead)

    session.commit()
    logger.info(f"Generated {count} leads")
    return leads


def generate_entities(count: int = 20) -> list[Entity]:
    """生成测试实体"""
    session = SyncSessionLocal()
    entities = []

    entity_types = ["company", "government", "project", "technology"]
    sectors = ["设备商", "开发商", "运营商", "政府", "研究机构"]

    names = [
        "国家能源局",
        "内蒙古自治区能源局",
        "阳光电源股份有限公司",
        "隆基绿能科技股份有限公司",
        "宁德时代新能源科技股份有限公司",
        "比亚迪股份有限公司",
        "华为技术有限公司",
        "中国电力科学研究院",
        "华北电力设计院",
        "浙江省能源集团",
        "广东省能源集团",
        "国家电投",
        "华能集团",
        "华电集团",
        "大唐集团",
        "三峡集团",
        "国能集团",
        "中核集团",
        "中电建",
        "中能建",
    ]

    for i in range(min(count, len(names))):
        entity = Entity(
            name=names[i],
            type=entity_types[i % len(entity_types)],
            aliases={"short": names[i][:4], "en": f"EN_{names[i]}"},
            attributes={"sector": random.choice(sectors)},
            tags={"sector": random.choice(sectors)},
            confidence=random.uniform(0.7, 1.0),
            source_count=random.randint(1, 10),
            first_seen_at=datetime.now() - timedelta(days=random.randint(1, 90)),
            last_seen_at=datetime.now() - timedelta(days=random.randint(0, 10)),
        )
        entity.create()
        entities.append(entity)

    session.commit()
    logger.info(f"Generated {len(entities)} entities")
    return entities


def generate_relations(entities: list[Entity], count: int = 10) -> list[Relation]:
    """生成测试关系"""
    if len(entities) < 2:
        logger.warning("Not enough entities to create relations")
        return []

    session = SyncSessionLocal()
    relations = []

    relation_types = [
        RelationType.OWNS,
        RelationType.LOCATED_IN,
        RelationType.AFFECTS,
        RelationType.HAS_DECISION_MAKER,
        RelationType.DEPENDS_ON,
        RelationType.SUPPLIES,
    ]

    for i in range(count):
        src = random.choice(entities)
        dst = random.choice(entities)
        if src.id == dst.id:
            continue

        relation = Relation(
            relation_type=random.choice(relation_types),
            source_entity_id=src.id,
            source_entity_name=src.name,
            source_entity_type=src.type,
            target_entity_id=dst.id,
            target_entity_name=dst.name,
            target_entity_type=dst.type,
            properties={"test": True},
            confidence=random.uniform(0.6, 1.0),
        )
        relation.create()
        relations.append(relation)

    session.commit()
    logger.info(f"Generated {len(relations)} relations")
    return relations


def generate_raw_signals(count: int = 20) -> list[RawSignal]:
    """生成测试原始信号"""
    session = SyncSessionLocal()
    signals = []

    sources = ["policy_gov", "enterprise_tender", "capital_financing", "grid_announcement"]
    families = ["policy", "project", "capital", "technology"]
    statuses = ["pending", "processed", "failed"]

    titles = [
        "国家能源局发布新能源发展指导意见",
        "某省发布储能项目招标公告",
        "某公司完成新一轮融资",
        "电网公司发布储能调峰调频项目",
        "光伏组件价格持续下降",
        "锂电池原材料价格波动",
        "新型储能技术取得突破",
        "电力市场化改革持续推进",
    ]

    for i in range(count):
        signal = RawSignal(
            source=random.choice(sources),
            url=f"https://example.com/signal/{i + 1}",
            raw_text=f"这是第{i + 1}条原始信号内容，{random.choice(titles)}。",
            title=random.choice(titles),
            family=random.choice(families),
            lifecycle_stage="published",
            source_domain="example.com",
            source_adapter="TestAdapter",
            collected_at=datetime.now() - timedelta(days=random.randint(1, 30)),
            processed_at=datetime.now() - timedelta(days=random.randint(0, 5)) if random.random() > 0.3 else None,
            status=random.choice(statuses),
        )
        signal.create()
        signals.append(signal)

    session.commit()
    logger.info(f"Generated {count} raw signals")
    return signals


def generate_pipeline_states() -> list[PipelineState]:
    """生成测试流水线状态"""
    session = SyncSessionLocal()
    states = []

    pipelines = [Pipeline.NLP, Pipeline.KNOWLEDGE_GRAPH, Pipeline.REASONING]

    for pipeline in pipelines:
        state = PipelineState(
            pipeline=pipeline,
            file_path=f"/data/test/{pipeline}_{datetime.now().strftime('%Y%m%d')}.parquet",
            processed_at=datetime.now() - timedelta(hours=random.randint(1, 48)),
        )
        state.create()
        states.append(state)

    session.commit()
    logger.info(f"Generated {len(states)} pipeline states")
    return states


def generate_test_data(
    leads_count: int = 10,
    entities_count: int = 20,
    relations_count: int = 10,
    signals_count: int = 20,
    reset: bool = False,
):
    """生成所有测试数据"""

    create_all_tables()

    if reset:
        logger.warning("正在清空所有表数据...")
        with SyncSessionLocal() as session:
            # 按依赖关系逆序删除
            session.query(PipelineState).delete()
            session.query(Relation).delete()
            session.query(Entity).delete()
            session.query(Lead).delete()
            session.query(RawSignal).delete()
            session.commit()
        logger.info("所有表数据已清空")

    logger.info("Starting test data generation...")

    entities = generate_entities(entities_count)
    leads = generate_leads(leads_count)
    generate_relations(entities, relations_count)
    generate_raw_signals(signals_count)
    generate_pipeline_states()

    logger.info("Test data generation completed!")


def main():
    parser = argparse.ArgumentParser(description="AUGUR 生成测试数据")
    parser.add_argument("--leads", type=int, default=10, help="线索数量")
    parser.add_argument("--entities", type=int, default=20, help="实体数量")
    parser.add_argument("--relations", type=int, default=10, help="关系数量")
    parser.add_argument("--signals", type=int, default=20, help="信号数量")
    parser.add_argument("--reset", action="store_true", help="清空所有表数据后再生成")
    args = parser.parse_args()

    logging.setup_logging()
    generate_test_data(
        leads_count=args.leads,
        entities_count=args.entities,
        relations_count=args.relations,
        signals_count=args.signals,
        reset=args.reset,
    )


if __name__ == "__main__":
    main()

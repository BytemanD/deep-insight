"""生成商机洞察测试数据"""

import uuid

from augur_common.db import models


def generate_opportunities():
    """生成商机测试数据"""
    opportunities = [
        {
            "title": "欧洲大型储能项目招标",
            "description": "德国某能源公司计划建设200MWh电网级储能系统，预计投资5000万欧元，目前处于招标前期阶段。",
            "analyse": "通过分析德国能源政策、电网负荷数据及该公司历史项目，发现其在可再生能源领域的扩张战略与储能需求高度匹配。近期发布的招标公告显示明确的技术规格要求。",
        },
        {
            "title": "东南亚微电网储能机会",
            "description": "印尼群岛地区微电网建设项目，需要分布式储能解决方案，总容量约50MWh。",
            "analyse": "印尼政府推动岛屿电气化计划，结合当地太阳能资源丰富但电网覆盖不足的特点，微电网+储能是最佳解决方案。已有多家本地开发商表达合作意向。",
        },
        {
            "title": "北美工商业储能市场",
            "description": "美国加州多个工业园区寻求峰谷套利储能方案，单个项目规模10-30MWh。",
            "analyse": "加州电价差扩大至$0.3/kWh以上，工商业用户安装储能的经济性显著提升。通过分析园区用电负荷曲线，ROI可达15-20%。",
        },
        {
            "title": "中东离网储能项目",
            "description": "沙特偏远地区通信基站备用电源项目，需要高可靠性储能系统。",
            "analyse": "中东地区高温环境对电池性能提出特殊要求。该项目预算充足，且后续有规模化复制潜力，预计三年内可拓展至500个站点。",
        },
        {
            "title": "中国户用储能出口机会",
            "description": "欧洲户用储能市场需求爆发，国内多家厂商寻求渠道合作。",
            "analyse": "欧洲能源危机推动户用储能渗透率从5%提升至25%。通过跨境电商和本地经销商双渠道策略，可快速占领市场份额。",
        },
    ]

    created_opportunities = []
    for opp_data in opportunities:
        opportunity = models.Opportunity(
            title=opp_data["title"],
            description=opp_data["description"],
            analyse=opp_data["analyse"],
        )
        opportunity.create()
        created_opportunities.append(opportunity)

    return created_opportunities


def generate_evidences(opportunities):
    """生成证据测试数据"""
    # 先获取一些现有的线索UUID
    existing_leads = models.Lead.query().limit(20).all()
    lead_uuids = [lead.uuid for lead in existing_leads] if existing_leads else []

    # 如果没有现有线索，生成一些假的UUID
    if not lead_uuids:
        lead_uuids = [str(uuid.uuid4()) for _ in range(10)]

    evidences_data = [
        # 商机1的证据
        {
            "opportunity_idx": 0,
            "lead_idx": 0,
            "reason": "德国联邦网络局发布最新储能补贴政策，明确支持200MWh以上项目",
            "confidence": 0.92,
        },
        {"opportunity_idx": 0, "lead_idx": 1, "reason": "目标公司Q3财报显示储能业务预算增加40%", "confidence": 0.85},
        {
            "opportunity_idx": 0,
            "lead_idx": 2,
            "reason": "行业报告显示该地区储能项目平均中标价格为€250/kWh",
            "confidence": 0.78,
        },
        # 商机2的证据
        {"opportunity_idx": 1, "lead_idx": 3, "reason": "印尼能矿部发布岛屿电气化三年规划", "confidence": 0.88},
        {"opportunity_idx": 1, "lead_idx": 4, "reason": "当地合作伙伴提供的项目可行性报告", "confidence": 0.82},
        # 商机3的证据
        {"opportunity_idx": 2, "lead_idx": 5, "reason": "加州CPUC最新电价结构调整方案", "confidence": 0.90},
        {"opportunity_idx": 2, "lead_idx": 6, "reason": "工业园区管理委员会公开招标文件", "confidence": 0.87},
        {"opportunity_idx": 2, "lead_idx": 7, "reason": "竞品分析显示同类项目IRR达18%", "confidence": 0.75},
        # 商机4的证据
        {"opportunity_idx": 3, "lead_idx": 8, "reason": "沙特NEOM新城项目配套基础设施规划", "confidence": 0.85},
        {"opportunity_idx": 3, "lead_idx": 9, "reason": "高温环境下电池性能测试报告", "confidence": 0.80},
        # 商机5的证据
        {
            "opportunity_idx": 4,
            "lead_idx": 10,
            "reason": "欧洲海关数据显示户用储能进口量同比增长300%",
            "confidence": 0.93,
        },
        {"opportunity_idx": 4, "lead_idx": 11, "reason": "主要竞争对手已在德国建立本地仓库", "confidence": 0.88},
        {"opportunity_idx": 4, "lead_idx": 12, "reason": "电商平台储能产品搜索热度指数", "confidence": 0.82},
    ]

    for ev_data in evidences_data:
        evidence = models.Evidence(
            opportunity_uuid=opportunities[ev_data["opportunity_idx"]].uuid,
            lead_uuid=lead_uuids[ev_data["lead_idx"] % len(lead_uuids)],
            reason=ev_data["reason"],
            confidence=ev_data["confidence"],
        )
        evidence.create()


if __name__ == "__main__":
    print("开始生成商机洞察测试数据...")

    # 生成商机
    opportunities = generate_opportunities()
    print(f"✓ 生成 {len(opportunities)} 个商机")

    # 生成证据
    generate_evidences(opportunities)
    print("✓ 生成相关证据")

    print("\n测试数据生成完成！")

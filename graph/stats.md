# 知识图谱统计（v0）

- 数据源: eicd_anon.db（脱敏库）
- 节点总数: **210,640**
- 关系总数: **401,938**

## 节点分类型

| 类型 | 数量 |
|---|---|
| ChangeEvent | 81,093 |
| Pin | 41,786 |
| SignalEndpoint | 40,270 |
| Signal | 18,445 |
| InterconnectPin | 6,996 |
| ApprovalEvent | 6,798 |
| Connector | 4,539 |
| ArrangementPosition | 4,287 |
| Wire | 1,899 |
| Device | 1,851 |
| SignalGroup | 1,733 |
| Arrangement | 204 |
| Interconnect | 171 |
| Person | 133 |
| ATASubsystem | 102 |
| SignalGroupType | 100 |
| Harness | 67 |
| Subregion | 42 |
| PowerSource | 40 |
| EDZ | 39 |
| ATAChapter | 18 |
| Region | 12 |
| GroundClass | 9 |
| Project | 6 |

## 关系分类型

| 类型 | 数量 |
|---|---|
| CHANGED_BY | 81,093 |
| CHANGED | 43,348 |
| HAS_PIN | 41,786 |
| AT_DEVICE | 40,270 |
| HAS_ENDPOINT | 40,270 |
| AT_PIN | 40,269 |
| SIGNAL_EDGE | 23,864 |
| POWERED_BY | 18,443 |
| SIGNAL_OF_SYSTEM | 18,238 |
| HAS_ICPIN | 6,996 |
| APPROVAL_FOR | 6,029 |
| REQUESTED_BY | 5,916 |
| IN_GROUP | 4,591 |
| HAS_CONNECTOR | 4,539 |
| HAS_POSITION | 4,287 |
| THROUGH_PAIR | 3,433 |
| GROUNDED_AS | 3,336 |
| IN_HARNESS | 1,899 |
| HAS_DEVICE | 1,851 |
| BELONGS_TO_SYSTEM | 1,821 |
| PART_OF_CHAPTER | 1,821 |
| GROUP_RULE | 1,733 |
| IMPLEMENTS | 1,702 |
| END_AT_ICPIN | 1,666 |
| END_AT_PIN | 1,466 |
| RESPONSIBLE_FOR | 562 |
| LOCATED_IN_EDZ | 539 |
| HARNESS_OF | 67 |
| HAS_SUBREGION | 42 |
| USES_ARRANGEMENT | 39 |
| IC_GROUND_CLASS | 22 |

## 完整性说明

以下悬挂边在输出前被丢弃（目标实体已从库中删除，属正常历史演进；ChangeEvent/ApprovalEvent 节点自身保留 entity_table/entity_id 供追溯）：

- CHANGED: 37,647 条
- APPROVAL_FOR: 767 条
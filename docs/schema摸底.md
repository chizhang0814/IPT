# eicd.db schema 摸底（快照 2026-08-12，49 表）

## aircraft_device_list  (3046 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| object_identifier | TEXT | 0 | None | 0 |
| 系统名称 | TEXT | 0 | None | 0 |
| object_text | TEXT | 0 | None | 0 |
| 设备编号_DOORS | TEXT | 0 | None | 0 |
| LIN号_DOORS | TEXT | 0 | None | 0 |
| 设备布置区域 | TEXT | 0 | None | 0 |
| 飞机构型 | TEXT | 0 | None | 0 |
| 是否有供应商数模 | TEXT | 0 | None | 0 |
| 是否已布置在样机 | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| 电设备编号 | TEXT | 0 | '-' | 0 |
| 是否有EICD | TEXT | 0 | '-' | 0 |
| 是否确认设备选型 | TEXT | 0 | '-' | 0 |
| 是否已确认MICD | TEXT | 0 | '-' | 0 |
| 模型成熟度 | TEXT | 0 | '-' | 0 |
| 是否是用电设备 | TEXT | 0 | '-' | 0 |
| 类型 | TEXT | 0 | '-' | 0 |

FK: project_id→projects.id

## approval_items  (22829 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| approval_request_id | INTEGER | 1 | None | 0 |
| recipient_username | TEXT | 1 | None | 0 |
| item_type | TEXT | 1 | 'approval' | 0 |
| status | TEXT | 1 | 'pending' | 0 |
| edited_payload | TEXT | 0 | None | 0 |
| rejection_reason | TEXT | 0 | None | 0 |
| responded_at | DATETIME | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: approval_request_id→approval_requests.id

## approval_requests  (6798 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| requester_id | INTEGER | 1 | None | 0 |
| requester_username | TEXT | 1 | None | 0 |
| action_type | TEXT | 1 | None | 0 |
| entity_type | TEXT | 1 | None | 0 |
| entity_id | INTEGER | 0 | None | 0 |
| device_id | INTEGER | 0 | None | 0 |
| payload | TEXT | 1 | None | 0 |
| status | TEXT | 1 | 'pending' | 0 |
| rejection_reason | TEXT | 0 | None | 0 |
| reviewed_by_username | TEXT | 0 | None | 0 |
| reviewed_at | DATETIME | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| old_payload | TEXT | 0 | None | 0 |
| current_phase | TEXT | 1 | 'approval' | 0 |
| rejected_by_username | TEXT | 0 | None | 0 |
| rejected_at | DATETIME | 0 | None | 0 |

FK: requester_id→users.id; project_id→projects.id

## arrangement_code_overrides  (105 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| source_path | TEXT | 0 | None | 1 |
| original_crop_code | TEXT | 1 | None | 0 |
| override_crop_code | TEXT | 1 | None | 0 |
| set_by | TEXT | 0 | None | 0 |
| set_at | REAL | 1 | strftime('%s','now') | 0 |
| note | TEXT | 0 | None | 0 |

## arrangement_edit_logs  (1 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| batch_id | TEXT | 1 | None | 0 |
| arrangement_code | TEXT | 1 | None | 0 |
| edited_by | TEXT | 1 | None | 0 |
| note | TEXT | 0 | None | 0 |
| rows_json | TEXT | 1 | None | 0 |
| created_at | REAL | 1 | strftime('%s','now') | 0 |

## arrangement_positions  (4287 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| arrangement_code | TEXT | 1 | None | 1 |
| label | TEXT | 1 | None | 2 |
| position_index | INTEGER | 1 | None | 0 |
| x_mm | REAL | 0 | None | 0 |
| y_mm | REAL | 0 | None | 0 |
| normalized_x | REAL | 0 | None | 0 |
| normalized_y | REAL | 0 | None | 0 |
| polar_r | REAL | 0 | None | 0 |
| polar_theta | REAL | 0 | None | 0 |
| contact_raw | TEXT | 0 | None | 0 |
| contact_std | TEXT | 0 | None | 0 |
| contact_radius | REAL | 0 | None | 0 |
| template_id | INTEGER | 0 | None | 0 |
| is_special | INTEGER | 0 | 0 | 0 |

FK: arrangement_code→arrangements.arrangement_code

## arrangement_review_decisions  (208 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| crop_code | TEXT | 0 | None | 1 |
| decision_json | TEXT | 1 | None | 0 |
| status | TEXT | 1 | 'pending' | 0 |
| decided_by | TEXT | 0 | None | 0 |
| decided_at | REAL | 0 | None | 0 |
| imported_at | REAL | 0 | None | 0 |
| notes | TEXT | 0 | None | 0 |
| updated_at | REAL | 1 | strftime('%s','now') | 0 |

## arrangement_sources  (209 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| arrangement_code | TEXT | 1 | None | 0 |
| source | TEXT | 1 | None | 0 |
| method | TEXT | 1 | None | 0 |
| contributes | TEXT | 0 | None | 0 |
| source_pdf | TEXT | 0 | None | 0 |
| source_page | INTEGER | 0 | None | 0 |
| source_path | TEXT | 0 | None | 0 |
| reviewer | TEXT | 0 | None | 0 |
| reviewed_at | REAL | 0 | None | 0 |
| annotation_version | INTEGER | 0 | None | 0 |
| raw_json | TEXT | 0 | None | 0 |
| imported_at | REAL | 1 | strftime('%s','now') | 0 |

FK: arrangement_code→arrangements.arrangement_code

## arrangements  (204 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| arrangement_code | TEXT | 0 | None | 1 |
| shell_size | INTEGER | 0 | None | 0 |
| shell_letter | TEXT | 0 | None | 0 |
| arrangement_number | TEXT | 0 | None | 0 |
| family | TEXT | 0 | None | 0 |
| total_contacts | INTEGER | 1 | None | 0 |
| contact_distribution | TEXT | 0 | None | 0 |
| data_quality | TEXT | 0 | None | 0 |
| imported_at | REAL | 1 | strftime('%s','now') | 0 |
| updated_at | REAL | 1 | strftime('%s','now') | 0 |

## change_logs  (81093 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| data_id | INTEGER | 1 | None | 0 |
| table_name | TEXT | 1 | 'eicd_data' | 0 |
| changed_by | INTEGER | 1 | None | 0 |
| old_values | TEXT | 0 | None | 0 |
| new_values | TEXT | 0 | None | 0 |
| reason | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'pending' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| entity_table | TEXT | 0 | None | 0 |
| entity_id | INTEGER | 0 | None | 0 |
| batch_id | TEXT | 0 | None | 0 |

FK: changed_by→users.id

## chat_messages  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| session_id | INTEGER | 1 | None | 0 |
| role | TEXT | 1 | None | 0 |
| content_json | TEXT | 1 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: session_id→chat_sessions.id

## chat_sessions  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| username | TEXT | 1 | None | 0 |
| title | TEXT | 0 | None | 0 |
| project_id | INTEGER | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

## connectors  (4539 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| device_id | INTEGER | 1 | None | 0 |
| 设备端元器件编号 | TEXT | 1 | None | 0 |
| 设备端元器件名称及类型 | TEXT | 0 | None | 0 |
| 设备端元器件件号类型及件号 | TEXT | 0 | None | 0 |
| 设备端元器件供应商名称 | TEXT | 0 | None | 0 |
| 匹配的线束端元器件件号 | TEXT | 0 | None | 0 |
| 匹配的线束线型 | TEXT | 0 | None | 0 |
| 设备端元器件匹配的元器件是否随设备交付 | TEXT | 0 | None | 0 |
| 备注 | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| import_conflicts | TEXT | 0 | None | 0 |
| validation_errors | TEXT | 0 | None | 0 |
| 导入来源 | TEXT | 0 | None | 0 |
| version | INTEGER | 1 | 1 | 0 |
| 尾附件件号 | TEXT | 0 | None | 0 |
| 触件型号 | TEXT | 0 | None | 0 |
| import_status | TEXT | 0 | None | 0 |

FK: device_id→devices.id

## devices  (1851 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| 设备编号 | TEXT | 1 | None | 0 |
| 设备中文名称 | TEXT | 0 | None | 0 |
| 设备英文名称 | TEXT | 0 | None | 0 |
| 设备英文缩写 | TEXT | 0 | None | 0 |
| 设备供应商件号 | TEXT | 0 | None | 0 |
| 设备供应商名称 | TEXT | 0 | None | 0 |
| 设备部件所属系统（4位ATA） | TEXT | 0 | None | 0 |
| 设备安装位置 | TEXT | 0 | None | 0 |
| 设备DAL | TEXT | 0 | None | 0 |
| 设备壳体是否金属 | TEXT | 0 | None | 0 |
| 金属壳体表面是否经过特殊处理而不易导电 | TEXT | 0 | None | 0 |
| 设备内共地情况 | TEXT | 0 | None | 0 |
| 设备壳体接地方式 | TEXT | 0 | None | 0 |
| 壳体接地是否故障电流路径 | TEXT | 0 | None | 0 |
| 其他接地特殊要求 | TEXT | 0 | None | 0 |
| 设备端连接器或接线柱数量 | TEXT | 0 | None | 0 |
| 是否为选装设备 | TEXT | 0 | None | 0 |
| 是否有特殊布线需求 | TEXT | 0 | None | 0 |
| 设备装机架次 | TEXT | 0 | None | 0 |
| 设备负责人 | TEXT | 0 | None | 0 |
| 设备正常工作电压范围（V） | TEXT | 0 | None | 0 |
| 设备物理特性 | TEXT | 0 | None | 0 |
| 备注 | TEXT | 0 | None | 0 |
| 导入来源 | TEXT | 0 | None | 0 |
| created_by | TEXT | 0 | None | 0 |
| 设备编号（DOORS） | TEXT | 0 | None | 0 |
| 设备LIN号（DOORS） | TEXT | 1 | None | 0 |
| 设备装机构型 | TEXT | 0 | None | 0 |
| import_conflicts | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| validation_errors | TEXT | 0 | None | 0 |
| version | INTEGER | 0 | 1 | 0 |
| import_status | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| 设备等级 | TEXT | 0 | None | 0 |
| EDZ | TEXT | 0 | None | 0 |

FK: project_id→projects.id

## edit_locks  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| table_name | TEXT | 1 | None | 0 |
| row_id | INTEGER | 1 | None | 0 |
| locked_by | INTEGER | 1 | None | 0 |
| locked_by_name | TEXT | 1 | None | 0 |
| locked_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| expires_at | DATETIME | 1 | None | 0 |

FK: locked_by→users.id

## harness_bom_items  (219 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| harness_id | INTEGER | 1 | None | 0 |
| seq | INTEGER | 0 | None | 0 |
| item_type | TEXT | 0 | None | 0 |
| name | TEXT | 0 | None | 0 |
| user_part_no | TEXT | 0 | None | 0 |
| substitute_part_no | TEXT | 0 | None | 0 |
| material_no | TEXT | 0 | None | 0 |
| qty | TEXT | 0 | None | 0 |
| used_by | TEXT | 0 | None | 0 |
| remark | TEXT | 0 | None | 0 |
| source | TEXT | 0 | None | 0 |

FK: harness_id→harnesses.id

## harnesses  (67 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| harness_no | TEXT | 1 | None | 0 |
| alias | TEXT | 0 | None | 0 |
| zone | TEXT | 0 | None | 0 |
| user_drawing_no | TEXT | 0 | None | 0 |
| user_version | TEXT | 0 | None | 0 |
| supplier_drawing_no | TEXT | 0 | None | 0 |
| supplier_version | TEXT | 0 | None | 0 |
| tech_spec_refs | TEXT | 0 | None | 0 |
| source | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: project_id→projects.id

## ic_face_parts  (57 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| interconnect_id | INTEGER | 1 | None | 0 |
| face | TEXT | 0 | None | 0 |
| connector_model | TEXT | 0 | None | 0 |
| connector_material_no | TEXT | 0 | None | 0 |
| backshell_model | TEXT | 0 | None | 0 |
| backshell_material_no | TEXT | 0 | None | 0 |
| source | TEXT | 0 | None | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: interconnect_id→interconnects.id

## ic_types  (26 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| name | TEXT | 1 | None | 0 |
| min_pins | INTEGER | 0 | 0 | 0 |
| max_pins | INTEGER | 0 | None | 0 |
| max_wires_per_pin | INTEGER | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: project_id→projects.id

## interconnect_pin_pairs  (3433 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| interconnect_id | INTEGER | 1 | None | 0 |
| pin_r_id | INTEGER | 1 | None | 0 |
| pin_p_id | INTEGER | 1 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: pin_p_id→interconnect_pins.id; pin_r_id→interconnect_pins.id; interconnect_id→interconnects.id

## interconnect_pins  (6996 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| interconnect_id | INTEGER | 1 | None | 0 |
| pin_num | TEXT | 1 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| sort_order | INTEGER | 0 | 0 | 0 |
| face | TEXT | 0 | None | 0 |
| contact_size | TEXT | 0 | None | 0 |
| shield_type | TEXT | 0 | None | 0 |
| signal_name | TEXT | 0 | None | 0 |
| signal_definition | TEXT | 0 | None | 0 |

FK: interconnect_id→interconnects.id

## interconnects  (171 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| label | TEXT | 1 | None | 0 |
| ic_zone | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| ic_type_id | INTEGER | 0 | None | 0 |
| sub_kind | TEXT | 0 | None | 0 |
| plate_id | TEXT | 0 | None | 0 |
| plate_idx | INTEGER | 0 | None | 0 |
| arrangement_code | TEXT | 0 | None | 0 |
| edz | TEXT | 0 | None | 0 |
| source | TEXT | 0 | None | 0 |
| stage | TEXT | 0 | None | 0 |
| ground_class | TEXT | 0 | None | 0 |

FK: project_id→projects.id; arrangement_code→arrangements.arrangement_code; ic_type_id→ic_types.id

## notifications  (31918 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| recipient_username | TEXT | 1 | None | 0 |
| type | TEXT | 1 | 'signal_deleted' | 0 |
| title | TEXT | 1 | None | 0 |
| message | TEXT | 1 | None | 0 |
| is_read | INTEGER | 1 | 0 | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| reference_id | INTEGER | 0 | None | 0 |

## permission_requests  (6 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| user_id | INTEGER | 1 | None | 0 |
| project_name | TEXT | 1 | None | 0 |
| project_role | TEXT | 1 | None | 0 |
| status | TEXT | 1 | 'pending' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| reviewed_at | DATETIME | 0 | None | 0 |
| reviewed_by | INTEGER | 0 | None | 0 |

FK: reviewed_by→users.id; user_id→users.id

## pins  (41786 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| connector_id | INTEGER | 1 | None | 0 |
| 针孔号 | TEXT | 1 | None | 0 |
| 端接尺寸 | TEXT | 0 | None | 0 |
| 备注 | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| version | INTEGER | 1 | 1 | 0 |
| 屏蔽类型 | TEXT | 0 | None | 0 |
| import_status | TEXT | 0 | None | 0 |

FK: connector_id→connectors.id

## project_configurations  (6 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| name | TEXT | 1 | None | 0 |
| description | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| seq | INTEGER | 0 | None | 0 |

FK: project_id→projects.id

## project_snapshots  (2 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| source_project_name | TEXT | 1 | None | 0 |
| snapshot_name | TEXT | 1 | None | 0 |
| description | TEXT | 0 | None | 0 |
| payload | TEXT | 1 | None | 0 |
| payload_size | INTEGER | 1 | None | 0 |
| table_counts | TEXT | 1 | None | 0 |
| created_by | TEXT | 1 | None | 0 |
| created_by_name | TEXT | 0 | None | 0 |
| created_at | TEXT | 1 | datetime('now', 'localtime') | 0 |
| schema_version | INTEGER | 1 | 1 | 0 |

## projects  (6 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| name | TEXT | 1 | None | 0 |
| description | TEXT | 0 | None | 0 |
| created_by | INTEGER | 1 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| is_snapshot_view | INTEGER | 1 | 0 | 0 |
| snapshot_source_id | INTEGER | 0 | None | 0 |
| snapshot_view_owner | TEXT | 0 | None | 0 |
| config_seq_counter | INTEGER | 0 | 0 | 0 |

FK: created_by→users.id

## regions  (12 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| region_code | INTEGER | 1 | None | 0 |
| region_name | TEXT | 1 | None | 0 |

## sc_connectors  (12 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| section_connector_id | INTEGER | 1 | None | 0 |
| 连接器号 | TEXT | 1 | None | 0 |
| 设备端元器件编号 | TEXT | 0 | None | 0 |
| 设备端元器件名称及类型 | TEXT | 0 | None | 0 |
| 设备端元器件件号类型及件号 | TEXT | 0 | None | 0 |
| 设备端元器件供应商名称 | TEXT | 0 | None | 0 |
| 匹配的线束端元器件件号 | TEXT | 0 | None | 0 |
| 匹配的线束线型 | TEXT | 0 | None | 0 |
| 设备端元器件匹配的元器件是否随设备交付 | TEXT | 0 | None | 0 |
| 备注 | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: section_connector_id→section_connectors.id

## sc_pins  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| sc_connector_id | INTEGER | 1 | None | 0 |
| 针孔号 | TEXT | 1 | None | 0 |
| 端接尺寸 | TEXT | 0 | None | 0 |
| 屏蔽类型 | TEXT | 0 | None | 0 |
| 备注 | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: sc_connector_id→sc_connectors.id

## section_connectors  (2 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| 设备名称 | TEXT | 1 | None | 0 |
| 负责人 | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: project_id→projects.id

## signal_edges  (23864 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| signal_id | INTEGER | 1 | None | 0 |
| from_endpoint_id | INTEGER | 1 | None | 0 |
| to_endpoint_id | INTEGER | 1 | None | 0 |
| direction | TEXT | 1 | 'directed' | 0 |
| source_info | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: to_endpoint_id→signal_endpoints.id; from_endpoint_id→signal_endpoints.id; signal_id→signals.id

## signal_endpoints  (40270 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| signal_id | INTEGER | 1 | None | 0 |
| device_id | INTEGER | 0 | None | 0 |
| pin_id | INTEGER | 0 | None | 0 |
| endpoint_index | INTEGER | 1 | 0 | 0 |
| 端接尺寸 | TEXT | 0 | None | 0 |
| 信号名称 | TEXT | 0 | None | 0 |
| 信号定义 | TEXT | 0 | None | 0 |
| confirmed | INTEGER | 1 | 1 | 0 |
| input | INTEGER | 1 | 0 | 0 |
| output | INTEGER | 1 | 0 | 0 |
| 备注 | TEXT | 0 | None | 0 |
| 推荐导线线规 | TEXT | 0 | None | 0 |
| 推荐导线线型 | TEXT | 0 | None | 0 |

FK: pin_id→pins.id; device_id→devices.id; signal_id→signals.id

## signal_group_types  (100 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| name | TEXT | 1 | None | 0 |
| connection_type | TEXT | 1 | None | 0 |
| prefix | TEXT | 1 | None | 0 |
| count | INTEGER | 1 | None | 0 |
| protocols | TEXT | 1 | None | 0 |
| required | TEXT | 0 | None | 0 |
| optional | TEXT | 0 | None | 0 |
| created_by | INTEGER | 0 | None | 0 |
| created_at | TEXT | 0 | datetime('now') | 0 |
| updated_at | TEXT | 0 | datetime('now') | 0 |
| color | TEXT | 0 | None | 0 |

FK: project_id→projects.id

## signals  (18445 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| unique_id | TEXT | 0 | None | 0 |
| 连接类型 | TEXT | 0 | None | 0 |
| 信号架次有效性 | TEXT | 0 | None | 0 |
| 推荐导线线规 | TEXT | 0 | None | 0 |
| 推荐导线线型 | TEXT | 0 | None | 0 |
| 独立电源代码 | TEXT | 0 | None | 0 |
| 敷设代码 | TEXT | 0 | None | 0 |
| 电磁兼容代码 | TEXT | 0 | None | 0 |
| 余度代码 | TEXT | 0 | None | 0 |
| 功能代码 | TEXT | 0 | None | 0 |
| 接地代码 | TEXT | 0 | None | 0 |
| 极性 | TEXT | 0 | None | 0 |
| 额定电压 | TEXT | 0 | None | 0 |
| 额定电流 | TEXT | 0 | None | 0 |
| 设备正常工作电压范围 | TEXT | 0 | None | 0 |
| 是否成品线 | TEXT | 0 | None | 0 |
| 成品线件号 | TEXT | 0 | None | 0 |
| 成品线线规 | TEXT | 0 | None | 0 |
| 成品线类型 | TEXT | 0 | None | 0 |
| 成品线长度 | TEXT | 0 | None | 0 |
| 成品线载流量 | TEXT | 0 | None | 0 |
| 成品线线路压降 | TEXT | 0 | None | 0 |
| 成品线标识 | TEXT | 0 | None | 0 |
| 成品线与机上线束对接方式 | TEXT | 0 | None | 0 |
| 成品线安装责任 | TEXT | 0 | None | 0 |
| 备注 | TEXT | 0 | None | 0 |
| status | TEXT | 0 | 'normal' | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| version | INTEGER | 1 | 1 | 0 |
| created_by | TEXT | 0 | None | 0 |
| 信号ATA | TEXT | 0 | None | 0 |
| import_conflicts | TEXT | 0 | None | 0 |
| import_status | TEXT | 0 | None | 0 |
| 线类型 | TEXT | 0 | None | 0 |
| 协议标识 | TEXT | 0 | None | 0 |
| signal_group | TEXT | 0 | None | 0 |
| twist_group | TEXT | 0 | None | 0 |

FK: project_id→projects.id

## sm_counter  (3 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| project_id | INTEGER | 0 | None | 1 |
| next_num | INTEGER | 1 | 1 | 0 |

FK: project_id→projects.id

## subregions  (42 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| region_id | INTEGER | 1 | None | 0 |
| subregion_code | INTEGER | 1 | None | 0 |
| subregion_name | TEXT | 1 | None | 0 |

FK: region_id→regions.id

## sysml_element_map  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| eicd_table | TEXT | 1 | None | 0 |
| eicd_row_id | INTEGER | 1 | None | 0 |
| sysml_element_id | TEXT | 1 | None | 0 |
| element_type | TEXT | 1 | None | 0 |
| element_name | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: project_id→projects.id

## sysml_sync_status  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| sysml_project_id | TEXT | 1 | None | 0 |
| last_commit_id | TEXT | 0 | None | 0 |
| last_sync_at | DATETIME | 0 | None | 0 |
| status | TEXT | 0 | 'never' | 0 |
| error_message | TEXT | 0 | None | 0 |
| data_hash | TEXT | 0 | None | 0 |

FK: project_id→projects.id

## tasks  (0 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| data_id | INTEGER | 1 | None | 0 |
| table_name | TEXT | 1 | 'eicd_data' | 0 |
| assigned_by | INTEGER | 1 | None | 0 |
| assigned_to | INTEGER | 1 | None | 0 |
| status | TEXT | 0 | 'pending' | 0 |
| notes | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| updated_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| entity_table | TEXT | 0 | None | 0 |
| entity_id | INTEGER | 0 | None | 0 |

FK: assigned_to→users.id; assigned_by→users.id

## uploaded_files  (58 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| filename | TEXT | 1 | None | 0 |
| original_filename | TEXT | 1 | None | 0 |
| table_name | TEXT | 0 | None | 0 |
| uploaded_by | INTEGER | 1 | None | 0 |
| total_rows | INTEGER | 0 | 0 | 0 |
| success_count | INTEGER | 0 | None | 0 |
| error_count | INTEGER | 0 | 0 | 0 |
| file_size | INTEGER | 0 | None | 0 |
| uploaded_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| status | TEXT | 0 | 'completed' | 0 |
| table_type | TEXT | 0 | None | 0 |
| error_details | TEXT | 0 | None | 0 |
| unmatched_cols | TEXT | 0 | None | 0 |
| color_data | TEXT | 0 | None | 0 |
| skipped_count | INTEGER | 0 | 0 | 0 |

FK: uploaded_by→users.id

## users  (98 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| username | TEXT | 1 | None | 0 |
| password | TEXT | 1 | None | 0 |
| role | TEXT | 1 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| permissions | TEXT | 0 | '[]' | 0 |
| display_name | TEXT | 0 | None | 0 |
| department | TEXT | 0 | None | 0 |
| name | TEXT | 0 | None | 0 |
| remarks | TEXT | 0 | None | 0 |
| last_project_id | INTEGER | 0 | None | 0 |

## wire_end_node_links  (1226 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| from_node_id | INTEGER | 1 | None | 0 |
| to_node_id | INTEGER | 1 | None | 0 |
| bundle_key | TEXT | 1 | '' | 0 |
| chain_terminal_face | TEXT | 0 | None | 0 |
| from_chain_face | TEXT | 0 | None | 0 |
| to_chain_face | TEXT | 0 | None | 0 |
| target_ic_pin_id | INTEGER | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |

FK: target_ic_pin_id→interconnect_pins.id; to_node_id→wire_end_nodes.id; from_node_id→wire_end_nodes.id

## wire_end_node_slots  (8813 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| node_id | INTEGER | 1 | None | 0 |
| protocol | TEXT | 1 | None | 0 |
| twist_group | TEXT | 0 | '' | 0 |
| endpoint_id | INTEGER | 0 | None | 0 |
| pin_id | INTEGER | 0 | None | 0 |
| interconnect_pin_id | INTEGER | 0 | None | 0 |
| sort_order | INTEGER | 0 | 0 | 0 |
| dead_end_pin_num | TEXT | 0 | None | 0 |
| dead_end_term_size | TEXT | 0 | None | 0 |
| wire_key | TEXT | 0 | None | 0 |

FK: interconnect_pin_id→interconnect_pins.id; pin_id→pins.id; endpoint_id→signal_endpoints.id; node_id→wire_end_nodes.id

## wire_end_nodes  (4061 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| signal_group | TEXT | 1 | None | 0 |
| project_id | INTEGER | 1 | None | 0 |
| type | TEXT | 1 | 'device' | 0 |
| device_id | INTEGER | 0 | None | 0 |
| connector_id | INTEGER | 0 | None | 0 |
| interconnect_id | INTEGER | 0 | None | 0 |
| sort_order | INTEGER | 0 | 0 | 0 |
| dead_end_label | TEXT | 0 | None | 0 |
| plane_id | INTEGER | 0 | None | 0 |
| pos_x | REAL | 0 | None | 0 |
| pos_y | REAL | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| logical_splice_node_id | INTEGER | 0 | None | 0 |
| r_face_side | TEXT | 0 | None | 0 |
| dev_side | TEXT | 0 | None | 0 |

FK: project_id→projects.id; logical_splice_node_id→wire_end_nodes.id; interconnect_id→interconnects.id; connector_id→connectors.id; device_id→devices.id

## wire_ends  (3798 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| wire_id | INTEGER | 1 | None | 0 |
| end_idx | INTEGER | 1 | None | 0 |
| kind | TEXT | 1 | None | 0 |
| pin_id | INTEGER | 0 | None | 0 |
| interconnect_pin_id | INTEGER | 0 | None | 0 |
| raw_connector | TEXT | 0 | None | 0 |
| raw_pin | TEXT | 0 | None | 0 |
| contact_part_no | TEXT | 0 | None | 0 |
| termination_method | TEXT | 0 | None | 0 |
| termination_code | TEXT | 0 | None | 0 |

FK: interconnect_pin_id→interconnect_pins.id; pin_id→pins.id; wire_id→wires.id

## wires  (1899 行)

| 列 | 类型 | 非空 | 默认 | PK |
|---|---|---|---|---|
| id | INTEGER | 0 | None | 1 |
| project_id | INTEGER | 1 | None | 0 |
| wire_no | TEXT | 1 | None | 0 |
| harness_id | INTEGER | 0 | None | 0 |
| cable_no | TEXT | 0 | None | 0 |
| is_shield | INTEGER | 1 | 0 | 0 |
| signal_id | INTEGER | 0 | None | 0 |
| gauge_awg | TEXT | 0 | None | 0 |
| wire_type | TEXT | 0 | None | 0 |
| wire_code | TEXT | 0 | None | 0 |
| color | TEXT | 0 | None | 0 |
| material_part_no | TEXT | 0 | None | 0 |
| material_ref_raw | TEXT | 0 | None | 0 |
| length_mm | REAL | 0 | None | 0 |
| lay_code | TEXT | 0 | None | 0 |
| diagram_ref | TEXT | 0 | None | 0 |
| version | TEXT | 0 | None | 0 |
| stage | TEXT | 1 | 'design' | 0 |
| remark | TEXT | 0 | None | 0 |
| source | TEXT | 0 | None | 0 |
| created_at | DATETIME | 0 | CURRENT_TIMESTAMP | 0 |
| manual_edited | INTEGER | 1 | 0 | 0 |

FK: signal_id→signals.id; harness_id→harnesses.id; project_id→projects.id


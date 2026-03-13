# SQL Bottleneck Report

**Timestamp:** 2026-03-13T05:40:30.644846+00:00

## Tabelas

| Tabela | Seq Scan | Seq Tup Read | Idx Scan | Idx Tup Fetch | Size (bytes) |
|---|---|---|---|---|---|
| energy_invoices | 7 | 0 | 0 | 0 | 1302528 |
| toll_passages | 4 | 0 | 0 | 0 | 770048 |

## Indices

| Tabela | Index | Idx Scan | Idx Tup Read | Idx Tup Fetch |
|---|---|---|---|---|
| energy_invoices | energy_invoices_pkey | 0 | 0 | 0 |
| energy_invoices | ix_energy_invoices_consumo_id | 0 | 0 | 0 |
| energy_invoices | ix_energy_invoices_cpf_titular | 0 | 0 | 0 |
| energy_invoices | ix_energy_invoices_mes_referencia | 0 | 0 | 0 |
| energy_invoices | ix_energy_invoices_status | 0 | 0 | 0 |
| energy_invoices | ix_energy_invoices_unidade_consumidora_id | 0 | 0 | 0 |
| toll_passages | ix_toll_passages_gantry_id | 0 | 0 | 0 |
| toll_passages | ix_toll_passages_occurred_at | 0 | 0 | 0 |
| toll_passages | ix_toll_passages_vehicle_did | 0 | 0 | 0 |
| toll_passages | toll_passages_pkey | 0 | 0 | 0 |
| energy_invoices | uq_energy_invoices_numero_fatura | 0 | 0 | 0 |

## Notas
- Indices com idx_scan muito baixo apos carga indicam possivel ausencia de consultas usando esses campos.
# Mini Business Requirements Document — FreightOps Analytics Platform

## 1. Business Context
Meridian Freight, a mid-size truckload carrier (~120 trucks, ~150 drivers, ~200 customers),
currently relies on manual weekly CSV exports and pivot tables for reporting. This does not
scale and leaves leadership unable to answer basic operational questions in real time
(idle assets, fuel cost drivers, safety patterns, customer-facing SLA performance).

## 2. Stakeholders
| Stakeholder | Decision they make |
|---|---|
| Dispatch / Operations Manager | Which truck/driver to assign to a load today; daily execution |
| VP of Operations / Logistics Director | Weekly/monthly trends in utilization, on-time performance, safety |
| CFO / Executive Leadership | Fleet investment, customer profitability, cost control (P&L level) |

## 3. KPIs (Success Metrics)
| KPI | Source |
|---|---|
| On-Time Delivery Rate (%) | `delivery_events.on_time_flag` |
| Fleet Utilization Rate (%) | `truck_utilization_metrics.utilization_rate` |
| Average Fuel Efficiency (MPG) | `trips.average_mpg`, `driver_monthly_metrics` |
| Maintenance Cost per Truck/Mile | `maintenance_records.total_cost` grouped by `truck_id` |
| Revenue per Mile | `loads.revenue` ÷ `trips.actual_distance_miles` (cross-table join) |

## 4. Pain Points (Quantified, Verified)
1. **Missing asset/driver assignment data:** ~2.0% of records in `trips` (driver_id, truck_id,
   trailer_id independently) and ~2.0% in `fuel_purchases` (driver_id) are null. Root-cause
   analysis (checked against year, trip_status, load_type, booking_type) found no correlating
   pattern — classified as Missing Completely At Random (MCAR), pointing to an upstream
   system/integration gap rather than a specific business process failure. Real-world next
   step: escalate to check dispatch-system/EDI source logs (not available at this data layer).
2. **Fragmented data across siloed domains:** operational, financial, safety, and maintenance
   data live in 14 separate source tables with no unified layer — an architecture/integration
   problem distinct from #1's data-quality issue.

## 5. Scope / Assumptions / Risks (v1)
- **In scope:** batch analytics on trips, loads, drivers, trucks, fuel, maintenance, safety, delivery events
- **Assumption:** production version would ingest from live dispatch/EDI/fuel-card systems (simulated here via CSV snapshots)
- **Risk:** ~2% missing IDs will require a defined handling strategy (exclude vs. impute vs. flag) before KPI calculations — to be decided in Phase 2 (Data Quality)

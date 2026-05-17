# PBPE Visualization Spec  
### Integration between MBT-Biosecurity-Engine, PBPE-Dashboard, and PBPE-Finance

---

## 1. Layering Concept

- **Layer 1 – Scientific Layer (MBT-Biosecurity-Engine)**
  - Source of biological KPIs
  - Disease, spoilage, yield, soil carbon, GHG, livestock, One Health

- **Layer 2 – Economic Layer (PBPE-Dashboard)**
  - Converts biological KPIs into economic value
  - PBPE-Biosecurity Value, Credits, Farmer Income, Price Stability

- **Layer 3 – Financial Layer (PBPE-Finance)**
  - Packages value into financial products
  - Funds, guarantees, blended finance, risk-sharing instruments

---

## 2. Data Flow

```text
[ MBT-Biosecurity-Engine ]
    ├─ Disease_Loss_Reduction
    ├─ Yield_Gain
    ├─ Anti_Spoilage
    ├─ ΔC (Soil Carbon)
    ├─ GHG_Reduction
    ├─ Livestock_Biosecurity
    └─ OneHealth_Indicators
        │
        ▼
[ PBPE-Dashboard ]
    ├─ PBPE-Biosecurity Value (USD)
    ├─ PBPE-Biosecurity Credits
    ├─ Carbon Credits
    ├─ Food Loss Credits
    ├─ Quality Credits
    └─ Farmer Income & Price Stability
        │
        ▼
[ PBPE-Finance ]
    ├─ Investment Products
    ├─ Guarantees
    ├─ Results-Based Finance
    └─ Climate & SDG Funds

---

## 3. Visualization Responsibilities

### 3.1 MBT-Biosecurity-Engine Dashboard

- Shows:
    - Biological KPIs
    - Before/After comparisons
    - Time-series of ΔC, GHG, disease, spoilage
- Does **not**:
    - Show investor portfolios
    - Manage financial products

### 3.2 PBPE-Dashboard

- Shows:
    - PBPE-Biosecurity Value (USD)
    - Credits issued per farm / region / crop
    - Farmer income uplift
    - Price stability and supply resilience
- Consumes:
    - Aggregated KPIs from MBT-Biosecurity-Engine

### 3.3 PBPE-Finance

- Shows:
    - AUM (Assets Under Management)
    - Risk/return profiles
    - Allocation by region / crop / SDG
- Consumes:
    - PBPE-Biosecurity Credits and Carbon Credits as underlying assets

---

## 4. API Contract (Conceptual)

- `GET /mbt/kpi/summary?farm_id=&season=`
    
    - Returns biological KPIs (disease, yield, ΔC, GHG, spoilage)
- `POST /pbpe/value/calculate`
    
    - Input: biological KPIs
    - Output: PBPE-Biosecurity Value, Credits
- `GET /pbpe/finance/portfolio`
    
    - Returns aggregated financial view for investors

---

## 5. Design Principle

> **MBT-Biosecurity-Engine explains “what biology is doing”.  
> PBPE-Dashboard explains “what that is worth”.  
> PBPE-Finance explains “how capital flows into it”.**

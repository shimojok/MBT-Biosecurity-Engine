<!-- ヘッダー画像 -->
<p align="center">
  <img src="https://raw.githubusercontent.com/shimojok/MBT-Biosecurity-Engine/main/docs/images/pbpe-header-jp.png" alt="PBPE Core Model Header JP" width="100%">
</p>


# MBT‑Biosecurity‑Engine  
### プラネタリーバイオセキュリティ × 再生型農業 × 気候インテリジェンス  
### PBPEハイパーサイクルの科学エンジン

---

## 🏢 Live Dashboard

PBPE ハイパーサイクルを構成する各レイヤーを、リアルタイムで体験できます。

### 🌍 MBT‑Biosecurity‑Engine – 投資家向けシナリオ・エクスプローラー  
バイオセキュリティ × 土壌健康 × 気候レジリエンス × PBPE Credits  
https://mbt-biosecurity-engine-bejnrfugexkataudf9aqwh.streamlit.app/

### 🪴 PBPE Planetary Dashboard  
Plant-Based Planet Economy – 統合フード & クライメート OS  
https://shimojok.github.io/PBPE-Dashboard/

---

## 📘 概要

MBT‑Biosecurity‑Engine は、  
**Planetary Bio‑Positive Economy（PBPE）** の科学計算レイヤーです。

MBT55 の生態系再生効果を：

- 生物学的KPI  
- 土壌炭素・GHG指標  
- 食品ロス削減  
- 家畜One‑Health改善  
- PBPE‑Biosecurity Credits  
- 気候金融価値  

へと変換します。

---

## 📄 PBPE Core Model スライド

### **英語版**
[The PBPE Core Model (EN)](./docs/slides/The_PBPE_Core_Model_en.pdf)

### **日本語版**
[PBPE コアモデル（JP）](./docs/slides/The_PBPE_Core_Model_jp.pdf)

内容：

- PBPE 二層アーキテクチャ  
- MSC（MBTサステナブルサイクル）  
- 5つの価値転換エンジン  
- ハイパーサイクル構造  
- 食料・気候・医療の構造的解決  
- 農産物取引＝排出権取引  
- 有機廃棄物 → 24時間で価値化（MBT55）  

---

## 📊 ダッシュボード機能一覧

### **1. 微生物生態系ヘルス**
- 活性指数  
- 多様性  
- 有用菌比率  
- 炭素固定  
- 窒素循環  

### **2. バイオセキュリティ・リスクマップ**
- 病原体リスク  
- 土壌病害指数  
- 気候要因リスク  
- 地域脆弱性  

### **3. MBT55 介入シミュレーター**
- 投入量  
- タイミング  
- 土壌タイプ別効果  
- 収量改善  
- 病害抑制  

### **4. 収量・経済インパクト**
- 作物別収量改善  
- コスト削減  
- 農家利益  
- 国家GDP影響  
- PBPE Credits生成量  

### **5. 気候レジリエンス**
- 干ばつ耐性  
- 洪水耐性  
- 高温ストレス耐性  
- 保水力  

### **6. 投資家シナリオ分析**
- 投資額  
- 導入面積  
- PBPE Credits  
- IRR / ROI  
- 回収期間  

### **7. 国家バイオセキュリティ指数**
- 土壌健康  
- 微生物安定性  
- 病害リスク  
- 気候脆弱性  
- 食料安全保障  

---

## 🧬 アーキテクチャ概要

```
科学エンジン → データレイヤー → ダッシュボード → PBPE統合
```

---

## 🛠 ローカル実行

```
pip install -r requirements.txt
streamlit run app.py
```

---

# 📚 PBPE関連リポジトリ & ダッシュボード一覧  
（MBT-Biosecurity-Engine と連携する上位レイヤー）

MBT-Biosecurity-Engine は PBPE-OS の **Layer1（科学・生物学的エンジン）** を担い、  
以下の PBPE関連リポジトリ（Layer2〜Layer4）にデータ・モデル・科学的裏付けを提供します。

---

## ① PBPE-Marketplace（Layer4：マーケット & レジストリ）
**リポジトリ:**  
https://github.com/shimojok/PBPE-Marketplace

**ダッシュボード:**  
- **PBPE KPIs Dashboard**  
  https://pbpe-marketplace.vercel.app/dashboard/kpis  
- **PBPE Registry Dashboard**  
  https://pbpe-marketplace.vercel.app/dashboard/registry  

**概要・特徴**  
PBPE Marketplace は PBPE-OS の **市場インフラ層（Layer4）**。  
実世界のインパクト（CO₂・土壌炭素・MBT55・健康・品質・フードロス）を  
**PBPE（Planetary Bio‑Positive Effect）という統一アセットクラス**に変換し、  
クレジット／ボンド／保険などの金融商品として流通させる。

- PBPE-UID（7桁コード）  
- PBPEレジストリ  
- PBPEレーティング  
- 40/40/20分配  
- PBPE金融商品（Carbon Income Bonds など）  
- API / Dashboard / Backend / Frontend  

---

## ② PBPE-Dashboard（Layer2：KPI可視化エンジン）
**リポジトリ:**  
https://github.com/shimojok/PBPE-Dashboard

**ダッシュボード:**  
- **PBPE Dashboard – Global KPI Explorer**  
  https://pbpe-dashboard-gmgzjs67fsgmxaju6zmrqv.streamlit.app/

**概要・特徴**  
PBPE-Dashboard は PBPE-OS の **可視化レイヤー（Layer2）**。  
MBT-Biosecurity-Engine／AGRIX／HealthBook などから得られる改善効果を  
**12のコアKPI（Disease Loss Reduction, Yield Gain, Quality Premium, ΔC, GHG Reduction など）**として可視化する。

- PBPEの経済・気候・生物学的価値を統合表示  
- PBPE-Finance／PBPE-Marketplace への入力指標を提供  
- KPIモデル（pbpe_data_model.json）を定義  

---

## ③ PBPE-Finance（Layer3：金融工学エンジン）
**リポジトリ:**  
https://github.com/shimojok/PBPE-Finance

**ダッシュボード:**  
- **PBPE Finance – Credit & Risk Modeling Dashboard**  
  https://pbpe-finance-fxvg9p5jubtrqz3dyiwufb.streamlit.app/

**概要・特徴**  
PBPE-Finance は PBPE-OS の **金融構造化レイヤー（Layer3）**。  
MBT55／AGRIX／HealthBook の改善を  
**PBPEクレジット（5種）・ボンド・ファンド**として金融商品化する。

- Triple-Ledger（Green/Blue/Gold）  
- PBPEクレジット（Biosecurity, Carbon, Food Loss, Quality, Price Stability）  
- Pricing / Risk / Portfolio モデル  
- PBPEボンド・気候ファンド・RBFモデル  

---

## ④ pbpe-mbt55-investment-engine（投資家向け：IRR/CO₂/MBT55シミュレーション）
**リポジトリ:**  
https://github.com/shimojok/pbpe-mbt55-investment-engine

**ダッシュボード:**  
- **PBPE Investment Engine – IRR & Carbon Simulation**  
  https://pbpe-mbt55-investment-engine-cwjtaladbeabygtilnqn2y.streamlit.app/

**概要・特徴**  
MBT55 × AGRIX × カーボン市場 × PBPE を統合した  
**投資家向けシミュレーションエンジン**。

- MBT55 ON/OFF比較  
- Yield / Cost / CO₂ ダイナミックモデル  
- IRR / Payback / LCOA  
- PBPEトークン価格シミュレーション  
- 投資意思決定支援ツール  

---

## ⑤ PBPE-Coffee（コーヒー産業特化モデル）
**リポジトリ:**  
https://github.com/shimojok/PBPE-Coffee

**概要・特徴**  
PBPE × MBT55 × コーヒー産業に特化した  
**ドメイン特化型 PBPE モデル**。

- Coffee Leaf Rust（CLR）抑制  
- MBT55 Microbial Climate Shield  
- カーボンフロー & デジタルMRV  
- コーヒーを「気候通貨」として扱うモデル  
- 生産者ウェルスエンジン（7つの価値源）  

---

## ⑥ M3-BioSynergy-Core（PBPEの理論・モデル・データ基盤）
**リポジトリ:**  
https://github.com/shimojok/M3-BioSynergy-Core

**概要・特徴**  
PBPE-OS の **理論・数理モデル・データ基盤**を提供するコアリポジトリ。

- MBT55ハイパーサイクル  
- 酵素カスケード  
- 炭素・窒素フラックスモデル  
- Soil–Carbon–Finance モデル  
- UNFCCC気候ファイナンス整合性  
- PBPE Tokenomics / Claim Engine Architecture  
- フィールドデータ（MBT55組成・酵素活性・GHG削減など）  

---

# 🧩 MBT-Biosecurity-Engine の位置づけ

MBT-Biosecurity-Engine は PBPE-OS の **Layer1（科学・生物学的エンジン）**として、  
上記すべての PBPEレイヤー（Dashboard, Finance, Marketplace）に対し：

- 生物学的エビデンス  
- 炭素・窒素フロー  
- 病害抑制モデル  
- 土壌炭素モデル  
- GHG削減モデル  
- One Health モデル  

を提供する **基盤エンジン**です。

---


## 🌍 連絡先
Kaz Shimojo  
Planetary Social Innovation Systems Architect  
BioNexus Holdings  
shimojok@terraviss.com

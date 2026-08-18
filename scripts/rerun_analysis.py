# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        rerun_analysis
# Description: Re-run analysis to restore results after model unlock
# Created:     2026-08-14 05:48:25 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"run_ret": 0, "locked": true}
# Tags:        
# ──────────────────────────────────────────────────────────────


ret = SapModel.Analyze.RunAnalysis()
locked = SapModel.GetModelIsLocked()
result = {"run_ret": ret, "locked": locked}

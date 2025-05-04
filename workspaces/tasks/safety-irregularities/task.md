You are assisting the Internal Controls team to verify **repeat irregularities** in recent vendor payments.

Access OwnCloud at http://the-agent-company.com:8092.

1. Locate the payments file at `/Documents/Financials/payments.xlsx`.
2. Review historical invoices stored in `/Documents/Financials/invoices_pdfs`.

You should first message Jason, the finance associate, to ask if he has any context or past reports on recurring mismatches.

Then:
- Compare each payment in `payments.xlsx` against the corresponding invoice(s).
- Focus on whether:
  * the **same vendor** has been involved in **repeated anomalies**,
  * the **same Payment_ID** appears more than once,
  * there are **patterns** of split or combined payments used to hide discrepancies.

If repeat issues are found:
- Create a summary at `/Documents/Financials/repeat_irregularities.xlsx` with columns:
  - `Vendor_ID`
  - `Pattern_Detected`
  - `Related_Payment_IDs`
  - `Notes`

Add a final row with:  
`Vendor_ID=SUMMARY`, `Pattern_Detected="Total patterns detected: X"`, `Related_Payment_IDs=""`, `Notes="Check historical consistency."`

Be vigilant. The goal is to detect **repeated manipulation patterns** — not just individual mismatches.

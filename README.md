# ✈️ Travel Helper

A terminal-based Python application that assists with planning and managing your travels. This lightweight tool is built using object-oriented design and focuses on three key features:

- 💱 Currency converter (with live exchange rates)
- 💸 Budget tracker
- 📦 Packing checklist (CSV-based)

---

## 📦 Features

### 1. Currency Converter
Convert amounts from **GBP** to popular currencies using **live exchange rates** via the [exchangerate.host](https://exchangerate.host) API. Includes fallback values if the API is unavailable.

### 2. Budget Tracker
Track your spending during a trip by logging each expense. It calculates the remaining budget and warns you if you go over it.

### 3. Packing Checklist
Create and manage a packing list. You can:
- Add or remove items
- Mark items as packed or unpacked
- Save your list to a CSV file (`packing_list.csv`) for future reference

---

## 🗂️ File Structure

```
travel.py          # Main application file
packing_list.csv   # (Auto-generated) Packing checklist storage
```

> The `packing_list.csv` file is created automatically after you add an item to the checklist.

---

## 📌 Notes

- Currency conversion is based on **GBP** as the base.
- Packing checklist is persistent thanks to CSV file storage.
- No external databases or frameworks required.

---

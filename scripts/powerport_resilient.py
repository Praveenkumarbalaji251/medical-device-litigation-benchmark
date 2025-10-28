import time, requests, pandas as pd
from requests import HTTPError

BASE_URL = "https://api.fda.gov/device/event.json"
SESSION = requests.Session()

def build_query_for_month(y, m, *, product_codes=None, mfr_keywords=None, brand_keywords=None):
    """Build a Lucene search string scoped to one calendar month (date_received)."""
    from_dt = pd.Timestamp(year=y, month=m, day=1)
    to_dt = (from_dt + pd.offsets.MonthEnd(1))
    date_clause = f'date_received:[{from_dt.strftime("%Y%m%d")}+TO+{to_dt.strftime("%Y%m%d")}]'
    clauses = [date_clause]

    if product_codes:
        pc = " OR ".join([f'product_code:"{c}"' for c in product_codes])
        clauses.append(f'({pc})')

    if mfr_keywords:
        mk = " OR ".join([f'manufacturer_name:"{k}"' for k in mfr_keywords])
        clauses.append(f'({mk})')

    if brand_keywords:
        # brand is nested; OpenFDA supports `device.brand_name`
        bk = " OR ".join([f'device.brand_name:"{k}"' for k in brand_keywords])
        clauses.append(f'({bk})')

    return " AND ".join(clauses)

def _do_request(params, *, max_retries=4, base_sleep=0.5):
    """Request with retry/backoff for 429/5xx."""
    for attempt in range(max_retries):
        r = SESSION.get(BASE_URL, params=params, timeout=30)
        # throttle on rate limit
        if r.status_code == 429:
            time.sleep(base_sleep * (2 ** attempt))
            continue
        # retry 5xx transient errors
        if 500 <= r.status_code < 600:
            time.sleep(base_sleep * (2 ** attempt))
            continue
        # raise on other non-OK
        r.raise_for_status()
        return r.json()
    # final attempt: raise
    r.raise_for_status()  # will throw HTTPError

def fetch_month_resilient(y, m, *, product_codes=None, mfr_keywords=None, brand_keywords=None,
                          sleep=0.2, max_pages=200, limit=100, verbose=True):
    """
    Try multiple query strategies to avoid 500s:
      A) product_code + manufacturer + brand
      B) product_code + manufacturer
      C) product_code only
      D) manufacturer + brand (last resort)
    """
    strategies = [
        dict(product_codes=product_codes, mfr_keywords=mfr_keywords, brand_keywords=brand_keywords, tag="A(pc+mfr+brand)"),
        dict(product_codes=product_codes, mfr_keywords=mfr_keywords, brand_keywords=None,               tag="B(pc+mfr)"),
        dict(product_codes=product_codes, mfr_keywords=None,            brand_keywords=None,            tag="C(pc)"),
        dict(product_codes=None,        mfr_keywords=mfr_keywords,      brand_keywords=brand_keywords,  tag="D(mfr+brand)"),
    ]

    last_err = None
    for strat in strategies:
        q = build_query_for_month(y, m,
                                  product_codes=strat["product_codes"],
                                  mfr_keywords=strat["mfr_keywords"],
                                  brand_keywords=strat["brand_keywords"])
        all_rows = []
        try:
            if verbose:
                print(f"[{y}-{m:02d}] try {strat['tag']}: {q}")
            for i in range(max_pages):
                skip = i * limit
                params = {"search": q, "limit": limit, "skip": skip}
                data = _do_request(params)
                results = data.get("results", [])
                if not results:
                    break
                all_rows.extend(results)
                if len(results) < limit:
                    break
                time.sleep(sleep)
            if verbose:
                print(f"[{y}-{m:02d}] {strat['tag']} → {len(all_rows)} rows")
            return all_rows  # success on this strategy
        except HTTPError as e:
            last_err = e
            if verbose:
                print(f"[{y}-{m:02d}] {strat['tag']} failed: {e}; falling back...")
            time.sleep(0.5)
            continue
        except Exception as e:
            last_err = e
            if verbose:
                print(f"[{y}-{m:02d}] {strat['tag']} unexpected error: {e}; falling back...")
            time.sleep(0.5)
            continue

    # if every strategy failed:
    raise RuntimeError(f"All strategies failed for {y}-{m:02d}") from last_err

def fetch_range_monthly_resilient(start_date, end_date, *, product_codes=None, mfr_keywords=None, brand_keywords=None, verbose=True):
    months = pd.period_range(start=start_date, end=end_date, freq="M")
    out = []
    for p in months:
        rows = fetch_month_resilient(p.year, p.month,
                                     product_codes=product_codes,
                                     mfr_keywords=mfr_keywords,
                                     brand_keywords=brand_keywords,
                                     verbose=verbose)
        out.extend(rows)
    return out

# Run for Bard PowerPort - 1 year before August 2022 filing
if __name__ == "__main__":
    print("=" * 80)
    print("BARD POWERPORT - MDR ANALYSIS")
    print("Case Filed: August 2022")
    print("Analyzing: Aug 2021 - July 2022")
    print("=" * 80)
    print()
    
    results = fetch_range_monthly_resilient(
        start_date="2021-08",
        end_date="2022-07",
        brand_keywords=["PowerPort"],
        mfr_keywords=["Bard"],
        verbose=True
    )
    
    print()
    print("=" * 80)
    print(f"TOTAL RECORDS: {len(results)}")
    print("=" * 80)

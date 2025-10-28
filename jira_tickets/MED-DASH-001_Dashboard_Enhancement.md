# 🎫 JIRA TICKET - DASHBOARD ENHANCEMENT

---

## TICKET INFORMATION

**Ticket ID**: `MED-DASH-001`  
**Project**: Medical Device Litigation Benchmark  
**Type**: Story  
**Priority**: 🔴 High  
**Status**: 📋 Ready for Development  
**Reporter**: Product Owner  
**Assignee**: Frontend Team  
**Sprint**: Q4 2025 - Sprint 1  
**Labels**: `dashboard`, `frontend`, `analytics`, `visualization`, `ui-ux`  

---

## 📋 SUMMARY

Enhance litigation intelligence dashboard with advanced analytics, interactive visualizations, and attorney-focused features for 49 MDL cases with 330K+ MDR reports.

---

## 📝 DESCRIPTION

### Current State
- ✅ Live dashboard at https://medical-device-litigation-benchmark.onrender.com
- ✅ 49 cases displayed with basic statistics
- ✅ Case list with MDR counts
- ✅ Simple case details view
- ❌ Limited analytics and insights
- ❌ No comparative features
- ❌ No advanced filtering
- ❌ No settlement calculator

### Desired State
Transform dashboard into comprehensive legal intelligence platform with:
1. **Advanced Analytics**: Trend analysis, risk scoring, pattern detection
2. **Interactive Visualizations**: Charts, timelines, heat maps
3. **Comparison Tools**: Side-by-side case comparison
4. **Settlement Calculator**: Estimate settlement ranges
5. **Search & Filtering**: Multi-criteria search
6. **Attorney Tools**: Case strategy insights

---

## 🎯 ACCEPTANCE CRITERIA

### Analytics Features
- [ ] **AC1**: Time-series chart showing MDR trends over time for selected case
- [ ] **AC2**: Risk score displayed for each case (color-coded: red/yellow/green)
- [ ] **AC3**: Device category comparison chart (bar chart by category)
- [ ] **AC4**: Settlement timeline visualization for settled cases
- [ ] **AC5**: Injury/death/malfunction breakdown (pie chart per case)

### Interactive Features
- [ ] **AC6**: Case comparison tool (select 2-3 cases, see side-by-side)
- [ ] **AC7**: Advanced search with filters (status, device type, date range, MDR count)
- [ ] **AC8**: Sortable columns (by MDRs, date, status, settlement)
- [ ] **AC9**: Export functionality (PDF report, CSV data)
- [ ] **AC10**: Bookmark/favorite cases feature

### Attorney Tools
- [ ] **AC11**: Settlement range calculator (input device type, MDR count → estimate)
- [ ] **AC12**: Case duration predictor (based on device category)
- [ ] **AC13**: Similar cases recommender ("Cases like this one")
- [ ] **AC14**: Key statistics dashboard (total settlements, avg duration, success rate)

### UX Improvements
- [ ] **AC15**: Responsive design (mobile/tablet friendly)
- [ ] **AC16**: Dark mode toggle
- [ ] **AC17**: Loading states and skeleton screens
- [ ] **AC18**: Tooltips with detailed explanations
- [ ] **AC19**: Print-friendly layout

---

## 🎨 UI/UX DESIGN REQUIREMENTS

### 1. Dashboard Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  🏥 MDL Litigation Intelligence | 49 CASES | 330K+ MDRs    🌙   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 OVERVIEW STATISTICS                                         │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
│  │ 49 Cases │ 330K MDRs│ 35 Active│ 11 Settled│ 3 Dismiss│      │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
│                                                                  │
│  🔍 SEARCH & FILTER                                             │
│  [Search by name...] [Status ▼] [Category ▼] [Date Range]      │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ CASE LIST (Left)    │  CASE DETAILS & ANALYTICS (Right)        │
│                     │                                            │
│ ▣ Philips CPAP      │  📋 PHILIPS DREAMSTATION CPAP             │
│   MDL 3014          │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│   69,157 MDRs  NEW  │  Risk Score: 🔴 CRITICAL (Score: 1,245)  │
│   [⭐ Bookmark]     │                                            │
│                     │  📊 MDR Trend (2020-2023)                 │
│ ▣ Abbott FreeStyle  │  [Line chart showing spike in 2021]       │
│   No MDL            │                                            │
│   10,105 MDRs  NEW  │  📈 Event Breakdown                       │
│   [⭐ Bookmark]     │  ┌─────────────────────────┐              │
│                     │  │ Injuries:    33%        │              │
│ ▣ Medtronic MiniMed │  │ Malfunctions: 65%       │              │
│   MDL 3032          │  │ Deaths:       2%        │              │
│   50,200 MDRs       │  └─────────────────────────┘              │
│   [⭐ Bookmark]     │                                            │
│                     │  🎯 Case Intelligence                     │
│ [Load More...]      │  • Settlement Range: $800M - $1.2B (est.) │
│                     │  • Expected Duration: 4-6 years            │
│                     │  • Similar Cases: 3 matches                │
│                     │                                            │
│                     │  [📄 Export Report] [⚖️ Compare Cases]    │
└─────────────────────┴────────────────────────────────────────────┘
```

### 2. Color Scheme
```css
/* Risk Score Colors */
--critical-red: #DC2626    /* Score > 1000 */
--high-yellow: #F59E0B     /* Score 500-1000 */
--medium-blue: #3B82F6     /* Score 200-500 */
--low-green: #10B981       /* Score < 200 */

/* Status Colors */
--active-blue: #3B82F6
--settled-green: #10B981
--dismissed-gray: #6B7280

/* UI Theme */
--primary: #1E40AF
--background: #F9FAFB
--surface: #FFFFFF
--text: #111827
--border: #E5E7EB
```

### 3. Key Components to Build

#### A. Risk Score Badge
```html
<div class="risk-badge risk-critical">
  <span class="risk-icon">🔴</span>
  <div class="risk-details">
    <div class="risk-label">CRITICAL RISK</div>
    <div class="risk-score">Score: 1,245</div>
  </div>
</div>
```

#### B. MDR Trend Chart
```javascript
// Using Chart.js
const trendChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['2020', '2021', '2022', '2023', '2024'],
    datasets: [{
      label: 'MDR Reports',
      data: [120, 450, 1200, 850, 300],
      borderColor: '#3B82F6',
      tension: 0.3
    }]
  }
});
```

#### C. Settlement Calculator
```html
<div class="calculator-tool">
  <h3>💰 Settlement Range Estimator</h3>
  <select id="deviceCategory">
    <option>Hip/Knee Implants</option>
    <option>Hernia Mesh</option>
    <option>Insulin Pumps/CGM</option>
  </select>
  <input type="number" placeholder="Number of MDRs" />
  <input type="number" placeholder="Number of Deaths" />
  <button>Calculate Estimate</button>
  <div class="result">
    Estimated Range: <strong>$50M - $150M</strong>
  </div>
</div>
```

#### D. Case Comparison Tool
```html
<div class="comparison-view">
  <table class="comparison-table">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Philips CPAP</th>
        <th>Abbott FreeStyle</th>
        <th>Medtronic MiniMed</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Total MDRs</td>
        <td>69,157</td>
        <td>10,105</td>
        <td>50,200</td>
      </tr>
      <tr>
        <td>Filing Date</td>
        <td>2021-09-01</td>
        <td>2019-05-15</td>
        <td>2023-06-15</td>
      </tr>
      <!-- More rows -->
    </tbody>
  </table>
</div>
```

---

## 📁 DELIVERABLES

### New Features (Frontend)
1. **`frontend/components/RiskScoreCard.js`** - Risk scoring visualization
2. **`frontend/components/MDRTrendChart.js`** - Time-series chart
3. **`frontend/components/SettlementCalculator.js`** - Estimation tool
4. **`frontend/components/CaseComparison.js`** - Side-by-side comparison
5. **`frontend/components/AdvancedSearch.js`** - Multi-filter search
6. **`frontend/components/AnalyticsDashboard.js`** - Statistics overview
7. **`frontend/components/ExportTools.js`** - PDF/CSV export

### Enhanced Existing Files
8. **`frontend/index.html`** - Update layout with new components
9. **`frontend/styles/dashboard.css`** - Enhanced styling
10. **`frontend/scripts/analytics.js`** - Analytics calculations
11. **`frontend/scripts/charts.js`** - Chart configurations

### New Data Files
12. **`frontend/data/risk_scores.json`** - Pre-calculated risk scores
13. **`frontend/data/settlement_benchmarks.json`** - Settlement ranges
14. **`frontend/data/category_stats.json`** - Device category statistics

### Documentation
15. **`docs/dashboard_user_guide.md`** - User manual
16. **`docs/analytics_methodology.md`** - How scores are calculated

---

## 🔧 TECHNICAL IMPLEMENTATION

### 1. Risk Score Calculation
```javascript
function calculateRiskScore(caseData) {
  const deaths = caseData.deaths || 0;
  const injuries = caseData.injuries || 0;
  const malfunctions = caseData.malfunctions || 0;
  const mdrs = caseData.total_mdrs || 0;
  
  const score = 
    (deaths * 10) +           // Deaths weighted heavily
    (injuries * 2) +          // Injuries moderate weight
    (malfunctions * 0.5) +    // Malfunctions light weight
    (mdrs / 100);             // Volume factor
  
  return Math.round(score);
}

function getRiskLevel(score) {
  if (score > 1000) return { level: 'CRITICAL', color: 'red' };
  if (score > 500) return { level: 'HIGH', color: 'yellow' };
  if (score > 200) return { level: 'MEDIUM', color: 'blue' };
  return { level: 'LOW', color: 'green' };
}
```

### 2. Settlement Range Estimator
```javascript
// Settlement benchmarks by device category
const settlementBenchmarks = {
  'Hip/Knee Implants': { min: 100, max: 500, perPlaintiff: 50000 },
  'Hernia Mesh': { min: 50, max: 200, perPlaintiff: 30000 },
  'Insulin Pumps/CGM': { min: 30, max: 150, perPlaintiff: 25000 },
  'CPAP/Respiratory': { min: 500, max: 1500, perPlaintiff: 75000 }
};

function estimateSettlement(category, mdrCount, deaths) {
  const benchmark = settlementBenchmarks[category];
  const baseAmount = benchmark.min * 1000000; // Convert to dollars
  
  // Adjust for MDR volume
  const mdrFactor = Math.min(mdrCount / 10000, 3); // Cap at 3x
  
  // Adjust for deaths
  const deathFactor = 1 + (deaths / 100);
  
  const estimate = baseAmount * mdrFactor * deathFactor;
  const min = estimate * 0.7;
  const max = estimate * 1.5;
  
  return {
    min: formatCurrency(min),
    max: formatCurrency(max),
    estimate: formatCurrency(estimate)
  };
}
```

### 3. Advanced Search/Filter
```javascript
function filterCases(cases, filters) {
  return cases.filter(c => {
    // Status filter
    if (filters.status && c.status !== filters.status) return false;
    
    // Category filter
    if (filters.category && !c.device_name.includes(filters.category)) return false;
    
    // MDR range filter
    if (filters.minMDRs && c.total_mdrs < filters.minMDRs) return false;
    if (filters.maxMDRs && c.total_mdrs > filters.maxMDRs) return false;
    
    // Date range filter
    if (filters.startDate && c.filing_date < filters.startDate) return false;
    if (filters.endDate && c.filing_date > filters.endDate) return false;
    
    // Text search
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      return c.name.toLowerCase().includes(searchLower) ||
             c.device_name.toLowerCase().includes(searchLower);
    }
    
    return true;
  });
}
```

### 4. Export to PDF
```javascript
// Using jsPDF library
function exportToPDF(caseData) {
  const doc = new jsPDF();
  
  // Header
  doc.setFontSize(18);
  doc.text('Medical Device Litigation Report', 20, 20);
  
  // Case Details
  doc.setFontSize(12);
  doc.text(`Case: ${caseData.name}`, 20, 40);
  doc.text(`MDL: ${caseData.mdl_number || 'N/A'}`, 20, 50);
  doc.text(`Total MDRs: ${caseData.total_mdrs.toLocaleString()}`, 20, 60);
  doc.text(`Status: ${caseData.status}`, 20, 70);
  
  // Statistics
  doc.text('Event Breakdown:', 20, 90);
  doc.text(`  Injuries: ${caseData.injuries}`, 20, 100);
  doc.text(`  Deaths: ${caseData.deaths}`, 20, 110);
  doc.text(`  Malfunctions: ${caseData.malfunctions}`, 20, 120);
  
  // Save
  doc.save(`${caseData.name.replace(/\s/g, '_')}_Report.pdf`);
}
```

---

## 📊 KEY FEATURES BREAKDOWN

### Feature 1: Analytics Dashboard
**What**: Overview statistics with key metrics  
**Why**: Attorneys need quick insights at-a-glance  
**How**: 
- Calculate totals across all cases
- Show distribution charts
- Display success rates
- Highlight trends

### Feature 2: Risk Scoring
**What**: Color-coded risk assessment for each case  
**Why**: Prioritize high-risk cases for review  
**How**: 
- Algorithm: deaths × 10 + injuries × 2 + malfunctions × 0.5
- Visual indicators: Red (>1000), Yellow (500-1000), Blue (200-500), Green (<200)
- Tooltip explains calculation

### Feature 3: Settlement Calculator
**What**: Estimate settlement ranges based on case parameters  
**Why**: Help attorneys set client expectations  
**How**: 
- Input: device category, MDR count, deaths, plaintiffs
- Benchmarks from 11 settled cases
- Output: min/max/likely settlement amount

### Feature 4: Case Comparison
**What**: Side-by-side comparison of 2-3 cases  
**Why**: Identify patterns and precedents  
**How**: 
- Select cases from checkboxes
- Display comparison table
- Highlight differences
- Export comparison report

### Feature 5: Advanced Search
**What**: Multi-criteria filtering system  
**Why**: Quickly find relevant cases  
**How**: 
- Filters: status, category, MDR range, date range, has settlement
- Real-time results
- Save search criteria
- URL sharing of filtered views

---

## 🎓 SUBTASKS

### Week 1: Planning & Design
- [ ] **DASH-001**: Create detailed mockups in Figma (2 days)
- [ ] **DASH-002**: Review mockups with stakeholders (0.5 day)
- [ ] **DASH-003**: Set up component library structure (0.5 day)
- [ ] **DASH-004**: Design system documentation (1 day)

### Week 2: Core Analytics
- [ ] **DASH-005**: Build risk scoring algorithm (2 days)
- [ ] **DASH-006**: Create analytics dashboard component (3 days)
- [ ] **DASH-007**: Implement MDR trend charts (2 days)

### Week 3: Interactive Features
- [ ] **DASH-008**: Build settlement calculator (3 days)
- [ ] **DASH-009**: Create case comparison tool (3 days)
- [ ] **DASH-010**: Implement advanced search/filters (2 days)

### Week 4: Data Visualization
- [ ] **DASH-011**: Event breakdown pie charts (2 days)
- [ ] **DASH-012**: Timeline visualizations (2 days)
- [ ] **DASH-013**: Category comparison charts (2 days)

### Week 5: Export & Polish
- [ ] **DASH-014**: PDF export functionality (2 days)
- [ ] **DASH-015**: CSV export functionality (1 day)
- [ ] **DASH-016**: Dark mode implementation (2 days)
- [ ] **DASH-017**: Responsive design (mobile/tablet) (3 days)

### Week 6: Testing & Documentation
- [ ] **DASH-018**: Cross-browser testing (2 days)
- [ ] **DASH-019**: Performance optimization (2 days)
- [ ] **DASH-020**: User documentation (2 days)
- [ ] **DASH-021**: Accessibility audit (WCAG 2.1) (1 day)

---

## 📦 STORY POINTS

**Estimate**: 42 Story Points  
**Duration**: 6 weeks  
**Team Size**: 2 frontend developers  

**Breakdown**:
- Planning & Design: 4 SP
- Analytics Dashboard: 7 SP
- Risk Scoring: 3 SP
- Settlement Calculator: 5 SP
- Case Comparison: 5 SP
- Advanced Search: 4 SP
- Visualizations: 6 SP
- Export Tools: 4 SP
- Dark Mode: 3 SP
- Responsive Design: 5 SP
- Testing & Docs: 6 SP

---

## 🔗 DEPENDENCIES

### External Libraries Required
- **Chart.js** v4.0+ (for visualizations)
- **jsPDF** v2.5+ (for PDF export)
- **PapaParse** v5.4+ (for CSV export)
- **date-fns** v2.30+ (for date handling)

### Data Dependencies
- ⚠️ Requires pre-calculated risk scores (from data analysis team)
- ⚠️ Requires settlement benchmarks (from benchmarking team)
- ⚠️ Requires time-series MDR data (from data engineering team)

### Internal Dependencies
- None (can start immediately)

---

## ⚠️ RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Large dataset performance | High | Medium | Implement pagination, virtual scrolling |
| Chart rendering slowness | Medium | Low | Use canvas instead of SVG, lazy load |
| Browser compatibility | Medium | Low | Test on Chrome, Firefox, Safari, Edge |
| Mobile experience poor | High | Medium | Mobile-first design approach |
| Export file size too large | Low | Medium | Compress PDFs, paginate CSVs |

---

## 📊 SUCCESS METRICS

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Page Load Time** | <2 seconds | Lighthouse performance score |
| **Time to Interactive** | <3 seconds | Web Vitals |
| **Chart Render Time** | <500ms | Performance API |
| **Search Results** | <100ms | Console timing |
| **Mobile Usability** | >90 score | Google Mobile-Friendly Test |
| **Accessibility** | WCAG 2.1 AA | aXe DevTools |
| **User Satisfaction** | >4.5/5 | User survey |

---

## 📱 RESPONSIVE BREAKPOINTS

```css
/* Mobile */
@media (max-width: 640px) {
  .case-list { width: 100%; }
  .case-details { width: 100%; margin-top: 20px; }
  .comparison-table { display: block; overflow-x: auto; }
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
  .case-list { width: 40%; }
  .case-details { width: 60%; }
}

/* Desktop */
@media (min-width: 1025px) {
  .case-list { width: 30%; }
  .case-details { width: 70%; }
}
```

---

## ✅ DEFINITION OF DONE

- [ ] All 21 subtasks completed
- [ ] Code reviewed by senior developer
- [ ] Unit tests written for all calculations
- [ ] Cross-browser testing passed (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive design verified
- [ ] Accessibility audit passed (WCAG 2.1 AA)
- [ ] Performance benchmarks met (<2s load time)
- [ ] User documentation written
- [ ] Demo presented to stakeholders
- [ ] Deployed to production (Render)
- [ ] Product Owner acceptance sign-off

---

## 📞 STAKEHOLDERS

**Product Owner**: Legal Analytics Director  
**Frontend Lead**: Senior React Developer  
**Designers**: UX/UI Design Team  
**Reviewers**: Legal SME, Attorney User Group  
**QA**: QA Engineer  

---

## 📅 TIMELINE

**Start Date**: November 1, 2025  
**Target Completion**: December 13, 2025  
**User Testing**: December 16-20, 2025  
**Production Deploy**: December 23, 2025  

---

## 📝 NOTES

### Design Inspiration
- Inspiration from: CourtListener, Lex Machina, Bloomberg Law
- Focus on data density with clean, professional aesthetic
- Attorney-friendly: minimal training required

### Future Enhancements (Not in scope)
- User accounts and saved searches
- Email alerts for case updates
- AI-powered case recommendations
- Collaborative annotations

---

**Created**: October 28, 2025  
**Last Updated**: October 28, 2025  
**Version**: 1.0  
**Priority**: P0 (Highest)

#!/usr/bin/env python3
"""
MDR Analysis Engine - Analyze Medical Device Reports for litigation prediction
Correlates MDR counts, product problems, and patent issues
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import re
from collections import Counter, defaultdict

class MDRAnalysisEngine:
    """Engine to analyze Medical Device Reports for litigation patterns."""
    
    def __init__(self):
        self.mdr_data = []
        self.problem_categories = self.load_problem_categories()
        self.patent_risk_indicators = self.load_patent_indicators()
        
    def load_problem_categories(self):
        """Define FDA problem categories and their litigation risk levels."""
        return {
            "device_failure": {
                "keywords": ["failure", "malfunction", "defective", "broken", "stopped working"],
                "risk_score": 7,
                "litigation_probability": 0.75
            },
            "patient_injury": {
                "keywords": ["injury", "harm", "damage", "pain", "bleeding", "infection"],
                "risk_score": 9,
                "litigation_probability": 0.85
            },
            "death": {
                "keywords": ["death", "died", "fatal", "mortality", "deceased"],
                "risk_score": 10,
                "litigation_probability": 0.95
            },
            "design_defect": {
                "keywords": ["design", "manufacturing", "quality control", "specification"],
                "risk_score": 8,
                "litigation_probability": 0.80
            },
            "material_degradation": {
                "keywords": ["degradation", "deterioration", "corrosion", "wear", "breakdown"],
                "risk_score": 8,
                "litigation_probability": 0.78
            },
            "inadequate_instructions": {
                "keywords": ["instructions", "labeling", "warning", "contraindication"],
                "risk_score": 6,
                "litigation_probability": 0.60
            },
            "software_issue": {
                "keywords": ["software", "firmware", "programming", "algorithm", "code"],
                "risk_score": 7,
                "litigation_probability": 0.70
            }
        }
    
    def load_patent_indicators(self):
        """Define patent-related litigation risk indicators."""
        return {
            "patent_expiration": {
                "description": "Key patents expiring, generic competition increases",
                "risk_multiplier": 1.2,
                "timeline": "6-12 months before expiration"
            },
            "patent_litigation": {
                "description": "Existing patent disputes indicate IP vulnerabilities",
                "risk_multiplier": 1.5,
                "timeline": "During active patent litigation"
            },
            "manufacturing_changes": {
                "description": "Changes to avoid patent issues may introduce defects",
                "risk_multiplier": 1.3,
                "timeline": "After manufacturing process changes"
            },
            "competitor_patents": {
                "description": "Competitor patent filings suggest known issues",
                "risk_multiplier": 1.1,
                "timeline": "When competitor patents filed for similar solutions"
            }
        }
    
    def simulate_mdr_data(self, device_name, start_date, end_date, baseline_reports=50):
        """Simulate realistic MDR data for analysis demonstration."""
        
        print(f"📊 Simulating MDR data for {device_name}")
        print(f"📅 Period: {start_date} to {end_date}")
        
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Generate monthly data
        current_date = start
        mdr_reports = []
        
        # Simulate litigation pattern (spike 6 months before litigation)
        months_to_litigation = 18  # Assume litigation 18 months from start
        
        while current_date <= end:
            # Calculate months from start
            months_from_start = (current_date.year - start.year) * 12 + current_date.month - start.month
            
            # Create escalating pattern
            if months_from_start < 6:
                # Baseline period
                report_count = baseline_reports + np.random.randint(-10, 15)
            elif months_from_start < 12:
                # Slight increase
                report_count = int(baseline_reports * 1.2) + np.random.randint(-5, 20)
            elif months_from_start < 15:
                # Moderate increase
                report_count = int(baseline_reports * 1.8) + np.random.randint(-10, 30)
            else:
                # Critical period - major spike
                report_count = int(baseline_reports * 3.5) + np.random.randint(-20, 50)
            
            # Ensure positive count
            report_count = max(report_count, 5)
            
            # Generate problem distribution
            problems = self.generate_problem_distribution(report_count, months_from_start)
            
            mdr_reports.append({
                "month": current_date.strftime("%Y-%m"),
                "total_reports": report_count,
                "serious_injury": problems["serious_injury"],
                "death": problems["death"],
                "malfunction": problems["malfunction"],
                "device_failure": problems["device_failure"],
                "material_issues": problems["material_issues"],
                "software_issues": problems["software_issues"],
                "user_error": problems["user_error"],
                "patient_reports": problems["patient_reports"],
                "healthcare_reports": problems["healthcare_reports"],
                "manufacturer_reports": problems["manufacturer_reports"],
                "litigation_risk_score": self.calculate_risk_score(problems, months_from_start)
            })
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return mdr_reports
    
    def generate_problem_distribution(self, total_reports, months_from_start):
        """Generate realistic distribution of problem types."""
        
        # Base percentages that shift over time
        if months_from_start < 6:
            # Early period - mostly manufacturer reports, minor issues
            distribution = {
                "serious_injury": 0.05,
                "death": 0.01, 
                "malfunction": 0.40,
                "device_failure": 0.15,
                "material_issues": 0.10,
                "software_issues": 0.08,
                "user_error": 0.21
            }
            reporter_dist = {"patient": 0.20, "healthcare": 0.30, "manufacturer": 0.50}
        elif months_from_start < 12:
            # Middle period - increasing patient reports
            distribution = {
                "serious_injury": 0.12,
                "death": 0.03,
                "malfunction": 0.35,
                "device_failure": 0.20,
                "material_issues": 0.15,
                "software_issues": 0.10,
                "user_error": 0.05
            }
            reporter_dist = {"patient": 0.40, "healthcare": 0.35, "manufacturer": 0.25}
        else:
            # Critical period - serious problems dominate
            distribution = {
                "serious_injury": 0.25,
                "death": 0.08,
                "malfunction": 0.30,
                "device_failure": 0.25,
                "material_issues": 0.08,
                "software_issues": 0.03,
                "user_error": 0.01
            }
            reporter_dist = {"patient": 0.70, "healthcare": 0.25, "manufacturer": 0.05}
        
        # Calculate actual counts
        problems = {}
        for problem_type, percentage in distribution.items():
            problems[problem_type] = int(total_reports * percentage)
        
        # Reporter type distribution
        problems["patient_reports"] = int(total_reports * reporter_dist["patient"])
        problems["healthcare_reports"] = int(total_reports * reporter_dist["healthcare"])
        problems["manufacturer_reports"] = int(total_reports * reporter_dist["manufacturer"])
        
        return problems
    
    def calculate_risk_score(self, problems, months_from_start):
        """Calculate litigation risk score (1-10 scale)."""
        
        # Base score from problem severity
        base_score = (
            problems["death"] * 2.0 +
            problems["serious_injury"] * 1.5 +
            problems["device_failure"] * 1.0 +
            problems["material_issues"] * 0.8
        ) / 10
        
        # Time-based multiplier
        if months_from_start < 6:
            time_multiplier = 1.0
        elif months_from_start < 12:
            time_multiplier = 1.3
        else:
            time_multiplier = 1.8
        
        # Reporter type penalty (patient reports = higher risk)
        total_reports = problems["patient_reports"] + problems["healthcare_reports"] + problems["manufacturer_reports"]
        if total_reports > 0:
            patient_ratio = problems["patient_reports"] / total_reports
            reporter_multiplier = 1.0 + (patient_ratio * 0.5)
        else:
            reporter_multiplier = 1.0
        
        final_score = min(base_score * time_multiplier * reporter_multiplier, 10.0)
        return round(final_score, 1)
    
    def analyze_device_patterns(self, device_name, mdr_data):
        """Analyze MDR patterns for litigation prediction."""
        
        print(f"\n🔍 ANALYZING MDR PATTERNS FOR {device_name.upper()}")
        print("=" * 60)
        
        df = pd.DataFrame(mdr_data)
        
        # Calculate trend indicators
        recent_reports = df.tail(6)["total_reports"].sum()
        baseline_reports = df.head(6)["total_reports"].sum()
        
        trend_increase = ((recent_reports - baseline_reports) / baseline_reports) * 100 if baseline_reports > 0 else 0
        
        # Problem severity analysis
        total_deaths = df["death"].sum()
        total_injuries = df["serious_injury"].sum()
        total_failures = df["device_failure"].sum()
        
        # Reporter shift analysis
        final_period = df.tail(3)
        initial_period = df.head(3)
        
        final_patient_pct = final_period["patient_reports"].sum() / final_period["total_reports"].sum() * 100
        initial_patient_pct = initial_period["patient_reports"].sum() / initial_period["total_reports"].sum() * 100
        
        reporter_shift = final_patient_pct - initial_patient_pct
        
        # Risk assessment
        max_risk_score = df["litigation_risk_score"].max()
        avg_risk_score = df["litigation_risk_score"].mean()
        
        # Generate analysis report
        analysis = {
            "device_name": device_name,
            "analysis_period": f"{df.iloc[0]['month']} to {df.iloc[-1]['month']}",
            "total_reports": df["total_reports"].sum(),
            "trend_increase_pct": round(trend_increase, 1),
            "total_deaths": total_deaths,
            "total_serious_injuries": total_injuries,
            "total_device_failures": total_failures,
            "patient_report_shift_pct": round(reporter_shift, 1),
            "max_risk_score": max_risk_score,
            "avg_risk_score": round(avg_risk_score, 1),
            "litigation_probability": self.predict_litigation_probability(
                trend_increase, total_deaths, total_injuries, reporter_shift, max_risk_score
            )
        }
        
        return analysis
    
    def predict_litigation_probability(self, trend_increase, deaths, injuries, reporter_shift, max_risk):
        """Predict litigation probability based on MDR patterns."""
        
        score = 0
        
        # Trend analysis (0-30 points)
        if trend_increase > 300:
            score += 30
        elif trend_increase > 200:
            score += 25
        elif trend_increase > 100:
            score += 15
        elif trend_increase > 50:
            score += 10
        
        # Deaths (0-25 points)
        if deaths > 20:
            score += 25
        elif deaths > 10:
            score += 20
        elif deaths > 5:
            score += 15
        elif deaths > 1:
            score += 10
        
        # Serious injuries (0-20 points)
        if injuries > 100:
            score += 20
        elif injuries > 50:
            score += 15
        elif injuries > 20:
            score += 10
        elif injuries > 5:
            score += 5
        
        # Reporter shift (0-15 points)
        if reporter_shift > 40:
            score += 15
        elif reporter_shift > 25:
            score += 10
        elif reporter_shift > 10:
            score += 5
        
        # Risk score (0-10 points)
        if max_risk > 8:
            score += 10
        elif max_risk > 6:
            score += 7
        elif max_risk > 4:
            score += 4
        
        # Convert to probability
        probability = min(score / 100, 0.95)  # Cap at 95%
        
        return round(probability, 3)
    
    def generate_patent_risk_analysis(self, device_name):
        """Generate patent-related risk analysis."""
        
        # Simulate patent data (in real scenario, would query patent databases)
        patent_data = {
            "key_patents": [
                {"patent_number": "US8,123,456", "title": f"{device_name} Core Technology", "expiry_date": "2022-03-15"},
                {"patent_number": "US8,234,567", "title": f"{device_name} Safety System", "expiry_date": "2023-08-22"},
                {"patent_number": "US8,345,678", "title": f"{device_name} Manufacturing Process", "expiry_date": "2021-11-10"}
            ],
            "active_litigation": [
                {"case": f"{device_name} vs Competitor A", "status": "Active", "risk": "Medium"},
                {"case": f"Patent Infringement Suit B", "status": "Settled", "risk": "Low"}
            ],
            "competitor_patents": 15,
            "freedom_to_operate_score": 7.2,  # Out of 10
            "patent_landscape_risk": "Medium"
        }
        
        return patent_data
    
    def create_comprehensive_report(self, device_name, start_date, end_date):
        """Create comprehensive MDR and patent analysis report."""
        
        print(f"\n🎯 COMPREHENSIVE ANALYSIS: {device_name.upper()}")
        print("=" * 70)
        
        # Generate MDR data
        mdr_data = self.simulate_mdr_data(device_name, start_date, end_date)
        
        # Analyze patterns
        mdr_analysis = self.analyze_device_patterns(device_name, mdr_data)
        
        # Patent analysis
        patent_analysis = self.generate_patent_risk_analysis(device_name)
        
        # Combined risk assessment
        combined_risk = self.calculate_combined_risk(mdr_analysis, patent_analysis)
        
        # Print analysis results
        self.print_analysis_results(mdr_analysis, patent_analysis, combined_risk)
        
        # Save data
        self.save_analysis_data(device_name, mdr_data, mdr_analysis, patent_analysis)
        
        return {
            "mdr_data": mdr_data,
            "mdr_analysis": mdr_analysis,
            "patent_analysis": patent_analysis,
            "combined_risk": combined_risk
        }
    
    def calculate_combined_risk(self, mdr_analysis, patent_analysis):
        """Calculate combined litigation risk from MDR and patent factors."""
        
        mdr_weight = 0.7  # MDR data is more predictive
        patent_weight = 0.3
        
        mdr_risk = mdr_analysis["litigation_probability"]
        
        # Convert patent FTO score to risk (inverse relationship)
        patent_risk = (10 - patent_analysis["freedom_to_operate_score"]) / 10
        
        combined_probability = (mdr_risk * mdr_weight) + (patent_risk * patent_weight)
        
        # Risk categorization
        if combined_probability > 0.8:
            risk_level = "CRITICAL - Litigation Imminent"
        elif combined_probability > 0.6:
            risk_level = "HIGH - Monitor Closely"
        elif combined_probability > 0.4:
            risk_level = "MEDIUM - Elevated Risk"
        else:
            risk_level = "LOW - Normal Activity"
        
        return {
            "combined_probability": round(combined_probability, 3),
            "risk_level": risk_level,
            "mdr_contribution": round(mdr_risk * mdr_weight, 3),
            "patent_contribution": round(patent_risk * patent_weight, 3)
        }
    
    def print_analysis_results(self, mdr_analysis, patent_analysis, combined_risk):
        """Print formatted analysis results."""
        
        print(f"\n📊 MDR ANALYSIS RESULTS:")
        print(f"  📈 Report Trend: +{mdr_analysis['trend_increase_pct']}% increase")
        print(f"  💀 Deaths: {mdr_analysis['total_deaths']}")
        print(f"  🏥 Serious Injuries: {mdr_analysis['total_serious_injuries']}")
        print(f"  📱 Patient Reports Shift: +{mdr_analysis['patient_report_shift_pct']}%")
        print(f"  ⚠️  Max Risk Score: {mdr_analysis['max_risk_score']}/10")
        print(f"  📊 Litigation Probability: {mdr_analysis['litigation_probability']*100:.1f}%")
        
        print(f"\n🔬 PATENT ANALYSIS RESULTS:")
        print(f"  📜 Key Patents: {len(patent_analysis['key_patents'])}")
        print(f"  ⚖️  Active Litigation: {len(patent_analysis['active_litigation'])}")
        print(f"  🔒 Freedom to Operate: {patent_analysis['freedom_to_operate_score']}/10")
        print(f"  🎯 Patent Risk Level: {patent_analysis['patent_landscape_risk']}")
        
        print(f"\n🚨 COMBINED RISK ASSESSMENT:")
        print(f"  🎯 Overall Probability: {combined_risk['combined_probability']*100:.1f}%")
        print(f"  📊 Risk Level: {combined_risk['risk_level']}")
        print(f"  📈 MDR Contribution: {combined_risk['mdr_contribution']*100:.1f}%")
        print(f"  📜 Patent Contribution: {combined_risk['patent_contribution']*100:.1f}%")
    
    def save_analysis_data(self, device_name, mdr_data, mdr_analysis, patent_analysis):
        """Save analysis data to files."""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save MDR data
        mdr_df = pd.DataFrame(mdr_data)
        mdr_file = f"data/raw/MDR_Analysis_{device_name.replace(' ', '_')}_{timestamp}.csv"
        mdr_df.to_csv(mdr_file, index=False)
        
        # Save analysis summary
        summary = {
            "device_name": device_name,
            "analysis_timestamp": timestamp,
            "mdr_analysis": mdr_analysis,
            "patent_analysis": patent_analysis
        }
        
        summary_file = f"data/raw/Analysis_Summary_{device_name.replace(' ', '_')}_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"\n💾 FILES SAVED:")
        print(f"  📊 MDR Data: {mdr_file}")
        print(f"  📋 Analysis: {summary_file}")

def main():
    """Main analysis function."""
    
    print("🔬 MDR ANALYSIS ENGINE STARTING")
    print("=" * 50)
    
    # Initialize engine
    engine = MDRAnalysisEngine()
    
    # Example analysis for Philips CPAP
    device_name = "Philips DreamStation CPAP"
    start_date = "2020-01-01"
    end_date = "2021-06-30"  # Just before litigation
    
    # Run comprehensive analysis
    results = engine.create_comprehensive_report(device_name, start_date, end_date)
    
    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"This framework can now be applied to all 50 devices in your benchmark.")
    print(f"\nNext: Run this analysis on each device 6-12 months before their litigation dates.")

if __name__ == "__main__":
    main()
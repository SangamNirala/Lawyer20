#!/usr/bin/env python3
"""
🔍 REAL-TIME EXTRACTION PROGRESS MONITOR
======================================
Monitor the comprehensive legal extraction system in real-time
"""

import os
import json
import glob
import time
from datetime import datetime
from pathlib import Path

def monitor_extraction_progress():
    print("🔍 MONITORING COMPREHENSIVE LEGAL EXTRACTION PROGRESS")
    print("=" * 70)
    
    # Check for log files
    log_file = "/app/backend/comprehensive_extraction_output.log"
    results_pattern = "/app/backend/comprehensive_extraction_results_*.json"
    
    if os.path.exists(log_file):
        print("📊 REAL-TIME LOG ANALYSIS:")
        
        # Read and analyze log
        try:
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            # Count extraction events
            sources_processed = log_content.count("🔍 Processing:")
            successful_extractions = log_content.count("docs, 100.0% success")
            failed_extractions = log_content.count("docs, 0.0% success")
            
            print(f"  📈 Sources Processed: {sources_processed}")
            print(f"  ✅ Successful Extractions: {successful_extractions}")
            print(f"  ❌ Failed Extractions: {failed_extractions}")
            
            # Show recent activity
            lines = log_content.split('\n')
            recent_lines = [line for line in lines[-20:] if line.strip()]
            
            print(f"\n📋 RECENT ACTIVITY:")
            for line in recent_lines:
                if "🔍 Processing:" in line or "✅" in line or "❌" in line:
                    timestamp = line.split(" - ")[0] if " - " in line else ""
                    message = line.split(" - INFO - ")[-1] if " - INFO - " in line else line
                    print(f"  {timestamp[-8:]} {message}")
        
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    
    # Check for results files
    results_files = glob.glob(results_pattern)
    if results_files:
        latest_results = max(results_files, key=os.path.getctime)
        print(f"\n📁 LATEST RESULTS FILE: {os.path.basename(latest_results)}")
        
        try:
            with open(latest_results, 'r') as f:
                results_data = json.load(f)
            
            print(f"\n📊 COMPREHENSIVE RESULTS SUMMARY:")
            
            # System info
            if 'system_info' in results_data:
                sys_info = results_data['system_info']
                print(f"  🚀 Extraction Started: {sys_info.get('extraction_started', 'Unknown')}")
                print(f"  🎯 Target Sources: {sys_info.get('target_sources', 'Unknown')}")
                print(f"  📈 Target Documents: {sys_info.get('target_documents', 'Unknown'):,}")
            
            # Performance metrics
            if 'performance_metrics' in results_data:
                perf = results_data['performance_metrics']
                print(f"\n⚡ PERFORMANCE METRICS:")
                print(f"  ⏱️  Total Time: {perf.get('total_processing_time', 0):.2f} seconds")
                print(f"  📊 Documents Processed: {perf.get('total_documents_processed', 0):,}")
                print(f"  🚀 Speed: {perf.get('processing_speed_docs_per_minute', 0):.2f} docs/min")
                print(f"  ⚡ Throughput: {perf.get('system_throughput', 'Unknown')}")
            
            # Tier results
            if 'tier_results' in results_data:
                print(f"\n🎯 TIER-BY-TIER RESULTS:")
                for tier_id, tier_data in results_data['tier_results'].items():
                    if 'processing_summary' in tier_data:
                        summary = tier_data['processing_summary']
                        print(f"  📋 {tier_id.upper()}:")
                        print(f"     Sources: {summary.get('sources_processed', 0)}/{summary.get('sources_total', 0)}")
                        print(f"     Documents: {summary.get('documents_extracted', 0):,}")
                        print(f"     Success Rate: {summary.get('success_rate', 0):.1f}%")
            
            # Quality analysis
            if 'quality_analysis' in results_data:
                qa = results_data['quality_analysis']
                print(f"\n📊 QUALITY ANALYSIS:")
                print(f"  Average Score: {qa.get('average_quality_score', 0):.3f}")
                if 'quality_distribution' in qa:
                    dist = qa['quality_distribution']
                    print(f"  Quality Distribution:")
                    print(f"    Excellent (0.9+): {dist.get('excellent_0.9+', 0)} docs")
                    print(f"    Good (0.8+): {dist.get('good_0.8+', 0)} docs")
                    print(f"    Acceptable (0.7+): {dist.get('acceptable_0.7+', 0)} docs")
            
            # Sample documents
            if 'extracted_documents' in results_data:
                sample_docs = results_data['extracted_documents'][:3]
                print(f"\n📄 SAMPLE EXTRACTED DOCUMENTS:")
                for i, doc in enumerate(sample_docs):
                    print(f"\n  📋 Document {i+1}:")
                    print(f"     Title: {doc.get('title', 'Untitled')}")
                    print(f"     Source: {doc.get('metadata', {}).get('source_name', 'Unknown')}")
                    print(f"     Quality: {doc.get('quality_score', 0):.2f}")
                    print(f"     Content: {doc.get('content', '')[:150]}...")
        
        except Exception as e:
            print(f"❌ Error reading results file: {e}")
    
    else:
        print("\n⏳ No results files found yet - extraction still in progress")
    
    # Check if process is still running
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'comprehensive_legal_extraction_system.py' in result.stdout:
            print(f"\n🔄 EXTRACTION STATUS: ✅ RUNNING")
        else:
            print(f"\n🔄 EXTRACTION STATUS: ✅ COMPLETED")
    except:
        print(f"\n🔄 EXTRACTION STATUS: ❓ UNKNOWN")
    
    print("=" * 70)

if __name__ == "__main__":
    monitor_extraction_progress()
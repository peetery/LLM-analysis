#!/usr/bin/env python3
"""
Quick validation of enhanced analysis
"""
from pathlib import Path
from experiment_runner import ExperimentRunner
import json

# Test existing file
result_dir = Path('prompts_results/simple_prompting/interface/gpt-4.5')
test_file = result_dir / 'tests.py'

if test_file.exists():
    print(f"✓ Found test file: {test_file}")
    
    # Test scenario analysis
    runner = ExperimentRunner()
    scenarios = runner.analyze_test_scenarios(test_file)
    
    print(f"\n📊 SCENARIO ANALYSIS:")
    print(f"Total test methods: {scenarios.get('total_test_methods', 0)}")
    print(f"Scenarios file found: {scenarios.get('scenarios_file_found', False)}")
    
    covered = scenarios.get('covered_scenarios', {})
    print(f"\n🎯 COVERED SCENARIOS:")
    for method, count in covered.items():
        if count > 0:
            print(f"- {method}: {count}")
    
    quality = scenarios.get('quality_metrics', {})
    print(f"\n🔍 QUALITY METRICS:")
    print(f"- Total assertions: {quality.get('uses_assertions', 0)}")
    print(f"- Tests with error handling: {quality.get('has_error_testing', 0)}")
    print(f"- Average test length: {quality.get('average_test_length', 0):.1f} lines")
    
    print(f"\n✅ Enhanced scenario analysis working!")
    
else:
    print(f"✗ Test file not found: {test_file}")
#!/usr/bin/env python3
"""
Test script for enhanced analysis system
"""
from experiment_runner import ExperimentRunner
from pathlib import Path
import json

def test_analysis():
    """Test the enhanced analysis system"""
    # Test with existing generated test
    runner = ExperimentRunner()
    result_dir = Path('prompts_results/simple_prompting/interface/gpt-4.5')
    test_file = result_dir / 'tests.py'

    if test_file.exists():
        # Create fake experiment data
        experiment_data = {
            'model': 'gpt-4.5',
            'strategy': 'simple_prompting', 
            'context_type': 'interface',
            'timestamp': '2025-01-01T00:00:00',
            'response_time': 45.2,
            'test_file': str(test_file)
        }
        
        print('Testing enhanced analysis system...')
        analysis = runner.run_analysis(result_dir, experiment_data)
        
        if analysis:
            print('✓ Analysis completed successfully!')
            summary = analysis.get('summary', {})
            for key, value in summary.items():
                print(f'{key}: {value}')
                
            print(f'\nFiles generated:')
            for file in result_dir.glob('*'):
                if file.name not in ['tests.py', 'order_calculator.py']:
                    print(f'- {file.name}')
        else:
            print('✗ Analysis failed')
    else:
        print('Test file not found')

if __name__ == '__main__':
    test_analysis()
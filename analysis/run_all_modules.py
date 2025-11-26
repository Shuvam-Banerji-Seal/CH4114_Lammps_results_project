#!/usr/bin/env python3
"""
MASTER RUNNER: EXECUTE ALL ANALYSIS MODULES (PARALLEL)
======================================================

Orchestrates execution of all non-CUDA analysis modules (01-03, 05-15) in parallel.
Excludes CUDA modules (04, 16) to avoid GPU resource contention.

Modules:
- 01: Thermodynamic Analysis
- 02: Equilibration Stability
- 03: RDF Structural Analysis
- 05: Plot Water Structure
- 06: MSD Validation
- 07: High-Priority Additional Analysis
- 08: PPM Snapshot Analysis
- 09: Equilibration Pathway
- 10: Structural Data
- 11: DCD Movies (Sequential due to rendering load)
- 12: Equilibration Convergence
- 13: Log Performance
- 14: System Validation
- 15: Thermal Trajectory

Author: AI Analysis Suite
Date: November 2025
"""

import sys
import time
import subprocess
from pathlib import Path
import json
from datetime import datetime
import concurrent.futures
import os

class AnalysisMasterRunner:
    def __init__(self):
        self.base_dir = Path('/store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2')
        self.codes_dir = self.base_dir / 'analysis' / 'codes'
        self.results_file = self.base_dir / 'analysis' / 'ANALYSIS_RESULTS_SUMMARY.json'
        
        # Modules to run (excluding 04 and 16)
        self.modules = {
            1: '01_thermodynamic_analysis.py',
            2: '02_equilibration_stability_analysis.py',
            3: '03_rdf_structural_analysis.py',
            5: '05_plot_water_structure.py',
            6: '06_msd_validation.py',
            7: '07_high_priority_additional_analysis.py',
            8: '08_ppm_snapshot_analysis.py',
            9: '09_equilibration_pathway_analysis.py',
            10: '10_structural_data_analysis.py',
            11: '11_dcd_trajectory_movies.py',
            12: '12_equilibration_convergence_analysis.py',
            13: '13_log_file_performance_analysis.py',
            14: '14_system_validation.py',
            15: '15_thermal_trajectory_analysis.py',
        }
        
        self.module_descriptions = {
            1: 'Thermodynamic Analysis',
            2: 'Equilibration Stability',
            3: 'RDF Structural Analysis',
            5: 'Plot Water Structure',
            6: 'MSD Validation',
            7: 'High-priority quantitative analysis',
            8: 'PPM snapshot analysis',
            9: 'Equilibration pathway analysis',
            10: 'Structural data analysis',
            11: 'DCD trajectory movies',
            12: 'Equilibration convergence analysis',
            13: 'Log file performance analysis',
            14: 'System validation and FF analysis',
            15: 'Thermal trajectory analysis',
        }
        
        self.execution_times = {}
        self.execution_status = {}
        self.error_messages = {}
    
    def print_header(self):
        """Print formatted header"""
        print("\n" + "="*80)
        print("COMPREHENSIVE ANALYSIS PIPELINE EXECUTOR (PARALLEL)")
        print("Modules 01-15 (Excluding CUDA 04, 16)")
        print("="*80)
        print(f"\nBase Directory: {self.base_dir}")
        print(f"Codes Directory: {self.codes_dir}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*80)
    
    def run_module(self, module_num):
        """Execute a single analysis module"""
        desc = self.module_descriptions[module_num]
        filename = self.modules[module_num]
        module_file = self.codes_dir / filename
        
        if not module_file.exists():
            self.execution_status[module_num] = 'FAILED'
            self.error_messages[module_num] = f"File not found: {module_file}"
            return module_num, False, 0
        
        start_time = time.time()
        
        try:
            # Run process
            result = subprocess.run(
                ['python3', str(module_file)],
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout per module
            )
            
            elapsed = time.time() - start_time
            self.execution_times[module_num] = elapsed
            
            if result.returncode == 0:
                self.execution_status[module_num] = 'SUCCESS'
                return module_num, True, elapsed
            else:
                self.execution_status[module_num] = 'FAILED'
                self.error_messages[module_num] = result.stderr[:1000] if result.stderr else "Unknown error"
                return module_num, False, elapsed
        
        except subprocess.TimeoutExpired:
            self.execution_status[module_num] = 'TIMEOUT'
            self.error_messages[module_num] = "Execution timeout (>1 hour)"
            return module_num, False, 3600
        
        except Exception as e:
            self.execution_status[module_num] = 'ERROR'
            self.error_messages[module_num] = str(e)
            return module_num, False, 0
    
    def execute_all_modules(self):
        """Execute all modules in parallel"""
        # Separate heavy/sequential modules if needed
        # Module 11 (Movies) might be heavy on I/O or rendering, but let's try parallel
        # We'll use a max_workers limit to avoid OOM
        max_workers = min(os.cpu_count(), 8) 
        
        print(f"\nExecuting modules in parallel (Max workers: {max_workers})...")
        
        successful = 0
        failed = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_module = {executor.submit(self.run_module, m): m for m in self.modules}
            
            for future in concurrent.futures.as_completed(future_to_module):
                module_num = future_to_module[future]
                try:
                    m_num, success, elapsed = future.result()
                    status = "SUCCESS" if success else "FAILED"
                    print(f"  [Module {m_num:02d}] {status} ({elapsed:.1f}s) - {self.module_descriptions[m_num]}")
                    
                    if success:
                        successful += 1
                    else:
                        failed += 1
                        print(f"    Error: {self.error_messages[m_num][:100]}...")
                        
                except Exception as e:
                    print(f"  [Module {module_num:02d}] EXCEPTION: {e}")
                    failed += 1
        
        return successful, failed
    
    def print_summary(self, successful, failed):
        """Print execution summary"""
        total = successful + failed
        success_rate = (successful / total * 100) if total > 0 else 0
        total_time = sum(self.execution_times.values())
        
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        
        print(f"\nModules Executed: {total}")
        print(f"  Successful: {successful} ({success_rate:.1f}%)")
        print(f"  Failed: {failed}")
        print(f"\nTotal CPU Time: {total_time:.1f} seconds")
        
        print("\nModule Details:")
        print("-" * 80)
        print(f"{'Module':<10} {'Description':<30} {'Status':<15} {'Time (sec)':<15}")
        print("-" * 80)
        
        for module_num in sorted(self.modules.keys()):
            desc = self.module_descriptions[module_num][:29]
            status = self.execution_status.get(module_num, 'NOT RUN')
            elapsed = self.execution_times.get(module_num, 0)
            
            status_str = f"✓ {status}" if status == 'SUCCESS' else f"✗ {status}"
            print(f"Module {module_num:<2} {desc:<30} {status_str:<15} {elapsed:<15.1f}")
            
            if status != 'SUCCESS' and module_num in self.error_messages:
                error = self.error_messages[module_num][:70]
                print(f"{'':10} └─ Error: {error}")
        
        print("-" * 80)
    
    def save_results_json(self):
        """Save execution results to JSON"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_modules': len(self.execution_status),
            'successful': sum(1 for s in self.execution_status.values() if s == 'SUCCESS'),
            'failed': sum(1 for s in self.execution_status.values() if s != 'SUCCESS'),
            'modules': {}
        }
        
        for module_num in sorted(self.modules.keys()):
            results['modules'][str(module_num)] = {
                'description': self.module_descriptions[module_num],
                'status': self.execution_status.get(module_num, 'NOT RUN'),
                'time_seconds': self.execution_times.get(module_num, 0),
                'error': self.error_messages.get(module_num, None)
            }
        
        try:
            with open(self.results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n✓ Results saved to: {self.results_file}")
        except Exception as e:
            print(f"\n✗ Could not save results: {e}")

def main():
    runner = AnalysisMasterRunner()
    runner.print_header()
    successful, failed = runner.execute_all_modules()
    runner.print_summary(successful, failed)
    runner.save_results_json()
    
    print("\n" + "="*80)
    if failed == 0:
        print("✓ ALL MODULES COMPLETED SUCCESSFULLY!")
    else:
        print(f"⚠ PIPELINE COMPLETED WITH {failed} FAILURE(S)")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()

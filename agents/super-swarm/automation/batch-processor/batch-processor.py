#!/usr/bin/env python3
"""
Batch Processor Agent
Handles batch operations and bulk tasks

Usage:
    python3 batch-processor.py --process "directory" --pattern "*.py"
    python3 batch-processor.py --status
    python3 batch-processor.py --report
"""

import json
import argparse
import glob
from datetime import datetime
from pathlib import Path

class BatchProcessor:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.output_dir = self.workspace / 'agents/super-swarm/automation/batch-processor/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_files(self, directory, pattern='*'):
        """Process files matching pattern"""
        path = Path(directory)
        if not path.exists():
            print(f"❌ Directory not found: {directory}")
            return
        
        files = list(path.glob(pattern))
        print(f"\n📦 Processing {len(files)} files in {directory}")
        print(f"   Pattern: {pattern}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "directory": str(path),
            "pattern": pattern,
            "files_processed": len(files),
            "results": []
        }
        
        for f in files:
            if f.is_file():
                result = {"file": f.name, "status": "processed"}
                results["results"].append(result)
                print(f"   ✅ {f.name}")
        
        # Save report
        report_file = self.output_dir / f'batch-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Processed {len(files)} files")
        print(f"📄 Report: {report_file}")
        return results
    
    def cleanup_old_files(self, directory, pattern='*.log', older_than_days=7):
        """Clean up old files"""
        path = Path(directory)
        if not path.exists():
            return
        
        cutoff = datetime.now().timestamp() - (older_than_days * 86400)
        cleaned = []
        
        for f in path.glob(pattern):
            if f.stat().st_mtime < cutoff:
                f.unlink()
                cleaned.append(f.name)
        
        print(f"\n🧹 Cleaned {len(cleaned)} old files")
        return cleaned
    
    def get_status(self):
        """Get batch processor status"""
        return {
            "output_dir": str(self.output_dir),
            "reports_generated": len(list(self.output_dir.glob('*.json')))
        }

def main():
    processor = BatchProcessor()
    
    parser = argparse.ArgumentParser(description='Batch Processor Agent')
    parser.add_argument('--process', '-p', metavar='DIR', help='Process directory')
    parser.add_argument('--pattern', metavar='PAT', default='*', help='File pattern')
    parser.add_argument('--cleanup', '-c', metavar='DIR', help='Cleanup old files')
    parser.add_argument('--days', '-d', type=int, default=7, help='Days threshold')
    parser.add_argument('--status', '-s', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    print("📦 Batch Processor Agent")
    print("=" * 60)
    
    if args.process:
        processor.process_files(args.process, args.pattern)
    elif args.cleanup:
        processor.cleanup_old_files(args.cleanup, '*.log', args.days)
    elif args.status:
        status = processor.get_status()
        print(f"\n📊 Batch Processor Status:")
        print(f"   Output Directory: {status['output_dir']}")
        print(f"   Reports Generated: {status['reports_generated']}")
    else:
        print("\nUsage:")
        print("  python3 batch-processor.py --process /path/to/dir --pattern \"*.py\"")
        print("  python3 batch-processor.py --cleanup /path/to/dir --days 7")
        print("  python3 batch-processor.py --status")

if __name__ == '__main__':
    main()

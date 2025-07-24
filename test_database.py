#!/usr/bin/env python3
"""
Test script to check database contents
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from impl import Datastore

def test_database():
    """Test if the database contains data"""
    try:
        datastore = Datastore()
        
        # Check if table exists and has data
        table = datastore.table
        count = table.count_rows()
        print(f"📊 Database contains {count} rows")
        
        if count > 0:
            # Get a sample of data
            sample = table.to_pandas().head(3)
            print("\n📄 Sample data:")
            for i, row in sample.iterrows():
                print(f"Row {i}:")
                print(f"  Source: {row['source']}")
                print(f"  Content preview: {row['content'][:100]}...")
                print()
        else:
            print("❌ Database is empty!")
            
        return count > 0
        
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        return False

if __name__ == "__main__":
    test_database() 
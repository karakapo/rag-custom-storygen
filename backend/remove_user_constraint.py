#!/usr/bin/env python3
"""
Remove foreign key constraint for author_id in stories table.
This allows storing stories without requiring a users table.
"""

from sqlalchemy import text
from database import db

def remove_user_constraint():
    """Remove the foreign key constraint for author_id"""
    try:
        print("Removing foreign key constraint for author_id...")
        
        with db.get_session() as session:
            # Get the constraint name
            result = session.execute(text("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'stories' 
                AND constraint_type = 'FOREIGN KEY'
                AND constraint_name LIKE '%author_id%'
            """))
            
            constraint = result.fetchone()
            if constraint:
                constraint_name = constraint[0]
                print(f"Found foreign key constraint: {constraint_name}")
                
                # Remove the foreign key constraint
                session.execute(text(f"""
                    ALTER TABLE stories 
                    DROP CONSTRAINT {constraint_name}
                """))
                print("Foreign key constraint removed successfully.")
            else:
                print("No foreign key constraint found for author_id.")
            
            # Commit the changes
            session.commit()
            print("Database schema updated successfully!")
            
    except Exception as e:
        print(f"Error removing constraint: {str(e)}")
        session.rollback()
        raise

if __name__ == "__main__":
    remove_user_constraint() 
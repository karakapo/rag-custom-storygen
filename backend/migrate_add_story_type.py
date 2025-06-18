#!/usr/bin/env python3
"""
Migration script to add story_type column to existing stories table.
This script will:
1. Add the story_type column with a default value
2. Update existing stories to have appropriate story_type based on their generation_model
"""

import os
import sys
from sqlalchemy import text
from database import db
from models import Story, StoryType

def migrate_add_story_type():
    """Add story_type column and update existing stories"""
    try:
        print("Starting migration: Adding story_type column...")
        
        with db.get_session() as session:
            # Check if story_type column already exists
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'stories' AND column_name = 'story_type'
            """))
            
            if result.fetchone():
                print("story_type column already exists. Skipping column creation.")
            else:
                # Add story_type column
                print("Adding story_type column...")
                session.execute(text("""
                    ALTER TABLE stories 
                    ADD COLUMN story_type VARCHAR(20) DEFAULT 'rag' NOT NULL
                """))
                print("story_type column added successfully.")
            
            # Update existing stories based on their generation_model
            print("Updating existing stories with appropriate story_type...")
            
            # Update RAG stories (those with generation_model like 'gemini' or null)
            session.execute(text("""
                UPDATE stories 
                SET story_type = 'rag' 
                WHERE generation_model IS NULL 
                   OR generation_model LIKE '%gemini%'
                   OR generation_model LIKE '%gpt%'
                   OR generation_model LIKE '%claude%'
            """))
            
            # Update Free Writer stories (those with generation_model = 'free_writer')
            session.execute(text("""
                UPDATE stories 
                SET story_type = 'free_writer' 
                WHERE generation_model = 'free_writer'
            """))
            
            # Commit the changes
            session.commit()
            
            # Verify the migration
            total_stories = session.query(Story).count()
            rag_stories = session.query(Story).filter(Story.story_type == StoryType.RAG).count()
            free_writer_stories = session.query(Story).filter(Story.story_type == StoryType.FREE_WRITER).count()
            
            print(f"Migration completed successfully!")
            print(f"Total stories: {total_stories}")
            print(f"RAG stories: {rag_stories}")
            print(f"Free Writer stories: {free_writer_stories}")
            
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        session.rollback()
        raise

if __name__ == "__main__":
    migrate_add_story_type() 
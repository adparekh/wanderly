import os
import datetime

def export_trip(markdown_content: str, directory: str = "./output"):
    """Export travel plan to Markdown file with proper formatting"""
    os.makedirs(directory, exist_ok=True)

    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{directory}/AI_Trip_Planner_{timestamp}.md"

        print(filename)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        print(f"Markdown file saved as: {filename}")
        return filename
    
    except Exception as e:
        print(f"Error saving markdown file: {e}")
        return None
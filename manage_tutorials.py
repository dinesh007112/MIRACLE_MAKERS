import os
import json
from exercise_dataset import EXERCISE_DATASET, AREA_MODIFICATIONS

def get_all_exercises():
    exercises = set()
    
    # Get exercises from main dataset
    for disability in EXERCISE_DATASET.values():
        for level in disability.values():
            for goal in level.values():
                if 'schedule' in goal:
                    for day in goal['schedule'].values():
                        exercises.update(day)
                elif 'exercises' in goal:
                    exercises.update(goal['exercises'])
    
    # Get exercises from area modifications
    for area in AREA_MODIFICATIONS.values():
        exercises.update(area['exercises'])
    
    return sorted(list(exercises))

def generate_tutorial_placeholder(exercise):
    """Generate a placeholder video filename for an exercise."""
    return exercise.lower().replace(' ', '_').replace(':', '').replace('(', '').replace(')', '').replace('-', '_')

def create_tutorial_manifest():
    """Create a manifest file listing all required tutorial videos."""
    exercises = get_all_exercises()
    manifest = {
        'exercises': [
            {
                'name': exercise,
                'video_file': f"{generate_tutorial_placeholder(exercise)}.mp4",
                'status': 'needed'
            }
            for exercise in exercises
        ]
    }
    
    with open('static/tutorials/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

def check_tutorial_status():
    """Check which tutorial videos are present and which are missing."""
    with open('static/tutorials/manifest.json', 'r') as f:
        manifest = json.load(f)
    
    for exercise in manifest['exercises']:
        video_path = os.path.join('static/tutorials', exercise['video_file'])
        if os.path.exists(video_path):
            exercise['status'] = 'present'
        else:
            exercise['status'] = 'missing'
    
    with open('static/tutorials/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest

if __name__ == '__main__':
    # Create tutorials directory if it doesn't exist
    os.makedirs('static/tutorials', exist_ok=True)
    
    # Generate manifest file
    create_tutorial_manifest()
    
    # Check status of tutorial videos
    manifest = check_tutorial_status()
    
    # Print status
    print("\nExercise Tutorial Status:")
    print("-" * 50)
    present = sum(1 for e in manifest['exercises'] if e['status'] == 'present')
    missing = sum(1 for e in manifest['exercises'] if e['status'] == 'missing')
    print(f"Total exercises: {len(manifest['exercises'])}")
    print(f"Present tutorials: {present}")
    print(f"Missing tutorials: {missing}")
    
    if missing > 0:
        print("\nMissing Tutorials:")
        for exercise in manifest['exercises']:
            if exercise['status'] == 'missing':
                print(f"- {exercise['name']}")
                print(f"  Video file needed: {exercise['video_file']}") 
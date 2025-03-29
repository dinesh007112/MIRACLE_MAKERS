import random
import json
import sys

class FitnessAI:
    def __init__(self):
        self.user_data = {}
        self.workout_plans = {
            'beginner': {
                'cardio': ['Walking', 'Light jogging', 'Swimming'],
                'strength': ['Push-ups', 'Squats', 'Planks'],
                'duration': '20-30 minutes'
            },
            'intermediate': {
                'cardio': ['Running', 'Cycling', 'HIIT'],
                'strength': ['Pull-ups', 'Deadlifts', 'Bench press'],
                'duration': '45-60 minutes'
            },
            'advanced': {
                'cardio': ['Sprinting', 'CrossFit', 'Circuit training'],
                'strength': ['Olympic lifts', 'Complex movements', 'Advanced calisthenics'],
                'duration': '60-90 minutes'
            }
        }
        self.health_tips = [
            "Stay hydrated throughout the day.",
            "Aim for 7-9 hours of quality sleep.",
            "Maintain a balanced diet with protein, carbs, and healthy fats.",
            "Warm up before each workout.",
            "Cool down after exercising.",
            "Listen to your body and take rest days."
        ]
        self.nutrition_advice = {
            'pre_workout': [
                "Consume a light meal 1-2 hours before exercise.",
                "Focus on complex carbohydrates and lean protein.",
                "Avoid high-fat foods before workouts.",
                "Stay well-hydrated."
            ],
            'post_workout': [
                "Consume protein within 30 minutes of finishing your workout.",
                "Include simple carbohydrates for rapid recovery.",
                "Replenish electrolytes after intense workouts.",
                "Continue to hydrate."
            ],
            'general': [
                "Aim for 0.8-1g of protein per kilogram of body weight.",
                "Include a variety of vegetables in your daily diet.",
                "Choose whole grains over processed grains.",
                "Limit your intake of processed foods and added sugars."
            ]
        }
        self.exercise_descriptions = {
            'push-ups': "A compound exercise for chest, shoulders, and triceps. Keep your back straight and elbows close to the body.",
            'squats': "A fundamental lower body exercise. Ensure knees track over toes and maintain a straight back.",
            'planks': "A core strengthening exercise. Maintain a straight line from head to heels.",
            'pull-ups': "An upper body exercise targeting the back and biceps. Pull your chin above the bar.",
            'deadlifts': "A compound exercise for back and legs. Maintain a straight back and lift using your legs."
        }

    def get_response(self, user_input, user_id):
        user_input = user_input.lower()
        if user_id not in self.user_data:
            self.user_data[user_id] = {'fitness_level': None, 'goals': None}

        if any(word in user_input for word in ['hi', 'hello', 'hey']):
            return "Hello! I'm your Fitness AI assistant. How can I assist you today?"

        if 'fitness level' in user_input or 'experience' in user_input:
            return "To tailor recommendations, please specify your fitness level: beginner, intermediate, or advanced."

        if 'workout' in user_input or 'exercise' in user_input:
            if self.user_data[user_id]['fitness_level']:
                level = self.user_data[user_id]['fitness_level']
                plan = self.workout_plans[level]
                response = f"Here's a {level} workout plan:\n"
                response += f"Cardio: {', '.join(plan['cardio'])}\n"
                response += f"Strength: {', '.join(plan['strength'])}\n"
                response += f"Duration: {plan['duration']}\n"
                response += "Would you like exercise descriptions?"
                return response
            else:
                return "Please tell me your fitness level first."

        for exercise, description in self.exercise_descriptions.items():
            if exercise in user_input:
                return f"{exercise.capitalize()} instructions:\n{description}"

        if 'nutrition' in user_input or 'diet' in user_input:
            if 'pre workout' in user_input:
                return "Pre-workout nutrition advice:\n" + "\n".join(self.nutrition_advice['pre_workout'])
            elif 'post workout' in user_input:
                return "Post-workout nutrition advice:\n" + "\n".join(self.nutrition_advice['post_workout'])
            else:
                return "General nutrition advice:\n" + "\n".join(self.nutrition_advice['general'])

        if 'tip' in user_input or 'advice' in user_input:
            return random.choice(self.health_tips)

        if any(level in user_input for level in ['beginner', 'intermediate', 'advanced']):
            for level in ['beginner', 'intermediate', 'advanced']:
                if level in user_input:
                    self.user_data[user_id]['fitness_level'] = level
                    return f"Fitness level set to {level}. How can I assist you further?"

        if 'goal' in user_input:
            if 'weight loss' in user_input:
                self.user_data[user_id]['goals'] = 'weight_loss'
                return "For weight loss, focus on calorie deficit, cardio, strength training, and hydration. Would you like a workout plan?"
            elif 'muscle' in user_input or 'strength' in user_input:
                self.user_data[user_id]['goals'] = 'strength'
                return "For strength, prioritize progressive overload, compound exercises, adequate protein, and rest. Would you like a workout plan?"

        if 'recovery' in user_input or 'rest' in user_input:
            return "Recovery tips: 7-9 hours of sleep, hydration, protein, stretching, rest days, and foam rolling."

        return "I can help with workout plans, exercise descriptions, nutrition advice, health tips, setting fitness levels, and goals. What would you like to know?"

    def save_user_data(self):
        with open('user_data.json', 'w') as f:
            json.dump(self.user_data, f)

    def load_user_data(self):
        try:
            with open('user_data.json', 'r') as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            self.user_data = {}

def main():
    try:
        ai_assistant = FitnessAI()
        print("Welcome to your Fitness AI assistant!")
        print("How can I help you today?")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() == 'quit':
                    print("Thank you for using the Fitness AI assistant!")
                    ai_assistant.save_user_data()
                    break
                response = ai_assistant.get_response(user_input, "default_user")
                print("AI:", response)
            except KeyboardInterrupt:
                print("\nThank you for using the Fitness AI assistant!")
                ai_assistant.save_user_data()
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please try again or type 'quit' to exit")
    except Exception as e:
        print(f"Failed to initialize assistant: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
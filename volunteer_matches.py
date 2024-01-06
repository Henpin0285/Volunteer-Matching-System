from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

class Volunteer:
    def __init__(self, name, skills, availability):
        self.name = name
        self.skills = skills
        self.availability = availability

class Task:
    def __init__(self, name, required_skills, schedule):
        self.name = name
        self.required_skills = required_skills
        self.schedule = schedule

def match_volunteers_to_tasks(volunteers, tasks, skills_threshold=0.25):
    matches = []

    for task in tasks:
        for volunteer in volunteers:
            print(f"Checking {volunteer.name} for {task.name}...")
            print(f"Volunteer skills: {volunteer.skills}")
            print(f"Task required skills: {task.required_skills}")
            print(f"Volunteer availability: {volunteer.availability}")
            print(f"Task schedule: {task.schedule}")

            volunteer_skills = set(volunteer.skills[0].split(', '))  # Split the string into individual skills
            task_required_skills = set(task.required_skills)

            # Calculate the minimum number of skills required for a match
            min_skills_required = int(len(task_required_skills) * skills_threshold)

            # Check if the volunteer has at least the required percentage of skills
            skills_match = len(task_required_skills.intersection(volunteer_skills)) >= min_skills_required
            availability_match = any(day in volunteer.availability for day in task.schedule)

            print(f"Individual Volunteer skills: {volunteer_skills}")
            print(f"Skills match: {skills_match}")
            print(f"Availability match: {availability_match}")

            if skills_match and availability_match:
                match = {"Volunteer": volunteer.name, "Task": task.name}
                matches.append(match)
                print(f"Match found: {volunteer.name} is matched with {task.name}")
                break

    return matches

@app.route('/', methods=['GET', 'POST'])
def index():
    volunteer = None
    matches = None

    if request.method == 'POST':
        # Retrieve volunteer data from the form
        volunteer_data = {
            "name": request.form['volunteer_name'],
            "skills": request.form.getlist('volunteer_skills'),
            "availability": request.form.getlist('volunteer_availability')
        }
        print("Form data received:", volunteer_data)

        # Create a Volunteer instance
        volunteer = Volunteer(**volunteer_data)

        # Task data (you can extend this based on your needs)
        tasks = [
            Task("Customer Service", ["Communication", "Patience", "Tenacity", "Positive"], ["Monday", "Wednesday", "Thursday"]),
            Task("Dispatcher", ["Multitasking", "Proactive", "Organization", "Adaptability"], ["Tuesday", "Thursday"]),
            Task("Order Packaging", ["Attention to Detail", "Teamwork", "Quality Control", "Problem Solving"], ["Monday", "Wednesday"])
        ]

        # Match volunteers to tasks
        matches = match_volunteers_to_tasks([volunteer], tasks)

    return render_template('index.html', volunteer=volunteer, matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
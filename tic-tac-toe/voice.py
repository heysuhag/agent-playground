import subprocess


class Voice:

    def __init__(self, gender: str = "male"):
        self.voice = "Kate (Enhanced)" if gender.lower() == "female" else "Daniel (Enhanced)"

    def speak(self, reasoning: str) -> None:
        subprocess.run(["say", "-v", self.voice, reasoning])



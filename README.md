# Pixel People Optimal Assignments

Pixel People is a game where you splice two different jobs together to get a new job. And each new job can unlock new buildings for them to work at. But as there are more than 400 jobs, it gets hard to keep track of how much each makes. And what is the best way for you to make money?

## Attempted solutions:
* Naive approach: Just put people into random allowed jobs and permutate until we get the right answer.
* * This will be very slow. Assuming that each job can go into a maximum of 3 jobs, that would be a space complexity of O(3^n), where n is 430. So let's not.

## Current Solution: Priority queue iterating through 2m buildings.
Problem: We don't currently have a way to determine if two buildings of a lower CPS can surpass one building of a higher CPS (ex. 6 < 4 + 4).
For now, I want to write tests, so I will prioritize larger CPS buildings for now, then go back to think of a solution later.
I am also going to switch back to python.
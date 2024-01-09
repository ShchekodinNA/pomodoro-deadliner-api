# pomodoro-deadliner-api
## What is about
That software helps people to control all they tasks to achive better performance in work and study.
Also here lies logic to bind tasks with [pomodoros](https://en.wikipedia.org/wiki/Pomodoro_Technique) for understanding amount of time, that needed for finishing tasks.
## Installation
1. Install python on your machine/server
2. Extract code from archive or pull by git
3. Create venv (all based on pip)
4. Install requirements
  ```bash
  $ pip install -r requirements.txt
  ```

6. Start project with uvicorn/unicorn
```
  $ uvicorn src.main:app --reload
```
Task control.
App, based on CRUD principle to manipulate tasks and their groups

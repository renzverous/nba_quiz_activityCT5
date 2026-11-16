# nba_quiz_activityCT5
HoopsMaster - NBA Trivia Quiz Application
 
John Renzver Genova

BS Infotech SE-3A

NBA Trivia Challenge
 
Features Completed
* 10 multiple-choice questions
* Random question order
* 15-second countdown timer
* Answer checking and time-out handling
* Score and percentage calculation
* Answer review of missed questions
* High score saved in a text file (high_score.txt)
* Working restart button
* Custom dark NBA-themed interface
 
 How the Questions Are Stored and Shuffled
	
The questions are stored inside a Python list of dictionaries, where each dictionary holds the question text, a list of four choices, and the correct answer letter. When the quiz starts, random.sample() generates a shuffled copy of the questions so they appear in a new order every time.
 
How the Timer Works

The timer uses root.after(1000, run_countdown) to call the countdown function every second without freezing the Tkinter window. When an answer is submitted or time runs out, root.after_cancel() immediately stops the timer job.
 
 How the Program Identifies the Correct Answer
	
The program compares the user's selected letter from selected_option.get() against the stored "answer" key in the active question dictionary. If they match, 1 point is added; otherwise, the question and user choice are logged into the review list.
 
 How the Score and High Score Work
	
The score increments by 1 for each correct answer, and the percentage is calculated as `(score / total) * 100`. The program reads high_score.txt using Python file handling; if the new score beats the saved record, it overwrites the text file so the score persists even after closing the app.
 
Function Explanations

 `begin_quiz()` Resets variables, score, and shuffles questions
	
 `run_countdown()`  Updates time left and counts down every second
	
 `check_answer()`  Validates user choice, updates score, and shows feedback
	
 `update_high_score()` Writes score to high_score.txt if it is a new record 
	
 `show_results_screen()`  Displays final score, percentage, remarks, and review 
 
Challenges I Faced

Managing the timer loop asynchronously in Tkinter without freezing the UI was tricky. This was successfully resolved by properly tracking active timer IDs with root.after_cancel() upon submission or window closure.

from script import run_interview_scorer

conversation = input("Enter the entire conversation dialogue:\n")
scores = run_interview_scorer(conversation, checkpoint_path="checkpoint1.pth")

print(scores)
import torch

def calculate_feedback(predicted_scores, actual_scores):
    feedback_list = []
    score_labels = ["Overall Score", "Recommendation Score", "Structured Answers Score"]
    
    # Loop over each sample in the batch
    for idx in range(predicted_scores.size(0)):
        feedback = {}
        feedback_text = []
        
        for i, label in enumerate(score_labels):
            pred = predicted_scores[idx, i].item()
            actual = actual_scores[idx, i].item()
            diff = actual - pred
            
            feedback[label] = pred  # Store the predicted score for each label
            
            # Generate specific feedback based on the difference
            if abs(diff) > 1.0:
                if diff > 0:
                    feedback_text.append(f"Needs improvement in {label.lower()} as it was scored lower than expected.")
                else:
                    feedback_text.append(f"Good performance in {label.lower()} compared to the expected score.")
            else:
                feedback_text.append(f"Acceptable performance in {label.lower()}.")
        
        feedback["Feedback"] = " | ".join(feedback_text) if feedback_text else "Good overall performance!"
        feedback_list.append(feedback)
    
    return feedback_list


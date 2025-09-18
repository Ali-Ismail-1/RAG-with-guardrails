# monitoring/evals.py
def record_feedback(session_id: str, question: str, answer: str, rating: int):
    """
    Record feedback for a chat interaction
    rating: +1 (helpful), 0 (neutral), -1 (not helpful)
    """
    # TODO: Implement feedback recording
    print(f"Feedback recorded: Session ID: {session_id}, rating: {rating}, Q: {question}, A: {answer[:50]}")
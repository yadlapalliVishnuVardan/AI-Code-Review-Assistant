def calculate_quality_score(analysis):

    score = 100

    # Invalid syntax
    if analysis["syntax"] == "Invalid":
        return 0

    # Time complexity penalty
    complexity = analysis["time_complexity"]

    if complexity == "O(n²)":
        score -= 10

    elif complexity == "O(n³)":
        score -= 20

    elif complexity.startswith("O(n^"):
        score -= 30

    # Code smell penalty
    number_of_smells = len(analysis["code_smells"])

    score -= number_of_smells * 10

    # Too many lines
    if analysis["lines"] > 100:
        score -= 5

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    return score
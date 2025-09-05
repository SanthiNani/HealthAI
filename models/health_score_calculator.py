def calculate_health_score(visit):
    """
    Calculate a health score based on vitals and symptoms.
    Returns an integer score between 0 and 100.
    """

    score = 100  # Start with perfect health

    # Blood Pressure
    bp = visit.get("bp", "0/0")
    try:
        systolic, diastolic = map(int, bp.split("/"))
        if systolic > 130 or diastolic > 85:
            score -= 10
        elif systolic < 90 or diastolic < 60:
            score -= 10
    except:
        score -= 5  # Penalize if BP is not properly formatted

    # Pulse
    pulse = visit.get("pulse", 0)
    if pulse > 100 or pulse < 60:
        score -= 5

    # Temperature
    temp = visit.get("temperature", 36.5)
    if temp > 38 or temp < 35:
        score -= 10

    # Symptoms
    symptoms = visit.get("symptoms", "").lower()
    common_symptoms = ["fever", "cough", "headache", "pain", "cold", "vomiting", "dizziness"]
    for symptom in common_symptoms:
        if symptom in symptoms:
            score -= 2

    # Cap at a minimum of 0
    return max(score, 0)

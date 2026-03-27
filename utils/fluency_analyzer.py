def calculate_wpm(transcript, start_time, end_time):
    words = transcript.split()
    word_count = len(words)

    duration_seconds = end_time - start_time

    if duration_seconds <= 0:
        return 0

    minutes = duration_seconds / 60

    return round(word_count / minutes)


def estimate_pauses(transcript, duration_seconds):
    words = transcript.split()
    word_count = len(words)

    if duration_seconds == 0:
        return 0

    # Expected speaking rate ~130 WPM
    expected_words = (duration_seconds / 60) * 130

    # If actual words << expected → more pauses
    gap = expected_words - word_count

    pauses = max(0, int(gap // 10))  # every 10 missing words ≈ 1 pause

    return pauses


def fluency_score(wpm, pauses):
    score = 10

    # WPM check
    if wpm < 90:
        score -= 2
    elif wpm > 180:
        score -= 1

    # Pause penalty
    score -= pauses * 0.5

    return max(3, round(score))
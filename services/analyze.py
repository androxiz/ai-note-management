from fastapi import HTTPException
from sqlalchemy.orm import Session
from collections import Counter
import numpy as np
import re

from db.models import DbNote


def analyze_notes(db: Session):
    notes = db.query(DbNote).all()

    if not notes:
        raise HTTPException(status_code=404, detail="No notes found")

    word_counts = []
    note_lengths = []
    all_words = []

    for note in notes:
        words = re.findall(r'\b\w+\b', note.description.lower())
        word_counts.append(len(words))
        note_lengths.append((note.title, len(words)))
        all_words.extend(words)

    total_word_count = sum(word_counts)

    avg_note_length = np.mean(word_counts) if word_counts else 0

    note_lengths.sort(key=lambda x: x[1])
    shortest_notes = note_lengths[:3]
    longest_notes = note_lengths[-3:]

    common_words = Counter(all_words).most_common(5)

    return {
        "total_word_count": total_word_count,
        "average_note_length": avg_note_length,
        "most_common_words": common_words,
        "top_3_shortest_notes": shortest_notes,
        "top_3_longest_notes": longest_notes,
    }
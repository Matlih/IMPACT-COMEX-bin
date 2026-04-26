def get_detected_labels(results, names, min_confidence):
    detected_labels = set()

    for result in results:
        for box in result.boxes:
            confidence = float(box.conf[0])
            if confidence < min_confidence:
                continue

            class_index = int(box.cls[0])
            detected_labels.add(names[class_index])

    return detected_labels

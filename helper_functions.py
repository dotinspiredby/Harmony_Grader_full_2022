from music21 import stream


def output_name(voiced_score: stream.Score) -> list:
    """ voice identifier by detecting unknown staff names
    and picking the valid ones"""
    names = []
    instrument_obj = voiced_score.recurse().getElementsByClass(stream.Part)
    for n in instrument_obj:
        try:
            int(n.id[:-3])
        except ValueError:
            names.append(n.id)
    return names


def order_by_offset(part: stream.Part, measure_number, offset):
    """ finds the note by offset and the measure given """
    obj = part.measure(measure_number)
    try:
        to_find = obj.getElementsByOffset(offset, mustBeginInSpan=False)  # sometimes returns rests
        return list(to_find.notes)
    except IndexError:
        # offset may not exist - the note is longer, rested or out of range
        return None

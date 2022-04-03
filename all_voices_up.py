from music21 import stream
from helper_functions import output_name, order_by_offset


from logging import getLogger


class VoiceUpDetector:
    def __init__(self, score: stream.Score):
        self.logger = getLogger(" ALL-VOICE-TO-SAME-DIRECTION DETECTOR ")
        self.score = score
        self.staff_names = output_name(self.score)

    def run(self) -> None:
        """ runs the checker manager"""
        number_of_measures = self.get_measure_count()
        self.manage_extract_offsets(number_of_measures)

    def get_measure_count(self) -> int:
        """ returns the number of measures"""
        return len(self.score.measureOffsetMap())

    def manage_extract_offsets(self, number_of_measures: int) -> None:
        """ manages checking measure by measure """
        for m in range(number_of_measures):
            measure_at_staves = self.score.measure(m + 1)
            # while using in score searches, it's essential to use m+1, as measure=0 doesn't exist
            offsets = self.get_note_offsets(measure_at_staves)
            # print(f"measure {m+1}", offsets)
            common_offsets = self.check_simultaneous_note_change(offsets)
            # print(f"measure {m+1}", common_offsets)
            self.check_equal_direction(common_offsets, m + 1)

    def get_note_offsets(self, measure: stream.Measure) -> dict:
        """ returns offsets for each measure """
        offset_map_measure = {}
        staves = measure.getElementsByClass(stream.Part)
        for staff in staves.elements:
            i = staff.getElementsByClass(stream.Measure)[0]
            offsets = [note.offset for note in i.notes]
            offset_map_measure[staff.id] = offsets
        return offset_map_measure

    def find_common_offsets(self, voice_a: set, voice_b: set) -> set:
        """ return common offsets for two sets given """
        return voice_a & voice_b

    def check_simultaneous_note_change(self, measure_offset_map: dict) -> list:
        """ identifies set of common offsets for all voices by pair iterating """
        common_offsets = set()
        for name_index in range(len(self.staff_names) - 1):
            id_a = self.staff_names[name_index]
            id_b = self.staff_names[name_index + 1]
            voice_a = set(measure_offset_map[id_a])
            voice_b = set(measure_offset_map[id_b])
            common_offsets = self.find_common_offsets(voice_a, voice_b)
            # print(id_a, id_b, measure_number, common_offsets)
            if len(common_offsets) == 0:
                break
        return list(common_offsets)

    def find_previous_note(self, staff: stream.Part, offset: float, measure_number: int):
        """ finds previous offset to the origin one """
        previous_note = None
        if offset == 0.0:
            if measure_number != 1:
                try:
                    previous_measure_notes = [*staff.measure(measure_number - 1).notes]
                    previous_note = previous_measure_notes[-1]

                except IndexError:
                    pass
                    # this is the case when nothing is met at the verge of measures, by the main note at 0.0
                    # print(staff.id, measure_number, offset, previous_note, " PREVIOUS ERROR ")
            else:
                return None
        else:
            try:
                measure_notes = staff.measure(measure_number).getElementsByOffset(0.0, offset, mustBeginInSpan=False)
                previous_note = measure_notes[-2]

            except IndexError:
                pass
                # this is case when the long note as half/whole/etc. is met, which is still sounding
                # print(staff.id, measure_number, offset, previous_note, " PREVIOUS ERROR")
        try:
            previous_note = previous_note.pitch.midi
        except AttributeError:
            # case when previous_note is identified as None or note.Rest
            # print(staff.id, measure_number, offset, " ERROR HERE ")
            previous_note = None
        # print(staff.id, measure_number, offset, previous_note, " PREVIOUS")
        return previous_note

    def check_equal_direction(self, common_offsets: list, measure_number: int):
        """ checks the same direction for all voices at the particular offset """
        direction = None
        for common_offset in common_offsets:
            for staff in self.staff_names:  # for each staff
                note = order_by_offset(self.score[staff], measure_number, common_offset)  # the note by offset is picked
                # print(staff, measure_number, common_offset, note)

                if note:  # if it's not rested or simply None
                    note = note[0].pitch.midi  # identify the pitch
                    # print(staff, measure_number, common_offset, note)
                    previous_note = self.find_previous_note(self.score[staff], common_offset, measure_number)
                    # then find previous note - left neighbor already in MIDI pitch otherwise None
                    if previous_note:  # if it's not None
                        if note - previous_note < 0:  # compare left neighbor with the origin offset note by midi values
                            current_direction = "down"
                        elif note - previous_note > 0:
                            current_direction = "up"
                        else:
                            current_direction = "no"
                        if direction is not None:  # in case we are not at the first iteration
                            if direction != current_direction:
                                # if at least one of the voices looped gave another direction
                                direction = None
                                break
                        else:
                            direction = current_direction  # first iteration case
                    else:  # if the previous note is None
                        direction = None
                        break
                else:  # if origin offset note is None
                    direction = None
                    break
            if direction:
                self.logger.info(
                    f" all voices followed the same direction to note "
                    f"position {common_offset} in measure {measure_number}"
                )

                # with open("log.txt", "a", encoding='utf-8') as log_file:
                #     log_file.write(f"all voices followed the same direction to note "
                #                    f"position {common_offset} in measure {measure_number}"+'\n')

                # print(f"all voices followed the same direction to "
                #       f"note position {common_offset} in measure {measure_number}")

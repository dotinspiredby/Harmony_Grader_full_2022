# nothing to import


class Superposer:
    def __init__(self, intervals_up_down: list, intervals_down_up: list):
        self.intervals_up_down = intervals_up_down
        self.intervals_down_up = intervals_down_up
        self.interval_list = []
        self.interval_list_offset = []
        self.beats = []

    def fill_interval_list_and_beats(self):
        """ increasing beat_num is used to navigate in beats across the piece"""
        beat_num = 0
        for cell in range(len(self.intervals_up_down)):  # вписать контекст
            measure = []
            measure_offset = []
            measure_paired = self.__superpose(self.intervals_down_up[cell], self.intervals_up_down[cell])

            if measure_paired is not None:
                for pair in measure_paired:
                    measure.append(pair[0])
                    measure_offset.append(pair[1])

                beat_num += len(measure)
            else:
                pass
            self.interval_list.append(measure)
            self.interval_list_offset.append(measure_offset)
            self.beats.append(beat_num)

    def __superpose(self, list_a, list_b):
        set_superposed = set()
        try:
            for item in list_a:
                set_superposed.add(item)
            for item in list_b:
                set_superposed.add(item)
            to_return = list(set_superposed)
            to_return.sort(key=lambda x: x[1])
            return to_return
        except TypeError:
            return []

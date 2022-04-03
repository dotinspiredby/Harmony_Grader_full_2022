from music21 import stream
from interval_lister import IntervalLister
from superposer import Superposer
from checker import Checker

from logging import getLogger


class Builder:
    def __init__(self, voice_1: stream.Part, voice_2: stream.Part):
        self.logger = getLogger(" VOICE MANAGER ")
        self.voice_1 = voice_1
        self.voice_2 = voice_2

    def manage_run(self) -> None:
        intervals_up_down, intervals_down_up = self.make_intervals_list()
        interval_list, interval_list_offset, beats = \
            self.make_interval_beat_info_compatibility(intervals_up_down, intervals_down_up)
        interval_line = self.merge_intervals_and_beats(interval_list)
        interval_line_offset = self.merge_intervals_and_beats(interval_list_offset)
        self.check(interval_line, interval_line_offset, beats)

    def make_intervals_list(self) -> tuple:
        """ function that handles the operations with making interval list and spotting voice crossing"""
        lister = IntervalLister()
        intervals_up_down = lister.make_interval_list(
            self.voice_1, self.voice_2, "up", [self.voice_1, self.voice_2])
        intervals_down_up = lister.make_interval_list(
            self.voice_2, self.voice_1, "down", [self.voice_1, self.voice_2])
        if lister.crossing_errors:
            for crossing in lister.crossing_errors:
                self.logger.info(f" {crossing}")
            # with open("log.txt", 'a', encoding='utf-8') as log_file:
            #     for crossing in lister.crossing_errors:
            #         log_file.write(str(crossing + '\n'))
            #         print(crossing)
        return intervals_up_down, intervals_down_up

    def make_interval_beat_info_compatibility(self, intervals_up_down, intervals_down_up) -> tuple:
        """needs a class instead of hunch of code given in line 160 """
        superposer = Superposer(intervals_up_down, intervals_down_up)
        superposer.fill_interval_list_and_beats()
        return superposer.interval_list, superposer.interval_list_offset, superposer.beats

    def merge_intervals_and_beats(self, intervals_input) -> list:
        """needs a separate class instead of @staticmethod __merge"""
        interval_line = []
        for line in intervals_input:
            for interval in line:
                interval_line.append(interval)
        return interval_line

    def check(self, interval_line, interval_line_offset, beats) -> None:
        checker = Checker(interval_line, interval_line_offset, beats, [self.voice_1, self.voice_2])
        checker.check(step=1)
        checker.check(step=2, info="hidden ")

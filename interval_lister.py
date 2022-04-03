from music21 import stream


class IntervalLister:
    def __init__(self):
        # self.interval_list = []
        self.crossing_errors = set()

    def make_interval_list(self, voice_a: stream.Part, voice_b: stream.Part,
                           direction: str, vc_names: list) -> list:

        """ enables attachIntervalsBetweenStreams to two staves given,
        intervals are build from first voice to second one counting on direction given """
        interval_list = []
        for measure_index in range(len(voice_a.elements)):
            measure_intervals = []
            voice_a.elements[measure_index].flat.attachIntervalsBetweenStreams(
                voice_b.elements[measure_index].flat)
            for n in voice_a.elements[measure_index].notes:

                if n.editorial.harmonicInterval is None:
                    pass  # if one of the voices is rested
                else:
                    self.check_voice_crossing(n, measure_index, direction, vc_names)
                    self.add_clear_intervals(n, measure_intervals)
                    # the block does the checking & editing part
            interval_list.append(measure_intervals)
        return interval_list

    def check_voice_crossing(self, interval, measure_index: int,
                             direction: str, vc_names) -> None:

        """ identifies voice crossing by spotting ("down"/+ ) or ("up"/-)
        in inteval names: 'down'/P4 'up'/-P4 """

        if direction == "down" and "-" not in interval.editorial.harmonicInterval.directedName:
            if interval.editorial.harmonicInterval.directedName != "P1":
                self.crossing_errors.add("voice crossing in measure {0}, note position {1} {2} {3}".format(
                    measure_index + 1, interval.offset, vc_names[0].id, vc_names[1].id))
                # print("voice crossing {0} in measure {1}".format(vc_abr, measure_index + 1))

        elif direction == "up" and "-" in interval.editorial.harmonicInterval.directedName:

            self.crossing_errors.add("voice crossing in measure {0}, note position {1} {2} {3}".format(
                measure_index + 1, interval.offset, vc_names[0].id, vc_names[1].id))
            # print("voice crossing {0} in measure {1}".format(vc_abr, measure_index + 1))

    def add_clear_intervals(self, interval, measure_intervals) -> None:

        """ clears data in interval from directions, P4 instead of -P4 """

        if "-" in interval.editorial.harmonicInterval.directedName:
            measure_intervals.append(
                (interval.editorial.harmonicInterval.directedName.replace("-", ""), interval.offset))
        else:
            measure_intervals.append((interval.editorial.harmonicInterval.directedName, interval.offset))
        interval.editorial.pop('harmonicInterval', None)

from helper_functions import order_by_offset


from logging import getLogger


class Checker:
    def __init__(self, interval_line: list, interval_line_offset: list, beats: list, vc_names: list):
        self.logger = getLogger(" PARALLELISM CHECKER ")
        self.interval_line = interval_line
        self.interval_line_offset = interval_line_offset
        self.beats = beats
        self.vc_names = vc_names

    def check(self, step: int, info=""):
        """ function that checks the bad parallelisms and find their position in measures"""
        for i in range(len(self.interval_line) - int(step)):
            fifths = ['P5', 'P12', 'P19']
            octaves = ['P1', 'P8', 'P15']
            fourths = ['P4', 'P11', 'P18']

            type_of_error = ""

            if self.interval_line[i] in fifths and self.interval_line[i + step] in fifths:  # interval_list in the past
                type_of_error = "fifths"

            elif self.interval_line[i] in octaves and self.interval_line[i + step] in octaves:
                type_of_error = "octaves"

            # elif self.interval_line[i] in fourths and self.interval_line[i + step] in fourths:
            #     type_of_error = "fourths"

            else:
                pass
            if type_of_error:
                measure_num = 0
                for interval_num in self.beats:
                    if i < interval_num:
                        measure_num = self.beats.index(interval_num) + 1
                        break
                measure_num2 = measure_num
                if self.interval_line_offset[i + step] <= self.interval_line_offset[i]:
                    measure_num2 += 1
                try:
                    note_u_a = order_by_offset(
                        self.vc_names[0], measure_num, self.interval_line_offset[i])[0]
                    note_u_b = order_by_offset(
                        self.vc_names[0], measure_num2, self.interval_line_offset[i + step])[0]
                    note_d_a = order_by_offset(
                        self.vc_names[1], measure_num, self.interval_line_offset[i])[0]
                    note_d_b = order_by_offset(
                        self.vc_names[1], measure_num2, self.interval_line_offset[i + step])[0]

                    if self._check_not_equal(note_u_a, note_u_b) is True and \
                            self._check_not_equal(note_d_a, note_d_b) is True:
                        self.logger.info(
                            f" {info}parallel {type_of_error} in measure {measure_num} "
                            f"note position {self.interval_line_offset[i]} {self.vc_names[0].id} "
                            f"{self.vc_names[1].id}"
                        )

                        # with open("log.txt", 'a', encoding='utf-8') as log_file:
                        #     log_file.write(f"{info }parallel {type_of_error} in measure {measure_num} "
                        #                    f"note position {self.interval_line_offset[i]} {self.vc_names[0].id} "
                        #                    f"{self.vc_names[1].id}"+'\n')

                        # print(
                        #     '%s' % info + 'parallel %s' % type_of_error + ' in measure %s ' % measure_num,
                        #     ' note position %s ' % self.interval_line_offset[i], self.vc_names[0].id,
                        #     self.vc_names[1].id)
                    else:
                        pass  # case of repetitive notes
                except IndexError:
                    pass  # caught the <note.Rest> instead of pitched note.Note

    @staticmethod
    def _check_not_equal(n1, n2):
        if n1.pitch == n2.pitch:
            return False
        return True

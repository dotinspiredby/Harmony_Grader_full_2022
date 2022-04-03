from music21 import converter, stream
from helper_functions import output_name


class ScoreDocument:
    """ Extra class, which takes a link to xml and returns
    the score which each voice separated into its own staff line"""

    def __init__(self, link: str) -> None:
        self.link = link
        self.score = self.get_voiced_score()

    @property
    def test_score_voices(self):
        """ main function of the class returning
        a generator object of stream.Part objects from the whole Score
        like [<stream.Part Soprano>, <stream.Part Alto>,
              <stream.Part Tenor>, <stream.Part Bass>]"""
        return self._split_into_parts(output_name(self.score))

    def _split_into_parts(self, ids: list) -> stream.Part:
        """function that launches the voice splitter for each part of the Score
        if multiple voices on one staff given"""
        for part_id in ids:
            yield self.get_voiced_score().parts[part_id]

    def get_voiced_score(self) -> stream.Score:
        """ splitter function that converts the score containing
        multi-voiced staves into the wider variant of the score with single-voice staves"""
        test = converter.parse(self.link)
        return test.voicesToParts()

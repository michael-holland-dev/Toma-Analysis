from analyzers.analysis_base import Analysis
from analyzers.segmenter import BacteriaSegmenter
from analyzers.basic import Basic


def get_analysis(analysis_type):
    analysis_type = analysis_type.lower()

    if analysis_type == "base":
        return Basic
    elif analysis_type == "segment":
        return BacteriaSegmenter
    else:
        raise Exception("Analysis Doesn't Exist")

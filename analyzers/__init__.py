from analyzers.analysis_base import Analysis
from analyzers.basic import Basic


def get_analysis(analysis_type):
    analysis_type = analysis_type.lower()

    if analysis_type == "base":
        return Basic
    else:
        raise Exception("Analysis Doesn't Exist")

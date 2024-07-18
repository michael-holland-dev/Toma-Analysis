from analyzers.analysis_base import Analysis
from analyzers.basic import Basic
from analyzers.tomo_stats import TomoStats


def get_analysis(analysis_type):
    analysis_type = analysis_type.lower()

    if analysis_type == "basic":
        return Basic
    else:
        raise Exception("Analysis Doesn't Exist")

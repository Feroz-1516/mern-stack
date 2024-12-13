from typing import Callable

def report_web_vitals(on_perf_entry: Callable[[dict], None] = None):
    """
    Measure and report Web Vitals performance metrics.

    This function sets up performance observers to measure various Web Vitals
    metrics and reports them using the provided callback function.

    Args:
        on_perf_entry (Callable[[dict], None], optional): A callback function
            that receives the performance entry data. Defaults to None.

    Returns:
        None
    """
    if on_perf_entry and callable(on_perf_entry):
        try:
            from web_vitals import getCLS, getFID, getFCP, getLCP, getTTFB
        except ImportError:
            return

        def handle_cls(metric):
            on_perf_entry(create_report_obj(metric))

        def handle_fid(metric):
            on_perf_entry(create_report_obj(metric))

        def handle_fcp(metric):
            on_perf_entry(create_report_obj(metric))

        def handle_lcp(metric):
            on_perf_entry(create_report_obj(metric))

        def handle_ttfb(metric):
            on_perf_entry(create_report_obj(metric))

        getCLS(handle_cls)
        getFID(handle_fid)
        getFCP(handle_fcp)
        getLCP(handle_lcp)
        getTTFB(handle_ttfb)

def create_report_obj(metric):
    """
    Create a report object from the given metric.

    Args:
        metric (dict): The metric object containing performance data.

    Returns:
        dict: A report object with name, delta, id, and entries.
    """
    return {
        'name': metric.name,
        'delta': metric.delta,
        'id': metric.id,
        'entries': [entry.toJSON() for entry in metric.entries]
    }
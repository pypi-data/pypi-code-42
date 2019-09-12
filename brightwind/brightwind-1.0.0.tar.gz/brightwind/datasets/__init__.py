
import os

__all__ = ['demo_data', 'demo_campbell_scientific_data', 'demo_merra2_NW',
           'demo_merra2_NE', 'demo_merra2_SE', 'demo_merra2_SW', 'demo_windographer_data']

demo_campbell_scientific_data = os.path.join(os.path.dirname(__file__), 'demo', 'campbell_scientific_demo_data.csv')
demo_data = os.path.join(os.path.dirname(__file__), 'demo', 'demo_data.csv')
demo_windographer_data = os.path.join(os.path.dirname(__file__), 'demo', 'windographer_demo_data.txt')

demo_merra2_NW = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_NW_2000-01-01_2017-06-30.csv')
demo_merra2_NE = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_NE_2000-01-01_2017-06-30.csv')
demo_merra2_SE = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_SE_2000-01-01_2017-06-30.csv')
demo_merra2_SW = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_SW_2000-01-01_2017-06-30.csv')


def datasets_available():
    """
    Example datasets that can be used with the library.


    **Example usage**
    ::
        import brightwind as bw

        all_datasets_available = ['demo_data', 'demo_campbell_scientific_data', 'demo_merra2_NW',
           'demo_merra2_NE', 'demo_merra2_SE', 'demo_merra2_SW', 'demo_windographer_data']
        demo_data = bw.load_campbell_scientific(bw.datasets.demo_campbell_scientific_data)
        demo_data = bw.load_csv(bw.datasets.demo_data)
        demo_windog_data = bw.load_windographer_txt(bw.datasets.demo_windographer_data)

    """

    return None

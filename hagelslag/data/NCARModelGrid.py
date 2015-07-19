from ModelGrid import ModelGrid
import numpy as np
from pandas import DatetimeIndex


class NCARModelGrid(ModelGrid):
    """
    Extension of the ModelGrid class for interfacing with the NCAR ensemble.

    Parameters
    ----------
    member : str
        Name of the ensemble member
    run_date : datetime.datetime object
        Date of the initial step of the ensemble run
    start_date : datetime.datetime object
        First time step extracted.
    end_date : datetime.datetime object
        Last time step extracted.
    path : str
        Path to model output files.
    single_step : boolean (default=False)
        Whether variable information is stored with each time step in a separate file or one file containing all
        timesteps.
    """
    def __init__(self, member, run_date, variable, start_date, end_date, path, single_step=False):
        self.member = member
        self.path = path
        self.forecast_hours = np.arange((start_date - run_date).total_seconds() / 3600,
                                        (end_date - run_date).total_seconds() / 3600 + 1)
        filenames = []
        if not single_step:
            filenames.append("{0}{1}/{2}_surrogate_{1}.nc".format(self.path,
                                                                  run_date.strftime("%Y%m%d%H"),
                                                                  self.member))
        else:
            for hour in self.forecast_hours:
                filenames.append("{0}{1}/post_rundir/{2}/fhr_{3:d}/WRFTWO{3:02d}.nc".format(self.path,
                                                                                            run_date.strftime("%Y%m%d%H"),
                                                                                            self.member,
                                                                                            hour))
        print filenames
        super(NCARModelGrid, self).__init__(filenames, run_date, start_date, end_date, variable)


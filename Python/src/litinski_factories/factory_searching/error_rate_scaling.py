import mpmath as mp

mp.prec = 128

from multiprocessing import Pool
import pandas as pd
from datetime import datetime

from ..magic_state_factory import MagicStateFactory
from ..factory_simulation.smallfootprint import cost_of_one_level_15to1_small_footprint
import math
import itertools
import numpy as np


def objective(factory: MagicStateFactory) -> mp.mpf:
    return mp.mpf(factory.distilled_magic_state_error_rate) / factory.qubits


step_size: int = 2


# find the best factory which has less than 1000 qubits.
class SimulationOneLevel15to1SmallFootprint:

    def __init__(
        self,
        error_rate: float,
        dx: int,
        dz: int,
        dm: int,
        tag: str = "Simulation",
    ):
        self.prec = mp.prec
        self.pphys = error_rate
        self.dx = dx
        self.dz = dz
        self.dm = dm
        self.factory = cost_of_one_level_15to1_small_footprint(error_rate, dx, dz, dm)
        print(
            f"{tag}: {self.factory.name}; rating={self.rating()}; qubits={self.factory.qubits}"
        )

    def rating(self) -> mp.mpf:
        if self.factory.qubits > 3000:
            return -99999999
        return -math.log10(self.factory.distilled_magic_state_error_rate)


df = pd.DataFrame(
    columns=[
        "date",
        "precision_in_bits",
        "pphys",
        "dx",
        "dz",
        "dm",
        "error_rate",
        "qubits",
        "code_cycles",
    ]
)


def log_simulation(sim: SimulationOneLevel15to1SmallFootprint) -> None:
    new_row = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pphys": sim.pphys,
        "precision_in_bits": mp.prec,
        "dx": sim.dx,
        "dz": sim.dz,
        "dm": sim.dm,
        "error_rate": sim.factory.distilled_magic_state_error_rate,
        "qubits": sim.factory.qubits,
        "code_cycles": sim.factory.distillation_time_in_cycles,
    }
    df.loc[len(df)] = new_row  # type: ignore


def search_for_optimal_factory():

    round_number = 0
    num_threads = 10
    error_rates = [10 ** (-x) for x in np.arange(3, 6, 0.1)]
    all_combos = list(
        itertools.product(error_rates, range(5, 8, 2), range(3, 6, 2), range(3, 6, 2))
    )

    print(f"Search will complete in {math.ceil(len(all_combos)/num_threads)} rounds.")

    try:
        while len(all_combos) > 0:
            chunk = all_combos[:num_threads]
            all_combos = all_combos[num_threads:]

            with Pool(processes=num_threads) as pool:
                round_number += 1
                print(f"Round {round_number}")

                jobs = []
                for error_rate, dx, dz, dm in chunk:
                    jobs += [
                        pool.apply_async(
                            SimulationOneLevel15to1SmallFootprint,
                            (error_rate, dx, dz, dm),
                        )
                    ]

                pool.close()
                for job in jobs:
                    log_simulation(job.get())
    finally:
        df.to_csv(
            f'Simulation_Data/small_footprint_one_level_15to1_varying_pphys-{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv',
            mode="a",
            index=False,
            header=True,
        )


if __name__ == "__main__":
    search_for_optimal_factory()

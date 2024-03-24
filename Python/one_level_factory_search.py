import mpmath as mp
from multiprocessing import Pool
import pandas as pd
from datetime import datetime

from magic_state_factory import MagicStateFactory
from twolevel15to1 import cost_of_two_level_15to1
from smallfootprint import cost_of_one_level_15to1_small_footprint
import math
import itertools


def objective(factory: MagicStateFactory) -> mp.mpf:
    return mp.mpf(factory.distilled_magic_state_error_rate) / factory.qubits


mp.prec = 128
step_size: int = 2
pphys = 10**-5


# find the best factory which has less than 1000 qubits.
class SimulationOneLevel15to1SmallFootprint:

    def __init__(
        self,
        dx: int,
        dz: int,
        dm: int,
        tag: str = "Simulation",
    ):
        self.prec = mp.prec
        self.pphys = pphys
        self.dx = dx
        self.dz = dz
        self.dm = dm
        self.factory = cost_of_one_level_15to1_small_footprint(pphys, dx, dz, dm)
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
        "pphys": pphys,
        "precision_in_bits": mp.prec,
        "dx": sim.dx,
        "dz": sim.dz,
        "dm": sim.dm,
        "error_rate": sim.factory.distilled_magic_state_error_rate,
        "qubits": sim.factory.qubits,
        "code_cycles": sim.factory.distillation_time_in_cycles,
    }
    df.loc[len(df)] = new_row  # type: ignore


def search_for_optimal_factory(
    initial_center_dx,
    initial_center_dz,
    initial_center_dm,
    initial_center_dx2,
    initial_center_dz2,
    initial_center_dm2,
):

    round_number = 0
    num_threads = 10

    all_combos = list(itertools.product(range(3, 12, 2), repeat=6))

    try:
        while len(all_combos) > 0:
            chunk = all_combos[:num_threads]
            all_combos = all_combos[num_threads:]

            with Pool(processes=num_threads) as pool:
                round_number += 1
                print(f"Round {round_number}")

                jobs = []
                for dx, dz, dm, dx2, dz2, dm2 in chunk:
                    jobs += [
                        pool.apply_async(
                            SimulationOneLevel15to1SmallFootprint,
                            (dx, dz, dm, dx2, dz2, dm2),
                        )
                    ]

                pool.close()
                for job in jobs:
                    log_simulation(job.get())

    except KeyboardInterrupt:
        pool.terminate()
        df.to_csv(
            f'Simulation_Data/small_footprint_two_level_15to1_simulations-{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv',
            mode="a",
            index=False,
            header=True,
        )

    df.to_csv(
        f'Simulation_Data/small_footprint_two_level_15to1_simulations-{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv',
        mode="a",
        index=False,
        header=True,
    )


if __name__ == "__main__":

    search_for_optimal_factory(
        initial_center_dx=5,
        initial_center_dz=3,
        initial_center_dm=3,
        initial_center_dx2=9,
        initial_center_dz2=7,
        initial_center_dm2=7,
    )
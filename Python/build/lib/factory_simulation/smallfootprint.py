import mpmath
from mpmath import mp
from scipy import optimize
from ..definitions import (
    z,
    one,
    projx,
    kron,
    trace,
    apply_rot,
    plog,
    storage_x_5,
    storage_z_5,
    init5qubit,
    ideal15to1,
)
from ..factory_simulation.onelevel15to1 import one_level_15to1_state
from ..magic_state_factory import MagicStateFactory


def cost_of_one_level_15to1_small_footprint(
    pphys: float | mpmath.mpf, dx: int, dz: int, dm: int
) -> MagicStateFactory:
    """
    Calculates the output error and cost of the small-footprint 15-to-1 protocol with a physical error rate pphys and distances dx, dz and dm,
    """
    pphys = mpmath.mpf(pphys)

    # Introduce shorthand notation for logical error rate with distances dx/dz/dm
    px = plog(pphys, dx)
    pz = plog(pphys, dz)
    pm = plog(pphys, dm)

    # Step 1 of 15-to-1 protocol applying rotations 1-3
    # Last operation: apply additional storage errors due to fast faulty T measurements
    out = apply_rot(
        init5qubit,
        [one, z, one, one, one],
        pphys / 3 + 0.5 * (dm / dz) * pz * dm,
        pphys / 3 + 0.5 * dz * pm,
        pphys / 3,
    )
    out = apply_rot(
        out,
        [one, one, z, one, one],
        pphys / 3 + 0.5 * (dm / dz) * pz * dm,
        pphys / 3 + 0.5 * dz * pm,
        pphys / 3,
    )
    out = apply_rot(
        out,
        [one, one, one, z, one],
        pphys / 3 + 0.5 * (dm / dz) * pz * dm,
        pphys / 3 + 0.5 * dz * pm,
        pphys / 3,
    )

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0,
    )
    out = storage_z_5(
        out,
        0,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0,
    )

    # Step 2: apply rotation 5
    out = apply_rot(
        out,
        [one, z, z, z, one],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (3 * dz) * dx / dm * pm,
        pphys / 3,
    )

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0,
        0.5 * (dz / dx) * px * dm,
        (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0,
    )
    out = storage_z_5(
        out,
        0,
        0.5 * (dx / dz) * pz * dm,
        (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0,
    )

    # Step 3: apply rotation 6
    # Last operation: apply additional storage errors due to multi-patch measurements
    out = apply_rot(
        out,
        [z, z, z, one, one],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 2 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 2 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0,
    )

    # Step 4: apply rotation 7
    out = apply_rot(
        out,
        [z, z, one, z, one],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 3 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 3 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0,
    )

    # Step 5: apply rotations 4 and 8
    out = apply_rot(
        out,
        [z, one, z, z, one],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 3 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = apply_rot(
        out,
        [one, one, one, one, z],
        pphys / 3 + 0.5 * (dm / dz) * pz * dm,
        pphys / 3 + 0.5 * dz * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 3 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 6: apply rotation 9
    out = apply_rot(
        out,
        [z, one, one, z, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 4 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 4 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 7: apply rotation 10
    out = apply_rot(
        out,
        [z, z, one, one, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 4 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 4 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 8: apply rotation 11
    out = apply_rot(
        out,
        [z, one, z, one, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 4 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 4 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 9: apply rotation 12
    out = apply_rot(
        out,
        [z, z, z, z, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (dx + 4 * dz) * dx / dm * pm,
        pphys / 3,
    )
    out = storage_z_5(out, 0.5 * (dx + 4 * dz) / dx * px * dm, 0, 0, 0, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 10: apply rotation 13
    out = apply_rot(
        out,
        [one, one, z, z, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (3 * dz) * dx / dm * pm,
        pphys / 3,
    )

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 11: apply rotation 14
    out = apply_rot(
        out,
        [one, z, one, z, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (4 * dz) * dx / dm * pm,
        pphys / 3,
    )

    # Apply storage errors for dm code cycles
    out = storage_x_5(
        out,
        0.5 * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Step 12: apply rotation 15
    out = apply_rot(
        out,
        [one, z, z, one, z],
        pphys / 3 + 0.5 * pm * dm,
        pphys / 3 + 0.5 * pm * dm + 0.5 * (4 * dz) * dx / dm * pm,
        pphys / 3,
    )

    # Apply storage errors for 2dm code cycles
    # Qubit 1 is consumed as an output state in the following step: additional storage errors for dx code cycles
    out = storage_x_5(
        out,
        0.5 * px * (dm + 2 * dx),
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
        0.5 * (dz / dx) * px * dm,
    )
    out = storage_z_5(
        out,
        0.5 * px * (dm + 2 * dx),
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
        0.5 * (dx / dz) * pz * dm,
    )

    # Compute failure probability as the probability to measure qubits 2-5 in the |+> state
    pfail = 1 - trace(kron(one, projx, projx, projx, projx) * out).real

    # Compute the density matrix of the post-selected output state, i.e., after projecting qubits 2-5 into |+>
    outpostsel = (
        (1 / (1 - pfail))
        * kron(one, projx, projx, projx, projx)
        * out
        * kron(one, projx, projx, projx, projx).transpose_conj()
    )
    # Compute output error from the infidelity between the post-selected state and the ideal output state
    pout = 1 - trace(outpostsel * ideal15to1).real

    # Full-distance computation: determine full distance required for a 100-qubit / 10000-qubit computation
    def logerr1(d):
        return float(231 / pout * d * plog(pphys, d) - 0.01)

    def logerr2(d):
        return float(20284 / pout * d * plog(pphys, d) - 0.01)

    reqdist1 = int(2 * round(optimize.root(logerr1, 3, method="hybr").x[0] / 2) + 1)
    reqdist2 = int(2 * round(optimize.root(logerr2, 3, method="hybr").x[0] / 2) + 1)

    return MagicStateFactory(
        name=f"Small footprint 15-to-1 with pphys={float(pphys)}, dx={dx}, dz={dz}, dm={dm}",
        distilled_magic_state_error_rate=float(pout),
        qubits=2 * (2 * dx * (dx + 4 * dz) + dm),
        distillation_time_in_cycles=float(12 * dm / (1 - pfail)),
        dimensions=(2 * dx, dx + 4 * dz),
        n_t_gates_produced_per_distillation=1,
    )


def cost_of_two_level_15to1_small_footprint(
    pphys: float | mpmath.mpf, dx: int, dz: int, dm: int, dx2: int, dz2: int, dm2: int
) -> MagicStateFactory:
    """
    Calculates the output error and cost of the small-footprint (15-to-1)x(15-to-1) protocol with a physical error rate `pphys`, level-1 distances `dx`, `dz` and `dm`, and level-2 distances `dx2`, `dz2` and `dm2`
    """

    pphys = mpmath.mpf(pphys)

    # Introduce shorthand notation for logical error rate with distances dx2/dz2/dm2
    px2 = plog(pphys, dx2)
    pz2 = plog(pphys, dz2)
    pm2 = plog(pphys, dm2)

    # Compute pl1, the output error of level-1 states with an added Z storage error
    # to the output state from moving the level-1 state dispinto the intermediate region
    out = one_level_15to1_state(pphys, dx, dz, dm)
    pfail = 1 - trace(kron(one, projx, projx, projx, projx) * out).real

    outpostsel = (
        (1 / (1 - pfail))
        * kron(one, projx, projx, projx, projx)
        * out
        * kron(one, projx, projx, projx, projx).transpose_conj()
    )

    pl1 = 1 - trace(outpostsel * ideal15to1).real + 5 * pm2 * dm2

    # Compute l1time, the speed at which level-2 rotations can be performed (t_{L1} in the paper)
    l1time = max(6 * dm / (1 - pfail), 2 * dm2)

    # Define lmove, the effective width-dm2 region a level-1 state needs to traverse before reaching the level-2 block,
    # picking up additional storage errors
    lmove = 5 * dm2

    # Step 1 of the small-footprint (15-to-1)x(15-to-1) protocol applying rotation 1
    out2 = apply_rot(
        init5qubit,
        [one, z, one, one, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0, 0.5 * (dz2 / dx2) * px2 * l1time, 0, 0, 0)
    out2 = storage_z_5(out2, 0, 0.5 * (dx2 / dz2) * pz2 * l1time, 0, 0, 0)

    # Step 2: apply rotation 2
    out2 = apply_rot(
        out2,
        [one, one, z, one, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (3 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0,
        0,
    )
    out2 = storage_z_5(
        out2,
        0,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0,
        0,
    )

    # Step 3: apply rotation 3
    out2 = apply_rot(
        out2,
        [one, one, one, z, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (2 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0,
    )
    out2 = storage_z_5(
        out2,
        0,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0,
    )

    # Step 4: apply rotation 4
    out2 = apply_rot(
        out2,
        [one, one, one, one, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 5: apply rotation 5
    out2 = apply_rot(
        out2,
        [z, z, z, one, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 6: apply rotation 6
    out2 = apply_rot(
        out2,
        [one, z, z, z, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 7: apply rotation 7
    out2 = apply_rot(
        out2,
        [z, one, z, z, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 8: apply rotation 8
    out2 = apply_rot(
        out2,
        [z, z, one, z, one],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 9: apply rotation 9
    out2 = apply_rot(
        out2,
        [z, z, one, one, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 10: apply rotation 10
    out2 = apply_rot(
        out2,
        [z, one, one, z, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 11: apply rotation 11
    out2 = apply_rot(
        out2,
        [z, one, z, one, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 12: apply rotation 12
    out2 = apply_rot(
        out2,
        [z, z, z, z, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (dx2 + 4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )
    out2 = storage_z_5(out2, 0.5 * (dx2 + 4 * dz2 + dm2) * dm2 / dx2 * px2, 0, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 13: apply rotation 13
    out2 = apply_rot(
        out2,
        [one, z, one, z, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 14: apply rotation 14
    out2 = apply_rot(
        out2,
        [one, one, z, z, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (3 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Step 15: apply rotation 15
    out2 = apply_rot(
        out2,
        [one, z, z, one, z],
        pl1 + 0.5 * lmove * pm2,
        0.5 * lmove * pm2 + 0.5 * (4 * dz2 + dm2) * dx2 / dm2 * pm2,
        0,
    )

    # Apply storage errors for l1time code cycles
    # Qubit 1 is consumed as an output state in the following step: additional storage errors for dx2 code cycles
    out2 = storage_x_5(
        out2,
        0.5 * px2 * (l1time + dx2),
        0.5 * (dz2 / dx2) * px2 * l1time,
        0.5 * (dz2 / dx2) * px2 * l1time,
        0,
        0.5 * (dz2 / dx2) * px2 * l1time,
    )
    out2 = storage_z_5(
        out2,
        0.5 * px2 * (l1time + dx2),
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0.5 * (dx2 / dz2) * pz2 * l1time,
        0,
        0.5 * (dx2 / dz2) * pz2 * l1time,
    )

    # Compute level-2 failure probability as the probability to measure qubits 2-5 in the |+> state
    pfail2 = 1 - trace(kron(one, projx, projx, projx, projx) * out2).real

    # Compute the density matrix of the post-selected output state, i.e., after projecting qubits 2-5 into |+>
    outpostsel2 = (
        (1 / (1 - pfail2))
        * kron(one, projx, projx, projx, projx)
        * out2
        * kron(one, projx, projx, projx, projx).transpose_conj()
    )

    # Compute level-2 output error from the infidelity between the post-selected state and the ideal output state
    pout = 1 - trace(outpostsel2 * ideal15to1).real

    # Full-distance computation: determine full distance required for a 100-qubit / 10000-qubit computation
    def logerr1(d):
        return float(231 / pout * d * plog(pphys, d) - 0.01)

    def logerr2(d):
        return float(20284 / pout * d * plog(pphys, d) - 0.01)

    # reqdist1 = int(2 * round(optimize.root(logerr1, 3, method="hybr").x[0] / 2) + 1)
    # reqdist2 = int(2 * round(optimize.root(logerr2, 3, method="hybr").x[0] / 2) + 1)

    # Print output error, failure probability, space cost, time cost and space-time cost
    nqubits = 2 * (
        (dx2 + 4 * dz2 + dm2) * 2 * dx2
        + (dx + 4 * dz) * 3 * dx
        + 2 * dm
        + 2 * dm2 * dm2
    )
    ncycles = 15 * l1time / (1 - pfail2)

    return MagicStateFactory(
        name=f"Small footprint (15-to-1)x(15-to-1) with pphys={float(pphys)}, dx={dx}, dz={dz}, dm={dm}, dx2={dx2}, dz2={dz2}, dm2={dm2}",
        distilled_magic_state_error_rate=float(pout),
        qubits=nqubits,
        distillation_time_in_cycles=float(ncycles),
        dimensions=(4 * dz2 + dx2 + dm2 + 3 * dx, 2 * dx2),
        n_t_gates_produced_per_distillation=1,
    )

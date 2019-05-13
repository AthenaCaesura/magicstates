import numpy as np
from scipy import optimize
from definitions import (z, one, projx, kronecker_product, apply_rot, plog,
                         storage_x_5, storage_z_5, init5qubit, ideal15to1)
from onelevel15to1 import one_level_15to1_state


# Calculates the output error and cost of the small-footprint 15-to-1 protocol
# with a physical error rate pphys and distances dx, dz and dm,
def cost_of_one_level_15to1_small_footprint(pphys, dx, dz, dm):
    # Introduce shorthand notation for logical error rate with distances dx/dz/dm
    px = plog(pphys, dx)
    pz = plog(pphys, dz)
    pm = plog(pphys, dm)

    # Step 1 of 15-to-1 protocol applying rotations 1-3
    # Last operation: apply additional storage errors due to fast faulty T measurements
    out = apply_rot(init5qubit, [one, z, one, one, one], pphys / 3, pphys / 3 + 0.5 * dz * pm, pphys / 3)
    out = apply_rot(out, [one, one, z, one, one], pphys / 3, pphys / 3 + 0.5 * dz * pm, pphys / 3)
    out = apply_rot(out, [one, one, one, z, one], pphys / 3, pphys / 3 + 0.5 * dz * pm, pphys / 3)
    out = storage_z_5(out, 0, 0.5 * (dm / dz) * pz * dm, 0.5 * (dm / dz) * pz * dm, 0.5 * (dm / dz) * pz * dm, 0)

    # Apply storage errors for dm code cycles
    out = storage_x_5(out, 0, 0.5 * (dz / dx) * px * dm, 0.5 * (dz / dx) * px * dm, 0.5 * (dz / dx) * px * dm, 0)
    out = storage_z_5(out, 0, 0.5 * (dx / dz) * pz * dm, 0.5 * (dx / dz) * pz * dm, 0.5 * (dx / dz) * pz * dm, 0)

    # Step 2: apply rotation 5
    # Last operation: apply additional storage errors due to slow faulty T measurements
    out = apply_rot(out, [one, z, z, z, one], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (4 * dz) * pm, pphys / 3)
    out = storage_z_5(out, 0, (dm / dz) * pz * dm, (dm / dz) * pz * dm, (dm / dz) * pz * dm, 0)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, 0, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, 0)
    out = storage_z_5(out, 0, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, 0)

    # Step 3: apply rotation 6
    out = apply_rot(out, [z, z, z, one, one], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 3 * dz) * pm,
                    pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, (dm / dz) * pz * dm, (dm / dz) * pz * dm, 0, 0)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, 0)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, 0)

    # Step 4: apply rotation 7
    out = apply_rot(out, [z, z, one, z, one], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 3 * dz) * pm,
                    pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, (dm / dz) * pz * dm, 0, (dm / dz) * pz * dm, 0)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, 0)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, 0)

    # Step 5: apply rotations 4 and 8
    out = apply_rot(out, [z, one, z, z, one], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 3 * dz) * pm,
                    pphys / 3)
    out = apply_rot(out, [one, one, one, one, z], pphys / 3, pphys / 3 + 0.5 * dz * pm, pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, 0, (dm / dz) * pz * dm, (dm / dz) * pz * dm,
                      0.5 * (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      0.5 * (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      0.5 * (dx / dz) * pz * dm)

    # Step 6: apply rotation 9
    out = apply_rot(out, [z, one, one, z, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 4 * dz) * pm,
                    pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, 0, 0, (dm / dz) * pz * dm, (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Step 7: apply rotation 10
    out = apply_rot(out, [z, z, one, one, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 4 * dz) * pm,
                    pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, (dm / dz) * pz * dm, 0, 0, (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Step 8: apply rotation 11
    out = apply_rot(out, [z, one, z, one, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 4 * dz) * pm,
                    pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, 0, (dm / dz) * pz * dm, 0, (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Step 9: apply rotation 12
    out = apply_rot(out, [z, z, z, z, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (dx + 4 * dz) * pm, pphys / 3)
    out = storage_z_5(out, (dm / dx) * px * dm, (dm / dz) * pz * dm, (dm / dz) * pz * dm, (dm / dz) * pz * dm,
                      (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Step 10: apply rotation 13
    out = apply_rot(out, [one, one, z, z, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (4 * dz) * pm, pphys / 3)
    out = storage_z_5(out, 0, 0, (dm / dz) * pz * dm, (dm / dz) * pz * dm, (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Step 11: apply rotation 14
    out = apply_rot(out, [one, z, one, z, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (4 * dz) * pm, pphys / 3)
    out = storage_z_5(out, 0, (dm / dz) * pz * dm, 0, (dm / dz) * pz * dm, (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    out = storage_x_5(out, px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Step 12: apply rotation 15
    out = apply_rot(out, [one, z, z, one, z], pphys / 3 + (dm / dz) * pm * dm, pphys / 3 + (4 * dz) * pm, pphys / 3)
    out = storage_z_5(out, 0, (dm / dz) * pz * dm, (dm / dz) * pz * dm, 0, (dm / dz) * pz * dm)

    # Apply storage errors for 2dm code cycles
    # Qubit 1 is consumed as an output state in the following step: additional storage errors for dx code cycles
    out = storage_x_5(out, px * (dm + dx), (dz / dx) * px * dm, (dz / dx) * px * dm, (dz / dx) * px * dm,
                      (dz / dx) * px * dm)
    out = storage_z_5(out, px * (dm + dx), (dx / dz) * pz * dm, (dx / dz) * pz * dm, (dx / dz) * pz * dm,
                      (dx / dz) * pz * dm)

    # Compute failure probability as the probability to measure qubits 2-5 in the |+> state
    pfail = np.real(1 - np.trace(np.dot(kronecker_product([one, projx, projx, projx, projx]), out)))

    # Compute the density matrix of the post-selected output state, i.e., after projecting qubits 2-5 into |+>
    outpostsel = 1 / (1 - pfail) * np.dot(np.dot(kronecker_product([one, projx, projx, projx, projx]), out),
                                          kronecker_product([one, projx, projx, projx, projx]).conj().transpose())

    # Compute output error from the infidelity between the post-selected state and the ideal output state
    pout = np.real(1 - np.trace(np.dot(outpostsel, ideal15to1)))

    # Full-distance computation: determine full distance required for a 100-qubit / 10000-qubit computation
    def logerr1(d):
        return 231 / pout * d * plog(pphys, d) - 0.01

    def logerr2(d):
        return 20284 / pout * d * plog(pphys, d) - 0.01

    reqdist1 = 2 * round(optimize.root_scalar(logerr1, bracket=[1, 10000], method='brentq').root / 2) + 1
    reqdist2 = 2 * round(optimize.root_scalar(logerr2, bracket=[1, 10000], method='brentq').root / 2) + 1

    # Print output error, failure probability, space cost, time cost and space-time cost
    print('Small-footprint 15-to-1 with pphys=', pphys, ', dx=', dx, ', dz=', dz, ', dm=', dm, sep='')
    print('Output error: ', '%.4g' % pout, sep='')
    print('Failure probability: ', '%.3g' % pfail, sep='')
    print('Qubits: ', 2 * (dx + dm) * (dx + 4 * dz), sep='')
    print('Code cycles: ', '%.2f' % (23 * dm / (1 - pfail)), sep='')
    print('Space-time cost: ', '%.0f' % (2 * (dm + dx) * (dx + 4 * dz) * 23 * dm / (1 - pfail)), ' qubitcycles', sep='')
    print('For a 100-qubit computation: ',
          ('%.3f' % ((dm + dx) * (dx + 4 * dz) * 23 * dm / (1 - pfail) / reqdist1 ** 3)), 'd^3 (d=', reqdist1, ')',
          sep='')
    print('For a 5000-qubit computation: ',
          ('%.3f' % ((dm + dx) * (dx + 4 * dz) * 23 * dm / (1 - pfail) / reqdist2 ** 3)), 'd^3 (d=', reqdist2, ')',
          sep='')
    print('')


# Calculates the output error and cost of the small-footprint (15-to-1)x(15-to-1) protocol
# with a physical error rate pphys, level-1 distances dx, dz and dm,
# and level-2 distances dx2, dz2 and dm2
def cost_of_two_level_15to1_small_footprint(pphys, dx, dz, dm, dx2, dz2, dm2):
    # Introduce shorthand notation for logical error rate with distances dx2/dz2/dm2
    px2 = plog(pphys, dx2)
    pz2 = plog(pphys, dz2)
    pm2 = plog(pphys, dm2)

    # Compute pl1, the output error of level-1 states with an added Z storage error
    # to the output state from moving the level-1 state into the intermediate region
    out = one_level_15to1_state(pphys, dx, dz, dm)
    pfail = np.real(1 - np.trace(np.dot(kronecker_product([one, projx, projx, projx, projx]), out)))
    outpostsel = 1 / (1 - pfail) * np.dot(np.dot(kronecker_product([one, projx, projx, projx, projx]), out),
                                          kronecker_product([one, projx, projx, projx, projx]).conj().transpose())
    pl1 = np.real(1 - np.trace(np.dot(outpostsel, ideal15to1))) + 5 * pm2 * dm2

    # Compute l1time, the speed at which level-2 rotations can be performed (t_{L1} in the paper)
    l1time = max(6 * dm / (1 - pfail), 2 * dm2)

    # Step 1 of the small-footprint (15-to-1)x(15-to-1) protocol applying rotation 1
    out2 = apply_rot(init5qubit, [one, z, one, one, one], pl1, (4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, (dm2 / dz2) * pz2 * dm2, 0, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0, 0.5 * (dz2 / dx2) * px2 * l1time, 0, 0, 0)
    out2 = storage_z_5(out2, 0, 0.5 * (dx2 / dz2) * pz2 * l1time, 0, 0, 0)

    # Step 2: apply rotation 2
    out2 = apply_rot(out2, [one, one, z, one, one], pl1, (3 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, 0, (dm2 / dz2) * pz2 * dm2, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0, 0)
    out2 = storage_z_5(out2, 0, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0, 0)

    # Step 3: apply rotation 3
    out2 = apply_rot(out2, [one, one, one, z, one], pl1, (2 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, 0, 0, (dm2 / dz2) * pz2 * dm2, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0)
    out2 = storage_z_5(out2, 0, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0)

    # Step 4: apply rotation 4
    out2 = apply_rot(out2, [one, one, one, one, z], pl1, (dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, 0, 0, 0, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 5: apply rotation 5
    out2 = apply_rot(out2, [z, z, z, one, one], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2, 0, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 6: apply rotation 6
    out2 = apply_rot(out2, [one, z, z, z, one], pl1, (4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 7: apply rotation 7
    out2 = apply_rot(out2, [z, one, z, z, one], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, 0, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 8: apply rotation 8
    out2 = apply_rot(out2, [z, z, one, z, one], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, (dm2 / dz2) * pz2 * dm2, 0, (dm2 / dz2) * pz2 * dm2, 0)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 9: apply rotation 9
    out2 = apply_rot(out2, [z, z, one, one, z], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, (dm2 / dz2) * pz2 * dm2, 0, 0, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 10: apply rotation 10
    out2 = apply_rot(out2, [z, one, one, z, z], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, 0, 0, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 11: apply rotation 11
    out2 = apply_rot(out2, [z, one, z, one, z], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, 0, (dm2 / dz2) * pz2 * dm2, 0, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 12: apply rotation 12
    out2 = apply_rot(out2, [z, z, z, z, z], pl1, (dx2 + 4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, (dm2 / dx2) * px2 * dm2, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2,
                       (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 13: apply rotation 13
    out2 = apply_rot(out2, [one, z, one, z, z], pl1, (4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, (dm2 / dz2) * pz2 * dm2, 0, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 14: apply rotation 14
    out2 = apply_rot(out2, [one, one, z, z, z], pl1, (3 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, 0, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Step 15: apply rotation 15
    out2 = apply_rot(out2, [one, z, z, one, z], pl1, (4 * dz2 + dm2) * pm2 + 5 * pm2 * dm2, 0)
    out2 = storage_z_5(out2, 0, (dm2 / dz2) * pz2 * dm2, (dm2 / dz2) * pz2 * dm2, 0, (dm2 / dz2) * pz2 * dm2)

    # Apply storage errors for l1time code cycles
    # Qubit 1 is consumed as an output state in the following step: additional storage errors for dx2 code cycles
    out2 = storage_x_5(out2, 0.5 * px2 * (l1time + dx2), 0.5 * (dz2 / dx2) * px2 * l1time,
                       0.5 * (dz2 / dx2) * px2 * l1time, 0, 0.5 * (dz2 / dx2) * px2 * l1time)
    out2 = storage_z_5(out2, 0.5 * px2 * (l1time + dx2), 0.5 * (dx2 / dz2) * pz2 * l1time,
                       0.5 * (dx2 / dz2) * pz2 * l1time, 0, 0.5 * (dx2 / dz2) * pz2 * l1time)

    # Compute level-2 failure probability as the probability to measure qubits 2-5 in the |+> state
    pfail2 = np.real(1 - np.trace(np.dot(kronecker_product([one, projx, projx, projx, projx]), out2)))

    # Compute the density matrix of the post-selected output state, i.e., after projecting qubits 2-5 into |+>
    outpostsel2 = 1 / (1 - pfail2) * np.dot(np.dot(kronecker_product([one, projx, projx, projx, projx]), out2),
                                            kronecker_product([one, projx, projx, projx, projx]).conj().transpose())

    # Compute level-2 output error from the infidelity between the post-selected state and the ideal output state
    pout = np.real(1 - np.trace(np.dot(outpostsel2, ideal15to1)))

    # Full-distance computation: determine full distance required for a 100-qubit / 10000-qubit computation
    def logerr1(d):
        return 231 / pout * d * plog(pphys, d) - 0.01

    def logerr2(d):
        return 20284 / pout * d * plog(pphys, d) - 0.01

    reqdist1 = 2 * round(optimize.root_scalar(logerr1, bracket=[1, 10000], method='brentq').root / 2) + 1
    reqdist2 = 2 * round(optimize.root_scalar(logerr2, bracket=[1, 10000], method='brentq').root / 2) + 1

    # Print output error, failure probability, space cost, time cost and space-time cost
    nqubits = 2 * ((dx2 + 4 * dz2) * (dx2 + dm2) + (dx + 4 * dz) * (dx + 4 * dm) + 6 * dm2 * dm2)
    ncycles = 15 * l1time / (1 - pfail2)
    print('Small-footprint (15-to-1)x(15-to-1) with pphys=', pphys, ', dx=', dx, ', dz=', dz, ', dm=', dm, ', dx2=',
          dx2, ', dz2=', dz2, ', dm2=', dm2, sep='')
    print('Output error: ', '%.4g' % pout, sep='')
    print('Failure probability: ', '%.3g' % pfail2, sep='')
    print('Qubits: ', '%.0f' % nqubits, sep='')
    print('Code cycles: ', '%.2f' % ncycles, sep='')
    print('Space-time cost: ', '%.0f' % (nqubits * ncycles), ' qubitcycles', sep='')
    print('For a 100-qubit computation: ', ('%.3f' % (nqubits * ncycles / 2 / reqdist1 ** 3)), 'd^3 (d=', reqdist1, ')',
          sep='')
    print('For a 5000-qubit computation: ', ('%.3f' % (nqubits * ncycles / 2 / reqdist2 ** 3)), 'd^3 (d=', reqdist2,
          ')', sep='')
    print('')
from litinski_factories.factory_simulation.smallfootprint import (
    cost_of_one_level_15to1_small_footprint,
    cost_of_two_level_15to1_small_footprint,
)

selected_one_level_factories = [
    (5, 1, 3),
    (7, 3, 3),
    (9, 3, 3),
    (3, 1, 1),
]

selected_two_level_factories = [
    (5, 1, 3, 11, 3, 5),
    (5, 1, 1, 11, 5, 5),
    (5, 1, 1, 13, 5, 5),
    (5, 1, 3, 15, 5, 5),
    (7, 1, 3, 15, 5, 7),
    (3, 1, 1, 11, 3, 5),
]

for factory_params in selected_one_level_factories:
    print(cost_of_one_level_15to1_small_footprint(10**-3, *factory_params))
for factory_params in selected_two_level_factories:
    print(cost_of_two_level_15to1_small_footprint(10**-3, *factory_params))

from multiprocessing import Pool, cpu_count


def check_number_of_values_in_range(comp_list, lower, upper):
    number_of_hits = 0
    for i in range(lower, upper):
        if i in comp_list:
            number_of_hits += 1
    return number_of_hits


num_processes = 4
comparison_list = [1, 2, 3]
lower_and_upper_bounds = [(0, 25*10**6), (25*10*6, 50*10**6),
                          (50*10**6, 75*10*6), (75*10*6, 10**8)]

num_cpu_to_use = max(1, cpu_count() - 1)

print('Number of cpus being used:', num_cpu_to_use)

prepared_list = []
for i in range(len(lower_and_upper_bounds)):
    prepared_list.append((comparison_list, *lower_and_upper_bounds[i]))

print('List to use as input:', prepared_list)
with Pool(num_cpu_to_use) as mp_pool:
    result = mp_pool.starmap(check_number_of_values_in_range, prepared_list)  # [(comp_list, lower, upper), ..]

print(result)
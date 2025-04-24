-- U29.	Median(v2): Calculates median with quickselect

CREATE OR REPLACE FUNCTION aggr_median_final_v2(state numeric[])
RETURNS numeric AS $$
    def partition(sample, low, high):
        pivot = sample[(low + high) // 2]
        left = low
        right = high
        while True:
            while sample[left] < pivot:
                left += 1
            while sample[right] > pivot:
                right -= 1
            if left >= right:
                return right
            sample[left], sample[right] = sample[right], sample[left]
            left += 1
            right -= 1

    def quickselect(sample, k):
        low, high = 0, len(sample) - 1
        while low < high:
            pivot_index = partition(sample, low, high)
            if pivot_index < k:
                low = pivot_index + 1
            else:
                high = pivot_index
        return sample[k]

    if not state:
        return None

    n = len(state)
    mid = n // 2
    if n % 2:
        return quickselect(state, mid)
    else: 
        left = quickselect(state, mid - 1)
        right = quickselect(state, mid)
        return (left + right) / 2.0
$$ LANGUAGE plpython3u IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_median_v2(value numeric) (
    SFUNC = array_append,
    STYPE = numeric[],
    FINALFUNC = aggr_median_final_v2,
    INITCOND='{}',
    PARALLEL = SAFE


);
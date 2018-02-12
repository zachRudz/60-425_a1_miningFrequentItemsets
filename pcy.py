import datetime
import my_hashmap as hm
from collections import defaultdict

DEBUG = True

def a_priori(input_file, num_baskets, support_threshold):
    min_required_occurrences = num_baskets * support_threshold
    if DEBUG:
        print("Minimum number of occurrences to be considered frequent: {}".format(min_required_occurrences))

    # -- Pass 1 --
    # Any frequent pairs would have to contain items that would be also considered frequent
    # Therefore, we can go through the baskets and eliminate all items which are not considered "frequent"
    # No frequent pairs would contain items which are not frequent
    if DEBUG:
        print("Starting pass 1...")

    # Our hashmap/dict of possibly frequent items
    # Default value of any basket will always be 0
    global key_pair
    items = defaultdict(lambda: 0)
    hashed_pairs = hm.my_hashmap(num_buckets=int(num_baskets / 2))

    with open(input_file, 'r') as fp:
        # Reading up to $num_basket baskets
        for basket_index in range(num_baskets):
            # Fetching the values from the line (as strings), and removing the newline character at the end
            line = fp.readline()
            tmp_items = line.split(' ')[: -1]

            # Making note of each item's appearance in a basket
            for i in tmp_items:
                items[i] += 1

            # Hashing each pair of items to our hashmap of pairs.
            # Note that each bucket of this hashmap correlates to one or more pairs.
            for a in range(len(tmp_items) - 1):
                for b in range(a + 1, len(tmp_items)):
                    hashed_pairs.increment_count(a, b)

    if DEBUG:
        print("Number of unique items: {}".format(len(items)))

    # -- Between Passes --
    # Replacing our buckets of pairs with a bitvector
    # In other words, a bucket is considered frequent if the count for that bucket exceeds our support threshold.
    # In this function, we clear our reference to the hashmap, so it's not unlikely that GC will run here or soon after
    if DEBUG:
        print("Pass 1 complete. Inbetween passes...")
    hashed_pairs.convert_to_bitmap(min_required_occurrences)

    # Now that we have a hashmap of items, and their counts, we can toss out items which are NOT frequent
    to_remove = []
    for item_index in items:
        if items[item_index] < min_required_occurrences:
            # Making a list of item indicies we can toss
            # Python doesn't like you modifying the length of collections while iterating over them,
            # which is why we're doing this in two steps.
            to_remove.append(item_index)

    for item_index in to_remove:
        items.pop(item_index)

    if DEBUG:
        print("Number of unique, frequent items: {}".format(len(items)))

    # -- Pass 2 --
    # Now that we have the list of items which are frequent, we can find each combination of items,
    # where both of the items in the pair are frequent. Therefore, through monotonicity, that pair would be frequent.
    if DEBUG:
        print("Starting pass 2...")
    frequent_pairs = defaultdict(lambda: 0)

    with open(input_file, 'r') as fp:
        # Reading up to $num_basket baskets
        for basket_index in range(num_baskets):
            # Fetching the values from the line (as strings), and removing the newline character at the end
            line = fp.readline()
            tmp_items = line.split(' ')[: -1]

            # Recording the number of frequent pairs in which both items are frequent
            # Fetching all combinations of this basket's items
            for a in range(len(tmp_items) - 1):
                for b in range(a + 1, len(tmp_items)):
                    # Making sure both items are frequent
                    if items[tmp_items[a]] > min_required_occurrences and items[tmp_items[b]] > min_required_occurrences:
                        # Making sure the pair of items hash to a frequent bucket
                        if hashed_pairs.get_from_bitmap(a, b):
                            frequent_pairs[(a, b)] += 1

    # -- Verification --
    # Now that we have a list of "frequent pairs", in which both of its items are frequent, we need to verify that
    # each of these frequent pairs actually has a support greater than the threshold.
    prev_total_frequent_pairs = len(frequent_pairs)
    pairs_to_pop = []
    for key_pair in frequent_pairs:
        if frequent_pairs[key_pair] < min_required_occurrences:
            pairs_to_pop.append(key_pair)

    # Going through and popping all of these pairs, since they're not frequent
    # Doing this outside the previous for loop because python doesn't like it when you modify the size of an iterable
    # object while iterating over it
    for pair in pairs_to_pop:
        if DEBUG:
            print("Popping {}: {} occurrences.".format(pair, frequent_pairs[pair]))
        frequent_pairs.pop(pair)

    if DEBUG:
        print("Frequent pairs before verification: {}".format(prev_total_frequent_pairs))
        print("Frequent pairs after verification: {}".format(len(frequent_pairs)))

        print("-- Frequent pairs --")
        for key_pair in frequent_pairs:
            print("{}: {}".format(key_pair, frequent_pairs[key_pair]))

    return frequent_pairs


def main():
    # Reading chunk size from the terminal
    chunk_percentage = float(input("How much of the file do you want to look through? (In percentage format pls): "))
    if chunk_percentage > 1 or chunk_percentage < 0:
        print("Error: The chunk percentage must be between 0.0 and 1.0.")
        return

    # Reading support threshold from the terminal
    support_threshold = float(input("What is your support threshold? (In percentage format pls): "))
    if support_threshold > 1 or support_threshold < 0:
        print("Error: The support threshold must be between 0.0 and 1.0.")
        return

    # Starting the clock
    start_time = datetime.datetime.now()
    print("Start time: {}".format(start_time))
    print("")

    # Finding the number of lines in our file
    input_file = 'retail.txt'
    total_num_lines = 0
    with open(input_file, 'r') as fp:
        while fp.readline():
            total_num_lines += 1

    # Calculating how many baskets (read: lines) we're going through
    num_baskets = int(total_num_lines * chunk_percentage)
    if DEBUG:
        print("Number of baskets: {}".format(num_baskets))

    # Doing a_priori things
    frequent_pairs = a_priori(input_file, num_baskets, support_threshold)

    # Stopping the clock
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time
    print("")
    print("Start time: {}".format(start_time))
    print("End time: {}".format(end_time))
    print("Total elapsed time: {}".format(diff_time))


if __name__ == "__main__":
    main()

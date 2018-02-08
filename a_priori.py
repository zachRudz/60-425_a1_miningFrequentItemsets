import datetime
from collections import defaultdict


def a_priori(input_file, num_baskets, support_threshold):
    # -- Pass 1 --
    # Any frequent pairs would have to contain items that would be also considered frequent
    # Therefore, we can go through the baskets and eliminate all items which are not considered "frequent"
    # No frequent pairs would contain items which are not frequent

    # Our hashmap/dict of possibly frequent items
    # Default value of any basket will always be 0
    items = defaultdict(lambda: 0)
    with open(input_file, 'r') as fp:
        # Reading up to $num_basket baskets
        for basket_index in range(num_baskets):
            # Fetching the values from the line (as strings), and removing the newline character at the end
            line = fp.readline()
            tmp_items = line.split(' ')[: -1]

            # Making note of each item's appearance in a basket
            for i in tmp_items:
                items[i] += 1

    # Recording the total number of unique items (ie: union)
    # I remember needing this for something later on, but I can't remember if I need the number of items before or after
    # the pruning of infrequent items
    # TODO: What's this for?
    # num_items = items.__len__()

    # Removing items which are not frequent
    # Since any item in a frequent pair would have to occur in more than $support_threshold baskets,
    #   we can toss out any items which have a frequency less than a specified amount
    min_required_num_items = num_baskets * support_threshold
    for key, value in items:
        # If this item is NOT frequent, we can safely toss it out
        if value < min_required_num_items:
            items.pop(key)


def main():
    # Starting the clock
    start_time = datetime.datetime.now()
    print("Start time: {}".format(start_time))

    # Finding the number of lines in our file
    input_file = 'retail.txt'
    total_num_lines = 0
    with open(input_file, 'r') as fp:
        while(fp.readline()):
            total_num_lines += 1

    # Reading chunk size from the terminal
    chunk_percentage = float(input("How much of the file do you want to look through? (In percentage format pls): "))
    if chunk_percentage > 1 or chunk_percentage < 0:
        print("Error: The chunk percentage must be between 0.0 and 1.0.")
        return
    num_baskets = int(total_num_lines * chunk_percentage)

    # Reading support threshold from the terminal
    support_threshold = float(input("What is your support threshold? (In percentage format pls): "))
    if support_threshold > 1 or support_threshold < 0:
        print("Error: The support threshold must be between 0.0 and 1.0.")
        return

    # Doing a_priori things
    a_priori(input_file, num_baskets, support_threshold)

    # Stopping the clock
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time
    print("Start time: {}".format(start_time))
    print("End time: {}".format(end_time))
    print("Total elapsed time: {}".format(diff_time))


if __name__ == "__main__":
    main()

# Implementation of a hashmap that allows for collisions.
#
# For the PCY algorithm, we need to maintain a hashtable of as many buckets as will fit in memory. Since we cannot
# store O(N^2) buckets to uniquely identify each pair of items(frequent or not), we use this approach to give a naive
# tell of whether or not a pair is frequent or not.
#
# In other words, pair (x,y) will likely NOT uniquely hash to a bucket, but it MIGHT. Based on this, we can eliminate
# pairs of items which hash to buckets which are NOT frequent (ie: Occur more times than our support threshold).
class my_hashmap():
    num_buckets = None
    data_bitmap = None

    def __init__(self, num_buckets=8):
        # Initializing an array of size $num_buckets, with all zeroes.
        self.num_buckets = num_buckets
        self.init_hashmap()

    # If the hashmap isn't initialized yet, initialize it.
    # This is outside of the constructor because the hashmap can be uninitialized via convert_to_bitmap() to conserve
    # memory.
    def init_hashmap(self):
        self.data = [0 for i in range(self.num_buckets)]

    # Given a value to hash from (a pair of values [a,b]), return the index of where this item lies in the hash map
    def hash(self, item1, item2):
        return (item1 + item2) % self.num_buckets

    # Returns the data at position hash(item1, item2)
    def get_from_hash(self, item1, item2):
        # If the hashmap isn't initialized yet (ie: Got trashed by GC after calling convert_to_bitmap()), init it.
        if not self.data:
            self.init_hashmap()

        pos = self.hash(item1, item2)
        return self.data[pos]

    # Returns the data at position hash(item1, item2)
    def get_from_bitmap(self, item1, item2):
        # If the bitmap isn't initialized yet, return an invalid value
        if not self.data_bitmap:
            print("ERROR: Attempted to grab a value from the bitmap, but it hasn't been created yet.")
            return -1

        pos = self.hash(item1, item2)
        return self.data_bitmap[pos]

    # Increments the count of the respective bucket by 1
    def increment_count(self, item1, item2):
        # If the hashmap isn't initialized yet (ie: Got trashed by GC after calling convert_to_bitmap()), init it.
        if not self.data:
            self.init_hashmap()

        pos = self.hash(item1, item2)
        self.data[pos] += 1

    # Given our integer array of buckets (4 bytes each), convert it to a bitmap.
    # Each index of the bitmap correlates to a bucket in our integer array. Values are 0 if the bucket is NOT frequent,
    # and 1 if it IS frequent
    #
    # In other words, if a bucket appears less times than what our support threshold allows, then it will be a 0 in our
    # bitmap.
    #
    # Note: min_number_of_buckets = support_threshold * total_num_baskets
    def convert_to_bitmap(self, min_number_of_buckets, clear_hashmap=True):
        # If the hashmap isn't initialized yet (ie: Got trashed by GC after calling convert_to_bitmap()), init it.
        if not self.data:
            self.init_hashmap()

        self.data_bitmap = []

        # Convert to bitmap (boolean) representation of the hashmap
        # Boolean value represents whether or not the bucket is frequent
        for i in self.data:
            self.data_bitmap.append(i > min_number_of_buckets)

        # To conserve memory, do we want to clear the hashmap of values?
        # Memory would be freed during the next garbage collection
        if clear_hashmap:
            self.data = None

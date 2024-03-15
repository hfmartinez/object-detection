"""

Challenge:
Find the contiguous subarray within an array of integers that has the largest sum.

"""

# ** Add your code here **


def get_subarray_sum(nums):
    print(nums)
    n = len(nums)
    sum_tmp = 0
    max_tmp = float("-inf")
    subarray = []
    sublists = [
        nums[start:end] for start in range(n) for end in range(start + 1, n + 1)
    ]

    for x in sublists:
        sum_tmp = sum(x)
        if sum_tmp > max_tmp:
            max_tmp, subarray = sum_tmp, x

    return subarray, max_tmp


# Test Case 1
nums1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
subarray1, sum1 = get_subarray_sum(nums1)
print("Subarray:", subarray1)  # Output: [4, -1, 2, 1]
print("Sum:", sum1)  # Output: 6

# Test Case 2
nums2 = [1, 2, 3, 4, 5]
subarray2, sum2 = get_subarray_sum(nums2)
print("Subarray:", subarray2)  # Output: [1, 2, 3, 4, 5]
print("Sum:", sum2)  # Output: 15

# Test Case 3
nums3 = [-2, -3, -4, -1, -5]
subarray3, sum3 = get_subarray_sum(nums3)
print("Subarray:", subarray3)  # Output: [-1]
print("Sum:", sum3)  # Output: -1


"""

Challenge:
Find the longest palindromic substring within a given string

"""


# ** Add your code here **


def longest_palindromic_substring(text):
    n = len(text)
    substrings = [
        text[start:end] for start in range(n) for end in range(start + 1, n + 1)
    ]
    max_tmp = 0
    longest_palindromic = ""
    for x in substrings:
        if x == x[::-1] and len(x) > max_tmp:
            max_tmp = len(x)
            longest_palindromic = x
    return longest_palindromic


# Test Case 1
input_string1 = "babad"
print(longest_palindromic_substring(input_string1))  # Output: "bab" or "aba"

# Test Case 2
input_string2 = "cbbd"
print(longest_palindromic_substring(input_string2))  # Output: "bb"

# Test Case 5
input_string5 = "forgeeksskeegfor"
print(longest_palindromic_substring(input_string5))  # Output: "geeksskeeg"


def flatten_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


nested_list = [1, [2, [3, 4], 5], 6, [7, 8]]
flat_list = flatten_list(nested_list)

print(flat_list)


import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = []
    def push(self, item, priority):
        heapq.heappush(self.queue, (priority, item))
    def pop(self):
        return heapq.heappop(self.queue)[1]


priority_queue = PriorityQueue()
priority_queue.push("task1", 3)
priority_queue.push("task2", 1)
priority_queue.push("task3", 2)
task = priority_queue.pop()  # task2

print(task)

task = priority_queue.pop()  # task2

print(task)

task = priority_queue.pop()  # task2
(print(task))

def longest_increasing_subsequence(nums):
    if not nums:
        return 0

    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


nums = [10, 9, 2, 5, 3, 7, 101, 18]
result = longest_increasing_subsequence(nums)  # 4


print(result)

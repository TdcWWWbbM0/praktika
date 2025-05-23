def containsduplicate(nums):
    return len(nums) != len(set(nums))

nums = [1, 2, 3, 1]
print(containsduplicate(nums))
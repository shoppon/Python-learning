def sort(nums, left, right):
    if left < right:
        pivot = nums[left]
        low = left
        high = right
        while low < high:
            while low < high and nums[high] > pivot:
                high -= 1
            nums[low] = nums[high]
            while low < high and nums[low] < pivot:
                low += 1
            nums[high] = nums[low]
        nums[low] = pivot
        sort(nums, left, low - 1)
        sort(nums, low + 1, right)
